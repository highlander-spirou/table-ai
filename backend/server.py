from flask import Flask, render_template
import json
from config import Config
from models import db
from routes import htmx_routes, normal_routes

app = Flask(__name__, static_url_path='/static')

app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

def get_static_javascript():
    with open('./static/dist/manifest.json') as f:
        a = json.load(f)
    return "/static/dist/" + a['pseudo.html']['file']

@app.context_processor
def setup_j2_globals():
    return dict(environment="dev", get_static_javascript=get_static_javascript)


app.register_blueprint(normal_routes)
app.register_blueprint(htmx_routes)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
