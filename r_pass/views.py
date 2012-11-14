# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Home")


def service(request, service_id):
    return HttpResponse("Service id: "+service_id)


