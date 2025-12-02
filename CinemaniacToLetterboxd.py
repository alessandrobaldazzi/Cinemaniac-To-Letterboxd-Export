import json
from datetime import datetime
import csv
import random

def cinemaniac_to_list(filename):
    with open(filename, encoding="utf-8") as file:
        data = json.load(file)
    ratings = data['ratings']
    movies = data['movies']

    watched_movies = []
    watchlist = []

    for movie in movies:
        ## Remove unnecessary fields
        movie.pop('title')
        movie.pop('year')
        movie.pop('rating')
        movie.pop('duration')
        movie.pop('genres')
        movie.pop('backdrop')
        movie.pop('note')
        movie.pop('categories')
        movie.pop('overview', None)
        
        ## Change name to remaining ones
        movie['tmdbID'] = movie.pop('id_movie')

        ## Divide watched and not watched movies
        if(movie.pop('seen') == 0):
            movie.pop('date')
            watchlist.append(movie)
        else:
            ## If the date is not reasonable put random date between 2015 and 2020
            if(movie['date'] < 1420070400000):
                movie['date'] = random.randint(1420070400000, 1582070400000)

            ## Add watch date and rating to entry
            movie['WatchedDate'] = datetime.fromtimestamp(movie.pop('date')/1000).strftime("%Y-%m-%d")
            for rating in ratings:
                if(rating['id'] == movie['tmdbID']):
                    movie['Rating10'] = rating['r']
                    ratings.remove(rating)
                    break
            watched_movies.append(movie)
    ## Save to file
    with open('watched_movies.csv', 'w', newline='') as watched_file:
        fieldnames = ["tmdbID", "WatchedDate", "Rating10"]
        writer = csv.DictWriter(watched_file, fieldnames)
        writer.writeheader()
        writer.writerows(watched_movies)
    
    with open('watchlist.csv', 'w', newline='') as watchlist_file:
        fieldnames = ["tmdbID"]
        writer = csv.DictWriter(watchlist_file, fieldnames)
        writer.writeheader()
        writer.writerows(watchlist)


def main():
    filename = "Cinemaniac.bak"
    cinemaniac_to_list(filename)


if __name__ == "__main__":
    main()