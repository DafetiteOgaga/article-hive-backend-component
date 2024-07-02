from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import escape

items = [
    {
        'title': 'The Future of Technology',
        'author': 'Famous',
        'date': 'May 22, 2024',
        'content': 
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod'
    },
    {
        'title': 'What you need to know about IOT',
        'author': 'Paul',
        'date': 'May 22, 2024',
        'content': 
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod'
    },
    {
        'title': 'How to become a better Entrepreneur',
        'author': 'Deborah',
        'date': 'May 22, 2024',
        'content': 
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod'
    },
    {
        'title': 'Why Tech Experts are diverting into Farming',
        'author': 'Mayowa',
        'date': 'May 22, 2024',
        'content': 
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod'
    },
]

rated = [
    {
        'title': 'The 7 Benefits of BSc Degree',
        'content': 
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod',
        'author': 'Becky',
        'date': 'May 22, 2024',
    },
    {
        'title': 'The Truth about AI',
        'content': 
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod',
        'author': 'Dickson',
        'date': 'May 22, 2024',
    },
    {
        'title': 'How to be Excellent in Prompt Engineer',
        'content': 
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod',
        'author': 'Rotimi',
        'date': 'May 22, 2024',
    },
]

# Create your views here.
def home(request):
    return render(request, 'index.html', {'items': items, 'rated': rated})

def checkRequest(request):
    request_details1 = {
        'Method': request.method,
        'Headers': request.headers,
        'GET Parameters': request.GET,
        'POST Data': request.POST,
        'Body': request.body,
        'Files': request.FILES,
        'content_params': request.content_params,
        'content_type': request.content_type,
        'csrf_processing_done': request.csrf_processing_done,
        'encoding': request.encoding,
        'Cookies': request.COOKIES,
        'Path': request.path,
        'path_info': request.path_info,
        '_current_scheme_host': request._current_scheme_host,
        'scheme': request.scheme,
        'User': request.user,
        'session': request.session,
    }

    request_info1 = "<h1>Neccessary (need to know) Request Details</h1>"
    for key, value in request_details1.items():
        request_info1 += f"<h2>{escape(key)}</h2><pre>{escape(str(value))}</pre>"
    
    return HttpResponse(request_info1+'<br/><hr/><hr/><hr/><hr/><hr/><hr/><br/>')