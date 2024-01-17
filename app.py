from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

import music_review

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

br = music_review.MusicReview()

class PostReview(Resource):
    def post(self):
        """
        This method responds to the POST request for adding a music review to the database.
        ---
        tags:
        - music Reviews
        parameters:
            - in: body
              name: body
              required: true
              schema:
                id: MusicReview
                required:
                  - music
                  - rating
                properties:
                  music:
                    type: string
                    description: the name of the music
                  rating:
                    type: integer
                    description: the rating of the music (1-10)
                  notes:
                    type: string
                    default: ""
                    description: any additional notes about the music
        responses:
            201:
                description: A successful POST request
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                message:
                                    type: string
                                    description: A success message
            400:
                description: Bad request if the required fields are missing
        """
        data = request.json

        print(data)

        if not data:
            return {"error": "Request body must be in JSON format."}, 400

        music = data.get('music')
        review = data.get('rating')
        notes = data.get('notes', '')

        # Check if the required fields are provided
        if not music or not review:
            return {"error": "Both 'music' and 'rating' are required fields."}, 400
        
        # Add the new review to the database
        br.add_music_rating(music, review, notes)

        return {"message": "music review added successfully."}, 201

class AllReviews(Resource):
    def get(self):
        """
        This method responds to the GET request for retrieving all music reviews.
        ---
        tags:
        - music Reviews
        parameters:
            - name: sort
              in: query
              type: string
              required: false
              enum: [ASC, DESC]
              description: Sort order for reviews (ascending or descending)
            - name: max_records
              in: query
              type: integer
              required: false
              description: Maximum number of records to retrieve
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: array
                        items:
                            type: object
                            properties:
                                music_title:
                                    type: string
                                    description: The music title
                                music_rating:
                                    type: number
                                    description: The music rating
                                music_notes:
                                    type: string
                                    description: The music review
        """
        sort = request.args.get('sort', default=None)
        max_records = int(request.args.get('max_records', default=10))

        # Validate the sort parameter
        if sort and sort not in ['ASC', 'DESC']:
            return {"error": "Invalid sort value"}, 400

        # Sort the reviews based on the 'sort' parameter
        if sort == 'ASC':
            music_reviews = br.get_music_ratings(sort=sort, max_records=max_records)
        elif sort == 'DESC':
            music_reviews = br.get_music_ratings(sort=sort, max_records=max_records)
        else:
            music_reviews = br.get_music_ratings(max_records=max_records)

        return music_reviews, 200


class UppercaseText(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
        """
        text = request.args.get('text')

        return {"text": text.upper()}, 200
    
class ProcessText(Resource):
    def get(self):
        """
        This method responds to the GET request for processing text and returns the processed text.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be processed
            - name: duplication_factor
              in: query
              type: integer
              required: false
              description: The number of times to duplicate the text
            - name: capitalization
              in: query
              type: string
              required: false
              enum: [UPPER, LOWER, None]
              description: The capitalization style for the text
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            processed_text:
                                type: string
                                description: The processed text
        """
        text = request.args.get('text')
        duplication_factor = int(request.args.get('duplication_factor', 1))
        capitalization = request.args.get('capitalization', 'None')

        # Validate capitalization input
        if capitalization not in ['UPPER', 'LOWER', 'None']:
            return {"error": "Invalid capitalization value"}, 400

        # Process the text based on duplication_factor and capitalization
        if capitalization == 'UPPER':
            text = text.upper()
        elif capitalization == 'LOWER':
            text = text.lower()

        processed_text = text * duplication_factor

        return {"processed_text": processed_text}, 200

api.add_resource(PostReview, "/review")
api.add_resource(AllReviews, "/all_reviews")
api.add_resource(ProcessText, "/process_text")
api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)