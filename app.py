#!/usr/bin/env python

import time
from flask import Flask, jsonify, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/gridlock.db'
db = SQLAlchemy(app)

color_scheme = ''


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Service %r>' % self.name


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Location %r>' % self.name


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    status = db.Column(db.Numeric, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    env = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __init__(self,
                 service_id,
                 status,
                 location_id,
                 env,
                 timestamp,
                 description):
        self.service_id = service_id
        self.status = status
        self.location_id = location_id
        self.env = env
        self.timestamp = timestamp
        self.description = description


@app.route('/gridlock/api/v0.1/', methods=['PUT'])
def put_status():
    service = request.json['service']
    status = request.json['status']
    location = request.json['location']
    env = request.json['env']
    timestamp = request.json['timestamp']
    description = request.json['description']

    s = Service.query.filter_by(name=service).first()
    if s is None:
        del s
        s = Service(service)
        db.session.add(s)

    l = Location.query.filter_by(name=location).first()
    if l is None:
        del l
        l = Location(location)
        db.session.add(l)

    stuff = Status(s.id, status, l.id, env, timestamp, description)
    db.session.add(stuff)
    db.session.commit()

    return "OK", 201


@app.route('/', methods=['GET'])
def homepage():

    service_list = {}
    locs = []

    services = Service.query.all()
    locations = Location.query.all()

    for location in locations:
        locs.append(location.name)

    for service in services:
        service_list[service.name] = {}
        for location in locations:
            service_list[service.name][location.name] = []
            statuses = Status.query.filter_by((service_id=service.id,
                                              location_id=location.id).
                                              order_by(Status.timestamp.
                                              desc()).
                                              limit(1))
        for status in statuses:
            if (time.time() - int(status.timestamp)) >= 600:
                state = 4
            else:
                state = status.status

            stats = {"status": state,
                     "timestamp": status.timestamp,
                     "description": status.description}

            service_list[service.name][location.name].append(stats)

    return render_template('index.html', data=service_list, locs=locs)


@app.route('/detail', methods=['GET'])
def detail():
    service = request.args.get('service')
    location = request.args.get('location')

    sid = Service.query.filter_by(name=service).first()
    lid = Location.query.filter_by(name=location).first()

    if request.args.get('offset'):
        offset = request.args.get('offset')
    else:
        offset = 20

    history = Status.query.filter_by((service_id=sid.id,
                                     location_id=lid.id).
                                     order_by(Status.timestamp.desc()).
                                     limit(offset).all())

    h_array = []

    for h in history:
        new_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(float(h.timestamp)))
        stats = {"status": h.status,
                 "timestamp": new_time,
                 "description": h.description}

        h_array.append(stats)

    return render_template('detail.html',
                           data=h_array,
                           location=location,
                           service=service)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, passthrough_errors=True)
