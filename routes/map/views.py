from flask import Flask, Blueprint, render_template, redirect
import os

from helpers.map import create_map_all_walks
from helpers.log import logger

bp_map = Blueprint('map', __name__, template_folder="pages")

@bp_map.route('/')
def index():

    # TODO: cache map, so it doesn't have to be created every time
    create_map_all_walks()

    if os.path.exists("data/webMap.html"):
        with open("data/webMap.html", "r") as file:
            file = file.read()
    else:
        logger.error("Map not found!")
        file = "<h2>Map not found!</h2>"
    
    return render_template("mappage.html", htmlfile=file)