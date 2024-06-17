from flask import Blueprint, request, jsonify
from datetime import datetime
from app.extensions import client

webhook = Blueprint('webhook', __name__)

@webhook.route('/webhook/receiver', methods=['POST'])
def webhook_receiver():
    data = request.json
    if data:
        event_type = request.headers.get('X-GitHub-Event')
        events_collection = client.db.events

        if event_type == 'push':
            event = {
                "author": data['pusher']['name'],
                "to_branch": data['ref'].split('/')[-1],
                "timestamp": datetime.utcnow(),
                "type": "push"
            }
        elif event_type == 'pull_request' and data['action'] == 'opened':
            event = {
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow(),
                "type": "pull_request"
            }
        elif event_type == 'pull_request' and data['action'] == 'closed' and data['pull_request']['merged']:
            event = {
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow(),
                "type": "merge"
            }
        else:
            return jsonify({"message": "Event type not supported"}), 400

        events_collection.insert_one(event)
        return jsonify({"message": "Event received!"}), 200

    return jsonify({"status": "no data"}), 400
