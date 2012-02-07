import pymongo
from flask.helpers import jsonify, request
from identity import require_logged_in
from tracker.fighter import Fighter
from dice.dice_parser import DiceParser

def add_fighter_routes(app, g):


    @app.route('/fighters/', defaults={'page': 1})
    @app.route("/fighters/<int:page>/")
    @require_logged_in
    def get_fighters(page):
        if page < 1: page = 0

        return jsonify(fighters=g.fighterRepository.find(
            skip=(page-1)*100, limit=100, sort=[('name', pymongo.ASCENDING)]))


    @app.route("/fighter/<fighter_id>", methods=["GET"])
    @require_logged_in
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
    @require_logged_in
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
    @require_logged_in
    def post_fighter():
        initiative = None
        try:
            initiative = get_initiative()
        except (ValueError):
            return jsonify(success=False)

        fighter = Fighter(name=request.form["name"],
            initiative=initiative)

        return save_fighter(fighter)
