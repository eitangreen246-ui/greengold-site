from django.http import HttpResponse


def healthz(request):
    """Lightweight liveness endpoint for the platform health check.

    Returns 200 without touching the database or templates, so the deploy
    health check is fast and resilient."""
    return HttpResponse("ok", content_type="text/plain")
