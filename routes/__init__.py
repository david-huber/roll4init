from dice.dice_parser import DiceParser
from flask.helpers import jsonify, url_for, request
import pymongo
from tracker.fighter import Fighter

def add_fighter_routes(app, g):


    @app.route('/fighters/', defaults={'page': 1})
    @app.route("/fighters/<int:page>/")
    def get_fighters(page):
        if page < 1: page = 0

        return jsonify(fighters=g.fighterRepository.find(
            skip=(page-1)*100, limit=100, sort=[('name', pymongo.ASCENDING)]),
            next=url_for("fighters", page=page+1))


    @app.route("/fighter/<fighter_id>", methods=["GET"])
    def get_fighter(fighter_id):
        return jsonify(fighter=g.fighterRepository.find_one(_id=fighter_id))

    def get_initiative():
        dice_parser = DiceParser()
        initiative = dice_parser.parse(request.form["initiative"])
        return initiative

    def save_fighter(fighter):
        g.fighterRepository.save(fighter)
        return jsonify(success=False)

    @app.route("/fighter/<fighter_id>", methods=["PUT"])
    def put_fighter(fighter_id):
        initiative = None
        try:
            initiative = get_initiative()
        except (ValueError):
            return jsonify(success=False)

        fighter = Fighter(id= fighter_id,
            name=request.form["name"],
            initiative=initiative)

        return save_fighter(fighter)

    @app.route("/fighter", methods=["POST"])
    def post_fighter():
        initiative = None
        try:
            initiative = get_initiative()
        except (ValueError):
            return jsonify(success=False)

        fighter = Fighter(name=request.form["name"],
            initiative=initiative)

        return save_fighter(fighter)
