from flask_app.models.user import User
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


db = 'andrewexam2_db'

class Sighting:
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date_made = data['date_made']
        self.num_sasquatch = data['num_sasquatch']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    #Create Sighting
    @classmethod
    def create_sighting(cls,data):
        query = """
            INSERT INTO sightings (location, description, date_made, num_sasquatch, user_id)
            VALUES(%(location)s,%(description)s,%(date_made)s,%(num_sasquatch)s,%(user_id)s);
            """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM sightings
                JOIN users ON users.id = sightings.user_id;
                """
        results = connectToMySQL(db).query_db(query)
        sightings = []
        for sighting in results:
            new_sighting = cls(sighting)
            creator_data = {
            'id': sighting['users.id'],
            'first_name': sighting['first_name'],
            'last_name': sighting['last_name'],
            'email': sighting['email'],
            'password': sighting['password'],
            'created_at': sighting['users.created_at'],
            'updated_at': sighting['users.updated_at']
        }
            new_sighting.creator = User(creator_data)
            sightings.append(new_sighting)
        return sightings

    #@classmethod
    #def get_one(cls, data):
    #   query = """
    #        SELECT * FROM sightings 
    #        JOIN users ON users.id = sightings.user_id
    #        WHERE sightings.id = %(id)s
    #        """
    #    results = connectToMySQL(db).query_db(query, data)
    #    print(results)
    #    sighting = cls(results[0])
    #    owner_data = {
    #        'id': results[0]['users.id'],
    #       'first_name': results[0]['first_name'],
    #        'last_name': results[0]['last_name'],
    #        'email': results[0]['email'],
    #        'password': results[0]['password'],
    #        'created_at': results[0]['users.created_at'],
    #        'updated_at': results[0]['users.updated_at']
    #    }
    #    sighting.owner = User(owner_data)

    @classmethod
    def get_one(cls, data):
        query = """
            SELECT * FROM sightings 
            JOIN users ON users.id = sightings.user_id
            WHERE sightings.id = %(id)s
            """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        sighting = cls(results[0])
        creator_data = {  
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        sighting.creator = User(creator_data)
        return sighting

    @classmethod
    def update_sighting(cls, form_data, sighting_id):
        query = f'UPDATE sightings SET location = %(location)s, description = %(description)s, date_made = %(date_made)s, num_sasquatch = %(num_sasquatch)s WHERE id = {sighting_id};'
        return connectToMySQL(db).query_db(query, form_data)    

    @classmethod
    def delete_sighting(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)


    @staticmethod
    def validate(sighting):
        # what is validate doing? Well it is a function that is validating the sight
        isValid = True
        if len(sighting['location']) < 3:
            isValid = False
            flash("Name must be at least 3 characters.")
        if len(sighting['description']) < 3:
            isValid = False
            flash("Description must be at least 3 characters.")
        if len(sighting['date_made']) <= 0:
            isValid = False
            flash("Date is required.")
        if len(sighting['num_sasquatch']) <= 0:
            isValid = False
            flash("Number of Sasquatch is required.")
        return isValid