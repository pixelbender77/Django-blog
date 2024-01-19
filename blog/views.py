from django.shortcuts import render , get_object_or_404 , redirect 
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
from blog.models import Post,Comment,Like
from blog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User


class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now())  .order_by('-published_date') #descending order

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm    
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm    
    model = Post

class  PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date') # ascending order


#########################################     ######################################
#                                   FUNCTION CALLS
#########################################     ######################################

#I think these functions down here with the decorators are the equivalence of methods of an
#actuall manager class for the website. The difference here is that we can't create a class like that,
#since we'll have to fetch all records from database, instanciate and store them in say lists held by that
#that class. It will occupy space on the server and make the website slow. 
#    Instead, we get requests from client server, instanciate only at that moment and call member functions when 
# neccessary. We then use decorators to restrict or limit the access to the functions to a precise category of user
# user/ Client


@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


@login_required # You must be loggedin in order to comment any posts
def add_comment_to_post(request,pk):
    print("COMMENTING POST")
    post = get_object_or_404(Post,pk=pk) #getting the object of type 'Post' having that primary key
    if request.method == 'POST': #if the form was submitted already
        form = CommentForm(request.POST) #creating a Comment instance with the information filled in the form
        if form.is_valid(): #if the information was correctly filled...
            comment = form.save(commit=False) #we create a comment but do not commit it yet since it has a post field that can't be null. In other words, a comment must belong to a post
            comment.post = post #assigning the gotten/current post to the primary(not null) field of the comment. In other words, making the comment belong to a post
            comment.save() #saving the comment since it now has all the required fields
            return redirect('post_detail',pk=post.pk) # redirecting to post detail page with it's primary key after comment is posted
    else:
        form = CommentForm() #if the form was not submitted
    return render(request,'blog/comment_form.html',{'form':form}) #This will happen in 2 cases. Either the form is loaded for the first time, or the form was submitted already but wasn't valid                                                              # in both cases, it's all about the form not being complete

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk) #getting the comment object having that particular primary key
    comment.approve() #calling the approve method in that comment object to approve the comment
    return redirect('post_detail',pk=comment.post.pk) #redirecting to the post detail page after approving comment

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_primary_key = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_primary_key)

#@login_required
def add_like_to_post(request,pk):
    if request.user.is_authenticated :
        print("LIKED POST")
        post = get_object_or_404(Post,pk=pk)
        like = Like.objects.filter(author__id = request.user.id) & Like.objects.filter(post=post) # fetching the like object belonging to this particular post in the list of the user's likes
        
        #like = Like.objects.filter(Q(author__id=request.user.id)& Q(post=post) ) # This two queries are the same. Notice the (Like.objects.filter) which has been kind of 'factorized' thats to the Q objects. nice for complex queries 
        if not like : #if like does not exist (yet)(or might have been deleted(by an unlike event)), then it's our duty to create one
            print("Like Did not exist")
            newLike = Like()
            newLike.post = post
            newLike.author = request.user
            newLike.like()
        else:
            print("Like EXISTED")
            like.delete() #if User had like that post already, we delete it. (Unliking post)
        return redirect('post_detail',pk=post.pk)
    
    return redirect('login') #if user isn't authenticated then we redirect him to the login page

@login_required
def add_like_to_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    like = Like()
    like.save(commit=False)
    like.comment = comment
    like.save()
    return redirect('post_detail',pk=like.post.pk)

def coding(request):
    pass

'''
def add_like_to_post(request,pk):
    print("LIKED POST")
    post = get_object_or_404(Post,pk=pk)
    like = Like()
    like.post = post #attributing the gotten post to the like
    like.save()
    return redirect('post_detail',pk=like.post.pk)

def add_like_to_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    like = Like()
    like.save(commit=False)
    like.comment = comment
    like.save()
    return redirect('post_detail',pk=like.post.pk)
    '''

# Create your views here
