from PyQt5 import QtCore, QtWidgets, QtGui
import os
import sys


class Ui_Main(object):
    def __init__(self, data):
        self.data = data
        self.tabList, self.tableList, self.labelList, self.labelList2, self.perclist = ([] for _ in range(5))
        self.moduleTab = QtWidgets.QTabWidget()
        self.table_summary = QtWidgets.QTableWidget()
        self.average_label = QtWidgets.QLabel(self.moduleTab.widget(0))
        self.weights_btn, self.hide_btn, self.show_btn, self.logout_btn, self.custom_mark_btn = (QtWidgets.QPushButton(self.moduleTab.widget(0)) for _ in range(5))
        
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(630, 400)
        MainWindow.setWindowIcon(QtGui.QIcon(path("icon.png", True)))
        
        layoutList, frameList, frame_labelList, layout_labelList = ([] for _ in range(4))
        
        layout = QtWidgets.QVBoxLayout()
        main_widget = QtWidgets.QWidget()
        
        columns = ["Due Date", "Coursework Title", "Weight", "Mark", "Final Mark"]
        stylesheet = """
        QScrollBar:vertical, QScrollBar:horizontal {
            width:12px;
            height:12px;
        }
        QHeaderView::section{Background-color:rgb(34,221,81); font:bold}
        QTableView{gridline-color: rgb(107, 107, 107)}
        """
        
        for i in range(len(self.data)):
            self.tabList.append(QtWidgets.QWidget())
            frame_labelList.append(QtWidgets.QFrame())
            self.moduleTab.addTab(self.tabList[i], self.data[i]['Module'][0])
            
            layout_labelList.append(QtWidgets.QVBoxLayout(frame_labelList[i]))
            layoutList.append(QtWidgets.QVBoxLayout(self.tabList[i]))
            self.labelList.append(QtWidgets.QLabel())
            self.labelList2.append(QtWidgets.QLabel())
            self.tableList.append(QtWidgets.QTableWidget(self.tabList[i]))
            
            self.tableList[i].setColumnCount(len(columns))
            self.tableList[i].setRowCount((len(self.data[i]["Module"])))
            self.tableList[i].setHorizontalHeaderLabels(columns)
            self.tableList[i].horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
            self.tableList[i].setColumnWidth(0, 90)
            self.tableList[i].setColumnWidth(1, 170)
            self.tableList[i].verticalHeader().setVisible(False)
            self.tableList[i].setAlternatingRowColors(True)
            self.tableList[i].setStyleSheet(stylesheet)
            self.tableList[i].setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
            
            layout_labelList[i].addWidget(self.labelList[i])
            layout_labelList[i].addWidget(self.labelList2[i])
            self.labelList[i].setAlignment(QtCore.Qt.AlignCenter)
            self.labelList2[i].setAlignment(QtCore.Qt.AlignCenter)
            layoutList[i].addWidget(self.tableList[i], 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
            layoutList[i].addWidget(frame_labelList[i], 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)

        self.moduleTab.insertTab(0, QtWidgets.QWidget(), "Summary")
        self.moduleTab.setCurrentIndex(0)
        layout_summary = QtWidgets.QGridLayout(self.moduleTab.widget(0))
        button_layout = QtWidgets.QGridLayout()
        layout_summary.addLayout(button_layout, 0, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        layout_summary.addWidget(self.table_summary, 1, 0, QtCore.Qt.AlignCenter)
        self.table_summary.setAlternatingRowColors(True)
        self.table_summary.verticalHeader().setVisible(False)
        self.table_summary.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table_summary.setColumnCount(9)
        self.table_summary.setStyleSheet(stylesheet)
        self.table_summary.setHorizontalHeaderLabels(
            ["Module", "Current %", "Current Grade", "C/W Weight", "First", "2:1", "2:2", "Pass", "CustomMark"])
        self.table_summary.hideColumn(8)
        self.table_summary.setRowCount(len(self.data))
        self.table_summary.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_summary.horizontalHeaderItem(1).setToolTip(
            "Assumes you have at least attempted all of the coursework so far\nIf there is a coursework that you didn't do and the deadline has passed, then you will need to manually set that coursework mark to 0 in the respective module tab")
        for i in range(self.table_summary.columnCount()):
            self.table_summary.setItemDelegateForColumn(i, NotEditableTableItem(self.table_summary))
        
        self.weights_btn.setText("Get C/W weights")
        self.weights_btn.setToolTip(
            "Grabs the percentage that coursework makes up for each module. This is a requirement to calculate the marks needed in the exam")
        self.weights_btn.adjustSize()
        button_layout.addWidget(self.weights_btn, 0, 0)

        self.custom_mark_btn.setText("Custom mark")
        self.custom_mark_btn.setToolTip("Enter a custom target mark")
        self.custom_mark_btn.adjustSize()
        button_layout.addWidget(self.custom_mark_btn, 0, 0)

        self.hide_btn.setText("Hide exam marks")
        self.hide_btn.adjustSize()
        button_layout.addWidget(self.hide_btn, 0, 1)
        self.show_btn.setText("Show exam marks")
        self.show_btn.setToolTip("Displays the marks needed in the exam to obtain the grade shown")
        self.show_btn.adjustSize()
        button_layout.addWidget(self.show_btn, 0, 1)

        self.logout_btn.setText("Logout")
        self.logout_btn.adjustSize()
        button_layout.addWidget(self.logout_btn, 0, 2)
        layout_summary.addWidget(self.average_label, 2, 0, QtCore.Qt.AlignHCenter)
        
        layout.addWidget(self.moduleTab)
        main_widget.setLayout(layout)
        
        MainWindow.setCentralWidget(main_widget)
        MainWindow.setWindowTitle("Grades")
    

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
