from PyQt5 import QtCore, QtWidgets, QtGui
from dialogUI import Ui_Dialog
from mainUI import Ui_Main
import loginUI
import login
import sys
import os
import bisect
import pickle


class Ui_MainWindow(QtWidgets.QMainWindow, Ui_Main):
    def __init__(self, data):
        Ui_Main.__init__(self, data)
        Ui_Main.setupUi(self, MainWindow)
        self.setup_data()
        
    def setup_data(self):
        try:
            weights_file_r = open(path("weights"), "rb")
            pickle_weights = pickle.load(weights_file_r)  # have to unwrap layers of pickle
            if len(pickle_weights) == len(self.data):
                for x in range(len(self.data)):
                    self.table_summary.setItem(x, 3, QtWidgets.QTableWidgetItem(pickle_weights[x]))
                self.weights_btn.hide()
            else:
                self.show_btn.hide()
            weights_file_r.close()
        except (FileNotFoundError, EOFError):
            self.show_btn.hide()
        
        self.dict2table()
        self.hide_columns()
        self.update_widgets()
    
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        
        self.moduleTab.currentChanged.connect(lambda: self.resize_if_marks_shown())
        self.table_summary.cellPressed.connect(lambda: self.average_exam_mark(self.table_summary.currentColumn()))
        self.hide_btn.clicked.connect(lambda: self.hide_columns())
        self.show_btn.clicked.connect(lambda: self.show_columns())
        self.weights_btn.clicked.connect(lambda: self.add_weights(timer, 0))
        self.logout_btn.clicked.connect(lambda: self.logout())
        
        for table in self.tableList:
            table.cellChanged.connect(lambda: self.update_widgets())

    def hide_columns(self):
        for i in (4, 5, 6, 7):
            self.table_summary.hideColumn(i)
        MainWindow.setFixedSize(630, 400)
        self.show_btn.show()
        self.hide_btn.hide()
        self.average_label.setText("")
        if not self.weights_btn.isHidden():
            self.show_btn.hide()

    def show_columns(self):
        for i in (4, 5, 6, 7):
            self.table_summary.showColumn(i)
        MainWindow.setFixedSize(self.moduleTab.sizeHint().width() + 20, 400)
        self.hide_btn.show()
        self.show_btn.hide()

    def add_weights(self, timer, row):
        if row < len(self.data):
            MainWindow.setWindowTitle("Getting coursework weights...")
            weight = login.get_weights(self.data[row]['Module'][0])
            if weight == "Session Error":
                dialog = QtWidgets.QDialog()
                dialog.setWindowIcon(QtGui.QIcon(path("icon.png", True)))
                dialog_ui = Ui_Dialog()
                dialog_ui.setupUi(dialog)
                dialog_ui.label.setText("To get coursework weights, you must log in.\nClick OK to continue.")
                dialog_accepted = dialog.exec_()
                dialog.show()
                if dialog_accepted:
                    global form
                    form = LoginApp()
                    form.show()
                    MainWindow.close()
                else:
                    MainWindow.setWindowTitle("Grades")
                return
            self.table_summary.setItem(row, 3, QtWidgets.QTableWidgetItem(weight))
            timer.singleShot(0, lambda: self.add_weights(timer, row + 1))
        else:
            timer.stop()
            timer.deleteLater()
            MainWindow.setWindowTitle("Grades")
            self.weights_btn.hide()
            self.show_btn.show()
            self.fillSummary()
        
            list_of_cw_weights = [self.table_summary.item(i, 3).text() for i in range(len(self.data))]
            weights_file_w = open(path("weights"), "wb")
            pickle.dump(list_of_cw_weights, weights_file_w)
            weights_file_w.close()

    @staticmethod
    def logout():
        try:
            os.remove(path("data"))
            os.remove(path("weights"))
        except OSError:
            pass
        global form
        form = LoginApp()
        form.show()
        MainWindow.close()

    def resize_if_marks_shown(self):
        if self.moduleTab.currentIndex() == 0 and self.hide_btn.isVisible():
            MainWindow.setFixedSize(self.moduleTab.sizeHint().width() + 20, 400)
        else:
            MainWindow.setFixedSize(630, 400)

    def fillSummary(self):
        for i in range(len(self.data)):
            self.table_summary.setItem(i, 0, QtWidgets.QTableWidgetItem(self.data[i]['Module'][0]))
            item = QtWidgets.QTableWidgetItem(str(self.perclist[i]))
            self.table_summary.setItem(i, 1, item)
            self.marks_needed(i)
            grade = self.mark_to_grade(self.perclist[i])
            if grade in ("First Class", "Fail", "Pass"):
                if self.perclist[i] != "":
                    self.table_summary.setItem(i, 2, QtWidgets.QTableWidgetItem(grade))
                else:
                    self.table_summary.setItem(i, 2, QtWidgets.QTableWidgetItem())
            else:
                self.table_summary.setItem(i, 2, QtWidgets.QTableWidgetItem(grade[5:17]))
            self.paint_cell(self.table_summary.item(i, 1))

    def update_widgets(self):
        self.currPc()
        self.cell_color_value()
        self.fillSummary()
        self.average_exam_mark(self.table_summary.currentColumn())

    def average_exam_mark(self, column):
        total = 0
        count = 0
        for row in range(self.table_summary.rowCount()):
            try:
                total += float(self.table_summary.item(row, column).data(1))
                count += 1
            except (AttributeError, ValueError, TypeError):
                self.average_label.setText("")
                pass
        if count > 0 and column == 1:
            self.average_label.setText("<span style='font-size:12pt'>Average coursework percentage: {0}%</span>".format(str(round(total / count, 1))))
        elif count > 0:
            self.average_label.setText("<span style='font-size:12pt'>Average mark needed for a {0}: {1}</span>".format(self.table_summary.horizontalHeaderItem(column).text(), str(round(total / count, 1))))
        
    def dict2table(self):
        columns = ["Due Date", "Coursework Title", "Weight", "Mark", "Final Mark"]
        for i, table in enumerate(self.tableList):
            for x, column in enumerate(columns):
                for row, item in enumerate(self.data[i][column]):
                    new_item = QtWidgets.QTableWidgetItem(item)
                    self.tableList[i].setItem(row, x, new_item)
                    if column == "Final Mark":
                        new_item.setTextAlignment(QtCore.Qt.AlignCenter)
                        table.setItemDelegateForColumn(x, TransparentSelectionTableItem(table))
                    else:
                        if column == "Mark":
                            new_item.setTextAlignment(QtCore.Qt.AlignCenter)
                        table.setItemDelegateForColumn(x, NotEditableTableItem(table))
            table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)

    @staticmethod
    def perc_to_float(percentage):
        """ Takes a percentage of form int% and returns it as a float """
        return float(percentage.strip('%')) / 100

    @staticmethod
    def check_mark(entry):
        """ Checks if the table entry is a valid mark. Returns the float if it is and returns None if it is not."""
        try:
            return float(entry)
        except ValueError:
            return None

    def currPc(self):
        markList, weightList, sumprods, sumweights = ([] for _ in range(4))
        blockdict = {}
        block = {}
        del self.perclist[:]

        total = 0
        for i, table in enumerate(self.tableList):
            for x in range(table.rowCount()):
                markList.append(self.check_mark(table.item(x, 4).text()))
                weightList.append(self.perc_to_float(table.item(x, 2).text()))
                blockdict[i] = table.rowCount()
        for v in blockdict:
            total += blockdict[v]
            block[v] = total
        try:
            for y in range(len(block)):
                sumprods.append(sum(j * k if isinstance(j, float) else 0 for j, k in zip(markList[block[y]:block[y + 1]], weightList[block[y]:block[y + 1]])))
                sumweights.append(sum(k if isinstance(j, float) else 0 for j, k in zip(markList[block[y]:block[y + 1]], weightList[block[y]:block[y + 1]])))
        except KeyError:
            pass
        sumprods.insert(0, sum(j * k if isinstance(j, float) else 0 for j, k in zip(markList[:block[0]], weightList[:block[0]])))
        sumweights.insert(0, sum(k if isinstance(j, float) else 0 for j, k in zip(markList[:block[0]], weightList[:block[0]])))
        for x in range(len(sumprods)):
            if sumprods[x] in ("", "-") or sumweights[x] == 0:
                self.perclist.append("")
                self.labelList[x].setText("")
                self.labelList2[x].setText("")
            else:
                self.perclist.append(round((sumprods[x] / sumweights[x]), 2))
                if sumweights[x] < 1.001:
                    self.labelList[x].setText("<span style='font-size:12pt; font-weight:500'>Your current percentage is: </span><span style='font-size:12pt'>" + str(self.perclist[x]) + "%</span>")
                    self.labelList2[x].setText("<span style='font-size:12pt; font-weight:500'>Your current grade is: </span><span style='font-size:12pt'>" + self.mark_to_grade(self.perclist[x]) + "</span>")
                elif sumweights[x] > 1.001:
                    self.labelList[x].setText("<span style='font-size:12pt; font-weight:500'>(Sum of weights is >100%): </span><span style='font-size:12pt'>" + str(self.perclist[x]) + "%</span>")

    def cell_color_value(self):
        """ Feeds every mark from the table to the paint_cell function """
        for table in self.tableList:
            table.blockSignals(True)
            for x in range(len(self.data)):
                for row, item in enumerate(self.data[x]["Final Mark"]):
                    table_item = table.item(row, 4)
                    if table_item:  # table_item is None if empty
                        try:
                            mark = float(table_item.text())
                            self.paint_cell(table_item, mark)
                        except ValueError:
                            table_item.setBackground(QtGui.QBrush())
                            pass
            table.blockSignals(False)

    @staticmethod
    def paint_cell(table_item, mark=None, breakpoints=[40, 50, 60, 70], color=["#ff0000", "#ffdd00", "#eaff00", "#b7ff00", "#00ff00"]):
        """ Sets table_item cell background to a colour based on its value unless it has an invalid value"""
        if not table_item:
            return
        if not mark:
            try:
                mark = float(table_item.text())
            except ValueError:
                return
        if mark == 0:
            table_item.setBackground(QtGui.QBrush())
            return
        if mark >= 500:
            table_item.setBackground(QtGui.QBrush((QtGui.QPixmap(path("kappa.png", True)))))
            return

        i = bisect.bisect(breakpoints, mark)
        background = QtGui.QLinearGradient(0, 0, mark, 0)
        background.setColorAt(0.00, QtGui.QColor(color[i]))
        background.setColorAt(0.99, QtGui.QColor(color[i]))
        background.setColorAt(1.00, QtGui.QColor('#fafafa'))
        table_item.setBackground(QtGui.QBrush(background))

    @staticmethod
    def mark_to_grade(mark, breakpoints=[40, 50, 60, 70], grades=["Fail", "Pass", "2:2, Lower Second-Class", "2:1, Upper Second-Class", "First Class"]):
        """ Checks mark against breakpoints and returns the appropriate grade """
        if not mark:
            return grades[0]
        i = bisect.bisect(breakpoints, mark)
        return grades[i]

    def marks_needed(self, row):
        """ Calculates mark needed using a formula when given the weight of the coursework and current percentage """
        try:
            curr_perc = float(self.table_summary.item(row, 1).text()) / 100
            for i, j in zip(range(4, 8), reversed(range(4, 8))):
                # target_mark takes values of 0.7, 0.6, 0.5 and 0.4
                target_mark = i / 10.0
                target_mark_adj = target_mark
                num_modules = self.table_summary.rowCount()
                for x in range(num_modules):
                    if self.table_summary.item(x, 0).text() == "DEN318":
                        try:
                            project_mark = self.perc_to_float(self.table_summary.item(x, 1).text())
                        except ValueError:
                            break
                        target_mark_adj = ((target_mark * (num_modules + 1)) - project_mark * 2) / (num_modules - 1)
                        break
                
                cw_weight = self.perc_to_float(self.table_summary.item(row, 3).text())
                if cw_weight == 1.0:
                    break
                mark = round(100 * (target_mark - (curr_perc * cw_weight)) / (1.0 - cw_weight))
                mark_adj = round(100 * (target_mark_adj - (curr_perc * cw_weight)) / (1.0 - cw_weight))
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(mark))
                item.setData(1, mark_adj)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_summary.setItem(row, j, item)
                if mark > 100:
                    self.table_summary.item(row, j).setForeground(QtGui.QColor('#ff0000'))
                elif mark <= 0:
                    self.table_summary.item(row, j).setForeground(QtGui.QColor('#00ff00'))
        except (AttributeError, ValueError):
            # Marks are blank
            for i in range(4, 8):
                self.table_summary.setItem(row, i, QtWidgets.QTableWidgetItem())
            pass


