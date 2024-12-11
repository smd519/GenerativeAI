from flask import Flask
from routes.main import main_blueprint
from routes.uploads import upload_blueprint


app = Flask(__name__)

# Registeration of the the blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(upload_blueprint)


if __name__ == '__main__':
    app.run(debug=True)


