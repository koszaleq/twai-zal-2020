from django.shortcuts import render

# Create your views here.

from .models import Article, Comment, Rating, Topic
from .forms import CommentForm
from django.http import HttpResponseRedirect

def homePage(request):
    articles = Article.objects.all().order_by('-id')
    for article in articles:
        article.content = article.content[:64] + "..."

    topics = Topic.objects.all()
    return render(request, 'homePage.html', {
        'articles':articles,
        'topics':topics,
    })

def homePageByTopic(request, topicId):
    try:
        articles = Article.objects.filter(topic_id=topicId)
        for article in articles:
            article.content = article.content[:64] + "..."
        topics = Topic.objects.all()
        return render(request, 'homePage.html', {
        'articles':articles,
        'topics':topics,
        })
    except Article.DoesNotExist:
        topics = Topic.objects.all()
        return render(request, 'homePage.html', {
        'articles':[],
        'topics':topics,
        })


def articlerating(request, articleId, rate):
    try:
        article = Article.objects.get(id=articleId)
        rating = Rating.objects.get(article_id=article)
        if 0 < rate <= 5:
            rating.avg *= rating.rating_count
            rating.avg += rate
            rating.rating_count += 1
            rating.avg /= rating.rating_count
            rating.save()
            return HttpResponseRedirect('./')

    except Article.DoesNotExist:
        return render(request, '404.html')
    except Rating.DoesNotExist:
        rating = Rating(article_id=article, avg=0, rating_count=0)
        rating.save()
        return HttpResponseRedirect('./')
    except Exception as ex:
        template = "An excption of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


def getArticle(request, articleId):

    try:
        article = Article.objects.get(id=articleId)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                userName = form.cleaned_data['username']
                content = form.cleaned_data['content']
                comments = Comment.objects.filter(article_id=article, content=content)
                if len(comments) == 0:
                    newComment = Comment(content=content,
                    article_id=article,
                    username=userName)
                    newComment.save()
        comments = Comment.objects.filter(article_id=article)
        rating = None
        try:
            rating = Rating.objects.get(article_id=article)
        except Rating.DoesNotExist:
            rating = Rating(article_id=article, avg=0, rating_count=0)
            rating.save()
        form = CommentForm()
        topics = Topic.objects.all()
        return render(request, 'article.html', {
                'article': article,
                'comments': comments,
                'form': form,
                'rating': rating,
                'topics': topics,
            })
            
    except Article.DoesNotExist:
        return render(request, '404.html')
    except Exception as ex:
        template = "An excption of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def management(request):
    return render(request,'mgmt-panel.html')