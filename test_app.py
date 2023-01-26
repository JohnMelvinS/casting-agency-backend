import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.empty_object = {}

        self.actor = {
            "name" : "Tom Cruise",
            "gender" : "male",
            "dob" : "July 3, 1962"
        }
        
        self.new_movie = {
            "title" : "Mission: Impossible - Dead Reckoning - Part One",
            "release_date" : "2023-07-14",
            "cast": []
        }

        self.update_movie = {
            "title" : "Untitled Ghostbusters Afterlife Sequel",
            "release_date" : "December 20, 2023",
            "cast": [1]
        }

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "postgres", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.jwt_assistant = os.environ['JWT_ASSISTANT']
        self.jwt_director = os.environ['JWT_DIRECTOR']
        self.jwt_executive_producer = os.environ['JWT_EXECUTIVE_PRODUCER']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_authorization_header_missing(self):
        res = self.client().get("/api/v1/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Authorization Header Missing")

    '''
    GET /actors
    '''
    def test_get_actors_200(self):
        res = self.client().get("/api/v1/actors", headers={
            'Authorization': "Bearer {}".format(self.jwt_assistant)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_get_actors_401_authorization_header_must_be_bearer_token(self):
        res = self.client().get("/api/v1/actors", headers={
            'Authorization': "Basic Auth {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Authorization Header Must Be Bearer Token")

    '''
    GET /actors/<id>
    '''
    def test_get_actor_detail_200(self):
        res = self.client().get("/api/v1/actors/1", headers={
            'Authorization': "Bearer {}".format(self.jwt_director)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_get_actor_detail_401_token_not_found(self):
        res = self.client().get("/api/v1/actors/1", headers={
            'Authorization': "Bearer"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Token Not Found")

    '''
    POST /actors
    '''
    def test_post_actor_create_200(self):
        res = self.client().get("/api/v1/actors", json=self.actor, headers={
            'Authorization': "Bearer {}".format(self.jwt_director)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_post_actor_create_400(self):
        res = self.client().post("/api/v1/actors", json=self.empty_object, headers={
            'Authorization': "Bearer {}".format(self.jwt_director)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    '''
    PATCH /actors/<id>
    '''
    def test_patch_actor_update_200(self):
        res = self.client().patch("/api/v1/actors/14", json=self.actor, headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_patch_actor_update_405(self):
        res = self.client().patch("/api/v1/actors", json=self.actor, headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    '''
    DELETE /actors/<id>
    '''
    def test_delete_actor_200(self):
        # NOTE: Delete a different actor in each attempt
        res = self.client().delete("/api/v1/actors/10", headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], 10)

    def test_delete_actor_422(self):
        res = self.client().delete("/api/v1/actors/10000", headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Entity")

    '''
    GET /movies
    '''
    def test_get_movies_200(self):
        res = self.client().get("/api/v1/movies", headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    # TO DO FAILURE

    '''
    GET /movies/<id>
    '''
    def test_get_movie_detail_200(self):
        res = self.client().get("/api/v1/movies/1", headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    # TO DO FAILURE

    '''
    POST /movies
    '''
    def test_post_movie_create_200(self):
        res = self.client().post("/api/v1/movies", json=self.new_movie, headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_post_movie_create_405(self):
        res = self.client().post("/api/v1/movies/1", json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    '''
    PATCH /movies/<id>
    '''
    def test_patch_movie_update_200(self):
        res = self.client().patch("/api/v1/movies/8", json=self.update_movie, headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_patch_movie_update_403(self):
        res = self.client().patch("/api/v1/movies/8", json=self.update_movie, headers={
            'Authorization': "Bearer {}".format(self.jwt_assistant)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission Not Found")

    '''
    DELETE /movies/<id>
    '''
    def test_delete_movie_200(self):
        # NOTE: Delete a different movie in each attempt
        res = self.client().delete("/api/v1/movies/2", headers={
            'Authorization': "Bearer {}".format(self.jwt_executive_producer)
        })
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], 2)

    def test_delete_movie_403(self):
        res = self.client().delete("/api/v1/movies/10000", headers={
            'Authorization': "Bearer {}".format(self.jwt_director)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission Not Found")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()