from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ideas/', views.VisitIdeaListView.as_view(), name='visitidea_list'),
    path('ideas/nueva/', views.VisitIdeaCreateView.as_view(), name='visitidea_create'),
    path('ideas/<int:pk>/editar/', views.VisitIdeaEditView.as_view(), name='visitidea_edit'),
    path('ideas/<int:pk>/', views.VisitIdeaDetailView.as_view(), name='visitidea_detail'),
]
