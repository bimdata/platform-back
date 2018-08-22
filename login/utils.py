from django.urls import reverse


def absolutify(request, view_name):
    """Return the absolute URL of a path."""
    return request.build_absolute_uri(reverse(view_name))
