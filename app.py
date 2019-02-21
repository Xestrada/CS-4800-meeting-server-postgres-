from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

#Setup App
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS']) #Should change based on is in Development or Production
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

#Start Database
db = SQLAlchemy(app)

# Enable Variable port for Heroku
port = int(os.environ.get('PORT', 33507))

#Importing after as models required db from app
from models import Meeting

@app.route('/')
def hello():
    return "Hello There"

@app.route('/meetings/<id>', methods=['DELETE'])
def deleteMeeting(id):
    try:
        #Get meeting then delete
        Meeting.query.filter_by(id=id).delete()
        db.session.commit()
        return "Meeting Deleted"
    except Exception as e:
        return str(e)

@app.route('/meetings/<id>', methods=['PUT'])
def updateMeeting(id):

    data = request.get_json();
    newId = data['id']
    date = str(data['date'])
    meeting_time = str(data['meeting_time'])
    attended = str(data['attended'])
    topics = str(data['topics'])
    todo = str(data['todo'])
    completed = str(data['completed'])

    try:
        # Get and Update Meeting
        meeting = Meeting.query.filter_by(id=id).first()
        if newId is not None:
           meeting.id = newId
        meeting.date = date,
        meeting.meeting_time = meeting_time,
        meeting.attended = attended,
        meeting.topics = topics,
        meeting.todo = todo,
        meeting.completed = completed

        db.session.commit()
        return "Meeting Updated"
    except Exception as e:
        return str(e)

@app.route('/meetings', methods=['POST'])
def postMeeting():
    data = request.get_json()
    date = str(data['date'])
    meeting_time = str(data['meeting_time'])
    attended = str(data['attended'])
    topics = str(data['topics'])
    todo = str(data['todo'])
    completed = str(data['completed'])

    try:
        meeting= Meeting(
            date = date,
            meeting_time = meeting_time,
            attended = attended,
            topics = topics,
            todo = todo,
            completed = completed
        )
        db.session.add(meeting)
        db.session.commit()
        return "Meeting Added"
    except Exception as e:
        return str(e)

@app.route('/meetings', methods=['GET'])
def getMeetings():
    try:
        meetings = Meeting.query.order_by(Meeting.date).all()
        return jsonify({'meetings': [meeting.serialize() for meeting in meetings]})
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(port=port)