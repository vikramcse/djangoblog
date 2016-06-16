from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

import json
from django.template import RequestContext

from .forms import PostForm
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    errors = []

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                print "logged in by " + user.username
                login(request, user)
            else:
                erros.push('account disabled :(')
        else:
            erros.push('Invalid Login')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def log_in(request):
    return render(request, 'blog/login.html')

def dummy(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    data = []
    for p in posts:
        d = {
            'title': str(p.title),
            'author': str(p.author),
            'text': str(p.text),
            'created_date': str(p.created_date),
            'published_date': str(p.published_date),
        }
        data.append(d)

    return render_to_response('blog/dummy.html',
                          {'data': data},
                          context_instance=RequestContext(request))

def log_out(request):
    logout(request)
    return render(request, 'blog/login.html')

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
