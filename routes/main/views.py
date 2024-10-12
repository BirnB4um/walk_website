
from flask import Flask, Blueprint, render_template, redirect


bp_main = Blueprint('main', __name__, template_folder="pages")

@bp_main.route('/')
def index():
    return redirect("/map")