class NotEditableTableItem(QtWidgets.QItemDelegate):
    """
    Create a readOnly QTableWidgetItem
    """
    def __init__(self, parent):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        item = QtWidgets.QLineEdit(parent)
        item.setReadOnly(True)
        return item

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())


class TransparentSelectionTableItem(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def initStyleOption(self, option, index):
        super(TransparentSelectionTableItem,self).initStyleOption(option, index)
        if option.state & QtWidgets.QStyle.State_Selected:
            option.state &= ~QtWidgets.QStyle.State_Selected


class LoginApp(QtWidgets.QMainWindow, loginUI.Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_login.clicked.connect(self.login)
        self.lineEdit_password.returnPressed.connect(self.login)
        self.setWindowIcon(QtGui.QIcon(path("icon.png", True)))

    def login(self):
        self.setWindowTitle("Logging in...")
        doLogin_return = login.startLogin()
        dialog = QtWidgets.QDialog(None, QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)
        dialog.setWindowIcon(QtGui.QIcon(path("icon.png", True)))
        dialog_ui = Ui_Dialog()
        dialog_ui.setupUi(dialog)

        if doLogin_return == "Fail":
            self.setWindowTitle("Login")
            dialog_ui.label.setText("Login failed. Please try again.")
            dialog.exec_()
            dialog.show()
        elif doLogin_return == "Empty Fail":
            self.setWindowTitle("Login")
            dialog_ui.label.setText("Please enter your login details and try again.")
            dialog.exec_()
            dialog.show()
        elif doLogin_return == "Connection Fail":
            self.setWindowTitle("Login")
            dialog_ui.label.setText("Failed to establish a connection. Please check your network settings and the status of SEMS Intranet.")
            dialog.exec_()
            dialog.show()
        else:
            data = login.FormatData(doLogin_return)
            dialog.close()
            self.close()

            import main
            file = open(path("data"), "wb")
            main.pickle.dump(main.datetime.datetime.today(), file)
            main.pickle.dump(data, file)
            file.close()

            open_main_window(data)

    def input_user(self):
        user = self.lineEdit_username.text()
        return user

    def input_pass(self):
        passw = self.lineEdit_password.text()
        return passw


def path(file_name, packaged=False):
    # packaged: file packaged by program already (icons, images), else file generated by program
    if packaged:
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, file_name)

    base_path = os.path.dirname(sys.argv[0])
    return os.path.join(base_path, file_name)


def open_main_window(data):
    global MainWindow
    MainWindow = QtWidgets.QMainWindow()
    Ui_MainWindow(data)
    MainWindow.show()


def main_window():
    return form


def main():
    global form
    app = QtWidgets.QApplication(sys.argv)
    form = LoginApp()
    form.show()
    sys.exit(app.exec_())
