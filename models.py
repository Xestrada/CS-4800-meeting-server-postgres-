from app import db

#Model the Meetings Database
class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text)
    meeting_time = db.Column(db.Text)
    attended = db.Column(db.Text)
    topics = db.Column(db.Text)
    todo = db.Column(db.Text)
    completed = db.Column(db.Text)

    def __init__(self, date, meeting_time, attended, topics, todo, completed):
        self.date = date
        self.meeting_time = meeting_time
        self.attended = attended
        self.topics = topics
        self.todo = todo
        self.completed = completed

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'meeting_time': self.meeting_time,
            'attended': eval(self.attended), #eval ensures Response will be returned in JSON properly
            'topics': eval(self.topics),
            'todo': eval(self.todo),
            'completed': eval(self.completed)
        }
