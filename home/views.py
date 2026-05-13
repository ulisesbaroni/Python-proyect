from django.views import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html')