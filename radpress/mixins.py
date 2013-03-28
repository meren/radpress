from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.decorators import method_decorator
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

    def get_form_kwargs(self):
        kwargs = super(ZenModeViewMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        # save new entry
        entry = form.save()

        # define success url
        self.success_url = reverse('radpress-zen-mode-update', args=[entry.pk])

        # and redirect
        return super(ZenModeViewMixin, self).form_valid(form)


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


class EntryViewMixin(object):
    """
    Checks model object is_published value. If it's not published, it will
    raise Http404. It works only for Entry abstracted models that have
    `is_published` fields: Article, Page.
    """
    def get_object(self, queryset=None):
        obj = super(EntryViewMixin, self).get_object(queryset)

        if not obj.is_published:
            raise Http404

        return obj
