from __future__ import absolute_import
from django.template.base import Node, Library, TemplateSyntaxError, kwarg_re
from django.utils.encoding import smart_str
from django.conf import settings

register = Library()


class I18NURLNode(Node):
    "Copy of django's url node with a bit of i18n"

    def __init__(self, language, view_name, args, kwargs, asvar, legacy_view_name=True):
        self.language = language
        self.view_name = view_name
        self.legacy_view_name = legacy_view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import NoReverseMatch
        from statirator.core.utils import i18n_reverse

        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        language = self.language.resolve(context)

        view_name = self.view_name
        if not self.legacy_view_name:
            view_name = view_name.resolve(context)

        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail,
        # re-raise the NoReverseMatch unless we're using the
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
            url = i18n_reverse(language, view_name, args=args, kwargs=kwargs,
                               current_app=context.current_app)
        except NoReverseMatch, e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = i18n_reverse(
                        language, project_name + '.' + view_name,
                        args=args, kwargs=kwargs,
                        current_app=context.current_app)
                except NoReverseMatch:
                    if self.asvar is None:
                        # Re-raise the original exception, not the one with
                        # the path relative to the project. This makes a
                        # better error message.
                        raise e
            else:
                if self.asvar is None:
                    raise e

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url


@register.tag
def i18n_url(parser, token):
    """
    Returns an absolute URL matching given view with its parameters.

    This is a way to define links that aren't tied to a particular URL
    configuration::

        {% i18n_url language path.to.some_view arg1 arg2 %}

        or

        {% i18n_url language path.to.some_view name1=value1 name2=value2 %}

    The first argument is the language code.

    The second argument is a path to a view. It can be an absolute python path
    or just ``app_name.view_name`` without the project name if the view is
    located inside the project.  Other arguments are comma-separated values
    that will be filled in place of positional and keyword arguments in the
    URL. All arguments for the URL should be present.

    For example if you have a view ``app_name.client`` taking client's id and
    the corresponding line in a URLconf looks like this::

        ('^client/(\d+)/$', 'app_name.client')

    and this app's URLconf is included into the project's URLconf under some
    path::

        ('^clients/', include('project_name.app_name.urls'))

    then in a template you can create a link for a certain client like this::

        {% url app_name.client client.id %}

    The URL will look like ``/clients/client/123/``.
    """

    import warnings
    warnings.warn('The syntax for the url template tag is changing. Load the `url` tag from the `future` tag library to start using the new behavior.',
                  category=DeprecationWarning)

    bits = token.split_contents()
    if len(bits) < 3:
        raise TemplateSyntaxError("'%s' takes at least two arguments"
                                  " (labguage) (path to a view)" % bits[0])

    language = parser.compile_filter(bits[1])
    viewname = bits[2]
    args = []
    kwargs = {}
    asvar = None
    bits = bits[3:]
    if len(bits) >= 3 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    # Now all the bits are parsed into new format,
    # process them as template vars
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to i18n_url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return I18NURLNode(language, viewname, args, kwargs, asvar,
                       legacy_view_name=True)
