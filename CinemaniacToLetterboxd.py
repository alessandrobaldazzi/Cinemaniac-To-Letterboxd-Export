import json
from datetime import datetime
import csv
import random
import configparser

def cinemaniac_to_list(config):
    ## Opening input file
    filename = config.get('file-io','input')
    with open(filename, encoding="utf-8") as file:
        data = json.load(file)
    
    ## Creation of movie arrays
    movies = data['movies']

    watched_movies = []
    watchlist = []

    ## Creation of rating array (if selected)
    use_rating = config.get('options','use_rating') == 'True'

    if(use_rating):
        ratings = data['ratings']
        if(len(ratings) == 0):
            use_rating = False

    ## Date logic
    use_save_date_as_diary = config.get('options','use_save_date_as_diary') == 'True'
    random_date_if_invalid = config.get('options','random_date_if_invalid') == 'True'
    random_is_invalid_if_smaller = int(config.get('options','random_is_invalid_if_smaller'))
    random_lower_date = int(config.get('options','random_lower_date'))
    random_upper_date = int(config.get('options','random_upper_date'))

    ## Data manipulation
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
            ## Date append logic
            if(use_save_date_as_diary):
                ## If the date is not reasonable put random date
                if(random_date_if_invalid and movie['date'] < random_is_invalid_if_smaller):
                    movie['date'] = random.randint(random_lower_date, random_upper_date)

                ## Add watch date
                movie['WatchedDate'] = datetime.fromtimestamp(movie.pop('date')/1000).strftime("%Y-%m-%d")
            else:
                movie.pop('date')
            
            ## Rate append logic
            if(use_rating):
                ## Add rating to entry
                for rating in ratings:
                    if(rating['id'] == movie['tmdbID']):
                        movie['Rating10'] = rating['r']
                        ratings.remove(rating)
                        break
            
            watched_movies.append(movie)

    ## Save to file
    watched_filename = config.get('file-io','watched')
    watchlist_filename = config.get('file-io','watchlist')

    with open(watched_filename, 'w', newline='') as watched_file:
        fieldnames = ["tmdbID"]
        if(use_save_date_as_diary):
            fieldnames.append("WatchedDate")
        if(use_rating):
            fieldnames.append("Rating10")
        writer = csv.DictWriter(watched_file, fieldnames)
        writer.writeheader()
        writer.writerows(watched_movies)
    
    with open(watchlist_filename, 'w', newline='') as watchlist_file:
        fieldnames = ["tmdbID"]
        writer = csv.DictWriter(watchlist_file, fieldnames)
        writer.writeheader()
        writer.writerows(watchlist)

## Main Function
def main():
    config = configparser.ConfigParser()
    config.read(r'config.cfg')
    cinemaniac_to_list(config)

if __name__ == "__main__":
    main()