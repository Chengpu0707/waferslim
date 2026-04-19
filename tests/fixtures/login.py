class LoginFixture:
    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password

    def enter_username(self, username):
        self.login_name = username
    def enter_password(self, password):
        self.Login_password = password
    def is_logged_in(self):
        return self.login_name == "admin" and self.Login_password == "secret"
