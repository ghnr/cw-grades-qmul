from PyQt5 import QtCore, QtWidgets, QtGui


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setFixedSize(325, 100)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignTop)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.verticalLayout.addWidget(self.buttonBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Login")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

