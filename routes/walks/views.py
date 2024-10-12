
from flask import Blueprint, render_template

bp_walks = Blueprint('walks', __name__, template_folder="pages")

@bp_walks.route('/')
def index():
    return "Walks Page"