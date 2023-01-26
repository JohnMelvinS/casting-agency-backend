import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    # Manually Push a Context https://flask.palletsprojects.com/en/2.2.x/appcontext/
    with app.app_context():
        setup_db(app)

    cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
        )
        return response
  
    # ROUTES
    '''
    GET /actors
        it will require the 'get:actors' permission
        it will contain the actor.format() data representation
    returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
        or appropriate status code indicating reason for failure
    '''
    # Route that retrieves all actors.
    # JSON Response body keys: 'success', and 'actors'
    @app.route('/api/v1/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()
        fromatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": fromatted_actors
        })

    '''
    GET /actors/<id>
        where <id> is the existing model id
        it will require the 'get:actors' permission
        it will contain the actor.format() data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the actor with id '<id>'
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/actors/<int:id>')
    @requires_auth('get:actors')
    def get_actor_detail(payload,id):
        actor = Actor.query.get_or_404(id)

        return jsonify({
            "success": True,
            'actors': [actor.format()]
        }), 200
    
    '''
    POST /actors
        it will create a new row in the actors table
        it will require the 'post:actors' permission
        it will contain the actor.format() data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the newly created actor
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(payload):
        body = request.get_json()

        if 'name' and 'gender' and 'dob' not in body:
            abort(400)

        new_name = body['name']
        new_gender = body['gender']
        new_dob = body['dob']

        try:
            actor = Actor(name=new_name, gender=new_gender, dob=new_dob)
            actor.insert()
            return jsonify(
                {
                    "success": True,
                    'actors': [actor.format()]
                }
            )
        except:
            abort(422)

    '''
    PATCH /actors/<id>
        where <id> is the existing model id
        it will respond with a 404 error if <id> is not found
        it will update the corresponding row for <id>
        it will require the 'patch:actors' permission
        it will contain the actor.format() data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(payload,id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            
            if actor is None:
                abort(404)
            
            body = request.get_json()
            if 'name' in body:
                actor.name = body['name']
            if 'gender' in body:
                actor.gender = body['gender']
            if 'dob' in body:
                actor.dob = body['dob']

            actor.update()
            return jsonify(
                {
                    "success": True,
                    'actors': [actor.format()]
                }
            )
        except:
            abort(422)
    
    '''
    DELETE /actors/<id>
        where <id> is the existing model id
        it will respond with a 404 error if <id> is not found
        it will delete the corresponding row for <id>
        it will require the 'delete:actors' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload,id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            
            if actor is None:
                abort(404)
            
            actor.delete()
            
            return jsonify({
                "success": True,
                "delete": id
            })
        except:
            abort(422)
    
    '''
    GET /movies
        it will require the 'get:movies' permission
        it will contain only the movie.format() data representation
    returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()
        fromatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": fromatted_movies
        })

    '''
    GET /movies/<id>
        where <id> is the existing model id
        it will require the 'get:movies' permission
        it will contain the movie.format() data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the movie with id '<id>'
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/movies/<int:id>')
    @requires_auth('get:movies')
    def get_movie_detail(payload,id):
        movie = Movie.query.get_or_404(id)

        return jsonify({
            "success": True,
            'movies': [movie.format()]
        }), 200
    
    '''
    POST /movies
        it will create a new row in the movies table
        it will require the 'post:movies' permission
        it will contain the movie.format() data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the newly created movie
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        body = request.get_json()

        if 'title' and 'release_date' not in body:
            abort(400)

        new_title = body['title']
        new_release_date = body['release_date']
        if 'cast' in body:
            for id in body["cast"]:
                Actor.query.get_or_404(id)
            new_cast = Actor.query.filter(Actor.id.in_(body["cast"])).all()

        try:
            movie = Movie(title=new_title, release_date=new_release_date, cast=new_cast)
            movie.insert()
            return jsonify(
                {
                    "success": True,
                    'movies': [movie.format()]
                }
            )
        except:
            abort(422)

    '''
    PATCH /movies/<id>
        where <id> is the existing model id
        it will respond with a 404 error if <id> is not found
        it will update the corresponding row for <id>
        it will require the 'patch:movies' permission
        it will contain the movie.format() data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(payload,id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            
            if movie is None:
                abort(404)
            
            body = request.get_json()
            if 'title' in body:
                movie.title = body['title']
            if 'release_date' in body:
                movie.release_date = body['release_date']
            if 'cast' in body:
                for id in body["cast"]:
                    Actor.query.get_or_404(id)
                movie.cast = Actor.query.filter(Actor.id.in_(body["cast"])).all()

            movie.update()
            return jsonify(
                {
                    "success": True,
                    'movies': [movie.format()]
                }
            )
        except:
            abort(422)
    
    '''
    DELETE /movies/<id>
        where <id> is the existing model id
        it will respond with a 404 error if <id> is not found
        it will delete the corresponding row for <id>
        it will require the 'delete:movies' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
    '''
    @app.route('/api/v1/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload,id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            
            if movie is None:
                abort(404)
            
            movie.delete()
            
            return jsonify({
                "success": True,
                "delete": id
            })
        except:
            abort(422)
  
    """
    Error Handlers
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False, 
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)