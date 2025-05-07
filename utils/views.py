from rest_framework.exceptions import NotFound


def get_or_404(klass, *filter_args, **filters_kwargs):
    try:
        return klass.objects.get(*filter_args, **filters_kwargs)
    except (klass.DoesNotExist, TypeError, ValueError):
        raise NotFound(f"{klass.__name__} not found")
