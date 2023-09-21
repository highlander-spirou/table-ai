from flask import Flask, render_template
from interfaces import *
from config import Config
from routes import htmx_routes, normal_routes

app = Flask(__name__, static_url_path='/static')

app.config.from_object(Config)
app.register_blueprint(normal_routes)
app.register_blueprint(htmx_routes)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
