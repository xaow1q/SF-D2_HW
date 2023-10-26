from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    userA = models.OneToOneField(User, on_delete=models.CASCADE)
    rateA = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRate = self.post_set.all().aggregate(postRate=Sum('rate'))
        pRate = 0 
        pRate += postRate.get('postRate')

        commentRate = self.userA.comment_set.all().aggregate(comRate=sum('rateC'))
        cRate = 0 
        cRate += commentRate.get('comRate')

        self.rateA = pRate * 3 + cRate 
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length = 64, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    )
    catType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    dateCreate = models.DateTimeField(auto_now_add=True)
    postCat = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256)
    text = models.TextField()
    rate = models.SmallIntegerField(default=0)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

class PostCategory(models.Model):
    postCat = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    postCom = models.ForeignKey(Post, on_delete=models.CASCADE)
    userCom = models.ForeignKey(User, on_delete=models.CASCADE)
    textCom = models.TextField()
    dateCreate = models.DateTimeField(auto_now_add=True)
    rateC = models.SmallIntegerField(default=0)

    def like(self):
        self.rateC += 1
        self.save()

    def dislike(self):
        self.rateC -= 1
        self.save()




