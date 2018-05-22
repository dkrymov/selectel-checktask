from flask import Flask, request
import psycopg2
import json
from src.doer import Doer

import traceback

app = Flask(__name__)


@app.route("/api/tickets", methods=['POST'])
def tickets():  # add ticket
    required = ["subject", "body", "email"]
    for param in required:
        if param not in request.form:
            return json.dumps({'status': 'error', 'msg': param + ' is required'})
    try:
        m = Doer()
        new_id = m.ticket_add(request.form["subject"], request.form["body"], request.form["email"])
    except Exception as e:
        traceback.print_exc()
        return json.dumps({'status': 'error', 'msg': e.message})
    else:
        return json.dumps({'status': 'ok', 'ticket_id': "%s" % new_id})


@app.route("/api/tickets/<int:ticket_id>", methods=['POST', 'GET'])
def tickets_id(ticket_id):
    if request.method == 'POST':  # change status
        required = ["status"]
        for param in required:
            if param not in request.form:
                return json.dumps({'status': 'error', 'msg': param + ' is required'})
        try:
            m = Doer()
            if m.ticket_state_set(ticket_id, request.form["status"]) is None:
                return json.dumps({'status': 'error', 'msg': 'Such ticket doesn\'t exist'})
        except Exception as e:
            traceback.print_exc()
            return json.dumps({'status': 'error', 'msg': type(e).__name__ + ': ' + e.message})
        else:
            return json.dumps({'status': 'ok'})
    else:  # get ticket
        m = Doer()
        ticket = m.ticket_get(ticket_id)
        if ticket is None:
            return json.dumps({'status': 'error', 'msg': 'Such ticket doesn\'t exist'})
        else:
            return json.dumps({'status': 'ok', 'ticket': ticket}, indent=4)


@app.route('/api/tickets/<int:ticket_id>/comments', methods=['POST'])
def tickets_comments(ticket_id):  # add comment
    required = ["body", "email"]
    for param in required:
        if param not in request.form:
            return json.dumps({'status': 'error', 'msg': param + ' is required'})
    try:
        m = Doer()
        m.ticket_comment_add(ticket_id, request.form["body"], request.form["email"])
    except psycopg2.IntegrityError as e:
        return json.dumps({'status': 'error', 'msg': 'Such ticket doesn\'t exist'})
    except Exception as e:
        return json.dumps({'status': 'error', 'msg': type(e).__name__ + ': ' + e.message})
    else:
        return json.dumps({'status': 'ok'})

# if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=80)
