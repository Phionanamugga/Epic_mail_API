from api import app
from os import environ


@app.route('/')
def index():
    return ('hello user')

if __name__ == '__main__':
    app.run(debug=True)