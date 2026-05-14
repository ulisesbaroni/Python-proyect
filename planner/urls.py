from django.urls import path
from . import views

urlpatterns = [
    # Places
    path('lugares/', views.PlaceListView.as_view(), name='place_list'),
    path('lugares/nuevo/', views.PlaceCreateView.as_view(), name='place_create'),
    path('lugares/<int:pk>/', views.PlaceDetailView.as_view(), name='place_detail'),
    path('lugares/<int:pk>/editar/', views.PlaceEditView.as_view(), name='place_edit'),
    path('lugares/<int:pk>/borrar/', views.PlaceDeleteView.as_view(), name='place_delete'),

    # VisitIdeas
    path('ideas/', views.VisitIdeaListView.as_view(), name='visitidea_list'),
    path('ideas/nueva/', views.VisitIdeaCreateView.as_view(), name='visitidea_create'),
    path('ideas/<int:pk>/', views.VisitIdeaDetailView.as_view(), name='visitidea_detail'),
    path('ideas/<int:pk>/editar/', views.VisitIdeaEditView.as_view(), name='visitidea_edit'),
]
