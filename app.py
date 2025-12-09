
import io
from flask import Flask
from flask_security import  SQLAlchemyUserDatastore
from data.models import db, Student, Payment
from setting import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize db
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Student, Payment)

# Register routes
from routes.routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
