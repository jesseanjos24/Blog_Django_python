from django.contrib import admin
from .models import Tag, Category, Page, Post
from django_summernote.admin import SummernoteModelAdmin
from django.utils.safestring import mark_safe
from django.urls import reverse


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug":('name',),
    }

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug":('name',),
    }

@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    
    summernote_fields = ('content')

    list_display = (
        "id",
        "title",
        "slug",
        "is_published",
        "content",
    )

    list_display_links = ("title",)

    search_fields = (
        "id",
        "title",
        "slug",
    )

    list_per_page = 10

    ordering = ("-id",)

    prepopulated_fields = {
        "slug": ("title",),
    }
    
    readonly_fields = 'link',
    
    def link(self, obj):
        if not obj.pk:
            return '-'
        
        
        url_do_post = reverse('blog:page', args=(obj.slug,))
        safe_link = mark_safe(f'<a href="{url_do_post}">Ver No Site</a>')
        
        
        return safe_link
    
@admin.register(Post)    
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')
    list_display='id', 'title', 'is_published', 'created_at',
    list_display_links = 'title',
    search_fields = 'id', 'title', 'slug', 'excerpt','content',
    list_per_page = 10
    list_filter = 'category', 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by', 'link',
    prepopulated_fields = {
        "slug":('title',),
    }
    
    autocomplete_fields = 'tags', 'category',
    
    def link(self, obj):
        if not obj.pk:
            return '-'
        
        
        url_do_post = reverse('blog:post', args=(obj.slug,))
        safe_link = mark_safe(f'<a href="{url_do_post}">Ver No Site</a>')
        
        
        return safe_link
    
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)