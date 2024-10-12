
from flask import Flask

def load_blueprints(app):
    from routes.main.views import bp_main
    from routes.overview.views import bp_overview
    from routes.map.views import bp_map
    from routes.walks.views import bp_walks
    from routes.visualizations.views import bp_visualizations
    from routes.api.views import bp_api

    app.register_blueprint(bp_main, url_prefix="/")
    app.register_blueprint(bp_overview, url_prefix="/overview")
    app.register_blueprint(bp_map, url_prefix="/map")
    app.register_blueprint(bp_walks, url_prefix="/walks")
    app.register_blueprint(bp_visualizations, url_prefix="/visualizations")
    app.register_blueprint(bp_api, url_prefix="/api")



app = Flask(__name__)

load_blueprints(app)
