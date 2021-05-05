import re, os
import json
from utils import models
from utils import constants as cst
from PySide2 import QtWidgets, QtCore

from ui import login_ui

class LoginView(QtWidgets.QDialog, login_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(LoginView, self).__init__(parent=parent)

        self.setupUi(self)

        # Constant
        self.error.setText("")

        self.btn_tab.toggled.connect(self.change_tab)
        self.btn_sign.clicked.connect(self.register_user)
        self.btn_login.clicked.connect(self.login)

        self.db_connection = models.connection_to_db(cst.DATABASE)

    def load_ui(self):
        self.sign_user.setText('')
        self.sign_email.setText('')
        self.sign_passw.setText('')
        data = self.get_save_data()
        try:
            self.lg_email.setText(data['last_login']['user'])
            self.lg_passw.setText(data['last_login']['password'])
        except:
            pass

    def change_tab(self, checked):
        if checked:
            self.btn_tab.setText('Sign Up')
            self.stackedWidget.setCurrentIndex(0)
        else:
            self.btn_tab.setText('Login')
            self.stackedWidget.setCurrentIndex(1)

    def register_user(self):
        """Create a new user into the DataBase
        """
        user = self.sign_user.text().lower()
        mail = self.sign_email.text()
        password = self.sign_passw.text()
        # password = models.crypt_password(password=txt_password)
        # print(password)
        if not user or not mail or not password:
            self.error_2.setText("Please fill in all the fields.")
            return
        if self.sanity_check_validation_mail(mail):
            if models.sanity_check_mail_exist(self.db_connection, mail):
                id_user = models.create_user(self.db_connection,
                                             user, mail, password
                                             )
                self.error_2.setText('')
                self.close()
            else:
                self.error_2.setText("Mail already exist.")
        else:
            self.error_2.setText('Error Invalid Email')
        self.load_ui()

    def login(self):
        """Login method
        """
        user = self.lg_email.text().lower()
        password = self.lg_passw.text()
        # password = models.crypt_password(password=txt_password)
        # print(password)
        # print(models.get_all_users(self.db_connection))

        type_field = "user_username"
        if self.sanity_check_validation_mail(user):
            type_field = "mail"

        login = models.find_user_login(self.db_connection,
                                       user=user,
                                       password=password,
                                       type_field=type_field
                                       )
        if not login:
            self.error.setText("Login Fail.")
            return

        with open(self.setting_path, 'w') as f:
            pref = {"last_login": {"user": user, "password": password}}
            json.dump(pref, f, indent=4)

        self.close()

    def sanity_check_validation_mail(self, mail):
        """This method check if the text is a maim format.

        Args:
            mail ([str]): mail adress to check.

        Returns:
            [bool]: True if it is a mail.
        """
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if re.search(regex, mail):
            return True

    def get_save_data(self):
        with open(self.setting_path, 'r') as f:
            data = json.load(f)
        return data

    def show(self, *args, **kwargs):
        self.setting_path = os.path.join(os.getenv('APP_HOME'), "setting.json")
        self.load_ui()
        super(LoginView, self).show()
