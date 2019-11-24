from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from src.models import User
migrate = Migrate(app, db)

login_manager= LoginManager(app)
login_manager.login_view= 'userblueprint.login'
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(id):
  return User.query.get(id)

from src.components.event import event_blueprint
app.register_blueprint(event_blueprint, url_prefix='/event')

from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')


# from src.models.admin import MyAdmin
# admin = Admin(app, name='KHOA', template_mode='bootstrap3')
# admin.add_view(MyAdmin(User, db.session))


@app.route('/')
def root():
#   user = User.query.get(3)
#   login_user(user)
#   print(current_user.name)
  return redirect(url_for("userblueprint.root"))