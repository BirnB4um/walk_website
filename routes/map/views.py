
from flask import Flask, Blueprint, render_template, redirect

bp_map = Blueprint('map', __name__, template_folder="pages")

@bp_map.route('/')
def index():

    with open("data/webMap.html", "r") as file:
        file = file.read()
    
    return render_template("mappage.html", htmlfile=file)