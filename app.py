# app.py — MOBILE LEGENDS BANG BANG — ПОЛНАЯ ВЕРСИЯ С МУЛЬТИПЛЕЕРОМ
from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import os
import time
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
socketio = SocketIO(app, cors_allowed_origins="*")

# --- ПОЛНАЯ БАЗА ГЕРОЕВ ---
HEROES = {
    "alusard": {
        "name": "Алукард", "hp": 180, "dmg": 35, "speed": 4, "color": "#ff4444",
        "role": "Fighter", "skill_name": "Кровавый разрез", "skill_dmg": 2.5,
        "skill_cooldown": 3, "skill_desc": "Мощный удар с вампиризмом", "attack_range": 60
    },
    "miya": {
        "name": "Мия", "hp": 120, "dmg": 50, "speed": 3.5, "color": "#44ff44",
        "role": "Marksman", "skill_name": "Град стрел", "skill_dmg": 3.0,
        "skill_cooldown": 4, "skill_desc": "Залп из 3 стрел", "attack_range": 120
    },
    "tigreal": {
        "name": "Тигрил", "hp": 250, "dmg": 25, "speed": 2.5, "color": "#4444ff",
        "role": "Tank", "skill_name": "Священный щит", "skill_dmg": 1.5,
        "skill_cooldown": 5, "skill_desc": "Оглушение и защита", "attack_range": 50
    },
    "eudora": {
        "name": "Эвдора", "hp": 100, "dmg": 65, "speed": 3, "color": "#ff44ff",
        "role": "Mage", "skill_name": "Цепная молния", "skill_dmg": 3.5,
        "skill_cooldown": 3.5, "skill_desc": "Молния по области", "attack_range": 100
    },
    "fanny": {
        "name": "Фанни", "hp": 130, "dmg": 45, "speed": 6, "color": "#00ffff",
        "role": "Assassin", "skill_name": "Стальной трос", "skill_dmg": 2.8,
        "skill_cooldown": 2, "skill_desc": "Мгновенное перемещение", "attack_range": 70
    },
    "rafaela": {
        "name": "Рафаэль", "hp": 110, "dmg": 30, "speed": 3.5, "color": "#ff88ff",
        "role": "Support", "skill_name": "Исцеляющий свет", "skill_dmg": 1.2,
        "skill_cooldown": 6, "skill_desc": "Лечение союзников", "attack_range": 90,
        "heal_power": 50
    }
}

# --- ПРЕДМЕТЫ МАГАЗИНА ---
ITEMS = {
    "blade": {"name": "Меч Отчаяния", "cost": 500, "dmg": 25, "hp": 0, "crit": 10},
    "armor": {"name": "Кираса", "cost": 400, "dmg": 0, "hp": 80, "armor": 20},
    "boots": {"name": "Сапоги скорости", "cost": 250, "dmg": 5, "hp": 20, "speed": 1},
    "blood": {"name": "Кровожадность", "cost": 600, "dmg": 30, "hp": 50, "lifesteal": 15},
    "staff": {"name": "Посох мага", "cost": 550, "dmg": 40, "hp": 0, "mana": 100},
    "shield": {"name": "Щит света", "cost": 450, "dmg": 0, "hp": 100, "regen": 5}
}

# --- МОНСТРЫ ДЖУНГЛЕЙ ---
JUNGLE_MOBS = {
    "crab": {"name": "Краб", "hp": 80, "dmg": 15, "gold": 60, "exp": 30, "color": "#ffaa44"},
    "wolf": {"name": "Волк", "hp": 120, "dmg": 25, "gold": 100, "exp": 50, "color": "#8844ff"},
    "golem": {"name": "Голем", "hp": 200, "dmg": 40, "gold": 180, "exp": 80, "color": "#aa88ff"},
    "lord": {"name": "ЛОРД", "hp": 500, "dmg": 80, "gold": 500, "exp": 200, "color": "#ff0000"}
}

# --- ХРАНЕНИЕ ИГРОВЫХ КОМНАТ ---
game_rooms = {}  # {room_id: {"players": {}, "mobs": [], "towers": [], "state": "waiting"}}

