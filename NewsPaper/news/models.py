from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.validators import MinValueValidator


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    @property
    def rating_author(self):  # Определяем рейтинг автора публикации
        return self.rating

    @rating_author.setter
    def rating_author(self, value):  # Записываем рейтинг автора публикации
        self.rating = int(value) if value >= 0 else 0
        self.save()

    def update_rating(self):  # Пересчет рейтинга в соответствии с условием задачи
        self.rating = 0
        self.comment_rating = 0
        self.post_rating = 0
        self.total_comment_post = 0
        for com_iter in Comment.objects.filter(comment_user=self.user):
            self.comment_rating = self.comment_rating + com_iter.comment_rating
        for post_iter in Post.objects.filter(author=self):
            self.post_rating = self.post_rating + post_iter.post_rating
            for com_iter in Comment.objects.filter(comment_post=post_iter):
                self.total_comment_post = self.total_comment_post + com_iter.comment_rating
        self.rating = (self.post_rating * 3) + self.comment_rating + self.total_comment_post
        self.save()

    def __str__(self):  # При обращении возвращаем текст
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    news = 'news'
    articles = 'articles'

    CHOICES = [
        (news, 'Новости'),
        (articles, 'Статьи')]

    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    text = models.TextField()
    choice = models.CharField(max_length=10, choices=CHOICES, default=articles)
    posting_time = models.DateTimeField(null=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    post_rating = models.IntegerField(default=0)

    @property
    def rating_post(self):  # Определяем рейтинг  публикации
        return self.post_rating

    @rating_post.setter
    def rating_post(self, value):  # Записываем рейтинг  публикации
        self.post_rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):  # Превью длинной 124 символа
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'{self.news.title()}: {self.text[:10]}'  # !!!!!!!!!!!!!!!!!!!!

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)  # Связь: один ко многим
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)  # Связь: один ко многим

    def __str__(self):
        return self.category  # !!!!!!!!!!!!!!!!!!!


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(null=False)
    comment_date = models.DateTimeField(null=True)
    comment_rating = models.IntegerField(default=0)

    @property
    def rating_comment(self):  # Определяем рейтинг комментария
        return self.comment_rating

    @rating_comment.setter
    def rating_comment(self, value):  # Записываем рейтинг комментария
        self.comment_rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )