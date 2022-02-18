from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from django.db.models import F


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = 'Classic Blog Design'
        return contex


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return contex


class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = 'Записи по тегу' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return contex


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return contex

class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['s'] = f"s={self.request.GET.get('s')}&"
        return contex