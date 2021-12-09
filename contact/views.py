from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .forms import *
from .models import *


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = "/"
