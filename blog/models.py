from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Comment(models.Model):
    '''Encapsulate the idea of a Comment on an Article.'''

    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'
    
class Article(models.Model):
    '''Encapsulate the idea of a Article by some author.'''

    # data attributes of a Article:
    user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW
    
    # data attributes of a Article:
    title = models.TextField(blank=False)
    text = models.TextField(blank=False)
    author = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    #image_url = models.URLField(blank=True) # url as a string
    image_file = models.ImageField(blank=True) # an actual image
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('article', kwargs={'pk':self.pk})
    
    def get_comments(self):
        '''Return all of the comments about this article.'''

        comments = Comment.objects.filter(article=self)
        return comments