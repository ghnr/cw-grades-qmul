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
        Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
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

