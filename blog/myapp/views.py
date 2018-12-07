from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView)
from myapp.models import Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from myapp.forms import PostForm,CommentForm
from django.urls import reverse_lazy
# Create your views here.

class PostListView(LoginRequiredMixin,ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class MyPostListView(LoginRequiredMixin,ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-published_date')

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post

class CreatepostView(LoginRequiredMixin,CreateView):
    redirect_field_name = 'myapp/post_detail.html'

    model = Post
    form_class = PostForm

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class UpdatePostview(LoginRequiredMixin,UpdateView):
    redirect_field_name = 'myapp/post_detail.html'
    model = Post
    form_class = PostForm

class PostDeleteView(LoginRequiredMixin,DeleteView):
    success_url = reverse_lazy('post_list')
    model = Post

class DraftListView(LoginRequiredMixin,ListView):
    template_name = 'myapp/post_draft_list.html'
    redirect_field_name = 'myapp/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True, author=self.request.user).order_by('-created_date')

################################################################################

@login_required
def add_comment(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm
        return render(request,'myapp/comment_form.html',{'form':form})

@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def remove_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def publish_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
