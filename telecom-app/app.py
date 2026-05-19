from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'Rahul',  'email': 'rahul@telecom.com'},
    {'id': 2, 'name': 'Priya',  'email': 'priya@telecom.com'},
    {'id': 3, 'name': 'Amit',   'email': 'amit@telecom.com'}
]

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'app': 'telecom-app'})

@app.route('/users')
def get_users():
    return jsonify({'users': users, 'count': len(users)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
