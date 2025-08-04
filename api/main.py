import configparser
import docker
from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import os
from urllib.parse import unquote

class Episode:
    def __init__(self, intro, outro, filename, start_time,
               end_time, title, description, status, type, logo):
        self.intro = unquote(intro)
        self.outro = unquote(outro)
        self.filename = unquote(filename)
        self.start_time = [start_time]
        self.end_time = [end_time]
        self.clip_timestamps = self.set_clips()
        self.title = unquote(title)
        self.description = unquote(description)
        self.status = status
        self.type = type
        self.logo = logo

    def set_clips(self):
        o = []
        for i in range(0, len(self.start_time)):
            o.append([self.start_time[i], self.end_time[i]])
        return o
    
    def marshal_clips(self):
        o = []
        for i in self.clip_timestamps:
            o.append(",".join(str(e) for e in i))
        return(";".join(o))
    
    def start_workflow(self, client):

        config = configparser.ConfigParser()
        config.read('/app/assets/config.ini')

        client.containers.run(
            config['FEATURES']['ENGINE_CONTAINER'],
            environment={
                'INTRO': self.intro,
                'OUTRO': self.outro, 
                'FILENAME': self.filename,
                'START_TIME': self.start_time,
                'END_TIME': self.end_time,
                'CLIP_TIMESTAMPS': self.marshal_clips(),
                'TITLE': self.title,
                'DESCRIPTION': self.description,
                'STATUS': self.status,
                'TYPE': self.type,
                'LOGO': self.logo,
                'PODCAST_ACCOUNT': request.headers['Authorization']
            },
            volumes={
                config['PROD']['LOCAL_LZ']: {'bind': os.getenv('PODCAST_LZ'), 'mode': 'rw'},
                config['PROD']['LOCAL_ASSETS']: {'bind': os.getenv('PODCAST_ASSETS'), 'mode': 'rw'}
            },
            detach=config['FEATURES']['DETACH_CONTAINER'].lower()=='true',
            remove=config['FEATURES']['REMOVE_CONTAINER'].lower()=='true'
            )
        return 0

app = Flask(__name__)
CORS(app)

client = docker.from_env()

@app.route('/v1/podcasts/episode', methods=['POST'])
def post_episode():
    try:

        if not request.is_json:
            return jsonify({'response': 400, 'message': 'Request must be JSON'}), 400
        data = request.get_json()

        required_fields = ['intro', 'outro', 'filename', 'start_time', 'end_time', 
                          'title', 'description', 'status', 'type', 'logo']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'response': 400, 
                'message': f'Missing required fields: {missing_fields}'
            }), 400

        episode = Episode(
            data['intro'],
            data['outro'],
            data['filename'],
            data['start_time'],
            data['end_time'],
            data['title'],
            data['description'],
            data['status'],
            data['type'],
            data['logo']
        )
        episode.start_workflow(client)
        return jsonify({"response": 201, "message": "Episode details recieved."})
    
    except KeyError as e:
        app.logger.error(f"KeyError: {str(e)}")
        return jsonify({'response': 400, 'message': f'Missing field: {str(e)}'}), 400
    
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        app.logger.exception("Full traceback:")
        return jsonify({'response': 500, 'message': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    # app.run(debug=True, host='0.0.0.0', port=5000)
