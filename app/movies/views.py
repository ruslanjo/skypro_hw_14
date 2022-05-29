from flask import Blueprint, jsonify
from app.movies.dao.movies_dao import MoviesDAO
from config import DATABASE_PATH

movies_dao = MoviesDAO(DATABASE_PATH)

movies_blueprint = Blueprint('movies_blueprint', __name__)


@movies_blueprint.route('/movie/<title>')
def movie_page(title: str):
    try:
        movie = movies_dao.get_movie_by_title(title)
    except IndexError:
        return jsonify({'error': f'There is no movie with the title {title}'}), 404
    else:
        return jsonify(movie)


@movies_blueprint.route('/movie/<year_from>/to/<year_to>')
def movies_between_two_years(year_from: int, year_to: int):
    try:
        year_from, year_to = int(year_from), int(year_to)
    except ValueError:
        return jsonify({'error': 'year_from and year_to must be integers'})
    else:
        return jsonify(movies_dao.get_movies_by_year_range(year_from, year_to))


@movies_blueprint.route('/rating/<age_group>')
def films_by_rating_page(age_group: str):
    '''
    age_group может принимать значения:
    'children' - рейтинг G
    'family' - рейтинги G, PG, PG-13
    'adult' - рейтинги R, NC-17
    '''
    age_group = age_group.lower()
    if age_group not in ['children', 'family', 'adult']:
        return jsonify({'error': 'age_group not in allowed list'}), 404
    else:
        return jsonify(movies_dao.get_movies_by_age_rating(age_group))


@movies_blueprint.route('/genre/<genre>')
def genre_page(genre):
    return jsonify(movies_dao.get_latest_movies_by_genre(genre))
