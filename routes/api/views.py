import os
import json
from flask import Flask, Blueprint, request
from helpers.log import logger
from helpers.map import get_color

bp_api = Blueprint('api', __name__)


@bp_api.route('/test', methods=['POST'])
def test():
    print(request.json)
    logger.info("Hello, World!")
    return 'Hello, World!'


@bp_api.route('/upload_walks', methods=['POST'])
def upload_walks():
    # data as list of walk data

    # clear all walks
    for file in os.listdir("data/walks"):
        os.remove("data/walks/" + file)

    walk_config = {}
    new_walk_config = {}
    if os.path.exists("data/walk_config.json"):
        with open("data/walk_config.json", "r") as file:
            walk_config = json.load(file)


    for walk in request.json:
        # save walk to file
        with open(f"data/walks/{walk['start_time']}.json", "w") as file:
            json.dump(walk, file)

        # create new walk config
        if walk["start_time"] in walk_config:
            new_walk_config[walk["start_time"]] = walk_config[walk["start_time"]]
        else:
            new_walk_config[walk["start_time"]] = {"name": str(walk["start_time"]), "included": True, "color": get_color(255,0,0)}

    # save walk config
    with open("data/walk_config.json", "w") as file:
        json.dump(new_walk_config, file)
    

    return 'Walks uploaded!', 200

