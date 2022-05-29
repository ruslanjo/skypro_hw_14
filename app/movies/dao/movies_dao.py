import sqlite3
from collections import Counter
from config import CHILDREN_RATING, FAMILY_RATING, ADULT_RATING

counter = Counter()


def define_rating_by_keyword(age_rating: str) -> list:
    if age_rating.lower() == 'children':
        return CHILDREN_RATING
    elif age_rating.lower() == 'family':
        return FAMILY_RATING
    elif age_rating.lower() == 'adult':
        return ADULT_RATING


class MoviesDAO:
    def __init__(self, path: str) -> None:
        self.path = path

    def get_data_from_db(self, query: str) -> list:
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            result = cursor.execute(query).fetchall()
            return result

    def get_movie_by_title(self, title_to_find: str) -> dict:
        title_to_find = title_to_find.lower()
        title_query = f"""
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE LOWER(title) LIKE '%{title_to_find}%'
                    ORDER BY release_year DESC
                    LIMIT 1
                    """
        result = self.get_data_from_db(title_query)
        result = result[0]  # т.к. возвращается список из одного элемента
        result_to_return = {
            'title': result[0],
            'country': result[1],
            'release_year': result[2],
            'genre': result[3],
            'description': result[4]
        }
        return result_to_return

    def get_movies_by_year_range(self, year_from: int, year_to: int) -> list:
        if year_from > year_to:  # Защита на случай, если передан первый год, больший чем второй
            year_from, year_to = year_to, year_from
        year_range_query = f'''
                  SELECT title, release_year
                  FROM netflix
                  WHERE release_year BETWEEN {year_from} AND {year_to}
                  LIMIT 100
                  '''
        result = self.get_data_from_db(year_range_query)
        movies_list = []
        for row in result:
            movies_list.append({'title': row[0],
                                'release_year': row[1]})
        return movies_list

    def get_movies_by_age_rating(self, age_rating: str) -> list:
        rating = define_rating_by_keyword(age_rating)
        rating_query = f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating in {rating}
        """
        result = self.get_data_from_db(rating_query)
        movies_list = []
        for row in result:
            movies_list.append({'title': row[0],
                                'rating': row[1],
                                'description': row[2]})
        return movies_list

    def get_latest_movies_by_genre(self, genre: str) -> list:
        genre = genre.lower()
        '''Функция, которая получает название жанра в качестве аргумента и возвращает 10
        самых свежих фильмов в формате json'''
        genre_query = f"""
        SELECT title, description
        FROM netflix 
        WHERE LOWER(listed_in) LIKE '%{genre}%'
        ORDER BY date_added DESC
        LIMIT 10
        """
        result = self.get_data_from_db(genre_query)
        movies_list = []
        for row in result:
            movies_list.append({'title': row[0],
                                'description': row[1]})
        return movies_list

    def get_actors_who_played_more_than_2_times(self, actor_1: str, actor_2: str) -> list:
        '''
         Функция, которая получает в качестве аргумента имена двух актеров, сохраняет всех актеров
         из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз
        '''
        cast_query = f'''
        SELECT `cast`
        FROM netflix
        WHERE `cast` LIKE '%{actor_1}%'
          AND `cast` LIKE '%{actor_2}%'
        '''
        result = self.get_data_from_db(cast_query)
        for row in result:
            for actor in row[0].split(','):
                if actor.lower().strip() not in [actor_1.lower(), actor_2.lower()]:
                    counter[actor.strip()] += 1
        return [key for key, value in counter.items() if value >= 2]

    def get_movies_by_type_genre_year(self, picture_type: str, genre: str, year: int) -> list:
        picture_type, genre, year = picture_type.lower(), genre.lower(), int(year)
        query = f'''
        SELECT title, description
        FROM netflix
        WHERE release_year = {year}
          AND LOWER(listed_in) LIKE '%{genre}%'
          AND LOWER(`type`) LIKE '%{picture_type}%'
        '''
        result = self.get_data_from_db(query)
        movies_list = []
        for row in result:
            movies_list.append({'title': row[0], 'description': row[1]})
        return movies_list
