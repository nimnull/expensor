from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

__author__ = 'nimnull'


class AuthRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthRequiredMixin, self).dispatch(request, *args, **kwargs)

