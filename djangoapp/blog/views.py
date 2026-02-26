from django.shortcuts import render

# Create your views here.

def index(request):
    
    # context = (
    #     ...
    # )
    return render(
        request,
        'blog/pages/index.html',
    )


def page(request):
    
    # context = (
    #     ...
    # )
    return render(
        request,
        'blog/pages/page.html',
    )
    

def post(request):
    
    # context = (
    #     ...
    # )
    return render(
        request,
        'blog/pages/post.html',
    )