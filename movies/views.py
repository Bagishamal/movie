from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse

from .models import *
from .forms import *


class GenreYear():
    def get_genre(self):
        return Genre.objects.all()

    def get_year(self):
        return Movie.objects.filter(Draft=False).values("Year")


# class ActorsAdd(CreateView):
#     form_class = TestReview
#     template_name = "movies/test_for_forms.html"
#     http_method_names = ["get", "post"]
#     success_url = reverse_lazy("test_forms")
#     context_object_name = 'review'
#     # raise_exception=True
#

class AddRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("HTTP_ADDR")


    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.object.update_or_create(
                Ip = self.get_client_ip(request),
                Movie = int(request.POST.get('movie')),
                defaults ={'Stars_id': int(request.POST.get('star'))},
            )
            return  HttpResponse(status=201)
            # form = form.save(commit=False)
            # a = Movie.objects.get(pk=form["movie"])
            # RatingStars.objects.update(Movie = a)
        else:
            return HttpResponse(status=400)

class ActorView(GenreYear, DetailView):
    model = DirectorsActors
    template_name = "movies/actors.html"
    context_object_name = "actor"
    slug_field = 'Name'

    # def get_queryset(self, slug):
    #     q = DirectorsActors.objects.filter(Name = slug)
    #     part = q.Description.split("next")
    #     paginator = (q.Description, 2)

    # def get_context_data(self, film_actors, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["movies"] = Movie.objects.filter(Actors = film_actors.Name)
    #     return context


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    context_object_name = 'movies_detail'
    slug_field = 'Url'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context

class ReviewView(GenreYear, View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.Movie = movie
            # form.Parent_id=form.Name
            if request.POST.get("Parent", None):
                form.Parent = int(request.POST.get("Parent"))
            form.save()
        return redirect(movie.get_absolute_url())


# def get_name(request):
#     if request.method == "POST":
#         form = TextName(request.POST)
#         if form.is_valid():
#             return redirect("main")
#     else:
#         form = TextName()
#
#     return render(request, 'movies/test_for_forms.html', {"form":form})
#
#
# class ActorsAdd(CreateView):
#     form_class = Comment
#     template_name = "movies/test_for_forms"
#     success_url = redirect("main")


class MoviesView(GenreYear, ListView):
    paginate_by = 1

    model = Movie
    queryset = Movie.objects.filter(Draft=False)
    context_object_name = "movies_list"
    allow_empty = False
    ordering = ["Category"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class FilterMovieViews(GenreYear, ListView):
    template_name = "movies/Movie_list.html"
    # context_object_name = "movies_list"
    paginate_by = 2

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(Year__in=self.request.GET.getlist("Year")) |
            Q(Genre__in=self.request.GET.getlist("Genre"))
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["years"] = "".join([f"year={x}&" for x in self.request.GET.getlist("Year")])
        return context

# def TestPagView(request):
#     list = DirectorsActors.objects.all()
#     paginator = Paginator(list, 2)
#
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, "movies/test_paginator.html", {"page_obj": page_obj, "paginator":paginator})

    # template_name = "movies/Movie_list.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def get(self, request):
    #     movies = Movie.objects.all()
    #     return render(request, "movies/Movie_list.html", {"movies_list": movies})
    # queryset = Movie.objects.get(Url=slug)

# class ReviewFormView(CreateView):
#     form_class = ReviewForm
#     fields = ["Text", "Name", "Email"]
#     template_name = "movie/Movie_detail"

# def get_context_data(self, **kwargs):
#     context =


# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context["frames"] = FrameOfMovies.objects.filter(Movie=movies_detail.Movie)

# template_name = "movies/Movie_detail.html"
# queryset = Movie.objects.filter(Url= )
# def get(self, request, slug):
#     movies = Movie.objects.get(Url=slug)
#     return render(request, "movies/Movie_detail.html", {"movies_detail":movies})


# class AddReview(View):
#     def post(self, request, pk):
#         print(request.POST)
#
#         return redirect("/")


# class MoviesView(View):
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/Movie_list.html", {"movies_list": movies})
#
# class MovieDetailView(View):
#     def get(self, request, slug):
#         movies = Movie.objects.get(Url=slug)
#         return render(request, "movies/Movie_detail.html", {"movies_detail":movies})


#
# def index(request):
#     movies = Movie.objects.all()
#
#     context ={
#         "movies":movies
#     }
#
#     return render(request, "movies/Movie_detail.html", context=context)

class SearchView(GenreYear, ListView):
    '''Поиск фильма'''
    paginate_by = 3
    context_object_name = "movies_list"

    def get_queryset(self):
        return Movie.objects.filter(Title__icontains = self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context

class TestCaptcha(FormView):
    form_class = TestCaptchaForm
    template_name = "movies/test_for_captcha.html"
    success_url = reverse_lazy("main")
