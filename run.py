from flask import Flask

from app.posts.views import posts_blueprint
from app.api.views import api_blueprint
from app import logger

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False             # не  кодировать в ASCII, а выводимые строки в формате unicode --> utf-8

logger.create_logger()                          # создать логгер для записи действий

app.register_blueprint(posts_blueprint)         # регистрация блюпринтов для постов
app.register_blueprint(api_blueprint)           # регистрацию блюпринтов ля апи


if __name__ == "__main__":
    app.run(debug=True, port=2912)

