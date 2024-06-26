# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    quake = db.session.get(Earthquake, id)
    if quake:
        return jsonify({
            'id': quake.id,
            'magnitude': quake.magnitude,
            'location': quake.location,
            'year': quake.year
        }), 200
    else:
        return jsonify({'message': f'Earthquake {id} not found.'}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    response = {
        'count': len(quakes),
        'quakes': [
            {
                'id': quake.id,
                'magnitude': quake.magnitude,
                'location': quake.location,
                'year': quake.year
            } for quake in quakes
        ]
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
