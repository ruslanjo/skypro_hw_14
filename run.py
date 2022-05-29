from flask import Flask
from app.movies.views import movies_blueprint

app = Flask(__name__)

app.register_blueprint(movies_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
