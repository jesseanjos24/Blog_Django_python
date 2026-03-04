from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Page, Tag
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView

# Create your views here.

PER_PAGE = 9

class PostListView(ListView):

    template_name = 'blog/pages/index.html'
    context_object_name = "page_index"
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published() #type:ignore
    
    page_title = 'Home - '
    
    # def get_queryset(self):
    #     querryset =  super().get_queryset()
    #     querryset = querryset.filter(is_published=True)
        
    #     return querryset
    
    
    def get_context_data(self, **kwargs):
        cotext = super().get_context_data(**kwargs)
        
        cotext.update({
            "page_title": self.page_title,
        })
        
        return cotext


# def index(request):
    
#     posts = Post.objects.get_published() #type:ignore
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     page_title = 'Home - ' 
    
#     context = {
#         "post" : posts,
#         "page_obj": page_obj,
#         "page_title": page_title,
#     }
    
#     return render(
#         request,
#         'blog/pages/index.html',
#         context,
#     )


# def created_by(request, autor_url):
    
#     user = User.objects.filter(pk=autor_url).first()
    
#     if user is None:
#         raise Http404()
    
#     posts = Post.objects.get_published().filter(created_by__pk=autor_url) #type:ignore
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
    
#     user_full_name = user.username
#     if user.first_name:
#         user_full_name = f'{user.first_name} {user.last_name}'
        
#     page_title = user_full_name + 'Post - '
    
#     context = {
#         "post" : posts,
#         "page_obj": page_obj,
#         "page_title": page_title
#     }
    
#     return render(
#         request,
#         'blog/pages/index.html',
#         context,
#     )
    

class CriatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Posts de ' + user_full_name + ' - '

        ctx.update({
            "page_title": page_title,
        })

        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        
        return qs

    def get(self, request, *args, **kwargs):
        autor_url = self.kwargs.get('autor_url')
        user = User.objects.filter(pk=autor_url).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'autor_url': autor_url,
            'user': user,
        })

        return super().get(request, *args, **kwargs)
    

# def category(request, slug):
    
#     posts = Post.objects.get_published().filter(category__slug=slug) #type:ignore
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     if len(page_obj) == 0:
#         raise Http404()
        
#     page_title = f'{page_obj[0].category.name} - Category - '
    
#     context = {
#         "post" : posts,
#         "page_obj": page_obj,
#         "page_title": page_title
#     }
    
#     return render(
#         request,
#         'blog/pages/index.html',
#         context,
#     )


class CtegoryListViews(PostListView):
    allow_empty = False   
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Category - ' #type: ignore
        ctx.update({
            'page_title': page_title,
        })
        return ctx
        
    
class TagListViews(PostListView):
    allow_empty = False   

    def get_queryset(self):
        self.tag = get_object_or_404(
            Tag,
            slug=self.kwargs.get('slug')
        )

        return super().get_queryset().filter(
            tags=self.tag
        )
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['page_title'] = f'{self.tag.name} - Tags -'
        ctx['tag'] = self.tag

        return ctx
    
# def tag(request, slug):
    
#     posts = Post.objects.get_published().filter(tags__slug=slug) #type:ignore
    
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
    
#     context = {
#         "post" : posts,
#         "page_obj": page_obj,
#     }
    
#     return render(
#         request,
#         'blog/pages/index.html',
#         context,
#     )

class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self._search_value
        ctx.update({
            'page_title': f'{search_value[:30]} - Search - ',
            'search_value': search_value,
        })
        return ctx

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(request, *args, **kwargs)
    
      
# def search(request):
    
#     search_value = request.GET.get('search', '').strip()
#     posts = Post.objects.get_published().filter(Q(title__icontains=search_value)|Q(excerpt__icontains=search_value)|Q(content__icontains=search_value))[:PER_PAGE] #type:ignore
    
    
#     page_title = f'Search - {search_value[:25]} -'
    
#     context = {
#         "page_obj": posts,
#         "search_value": search_value,
#         "page_title": page_title,
#     }
    
#     return render(
#         request,
#         'blog/pages/index.html',
#         context,
#     )

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: #type: ignore
        ctx = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - Página - '  # type: ignore
        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


# def page(request, slug):
    
#     pages_obj = Page.objects.get_published().filter(slug=slug).first() #type:ignore
    
#     if pages_obj is None:
#         raise Http404()
    
#     page_title = f'{pages_obj.title[:25]} - Pages -'
    
#     context = {
#         "pages_obj": pages_obj,
#         "page_title": page_title,
#     }
    
#     return render(
#         request,
#         'blog/pages/page.html',
#         context
#     )
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    context_object_name = 'post'
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f'{post.title} - Post - '  # type: ignore
        ctx.update({
            'page_title': page_title,
        })
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

# def post(request, slug): 
    
#     posts_obj = Post.objects.get_published().filter(slug=slug).first() #type:ignore
    
#     if posts_obj is None:
#         raise Http404()
        
#     page_title = f'{posts_obj.title[:25]} - Posts - '
    
#     context = {
        
#         'post': posts_obj,
#         "page_title": page_title,
#     }
        
#     return render(
#         request,
#         'blog/pages/post.html',
#         context,
#     )