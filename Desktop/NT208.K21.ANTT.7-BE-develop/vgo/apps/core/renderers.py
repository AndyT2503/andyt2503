import json
import pdb;
from rest_framework.renderers import JSONRenderer


class VgoJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'objects'
    pagination_object_count = 'count'

    def render(self, data, media_type=None, renderer_context=None):
        if len(data):
            return json.dumps({
                self.pagination_object_label: data,
                self.pagination_count_label: len(data)
            })

        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        elif data.get('errors', None) is not None:
            return super(VgoJSONRenderer, self).render(data)

        else:
            return json.dumps({
                self.object_label: data
            })