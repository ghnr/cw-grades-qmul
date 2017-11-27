from PyQt5 import QtCore, QtWidgets, QtGui


class Ui_Dialog(object):

    def __init__(self, Dialog, allow_cancel=False, entry=False):
        self.dialog = Dialog
        self.vertical_layout = QtWidgets.QVBoxLayout(Dialog)
        self.label = QtWidgets.QLabel(Dialog)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.allow_cancel = allow_cancel
        self.entry = entry

    def setupUi(self):
        self.dialog.setWindowTitle("Login")
        self.vertical_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.vertical_layout.addWidget(self.label, 0, QtCore.Qt.AlignTop)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)

        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)
        if self.allow_cancel:
            self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        else:
            self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.vertical_layout.addWidget(self.button_box)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.button_box.accepted.connect(self.dialog.accept)
        self.button_box.rejected.connect(self.dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

