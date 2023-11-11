from django.urls import path

from . import views

app_name = 'ticketing'
urlpatterns = [
    path('movies/', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_details, name='movie_detail'),
    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinema/<int:cinema_id>/', views.cinema_details, name='cinema_detail'),
    path('showtime/', views.showtime_list, name='showtime_list'),
]
