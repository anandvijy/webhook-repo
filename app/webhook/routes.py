# from flask import Blueprint, request, jsonify, render_template, json
# from app.extensions import mongo
# from datetime import datetime

# webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# @webhook.route('/receiver', methods=["POST"])
# def receiver():
#     data = request.json
#     event = request.headers.get('X-GitHub-Event', '')
    
#     doc = {
#         'request_id': '',
#         'author': '',
#         'action': '',
#         'from_branch': None,
#         'to_branch': None,
#         'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
#     }
    
#     if event == 'push':
#         doc['request_id'] = data.get('after', '')
#         doc['author'] = data.get('pusher', {}).get('name', '')
#         doc['action'] = 'PUSH'
#         doc['to_branch'] = data.get('ref', '').replace('refs/heads/', '')
        
#     elif event == 'pull_request':
#         pr = data.get('pull_request', {})
#         doc['request_id'] = str(pr.get('number', ''))
#         doc['author'] = data.get('sender', {}).get('login', '')
#         doc['action'] = 'PULL_REQUEST'
#         doc['from_branch'] = pr.get('head', {}).get('ref', '')
#         doc['to_branch'] = pr.get('base', {}).get('ref', '')
        
#         if data.get('action') == 'closed' and pr.get('merged'):
#             doc['action'] = 'MERGE'
    
#     mongo.db.webhooks.insert_one(doc)
#     return {'success': True}, 200


# @webhook.route('/events', methods=["GET"])
# def get_events():
#     events = mongo.db.webhooks.find().sort('_id', -1).limit(20)
    
#     results = []
#     for e in events:
#         author = e.get('author')
#         action = e.get('action')
#         from_branch = e.get('from_branch')
#         to_branch = e.get('to_branch')
#         time = e.get('timestamp', '')
        
#         # Format date with suffix
#         if time:
#             dt = datetime.strptime(time.replace(' UTC', ''), '%Y-%m-%d %H:%M:%S')
#             day = dt.day
            
#             # Add suffix
#             if day in [1, 21, 31]:
#                 suffix = 'st'
#             elif day in [2, 22]:
#                 suffix = 'nd'
#             elif day in [3, 23]:
#                 suffix = 'rd'
#             else:
#                 suffix = 'th'
                
#             time_str = dt.strftime(f'{day}{suffix} %B %Y - %I:%M %p UTC')
#         else:
#             time_str = 'Unknown'
        
#         if action == 'PUSH':
#             msg = f'"{author}" pushed to "{to_branch}" on {time_str}'
#         elif action == 'PULL_REQUEST':
#             msg = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {time_str}'
#         elif action == 'MERGE':
#             msg = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {time_str}'
#         else:
#             continue
            
#         results.append(msg)
    
#     return jsonify({'events': results})


# @webhook.route('/')
# def index():
#     return render_template('index.html')

from flask import Blueprint, json, request

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        return json.dumps(request)
    