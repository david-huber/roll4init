from flask.helpers import jsonify, url_for

import pymongo

def add_fighter_routes(app, g):


    @app.route('/fighters/', defaults={'page': 1})
    @app.route("/fighters/<int:page>/")
    def get_fighters(page):
        if page < 1: page = 0

        return jsonify(fighters=g.fighterRepository.find(skip=(page-1)*100, limit=100, sort=[('name', pymongo.ASCENDING)]),
            next=url_for("fighters", page=page+1))


    @app.route("/fighter/<fighter_id>", methods=["GET"])
    def get_fighter(fighter_id):
        return jsonify(fighter=g.fighterRepository.find_one(_id=fighter_id))

    @app.route("/fighter/<fighter_id>", methods=["PUT"])
    def put_fighter(fighter_id):
        pass

    @app.route("/fighter", methods=["POST"])
    def post_fighter():
        pass