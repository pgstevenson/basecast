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

app = Flask(__name__)


@app.route('/v1/drivers', methods=['GET'])
def get_drivers():
    try:
        rows = session.execute("SELECT * FROM driver")
        out = []
        for row in rows:
            out.append(dict(row))
        return jsonify(out)
    except:
        return jsonify(400)


@app.route('/v1/drivers', methods=['POST'])
def post_drivers():
    try:
        query = "INSERT INTO driver (job_id, operation, trigger) values (%s, %s, %s)" % (
            uuid.uuid1(), request.args['operation'].split(','), request.args['trigger'].split(','))
        session.execute(query)
        return jsonify(200)
    except:
        return jsonify(400)


@app.route('/v1/drivers/<job_id>', methods=['DELETE'])
def delete_drivers(job_id):
    query = "DELETE FROM driver WHERE job_id=%s" % job_id
    try:
        session.execute(query)
        return jsonify(200)
    except:
        return jsonify(400)


@app.route('/v1/episodes/<episode_id>', methods=['GET'])
def get_episode(episode_id):
    try:
        query = "SELECT * FROM episodes WHERE episode_id=%s" % episode_id
        out = session.execute(query).one()
        return jsonify(dict(out))
    except:
        return jsonify(400)


@app.route('/v1/episodes', methods=['POST'])
def post_job():
    try:
        episode_id = uuid.uuid1()
        trigger = ['bronze', request.args['podcast_id'], request.args['filename']]
        query = """INSERT INTO episodes (podcast_id, episode_id, intro, outro, bronze, clips, title, description, status,
            type, logo) VALUES (%s, %s, %s, %s, %s, %s, $$%s$$, $$%s$$, '%s', '%s', '%s');""" % (
            request.args['podcast_id'],
            episode_id,
            request.args['intro'].split(','),
            request.args['outro'].split(','),
            trigger,
            [[time_to_sec(request.args['start_time']), time_to_sec(request.args['end_time'])]],
            request.args['title'],
            request.args['description'],
            request.args['status'],
            request.args['type'],
            request.args['logo']
        )
        session.execute(query)
        res = {"episode_id": str(episode_id)}
        return jsonify(res)
    except:
        return(400)


@app.route('/v1/episodes/<episode_id>', methods=['PATCH'])
def update_episode(episode_id):
    try:
        query = "UPDATE episodes SET %s=%s WHERE episode_id=%s" % (
            request.args['param'], request.args['value'].split(','), episode_id)
        session.execute(query)
        return jsonify(200)
    except:
        return jsonify(400)


@app.route('/v1/podcasts/<podcast_id>', methods=['GET'])
def get_podcast(podcast_id):
    try:
        query = "SELECT * FROM podcasts WHERE podcast_id=%s" % podcast_id
        out = session.execute(query).one()
        return jsonify(out)
    except:
        return jsonify(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
