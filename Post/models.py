from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    content = models.TextField(max_length=1000,default="",blank=False)
    createAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.user} - {self.content}"


class Comment(models.Model):
    post = models.ForeignKey(Post,null=True,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comment = models.TextField(blank=False,default="",max_length=1000)
    createdAt = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} - commented : {self.comment} - on {self.post} "