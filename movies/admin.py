from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _


class MovieAdminForm(forms.ModelForm):
    Description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


class FramesInline(admin.TabularInline):
    model = FrameOfMovies
    extra = 1
    readonly_fields = ("get_html_photo",)

    def get_html_photo(self, obj):
        if obj.Image:
            return mark_safe(f"<img src={obj.Image.url} width=50 height=50>")

    get_html_photo.short_description = "Кадр"


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"Url": ("Name",)}
    list_display = ("id", "Name", "Url")
    list_display_links = ("Name",)


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"Url": ("Name",)}


admin.site.register(Genre, GenreAdmin)


@admin.register(DirectorsActors)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("Name", "Age", "get_html_photo")
    readonly_fields = ("get_html_photo",)
    # prepopulated_fields = {"slug":("Name", )}

    def get_html_photo(self, obj):
        if obj.Image:
            return mark_safe(f"<img src={obj.Image.url} width=24 height=24")

    get_html_photo.short_description = "Фото"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"Url": ("Title",)}
    list_display = ("Title", "Category", "Url", "Draft", "get_html_photo")
    list_display_links = ("Title",)
    list_editable = ("Draft", "Category")
    list_filter = ("Category", "Title", "Genre")
    readonly_fields = ("get_html_photo",)
    form = MovieAdminForm
    actions = ["unpublish", "publish"]
    search_fields = ("Title", "Category__Name")
    # fields = ("Title", "Url")
    # inlines = [FramesInline, ReviewInline]
    # save_on_top = True
    save_as = True
    fieldsets = (
        ("Name", {
            "fields": (("Shirt_size", "Title", "Tagline"),)
        }),
        (None, {
            "fields": (("Description", "Poster", "get_html_photo"),)
        }),
        (None, {
            "fields": (("Year", "Country"),)
        }),
        (None, {
            "fields": (("Director", "Actors"),)
        }),
        ("Not important", {
            "fields": (("Genre", "World_premier", "Budjet", \
                        "Fees_in_Usa", "Fees_in_world", "Category", "Url", "Draft"),),
            "classes": ("collapse",)
        }),
    )

    def get_html_photo(self, object):
        if object.Poster:
            return mark_safe(f"<img src={object.Poster.url} width=24 height=24>")

    get_html_photo.short_description = "Постер"

    def unpublish(self, request, queryset):
        """Снятие с публикации"""
        row_update = queryset.update(Draft=True)
        if row_update == 1:
            self.message_user(request, "1 запись обновлена")
        else:
            self.message_user(request, f"{row_update} записей было обновлено")

    unpublish.short_description = 'Снять с публикации записи'
    unpublish.allowed_permissions = ('change', )

    def publish(self, request, queryset):
        row_update = queryset.update(Draft=False)
        if row_update == 1:
            self.message_user(request, "1 запись обновлена")
        else:
            self.message_update(request, f"{row_update} записей обновлено")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ("change", )




# admin.site.register(Movie, MovieAdmin)
@admin.register(RatingStars)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("Value",)
    list_filter = ("Value",)

    save_as = True
    save_on_top = True

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["Ip","Stars","Movie"]


@admin.register(FrameOfMovies)
class FrameOfMoviesAdmin(admin.ModelAdmin):
    list_display = ("Title", "Image", "get_html_photo")
    readonly_fields = ("get_html_photo",)

    def get_html_photo(self, obj):
        if obj.Image:
            return mark_safe(f"<img src={obj.Image.url} width=50 height=50>")


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("Name", "Email", "Movie", "Parent")
    list_display_links = ("Name",)
    list_filter = ("Name",)
    search_fields = ("Text", "Movie")
    readonly_fields = ("Email", "Name")


admin.site.site_title = "Видеотека"
admin.site.site_header = "Домашняя библиотека"
