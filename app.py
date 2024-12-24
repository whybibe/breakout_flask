from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Score {self.score}>'

with app.app_context():
    db.create_all()

@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.json
    new_score = Score(score=data['score'])
    db.session.add(new_score)
    db.session.commit()
    return jsonify({'message': 'Score added successfully'}), 201

@app.route('/scores', methods=['GET'])
def get_scores():
    scores = Score.query.order_by(Score.score.desc()).all()
    return jsonify([{'score': score.score, 'timestamp': score.timestamp} for score in scores])

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
