from django.db import models

# Create your models here.


class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return '%s'%(self.name)


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=128)
    author = models.CharField(max_length=128)
    date = models.DateTimeField()
    content = models.TextField(max_length=96000)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return '(%i) %s'%(self.id, self.title)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    username = models.CharField(max_length=128)
    content = models.TextField(max_length=2048)

class Rating(models.Model):
    article_id = models.ForeignKey(Article,unique=True, on_delete=models.CASCADE, primary_key=True)
    avg = models.DecimalField(max_digits=3, decimal_places=2)
    rating_count = models.IntegerField()