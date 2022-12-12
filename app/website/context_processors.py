from django.conf import settings


def get_global_context():
    """Return a dictionary of global context variables."""
    return {
        "DEBUG": settings.DEBUG,
    }


def customs(request):
    """Return a dictionary of context variables."""
    return get_global_context()
