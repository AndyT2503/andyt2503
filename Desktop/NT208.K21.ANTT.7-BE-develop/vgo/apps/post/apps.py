from django.apps import AppConfig


class PostAppConfig(AppConfig):
    name = 'vgo.apps.post'
    label = 'post'
    verbose_name = 'Post'

    def ready(self):
        import vgo.apps.post.signals

default_app_config = 'vgo.apps.post.PostAppConfig'
