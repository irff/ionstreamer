import flask

streaming = flask.Blueprint('streaming', __name__, template_folder='application/templates')

@streaming.route('/', methods=['GET', 'POST'])
def index():
    return flask.render_template('hello.html')

