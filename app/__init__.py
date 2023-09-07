from flask import Flask
from .config import Configuration
from .routes.orders import orders_bp
from .routes.session import session_bp
from .models import db, Employee
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(orders_bp)
app.register_blueprint(session_bp)
db.init_app(app)


login = LoginManager(app)
login.login_view = "session.login"

@login.user_loader
def load_user(id):
    return Employee.query.get(id)
