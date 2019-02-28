from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def root(request):
    return HttpResponseRedirect('home')

def home_page(request):
    context = {'client': 'A client is a piece of computer hardware or software that accesses a service made available by a server.',
                'server': 'In computing, a server is a computer program or a device that provides functionality for other programs or devices, called "clients".',
                'http_request': 'An HTTP client sends an HTTP request to a server in the form of a request message which includes following format',
                'http_response': 'HTTP Response is the packet of information sent by Server to the Client in response to an earlier Request made by Client. ',
                'django': 'Django is a Python-based free and open-source web framework, which follows the model-view-template architectural pattern. It is maintained by the Django Software Foundation, an independent organization established as a 501 non-profit. Djangos primary goal is to ease the creation of complex, database-driven websites'
                }
    response = render(request, 'index.html', context)
    return HttpResponse(response)
