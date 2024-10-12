
from flask import Blueprint, render_template

bp_visualizations = Blueprint('visualizations', __name__, template_folder="pages")

@bp_visualizations.route('/')
def index():
    return "Visualizations Page"