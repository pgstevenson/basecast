from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from dotenv import load_dotenv
import os
import uuid


def time_to_sec(hhmmss):
    arr = [int(x) for x in hhmmss.split(":")]
    sec = sum([a * b for a, b in zip(arr, [3600, 60, 1])])
    return sec


load_dotenv()

cluster = Cluster([os.getenv('SERVER')])
session = cluster.connect(os.getenv('KEYSPACE'))
session.row_factory = dict_factory

root = eval(os.getenv('LANDING_ZONE'))

app = Flask(__name__)


@app.route('/v1/clients/<client_id>/tokens', methods=['GET'])
def client_tokens(client_id):
    try:
        res = session.execute("SELECT tokens FROM clients WHERE client_id=%s" % client_id).one()
        return jsonify({"response": 200, "data": res})
    except:
        return jsonify({'response': 400})


@app.route('/v1/drivers', methods=['GET'])
def get_drivers():
    try:
        rows = session.execute("SELECT * FROM driver")
        for row in rows:
            job = dict(row)
            path = root + [job['filename']]
            if os.path.isfile(os.path.join(*path)):
                session.execute("DELETE FROM driver WHERE job_id=%s" % job['job_id'])
                return jsonify({"response": 200, "data": job})
        return jsonify({'response': 204})
    except:
        return jsonify({'response': 400})


@app.route('/v1/podcasts/<podcast_id>', methods=['GET'])
def get_podcast(podcast_id):
    try:
        query = "SELECT * FROM podcasts WHERE podcast_id=%s" % podcast_id
        out = session.execute(query).one()
        return jsonify({"response": 200, "data": dict(out)})
    except:
        return jsonify({'response': 400})


@app.route('/v1/podcasts/<podcast_id>/assets', methods=['GET'])
def get_assets(podcast_id):
    try:
        rows = session.execute("SELECT * FROM assets_by_podcasts WHERE podcast_id=%s" % podcast_id)
        out = []
        for row in rows:
            out.append(dict(row))
        return jsonify({"response": 200, "data": out})
    except:
        return jsonify({'response': 400})


@app.route('/v1/podcasts/<podcast_id>/episodes', methods=['POST'])
def post_job(podcast_id):
    try:
        episode_id = uuid.uuid1()
        query = """INSERT INTO episodes_by_podcasts (podcast_id, episode_id, intro, outro, filename, clips, title,
            description, status, type, logo) VALUES (%s, %s, '%s', '%s', '%s', %s, $$%s$$, $$%s$$, '%s', '%s', '%s');""" % (
                podcast_id,
                episode_id,
                request.args['intro'],
                request.args['outro'],
                request.args['filename'],
                [[time_to_sec(request.args['start_time']), time_to_sec(request.args['end_time'])]],
                request.args['title'],
                request.args['description'],
                request.args['status'],
                request.args['type'],
                request.args['logo']
            )
        session.execute(query)
        return jsonify({"response": 201, "data": {"episode_id": str(episode_id)}})
    except:
        return jsonify({'response': 400})


@app.route('/v1/podcasts/<podcast_id>/episodes/<episode_id>', methods=['POST'])
def post_drivers2(podcast_id, episode_id):
    try:
        query = "INSERT INTO driver (job_id, podcast_id, episode_id, filename) values (%s, %s, %s, '%s')" % (
            uuid.uuid1(), podcast_id, episode_id, request.args['filename'])
        session.execute(query)
        return jsonify({'response': 201})
    except:
        return jsonify({'response': 400})


@app.route('/v1/podcasts/<podcast_id>/episodes/<episode_id>', methods=['GET'])
def get_episode(podcast_id, episode_id):
    try:
        query = "SELECT * FROM episodes_by_podcasts WHERE podcast_id=%s AND episode_id=%s" % (podcast_id, episode_id)
        out = session.execute(query).one()
        return jsonify({"response": 200, "data": dict(out)})
    except:
        return jsonify({'response': 400})


@app.route('/v1/users/<user_email>/podcasts', methods=['GET'])
def get_podcasts(user_email):
    try:
        rows = session.execute("SELECT user_email, podcasts FROM users WHERE user_email='%s'" % user_email)
        out = []
        for row in rows:
            out.append(dict(row))
        return jsonify({"response": 200, "data": out})
    except:
        return jsonify({'response': 400})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
