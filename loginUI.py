from PyQt5 import QtCore, QtWidgets


class Ui_LoginWindow(object):

    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(300, 250)
        LoginForm.setMinimumSize(QtCore.QSize(300, 250))
        LoginForm.setMaximumSize(QtCore.QSize(300, 250))
        self.centralwidget = QtWidgets.QWidget(LoginForm)
        self.centralwidget.setObjectName("centralwidget")
        LoginForm.setObjectName("Form")
        self.frame_Form = QtWidgets.QFrame(LoginForm)
        self.frame_Form.setGeometry(QtCore.QRect(56, 85, 180, 70))
        self.frame_Form.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Form.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Form.setObjectName("frame_Form")
        self.formLayout = QtWidgets.QFormLayout(self.frame_Form)
        self.formLayout.setObjectName("formLayout")
        self.label_username = QtWidgets.QLabel(self.frame_Form)
        self.label_username.setObjectName("label_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_username)
        self.label_password = QtWidgets.QLabel(self.frame_Form)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.lineEdit_username = QtWidgets.QLineEdit(self.frame_Form)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_username)
        self.lineEdit_password = QtWidgets.QLineEdit(self.frame_Form)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        self.btn_login = QtWidgets.QPushButton(self.centralwidget)
        self.btn_login.setGeometry(QtCore.QRect(105, 160, 75, 23))
        self.btn_login.setObjectName("btn_login")
        self.btn_login.raise_()
        LoginForm.setCentralWidget(self.centralwidget)
        self.retranslateUi(LoginForm)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)

    def retranslateUi(self, LoginForm):
        LoginForm.setWindowTitle("Login")
        self.label_username.setText("Username")
        self.label_password.setText("Password")
        self.btn_login.setText("Login")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginForm = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginForm)
    LoginForm.show()
    sys.exit(app.exec_())

