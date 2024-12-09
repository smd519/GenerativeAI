from flask import Flask
from routes.main import main_blueprint

app = Flask(__name__)

# Registeration of the the blueprints
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
