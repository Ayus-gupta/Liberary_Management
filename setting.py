import os

# Base dir (same level as app.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database inside data/instance/
DB_PATH = os.path.join(BASE_DIR, "data", "lib.db")

class Config:
    SECRET_KEY = "m(sis)9@@@"  # ⚠️ in production, load from env
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Security configs
    SECURITY_PASSWORD_SALT = "!@#123qweASD"  # ⚠️ change to env var
    SECURITY_PASSWORD_HASH = "bcrypt"

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True


    # # Template folder for security views
    # SECURITY_LOGIN_USER_TEMPLATE = "security/login_user.html"
    # SECURITY_REGISTER_USER_TEMPLATE = "security/register_user.html"
    # SECURITY_FORGOT_PASSWORD_TEMPLATE = "security/forgot_password.html"
