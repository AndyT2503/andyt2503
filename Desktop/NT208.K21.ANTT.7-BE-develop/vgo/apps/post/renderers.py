from vgo.apps.core.renderers import VgoJSONRenderer


class PostJSONRenderer(VgoJSONRenderer):
    object_label = 'post'
    pagination_object_label = 'posts'
    pagination_count_label = 'postsCount'


class CommentJSONRenderer(VgoJSONRenderer):
    object_label = 'comment'
    pagination_object_label = 'comments'
    pagination_count_label = 'commentsCount'