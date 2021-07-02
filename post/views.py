from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import Http404
from django.utils import timezone
from django.contrib import messages
from django.views import generic
from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
class PostListView(generic.ListView):
    model = models.Post    
                 

    def get_queryset(self):
        return models.Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
class UserPost(generic.ListView):
    model = models.Post
    template_name = ''

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(
                                username__iexact = self.kwargs.get('username')
                                )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(generic.DetailView):
    model = models.Post 

    def get_queryset(self):
        queryset =super().get_queryset()
        return queryset.filter(
            user__username__iexact = self.kwargs.get('username')
        )
class AllPost(generic.DetailView):
    model = models.Post

    

class CreatePost(LoginRequiredMixin,generic.CreateView):
    #form_class = forms.PostForm
    fields = ('author','title','text')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletPost(LoginRequiredMixin,generic.DeleteView):
    model = models.Post
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id =self.request.user.id)
    
    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.method == 'POST':
        form = forms.CommentForm
        if form.is_valid():
            comment = form.save()
            comment.post = post
            comment.save()
            return redirect('posts:all', pk=post.pk)

    else:
        form = forms.CommentForm()
        return render(request,'',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    comment.approve()
    return redirect('post:detail',pk = comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(models.Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post:detail',pk = post_pk)



        