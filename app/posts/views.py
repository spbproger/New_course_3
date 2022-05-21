import logging
from json import JSONDecodeError

from flask import Blueprint, render_template, request, abort
from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDAO


posts_blueprint = Blueprint("posts_blueprint", __name__, template_folder="templates")   # объявляем блюпринт для постов
posts_dao = PostsDAO("data/posts.json")
comments_dao = CommentsDAO("data/comments.json")

logger = logging.getLogger("basic")

@posts_blueprint.route("/")
def posts_all():
    """Блюпринт для главной страницы со всеми постами"""
    logger.debug("Были запрошены все посты")
    try:
        posts = posts_dao.get_all()
        return render_template("index.html", posts=posts)
    except:
        return "Произошло что-то немыслимое)"


@posts_blueprint.route("/posts/<int:post_pk>/")
def posts_one(post_pk):
    """Блюпринт для поста со значением pk"""
    logger.debug(f"Был запрошен пост: {post_pk}")
    try:
        post = posts_dao.get_by_pk(post_pk)                     # Получаем пост для pk
        comments = comments_dao.get_by_post_pk(post_pk)         # Получаем комменты для pk
    except (JSONDecodeError, FileNotFoundError) as error:       # Если произошла JSON ошибка
        return render_template("error.html", error=error)
    except BaseException as e:                                  # Если произошла иная ошибка
        return render_template("error.html", error="неизвестная ошибка")
    else:
        if post is None:                                        # Если поста с pk не существует
            abort(404)
        number_of_comments = len(comments)                      # подсчет числа постов
        return render_template("post.html", post=post, comments=comments, number_of_comments=number_of_comments)


@posts_blueprint.route("/search/")
def posts_search():
    """Блюпринт для постов по искомому значению"""
    query = request.args.get("s", "")           # Получить параметр для запроса из аргументов

    if query != "":                             # Если запрос непустой
        posts = posts_dao.search(query)         # Получаем посты
        number_of_posts = len(posts)            # Получаем число постов
    else:                                       # Если запрос пустой
        posts = []
        number_of_posts = 0

    return render_template("search.html", query=query, posts=posts, number_of_posts=number_of_posts)


@posts_blueprint.route("/users/<username>/")
def posts_by_user(username):
    """ Блюпринт для постов конкретного юзера"""
    posts = posts_dao.get_by_user(username)              # Получаем пост для юзера
    number_of_posts = len(posts)                         # Получаем число постов для юзера
    return render_template("user-feed.html", posts=posts, number_of_posts=number_of_posts)


@posts_blueprint.errorhandler(404)
def post_error(e):
    """ Блюпринт для ошибки при поиске поста"""
    return "Такого поста найти не получилось", 404