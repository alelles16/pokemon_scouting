from flask import Flask
from routes import api
from config import Config
from database import db
from flasgger import Swagger

app = Flask(__name__)

cfg = Config()

app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

template_file = 'swagger.yml'
Swagger(app, template_file=template_file)

# Init db
db.init_app(app)

app.register_blueprint(api)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5001)
