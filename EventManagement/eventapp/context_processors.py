from .models import Event


def mylink(request):
    links = Event.objects.all()
    return dict(links=links)
