from flask import Flask, render_template
import json
from config import Config
from models import db, User
from routes import htmx_routes, normal_routes
from flask_login import LoginManager

app = Flask(__name__, template_folder='./static/dist/templates', static_folder='./static/dist/assets')

app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'normal_routes.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


with app.app_context():
    db.create_all()

app.register_blueprint(normal_routes)
app.register_blueprint(htmx_routes)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
