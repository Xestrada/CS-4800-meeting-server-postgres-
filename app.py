from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import config
import os

#Setup App
app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig) #Should change based on is in Development or Production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/Meetings'
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
        meeting = Meeting.query().filter_by(id=id).first()
        db.session.delete(meeting)
        db.session.commit()
        return "Meeting Deleted"
    except Exception as e:
        return str(e)

@app.route('/meetings/<id>', methods=['PUT'])
def updateMeeting(id):

    date = request.args.get('date')
    meeting_time = request.args.get('meeting_time')
    attended = request.args.get('attended')
    topics = request.args.get('topics')
    todo = request.args.get('todo')
    completed = request.args.get('completed')

    try:
        # Get and Update Meeting
        meeting = Meeting.query().filter_by(id=id).first()
        meeting.date = date,
        meeting.meeting_time = meeting_time,
        meeting.attended = str(attended),
        meeting.topics = str(topics),
        meeting.todo = str(todo),
        meeting.completed = str(completed)

        db.session.commit()
        return "Meeting Added"
    except Exception as e:
        return str(e)

@app.route('/meetings', methods=['POST'])
def postMeeting():
    date = request.args.get('date')
    meeting_time = request.args.get('meeting_time')
    attended = request.args.get('attended')
    topics = request.args.get('topics')
    todo = request.args.get('todo')
    completed = request.args.get('completed')

    try:
        meeting= Meeting(
            date = date,
            meeting_time = meeting_time,
            attended = str(attended),
            topics = str(topics),
            todo = str(todo),
            completed = str(completed)
        )
        db.session.add(meeting)
        db.session.commit()
        return "Meeting Added"
    except Exception as e:
        return str(e)

@app.route('/meetings', methods=['GET'])
def getMeetings():
    try:
        meetings = Meeting.query.all()
        return jsonify({'meetings': [meeting.serialize() for meeting in meetings]})
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(port=port)