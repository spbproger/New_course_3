import logging

from flask import Blueprint, request, jsonify
from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDAO

api_blueprint = Blueprint("api_blueprint", __name__)                # Создаем экземпляр для блюпринта апи

posts_dao = PostsDAO("data/posts.json")                             # берем посты из файла
comments_dao = CommentsDAO("data/comments.json")                    # берем комменты из файла

logger = logging.getLogger("basic")

@api_blueprint.route("/api/posts/")
def posts_all():
    """апишка для получения странички со всеми постами"""
    logger.debug("Запрошены все посты через API")
    posts = posts_dao.get_all()
    return jsonify(posts)


@api_blueprint.route("/api/posts/<int:post_pk>/")
def posts_one(post_pk):
    """апишка для получения одного поста по pk"""
    logger.debug(f"Запрошен пост с pk {post_pk} через API")
    post = posts_dao.get_by_pk(post_pk)
    return jsonify(post)


