
from flask import Blueprint, render_template

bp_overview = Blueprint('overview', __name__, template_folder="pages")

@bp_overview.route('/')
def index():
    return "Overview Page"