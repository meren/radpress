from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from radpress.forms import ZenModeForm
from radpress.models import Tag


class ZenModeViewMixin(object):
    """
    Receives all common context data for required for zen mode. Zen mode is
    written for only staff users, not readers. You don't have to use zen mode
    to add an article or page, but you can switch from admin panel with a
    button click easily.
    """
    template_name = 'radpress/zen_mode.html'
    form_class = ZenModeForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ZenModeViewMixin, self).dispatch(*args, **kwargs)


class TagViewMixin(object):
    """
    Adds list of available tags to context data. Tag list are used by most of
    radpress templates.
    """
    def get_context_data(self, **kwargs):
        tags = Tag.objects.get_available_tags()
        data = super(TagViewMixin, self).get_context_data(**kwargs)
        data.update({'tag_list': tags.values('name', 'slug')})

        return data
