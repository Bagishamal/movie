from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField, TextField, \
    SlugField, ImageField, DateField, ManyToManyField, \
    ForeignKey, BooleanField, GenericIPAddressField, EmailField, PositiveSmallIntegerField
from django.urls import reverse
from django.utils.safestring import mark_safe


class Category(models.Model):
    Name = CharField(
        "Категория",
        max_length=500,
        unique=True
    )
    Description = TextField(
        "Описание",
        blank=True
    )
    Url = SlugField(
        max_length=160,
        unique=True
    )

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["Name"]


class Genre(models.Model):
    Name = CharField(
        "Имя",
        max_length=100,
        unique=True
    )
    Description = TextField(
        "Описание",
        max_length=160,
        blank=True
    )
    Url = SlugField(
        "Ссылка",
        max_length=25,
        unique=True
    )

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "Жанры"
        verbose_name_plural = "Жанры"
        ordering = ["Name"]

def user_directory_path(instance, filename):
    return f'posters/%Y/%m/%d/{filename}'


class DirectorsActors(models.Model):
    Name = CharField(
        "Имя",
        max_length=100,
        unique=True
    )
    Age = PositiveSmallIntegerField(
        "Возраст",
        default=0
    )
    Description = TextField(
        "Описание"
    )
    Image = ImageField(
        "Фото",
        upload_to="directors/%Y/%m/%d"
    )

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "Режиссеры и актеры"
        verbose_name_plural = "Режиссеры и актеры"
        ordering = ["Name"]

    def get_absolute_url(self):
        return reverse("actors_page", kwargs={"slug": self.Name})



class Movie(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    Shirt_size = models.CharField(
        max_length=1,
        choices=SHIRT_SIZES,
        null=True
    )

    Title = CharField(
        "Название",
        max_length=100,
        unique=True
    )
    Tagline = CharField(
        "Слоган",
        max_length=100
    )
    Description = TextField(
        "Описание",
        default=""
    )
    Poster = ImageField(
        "Постеры",
        upload_to=user_directory_path,
        max_length=100
    )
    Year = DateField(
        "Дата выхода",
        default="2021",
    )
    Country = CharField(
        "Страна",
        max_length=30
    )
    Director = ManyToManyField(
        to=DirectorsActors,
        verbose_name="Режиссер",
        related_name="film_director"
    )
    Actors = ManyToManyField(
        to=DirectorsActors,
        verbose_name="Актеры",
        # related_name="film_actors"
    )
    Genre = ManyToManyField(
        to=Genre,
        verbose_name="Жанры"
    )
    World_premier = CharField(
        "Премьера",
        max_length=100,
        default=date.today
    )
    Budjet = PositiveSmallIntegerField(
        "Бюджет",
        default=0,
        help_text="Указывать сумму в долларах"
    )
    Fees_in_Usa = PositiveSmallIntegerField(
        "Сборы в США",
        default=0,
        help_text="Указывать сумму в долларах"
    )
    Fees_in_world = PositiveSmallIntegerField(
        "Сборы в мире",
        default=0,
        help_text="Указывать сумму в долларах"
    )
    Category = ForeignKey(
        Category,
        related_name="cat",
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True
    )
    Url = SlugField(
        max_length=160,
        unique=True
    )
    Draft = BooleanField(
        verbose_name="Черновичок ли ты?",
        default=False
    )

    def get_review(self):
        return self.reviews_set.filter(Parent__isnull=True)

    def get_absolute_url(self):
        return reverse("detail_view", kwargs={"slug":self.Url})

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["Title"]

class RatingStars(models.Model):
    Value = PositiveSmallIntegerField(
        "Значение рейтинга",
        # default=5
    )

    def __str__(self):
        return str(self.Value)

    class Meta:
        verbose_name = "Количество звезд в рейтинге"
        verbose_name_plural = "Количество звезд в рейтинге"
        ordering = ["-Value"]


class Rating(models.Model):
    Ip = GenericIPAddressField(
        "Ip адрес",
        protocol='IPv4',
        null=True
    )
    Stars = ForeignKey(
        to=RatingStars,
        on_delete=models.CASCADE,
        verbose_name="Рейтинг"
    )
    Movie = ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        verbose_name="Фильм",
        null=True
    )

    def __str__(self):
        return f"{self.Stars} - {self.Movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

def get_url_for_frames(instance, filename):
    return mark_safe(f"frames/%Y/%m/%d/{filename}")


class FrameOfMovies(models.Model):
    Title = CharField(
        "Заголовок",
        max_length=100
    )
    Description = TextField(
        "Описание",
    )
    Image = ImageField(
        "Кадры",
        upload_to=get_url_for_frames,
        max_length=50)

    Movie = ForeignKey(
        to=Movie,
        verbose_name="",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"
        ordering = ["Title"]

class Reviews(models.Model):
    Email = EmailField(
        "Email"
    )
    Name = CharField(
        "Имя пользователя",
        max_length=100,
        unique=True
    )
    Text = TextField(
        "Комментарии",
        max_length=5000
    )
    Parent = ForeignKey(
        to='self',
        to_field="Name",
        default="Name",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Родитель"
    )
    Movie = ForeignKey(
        verbose_name="Фильм",
        to=Movie,
        default=5,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.Name} - {self.Movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


# class BookMark(models.Model):
#     user = ManyToManyField(
#         to=User,
#         verbose_name="Пользователь"
#     )
#     mark = ForeignKey(
#         to=Movie,
#         verbose_name='Избранное'
#     )
#
#     class Meta:
#         abstract = True