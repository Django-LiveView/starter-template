from django.conf import settings


def get_global_context(consumer=None):
    """Return a dictionary of global context variables."""
    return {
        "DEBUG": settings.DEBUG,
        "user": consumer.scope["user"]
        if consumer and "user" in consumer.scope
        else None,
    }


def customs(request):
    """Return a dictionary of context variables."""
    return get_global_context()
