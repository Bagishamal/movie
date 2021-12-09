from modeltranslation.translator import register, TranslationOptions
from .models import Category, Genre, DirectorsActors, Movie, FrameOfMovies


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('Name', 'Description',)


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('Name', 'Description',)


@register(DirectorsActors)
class DirectorsActorsTranslationOptions(TranslationOptions):
    fields = ('Name', 'Description', 'Age')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('Title', 'Tagline', 'Description',)


@register(FrameOfMovies)
class FrameOfMoviesTranslationOptions(TranslationOptions):
    fields = ('Title', 'Description',)
