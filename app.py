from flask import Flask
# from database import db_session
import settings

"""import all controller from application.controllers"""
from controllers.streaming import streaming
"""import more controller"""

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

"""register each controller as blueprint"""
app.register_blueprint(streaming)
"""register more controller"""

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.debug = True
    app.run(port=settings.PORT, host=settings.HOST)