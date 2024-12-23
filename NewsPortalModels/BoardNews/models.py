from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_author_post = 0
        rating_author_comments = 0
        rating_comments_to_author_posts = 0
        posts = Post.objects.filter(author_post=self)
        author_comments = Comment.objects.filter(author=self.user)
        comments_to_author_posts = Comment.objects.filter(post__author_post=self)

        for i in posts:
            rating_author_post += i.rating

        for i in author_comments:
            rating_author_comments += i.rating

        for i in comments_to_author_posts:
            rating_comments_to_author_posts += i.rating

        self.rating = rating_author_post * 3 + rating_author_comments + rating_comments_to_author_posts
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    news = 'nw'
    article = 'ar'

    CHOICES_LIST = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]

    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2, choices=CHOICES_LIST, default=news)
    date_time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        if len(self.text) > 124:
            return f'{self.text[:124]}...'
        else:
            return self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
