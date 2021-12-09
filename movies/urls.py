from django.urls import path

from .views import *

urlpatterns = [
    path("", MoviesView.as_view(), name="main"),
    path("test/", TestCaptcha.as_view(), name="test"),
    path("search/", SearchView.as_view(), name="search"),
    path("filter/", FilterMovieViews.as_view(), name="filter"),
    path("add_rating/", AddRating.as_view(), name="add_rating"),
    path("detail/<slug:slug>", MovieDetailView.as_view(), name="detail_view"),
    # path("test_for_forms/", ActorsAdd.as_view(), name="test_forms"),
    path("review/<int:pk>", ReviewView.as_view(), name="create_review"),
    path("actors/<str:slug>/", ActorView.as_view(), name = "actors_page"),

]
