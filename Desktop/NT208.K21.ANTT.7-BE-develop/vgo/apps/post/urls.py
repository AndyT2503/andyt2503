from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet,
    CommentsListCreateAPIView, CommentsDestroyAPIView, ApiPostListView
)

router = DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),

    #url(r'^posts/feed/?$', PostsFeedAPIView.as_view()),

    # url(r'^posts/(?P<post_slug>[-\w]+)/favorite/?$',
    #     PostsFavoriteAPIView.as_view()),


    #.../a/postspi/list/?search=
    #.../a/postspi/list/?title=1&search=
    #.../a/postspi/list/?body=1&search=
    #.../a/postspi/list/?author=1&search=
    url(r'^posts/list/?$',ApiPostListView.as_view()),


    url(r'^posts/(?P<post_slug>[-\w]+)/comments/?$', 
        CommentsListCreateAPIView.as_view()),

    url(r'^posts/(?P<post_slug>[-\w]+)/comments/(?P<comment_pk>[\d]+)/?$',
        CommentsDestroyAPIView.as_view()),

    # url(r'^tags/?$', TagListAPIView.as_view()),
]

app_name = 'post'