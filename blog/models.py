from django.db import models
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now) #setting the creation time of the post to the current time
    published_date = models.DateTimeField(blank=True , null=True) #can be blank and even null at creation and even later

    def publish(self):
        self.published_date = timezone.now() #setting the publication time
        self.save() #calling the save method found in the models.Model class

    def approve_comments(self):
        return self.comments.filter( approved_comment = True ) 

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE) #the related name field is how post will access comment. in this case it'll by saying post.comments since we set the related name to 'comments'
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
    
    def get_absolute_url(self):  # is been called automatically by django everytime an object of the class is created
        return reverse('post_list')

    def __str__(self):
        return self.text

class Like(models.Model):
    author = models.ForeignKey('auth.User',related_name="likes", on_delete=models.CASCADE,null=True) #there must be an author for every like
    post = models.ForeignKey("blog.Post", related_name="likes", on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey("blog.Comment", related_name="likes", on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f'Like'+str(self.id)

    def like(self):
        super().save()
    
    

#verbose_name is the printable name of the variable/field. That is want i will see in the backend platforme

# Create your models here.
