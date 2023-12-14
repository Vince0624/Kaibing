from flask import Flask
from app import popular_words

app = Flask(__name__)

app.register_blueprint(popular_words)

if __name__ == '__main__':
    app.run()
