from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

CORS(app)
db = SQLAlchemy(app)

# Модель Player
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80))
    balance = db.Column(db.Integer, default=100)

    def to_dict(self):
        return {
            'id': self.id,
            'telegram_id': self.telegram_id,
            'username': self.username,
            'balance': self.balance
        }

# Создаем базу данных при первом запуске
with app.app_context():
    db.create_all()

# API для казино
@app.route('/api/casino/player/<telegram_id>', methods=['GET'])
def get_player(telegram_id):
    player = Player.query.filter_by(telegram_id=telegram_id).first()
    if not player:
        player = Player(telegram_id=telegram_id, balance=100)
        db.session.add(player)
        db.session.commit()
    return jsonify(player.to_dict())

@app.route('/api/casino/play/<telegram_id>', methods=['POST'])
def play_game(telegram_id):
    player = Player.query.filter_by(telegram_id=telegram_id).first()
    if not player:
        return jsonify({'error': 'Player not found'}), 404
    if player.balance < 10:
        return jsonify({'error': 'Not enough coins'}), 400

    player.balance -= 10
    rand = random.random()
    if rand < 0.4:
        winnings = 0
    elif rand < 0.7:
        winnings = 20
    elif rand < 0.9:
        winnings = 50
    else:
        winnings = 100

    player.balance += winnings
    db.session.commit()

    return jsonify({
        'new_balance': player.balance,
        'winnings': winnings
    })

# Статический фронтенд
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
