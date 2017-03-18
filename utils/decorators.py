from main.models import Macro
from django.http import Http404


def check_is_my_macro(macro_id=None):
    def decorator(func):
        def inner(self, *args, **kwargs):
            try:
                Macro.objects.get(id=self.kwargs[macro_id], user=self.request.user)
                return func(self, *args, **kwargs)
            except:
                raise Http404
        return inner
    return decorator