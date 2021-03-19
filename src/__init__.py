from flask import Flask 

# create new app instance
def create_app():
	app = Flask(__name__)

	from src import auth
	app.register_blueprint(auth.bp)
	# add more blueprints here from channel, message, etc

	return app