# --- HTML С ПОЛНЫМ ИНТЕРФЕЙСОМ ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MLBB — ПОЛНАЯ ВЕРСИЯ</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: linear-gradient(135deg, #0a0a1a, #1a0a2a);
            font-family: 'Arial', sans-serif;
            color: white;
            overflow: hidden;
        }
        #gameWrapper {
            display: flex;
            height: 100vh;
        }
        #gameArea {
            flex: 1;
            padding: 20px;
        }
        #sidePanel {
            width: 350px;
            background: rgba(0,0,0,0.8);
            padding: 20px;
            border-left: 3px solid gold;
            overflow-y: auto;
        }
        canvas { 
            border: 3px solid gold;
            border-radius: 15px;
            background: radial-gradient(circle, #1a2a4a, #0a0f1e);
            width: 100%;
            height: auto;
        }
        .hero-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            cursor: pointer;
            border: 2px solid transparent;
            transition: 0.3s;
        }
        .hero-card:hover {
            border-color: gold;
            transform: scale(1.02);
        }
        button {
            background: linear-gradient(45deg, #2a3a5c, #3a4a6c);
            color: white;
            border: none;
            padding: 12px 24px;
            margin: 5px;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            border: 1px solid #6a8cff;
            transition: 0.2s;
        }
        button:hover { 
            transform: scale(1.05);
            box-shadow: 0 0 15px #6a8cff;
        }
        .skill-btn { 
            background: linear-gradient(45deg, #8a4a2a, #aa5a3a);
            border-color: #ffaa00;
        }
        .shop-item {
            background: rgba(255,215,0,0.1);
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            border: 1px solid gold;
        }
        .player-list {
            margin: 20px 0;
        }
        .player-tag {
            display: inline-block;
            padding: 5px 10px;
            margin: 3px;
            background: rgba(100,100,255,0.3);
            border-radius: 15px;
        }
        #chat {
            height: 200px;
            overflow-y: auto;
            background: black;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .chat-input {
            display: flex;
        }
        .chat-input input {
            flex: 1;
            padding: 10px;
            background: #1a1a2e;
            color: white;
            border: 1px solid gold;
            border-radius: 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 15px 0;
        }
        .stat-box {
            background: rgba(0,0,0,0.5);
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
        .hp-bar {
            width: 100%;
            height: 15px;
            background: #3a1a1a;
            border-radius: 8px;
            margin: 5px 0;
        }
        .hp-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff4444, #ff6666);
            border-radius: 8px;
            transition: width 0.3s;
        }
        #minimap {
            width: 100%;
            height: 200px;
            margin: 15px 0;
        }
        .game-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .gold-display {
            color: #FFD700;
            font-size: 24px;
            font-weight: bold;
        }
        .level-badge {
            background: gold;
            color: black;
            padding: 5px 10px;
            border-radius: 20px;
            font-weight: bold;
        }
        @keyframes damage {
            0% { color: red; transform: scale(1); }
            50% { color: yellow; transform: scale(1.5); }
            100% { color: white; transform: scale(1); }
        }
        .damage-number {
            position: absolute;
            animation: damage 1s;
            pointer-events: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div id="gameWrapper">
        <div id="gameArea">
            {% if not session.get('hero_chosen') %}
                <!-- ЭКРАН ВЫБОРА ГЕРОЯ И КОМНАТЫ -->
                <div style="max-width: 1200px; margin: 0 auto;">
                    <h1 style="color: gold; text-align: center; font-size: 48px; margin: 30px 0;">
                        🔥 MOBILE LEGENDS BANG BANG 🔥
                    </h1>
                    
                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 30px;">
                        <div>
                            <h2>Выберите героя</h2>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                                {% for key, hero in heroes.items() %}
                                <div class="hero-card" onclick="selectHero('{{ key }}')" id="hero-{{ key }}">
                                    <h3 style="color: {{ hero.color }};">{{ hero.name }}</h3>
                                    <p>{{ hero.role }}</p>
                                    <p>❤️ {{ hero.hp }} | ⚔️ {{ hero.dmg }}</p>
                                    <p>✨ {{ hero.skill_name }}</p>
                                    <small>{{ hero.skill_desc }}</small>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div>
                            <h2>Игровые комнаты</h2>
                            <button onclick="createRoom()" style="width: 100%; margin-bottom: 20px;">
                                🎮 СОЗДАТЬ КОМНАТУ
                            </button>
                            <div id="roomList">
                                <p>Загрузка комнат...</p>
                            </div>
                            <div style="margin-top: 20px;">
                                <input type="text" id="roomIdInput" placeholder="ID комнаты" 
                                       style="width: 100%; padding: 10px; background: #1a1a2e; color: white; border: 1px solid gold; border-radius: 5px;">
                                <button onclick="joinRoom()" style="width: 100%; margin-top: 10px;">
                                    🔑 ПРИСОЕДИНИТЬСЯ
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            {% else %}
                <!-- ОСНОВНОЙ ИГРОВОЙ ЭКРАН -->
                <div class="game-header">
                    <div>
                        <h2 id="roomIdDisplay">Комната: {{ session['room'] }}</h2>
                        <p>Игроков: <span id="playerCount">1</span>/6</p>
                    </div>
                    <div class="gold-display">
                        💰 <span id="goldAmount">{{ session['gold'] }}</span>
                    </div>
                    <div class="level-badge">
                        ⭐ Уровень <span id="playerLevel">{{ session['level'] }}</span>
                    </div>
                </div>
                
                <canvas id="gameCanvas" width="1000" height="600"></canvas>
                
                <div style="display: flex; gap: 10px; margin-top: 15px; justify-content: center; flex-wrap: wrap;">
                    <button onclick="move('up')">⬆️</button>
                    <button onclick="move('down')">⬇️</button>
                    <button onclick="move('left')">⬅️</button>
                    <button onclick="move('right')">➡️</button>
                    <button onclick="attack()" style="background: #6b2a2a;">⚔️ АТАКА</button>
                    <button onclick="useSkill()" class="skill-btn" id="skillBtn">✨ {{ session['skill_name'] }}</button>
                    <button onclick="openShop()">🏪 МАГАЗИН</button>
                    <button onclick="recall()">🔵 РЕКОЛЛ</button>
                </div>
            {% endif %}
        </div>
        
        {% if session.get('hero_chosen') %}
        <div id="sidePanel">
            <div class="stats-grid">
                <div class="stat-box">
                    <h3>{{ session['hero_name'] }}</h3>
                    <p>{{ session['role'] }}</p>
                </div>
                <div class="stat-box">
                    <p>🗡️ Убийств: <span id="killsCount">0</span></p>
                    <p>💀 Смертей: <span id="deathsCount">0</span></p>
                </div>
            </div>
            
            <div class="hp-bar">
                <div class="hp-fill" id="playerHpBar" style="width: 100%;"></div>
            </div>
            <p>❤️ <span id="playerHp">{{ session['hp'] }}</span>/{{ session['max_hp'] }}</p>
            
            <div id="minimap">
                <canvas id="miniCanvas" width="300" height="200" style="width: 100%; height: 100%;"></canvas>
            </div>
            
            <div class="player-list">
                <h4>👥 ИГРОКИ</h4>
                <div id="playersList"></div>
            </div>
            
            <div id="chat">
                <div><span style="color: gold;">Система:</span> Добро пожаловать в MLBB!</div>
            </div>
            <div class="chat-input">
                <input type="text" id="chatInput" placeholder="Сообщение...">
                <button onclick="sendChat()">📤</button>
            </div>
            
            <div id="shop" style="display: none; margin-top: 20px;">
                <h3>🏪 МАГАЗИН</h3>
                {% for key, item in items.items() %}
                <div class="shop-item">
                    <b>{{ item.name }}</b><br>
                    <span style="color: gold;">{{ item.cost }}💰</span><br>
                    <small>⚔️+{{ item.dmg }} ❤️+{{ item.hp }}</small>
                    <button onclick="buyItem('{{ key }}')" style="padding: 5px; width: 100%;">КУПИТЬ</button>
                </div>
                {% endfor %}
                <button onclick="closeShop()">ЗАКРЫТЬ</button>
            </div>
            
            <button onclick="location.href='/leave_game'" style="width: 100%; margin-top: 20px; background: #6b2a2a;">
                🚪 ПОКИНУТЬ ИГРУ
            </button>
        </div>
        {% endif %}
    </div>

    <script>
        const socket = io();
        let selectedHero = null;
        let gameState = {
            players: {},
            mobs: [],
            towers: [],
            projectiles: [],
            effects: []
        };
        let myId = null;
        
        // Выбор героя
        function selectHero(heroKey) {
            selectedHero = heroKey;
            document.querySelectorAll('.hero-card').forEach(card => {
                card.style.border = '2px solid transparent';
            });
            document.getElementById(`hero-${heroKey}`).style.border = '3px solid gold';
        }
        
        // Создание комнаты
        function createRoom() {
            if (!selectedHero) {
                alert('Выберите героя!');
                return;
            }
            socket.emit('create_room', {hero: selectedHero});
        }
        
        // Присоединение к комнате
        function joinRoom() {
            if (!selectedHero) {
                alert('Выберите героя!');
                return;
            }
            const roomId = document.getElementById('roomIdInput').value;
            if (roomId) {
                socket.emit('join_room', {room: roomId, hero: selectedHero});
            }
        }
        
        // Управление движением
        function move(direction) {
            socket.emit('move', {direction: direction});
        }
        
        // Атака
        function attack() {
            socket.emit('attack');
        }
        
        // Использование скилла
        function useSkill() {
            socket.emit('skill');
        }
        
        // Магазин
        function openShop() {
            document.getElementById('shop').style.display = 'block';
        }
        
        function closeShop() {
            document.getElementById('shop').style.display = 'none';
        }
        
        function buyItem(itemKey) {
            socket.emit('buy_item', {item: itemKey});
        }
        
        // Реколл
        function recall() {
            socket.emit('recall');
        }
        
        // Чат
        function sendChat() {
            const input = document.getElementById('chatInput');
            if (input.value) {
                socket.emit('chat', {message: input.value});
                input.value = '';
            }
        }
        
        // Socket события
        socket.on('connect', () => {
            myId = socket.id;
            console.log('Connected:', myId);
        });
        
        socket.on('room_created', (data) => {
            window.location.href = '/game/' + data.room;
        });
        
        socket.on('game_state', (state) => {
            gameState = state;
            drawGame();
            updateUI();
        });
        
        socket.on('chat_message', (data) => {
            const chat = document.getElementById('chat');
            chat.innerHTML += `<div><span style="color: ${data.color};">${data.name}:</span> ${data.message}</div>`;
            chat.scrollTop = chat.scrollHeight;
        });
        
        socket.on('room_list', (rooms) => {
            const roomList = document.getElementById('roomList');
            roomList.innerHTML = '';
            for (let roomId in rooms) {
                roomList.innerHTML += `
                    <div style="background: rgba(255,255,255,0.1); padding: 10px; margin: 5px 0; border-radius: 5px;">
                        <span>Комната ${roomId}</span>
                        <span>(${rooms[roomId].players}/6 игроков)</span>
                        <button onclick="joinRoomById('${roomId}')">Войти</button>
                    </div>
                `;
            }
        });
        
        function joinRoomById(roomId) {
            document.getElementById('roomIdInput').value = roomId;
            joinRoom();
        }
        
        // Отрисовка игры
        function drawGame() {
            const canvas = document.getElementById('gameCanvas');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, 1000, 600);
            
            // Отрисовка линий
            ctx.strokeStyle = "#ffffff30";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 200); ctx.lineTo(1000, 200);
            ctx.moveTo(0, 400); ctx.lineTo(1000, 400);
            ctx.stroke();
            
            // Башни
            gameState.towers.forEach(tower => {
                ctx.fillStyle = tower.team === 'blue' ? '#4488ff' : '#ff4444';
                ctx.shadowColor = tower.team === 'blue' ? '#4488ff' : '#ff4444';
                ctx.shadowBlur = 20;
                ctx.beginPath();
                ctx.arc(tower.x, tower.y, 40, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
                
                // HP башни
                ctx.fillStyle = '#ff0000';
                ctx.fillRect(tower.x - 30, tower.y - 50, 60, 8);
                ctx.fillStyle = '#00ff00';
                ctx.fillRect(tower.x - 30, tower.y - 50, 60 * (tower.hp / tower.maxHp), 8);
            });
            
            // Мобы
            gameState.mobs.forEach(mob => {
                ctx.fillStyle = mob.color;
                ctx.shadowColor = mob.color;
                ctx.shadowBlur = 15;
                ctx.beginPath();
                ctx.arc(mob.x, mob.y, 25, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
                
                // HP моба
                ctx.fillStyle = '#ff0000';
                ctx.fillRect(mob.x - 25, mob.y - 35, 50, 6);
                ctx.fillStyle = '#00ff00';
                ctx.fillRect(mob.x - 25, mob.y - 35, 50 * (mob.hp / mob.maxHp), 6);
                
                ctx.fillStyle = 'white';
                ctx.font = '12px Arial';
                ctx.fillText(mob.type, mob.x - 20, mob.y - 40);
            });
            
            // Игроки
            for (let id in gameState.players) {
                const player = gameState.players[id];
                ctx.fillStyle = player.color;
                ctx.shadowColor = player.color;
                ctx.shadowBlur = 25;
                ctx.beginPath();
                ctx.arc(player.x, player.y, 28, 0, Math.PI * 2);
                ctx.fill();
                ctx.shadowBlur = 0;
                ctx.strokeStyle = id === myId ? 'gold' : 'white';
                ctx.lineWidth = id === myId ? 5 : 3;
                ctx.stroke();
                
                // Имя и HP
                ctx.fillStyle = 'white';
                ctx.font = 'bold 14px Arial';
                ctx.fillText(player.name, player.x - 35, player.y - 45);
                
                ctx.fillStyle = '#ff0000';
                ctx.fillRect(player.x - 35, player.y - 35, 70, 8);
                ctx.fillStyle = '#00ff00';
                ctx.fillRect(player.x - 35, player.y - 35, 70 * (player.hp / player.maxHp), 8);
                
                // Уровень
                ctx.fillStyle = 'gold';
                ctx.font = 'bold 12px Arial';
                ctx.fillText('Lv.' + player.level, player.x - 20, player.y - 50);
            }
            
            // Снаряды
            gameState.projectiles.forEach(p => {
                ctx.fillStyle = p.color;
                ctx.beginPath();
                ctx.arc(p.x, p.y, 8, 0, Math.PI * 2);
                ctx.fill();
            });
            
            // Мини-карта
            const miniCanvas = document.getElementById('miniCanvas');
            if (miniCanvas) {
                const miniCtx = miniCanvas.getContext('2d');
                miniCtx.clearRect(0, 0, 300, 200);
                miniCtx.fillStyle = '#0a0f1e';
                miniCtx.fillRect(0, 0, 300, 200);
                
                for (let id in gameState.players) {
                    const p = gameState.players[id];
                    miniCtx.fillStyle = p.color;
                    miniCtx.beginPath();
                    miniCtx.arc(p.x / 1000 * 300, p.y / 600 * 200, 5, 0, Math.PI * 2);
                    miniCtx.fill();
                }
            }
        }
        
        function updateUI() {
            const myPlayer = gameState.players[myId];
            if (myPlayer) {
                document.getElementById('playerHp').textContent = Math.floor(myPlayer.hp);
                document.getElementById('playerHpBar').style.width = (myPlayer.hp / myPlayer.maxHp * 100) + '%';
                document.getElementById('goldAmount').textContent = myPlayer.gold;
                document.getElementById('playerLevel').textContent = myPlayer.level;
                document.getElementById('killsCount').textContent = myPlayer.kills;
                document.getElementById('deathsCount').textContent = myPlayer.deaths;
                
                // Список игроков
                const playersList = document.getElementById('playersList');
                playersList.innerHTML = '';
                for (let id in gameState.players) {
                    const p = gameState.players[id];
                    playersList.innerHTML += `
                        <div class="player-tag" style="border-left: 3px solid ${p.color};">
                            ${p.name} Lv.${p.level}
                        </div>
                    `;
                }
            }
        }
        
        // Игровой цикл
        setInterval(() => {
            if (gameState.players[myId]) {
                drawGame();
                updateUI();
            }
        }, 1000/30);
        
        // Запрос списка комнат
        setInterval(() => {
            socket.emit('get_rooms');
        }, 2000);
    </script>
</body>
</html>
'''

# --- FLASK МАРШРУТЫ ---
@app.route('/')
def index():
    if 'hero_chosen' not in session:
        session['hero_chosen'] = False
    return render_template_string(HTML_TEMPLATE, heroes=HEROES, items=ITEMS)

@app.route('/pick_hero/<hero_key>')
def pick_hero(hero_key):
    hero = HEROES[hero_key]
    session['hero'] = hero_key
    session['hero_name'] = hero['name']
    session['role'] = hero['role']
    session['color'] = hero['color']
    session['skill_name'] = hero['skill_name']
    session['skill_dmg'] = hero['skill_dmg']
    session['hero_chosen'] = True
    session['hp'] = hero['hp']
    session['max_hp'] = hero['hp']
    session['dmg'] = hero['dmg']
    session['gold'] = 500
    session['level'] = 1
    session['exp'] = 0
    session['kills'] = 0
    session['deaths'] = 0
    return redirect(url_for('index'))

@app.route('/game/<room_id>')
def game_room(room_id):
    if not session.get('hero_chosen'):
        return redirect(url_for('index'))
    session['room'] = room_id
    return render_template_string(HTML_TEMPLATE, heroes=HEROES, items=ITEMS)

@app.route('/leave_game')
def leave_game():
    session.clear()
    return redirect(url_for('index'))

# --- WEBSOCKET СОБЫТИЯ ---
@socketio.on('create_room')
def create_room(data):
    room_id = str(random.randint(1000, 9999))
    hero_key = data['hero']
    hero = HEROES[hero_key]
    
    game_rooms[room_id] = {
        'players': {},
        'mobs': [],
        'towers': [
            {'x': 200, 'y': 200, 'hp': 500, 'maxHp': 500, 'team': 'blue'},
            {'x': 800, 'y': 400, 'hp': 500, 'maxHp': 500, 'team': 'red'}
        ],
        'state': 'waiting'
    }
    
    # Спавн мобов
    for mob_type, mob_data in JUNGLE_MOBS.items():
        for _ in range(2):
            game_rooms[room_id]['mobs'].append({
                'x': random.randint(300, 700),
                'y': random.randint(100, 500),
                'hp': mob_data['hp'],
                'maxHp': mob_data['hp'],
                'dmg': mob_data['dmg'],
                'type': mob_data['name'],
                'color': mob_data['color'],
                'gold': mob_data['gold'],
                'exp': mob_data['exp']
            })
    
    join_room(room_id)
    game_rooms[room_id]['players'][request.sid] = {
        'id': request.sid,
        'name': hero['name'],
        'hero': hero_key,
        'x': 400,
        'y': 300,
        'hp': hero['hp'],
        'maxHp': hero['hp'],
        'dmg': hero['dmg'],
        'color': hero['color'],
        'level': 1,
        'exp': 0,
        'gold': 500,
        'kills': 0,
        'deaths': 0,
        'skill_ready': True,
        'last_skill': 0,
        'inventory': []
    }
    
    emit('room_created', {'room': room_id})
    emit('game_state', game_rooms[room_id], room=room_id)

@socketio.on('join_room')
def handle_join_room(data):
    room_id = data['room']
    hero_key = data['hero']
    hero = HEROES[hero_key]
    
    if room_id in game_rooms:
        join_room(room_id)
        game_rooms[room_id]['players'][request.sid] = {
            'id': request.sid,
            'name': hero['name'],
            'hero': hero_key,
            'x': random.randint(300, 700),
            'y': random.randint(200, 400),
            'hp': hero['hp'],
            'maxHp': hero['hp'],
            'dmg': hero['dmg'],
            'color': hero['color'],
            'level': 1,
            'exp': 0,
            'gold': 500,
            'kills': 0,
            'deaths': 0,
            'skill_ready': True,
            'last_skill': 0,
            'inventory': []
        }
        emit('game_state', game_rooms[room_id], room=room_id)
        
        # Уведомление для всех
        emit('chat_message', {
            'name': 'Система',
            'message': f"{hero['name']} присоединился к игре!",
            'color': 'gold'
        }, room=room_id)

@socketio.on('move')
def handle_move(data):
    room_id = get_room_for_player(request.sid)
    if not room_id or request.sid not in game_rooms[room_id]['players']:
        return
    
    player = game_rooms[room_id]['players'][request.sid]
    speed = 5
    
    if data['direction'] == 'up':
        player['y'] = max(50, player['y'] - speed)
    elif data['direction'] == 'down':
        player['y'] = min(550, player['y'] + speed)
    elif data['direction'] == 'left':
        player['x'] = max(50, player['x'] - speed)
    elif data['direction'] == 'right':
        player['x'] = min(950, player['x'] + speed)
    
    emit('game_state', game_rooms[room_id], room=room_id)

@socketio.on('attack')
def handle_attack():
    room_id = get_room_for_player(request.sid)
    if not room_id or request.sid not in game_rooms[room_id]['players']:
        return
    
    player = game_rooms[room_id]['players'][request.sid]
    
    # Атака мобов
    for mob in game_rooms[room_id]['mobs']:
        dist = ((player['x'] - mob['x'])**2 + (player['y'] - mob['y'])**2)**0.5
        if dist < 80:
            mob['hp'] -= player['dmg']
            if mob['hp'] <= 0:
                player['gold'] += mob['gold']
                player['exp'] += mob['exp']
                game_rooms[room_id]['mobs'].remove(mob)
                check_level_up(player)
                # Респавн моба через 10 секунд
                socketio.sleep(10)
                spawn_mob(room_id)
            break
    
    emit('game_state', game_rooms[room_id], room=room_id)

@socketio.on('skill')
def handle_skill():
    room_id = get_room_for_player(request.sid)
    if not room_id or request.sid not in game_rooms[room_id]['players']:
        return
    
    player = game_rooms[room_id]['players'][request.sid]
    hero_data = HEROES[player['hero']]
    
    now = time.time()
    if not player['skill_ready'] or (now - player['last_skill']) < hero_data['skill_cooldown']:
        return
    
    player['skill_ready'] = False
    player['last_skill'] = now
    
    # Урон скилла
    skill_dmg = int(player['dmg'] * hero_data['skill_dmg'])
    
    for mob in game_rooms[room_id]['mobs']:
        dist = ((player['x'] - mob['x'])**2 + (player['y'] - mob['y'])**2)**0.5
        if dist < 120:
            mob['hp'] -= skill_dmg
            if mob['hp'] <= 0:
                player['gold'] += mob['gold']
                player['exp'] += mob['exp']
                game_rooms[room_id]['mobs'].remove(mob)
                check_level_up(player)
    
    # Кулдаун
    def reset_skill():
        player['skill_ready'] = True
    
    socketio.start_background_task(lambda: (time.sleep(hero_data['skill_cooldown']), reset_skill()))
    
    emit('game_state', game_rooms[room_id], room=room_id)
    emit('chat_message', {
        'name': player['name'],
        'message': f"Использовал {hero_data['skill_name']}!",
        'color': player['color']
    }, room=room_id)

@socketio.on('buy_item')
def handle_buy_item(data):
    room_id = get_room_for_player(request.sid)
    if not room_id or request.sid not in game_rooms[room_id]['players']:
        return
    
    player = game_rooms[room_id]['players'][request.sid]
    item_key = data['item']
    item = ITEMS.get(item_key)
    
    if item and player['gold'] >= item['cost']:
        player['gold'] -= item['cost']
        player['dmg'] += item['dmg']
        player['maxHp'] += item['hp']
        player['hp'] += item['hp']
        player['inventory'].append(item['name'])
        
        emit('game_state', game_rooms[room_id], room=room_id)

@socketio.on('recall')
def handle_recall():
    room_id = get_room_for_player(request.sid)
    if not room_id or request.sid not in game_rooms[room_id]['players']:
        return
    
    player = game_rooms[room_id]['players'][request.sid]
    player['x'] = 400
    player['y'] = 300
    player['hp'] = player['maxHp']
    
    emit('game_state', game_rooms[room_id], room=room_id)

@socketio.on('chat')
def handle_chat(data):
    room_id = get_room_for_player(request.sid)
    if not room_id or request.sid not in game_rooms[room_id]['players']:
        return
    
    player = game_rooms[room_id]['players'][request.sid]
    emit('chat_message', {
        'name': player['name'],
        'message': data['message'],
        'color': player['color']
    }, room=room_id)

@socketio.on('get_rooms')
def handle_get_rooms():
    rooms_info = {}
    for room_id, room_data in game_rooms.items():
        rooms_info[room_id] = {
            'players': len(room_data['players'])
        }
    emit('room_list', rooms_info)

def get_room_for_player(sid):
    for room_id, room_data in game_rooms.items():
        if sid in room_data['players']:
            return room_id
    return None

def check_level_up(player):
    exp_needed = player['level'] * 100
    if player['exp'] >= exp_needed:
        player['level'] += 1
        player['exp'] -= exp_needed
        player['maxHp'] += 30
        player['hp'] = player['maxHp']
        player['dmg'] += 10

def spawn_mob(room_id):
    if room_id in game_rooms:
        mob_types = list(JUNGLE_MOBS.items())
        mob_key, mob_data = random.choice(mob_types)
        game_rooms[room_id]['mobs'].append({
            'x': random.randint(300, 700),
            'y': random.randint(100, 500),
            'hp': mob_data['hp'],
            'maxHp': mob_data['hp'],
            'dmg': mob_data['dmg'],
            'type': mob_data['name'],
            'color': mob_data['color'],
            'gold': mob_data['gold'],
            'exp': mob_data['exp']
        })
        socketio.emit('game_state', game_rooms[room_id], room=room_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
