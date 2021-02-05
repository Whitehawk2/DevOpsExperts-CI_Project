"""
This module serves as a web frontend to allow getting requested username
from MySQL via db_connector from a browser (or by json request, too).

made to make testing with selenium easier.

"""
from flask import Flask
import db_connector as db

app = Flask(__name__)


@app.route('/users/get_user_data/<user_id>', methods=['GET'])
def user(user_id):
    """
    queries the database via json request to db_connector for requested
    username by supplied user_id.
    :param user_id: requested user id # to check DB against, in json.
    :return: HTML, test-friendly, response with username or error.
    """
    db_response = db.get_from_db({'id': user_id})
    if db_response == 500:
        return f'<H1 id="error">No such user: {user_id}</H1>'
    else:
        return f'<H1 id="user">' + db_response + '</H1>'


@app.route('/stop_server')
def stop_server():
    """
    Stops the running server by sending a CTRL-C / SIGTERM
    thru signal module
    """
    import os
    import signal
    try:
        # on windows:
        os.kill(os.getpid(), signal.CTRL_C_EVENT)
        print('server stopped - SIGTERM')
        return 'server stopped'

    except AttributeError:
        # on linux:
        os.kill(os.getpid(), signal.SIGTERM)
        print('server stopped')
        return 'server stopped'


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5001)
