from django.shortcuts import render

from ticketing.models import ShowTime
from .models import Movie, Cinema


def movie_list(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'ticketing/movie_list.html', context)


def cinema_list(request):
    cinemas = Cinema.objects.all()
    context = {
        'cinemas': cinemas
    }
    return render(request, 'ticketing/cinema_list.html', context)


def movie_details(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    context = {
        'movie': movie
    }
    return render(request, 'ticketing/movie_detail.html', context)


def cinema_details(request, cinema_id):
    cinema = Cinema.objects.get(cinema_code=cinema_id)
    context = {
        'cinema': cinema,
    }
    return render(request, 'ticketing/cinema_detail.html', context)


def showtime_list(request):
    showtimes = ShowTime.objects.all().order_by('start_time')
    context = {
        'showtimes': showtimes
    }
    return render(request, 'ticketing/showtime_list.html', context)
