# app.py — Mobile Legends Bang Bang слабый прототип
from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# --- ДАННЫЕ ГЕРОЕВ MLBB ---
HEROES = {
    "alusard": {"name": "Алукард", "hp": 100, "dmg": 25, "role": "Fighter"},
    "miya": {"name": "Мия", "hp": 70, "dmg": 35, "role": "Marksman"},
    "tigreal": {"name": "Тигрил", "hp": 150, "dmg": 15, "role": "Tank"}
}

MONSTERS = {
    "лесной крип": {"hp": 30, "dmg": 5, "gold": 50},
    "черепаха": {"hp": 60, "dmg": 10, "gold": 100},
    "ЛОРД": {"hp": 120, "dmg": 20, "gold": 300}
}

# --- HTML ШАБЛОН (всё в одном файле) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MLBB Прототип</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            background: #0a0f1e; 
            color: #f0e68c; 
            font-family: 'Arial', sans-serif; 
            max-width: 500px; 
            margin: 20px auto; 
            padding: 15px;
            text-shadow: 1px 1px 2px black;
        }
        .header {
            background: linear-gradient(45deg, #2c1a4d, #1a0f2e);
            padding: 10px;
            border-radius: 10px 10px 0 0;
            border-left: 3px solid gold;
            border-right: 3px solid gold;
            text-align: center;
        }
        .game-area {
            background: #1a1f2e;
            border: 2px solid #4a6fa5;
            border-radius: 10px;
            padding: 20px;
            margin-top: 10px;
            box-shadow: 0 0 20px rgba(0,0,255,0.2);
        }
        .stats {
            background: #0d111c;
            padding: 10px;
            border-radius: 8px;
            border-left: 5px solid #ff4444;
            margin-bottom: 20px;
        }
        .enemy-stats {
            border-left-color: #44ff44;
        }
        button {
            background: #2a3a5c;
            color: white;
            border: none;
            padding: 12px 20px;
            margin: 5px;
            border-radius: 30px;
            font-weight: bold;
            box-shadow: 0 4px 0 #0f1a2c;
            cursor: pointer;
            transition: 0.1s;
            border: 1px solid #6a8cff;
        }
        button:hover { background: #3a5a8c; transform: translateY(-2px); box-shadow: 0 6px 0 #0f1a2c; }
        button:active { transform: translateY(2px); box-shadow: 0 2px 0 #0f1a2c; }
        .danger { background: #6b2a2a; border-color: #ff6666; }
        .success { background: #2a5a3a; border-color: #66ff66; }
        .log {
            background: black;
            padding: 10px;
            height: 150px;
            overflow-y: scroll;
            border-radius: 5px;
            margin-top: 20px;
            font-family: monospace;
            color: #aaffaa;
            border: 1px inset gray;
        }
        .gold { color: #FFD700; font-weight: bold; }
        .hp-bar {
            width: 100%;
            height: 15px;
            background: #3a1a1a;
            border-radius: 10px;
            margin: 5px 0;
        }
        .hp-fill {
            height: 100%;
            background: #ff4444;
            border-radius: 10px;
            width: 100%;
        }
        a { color: #aaccff; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 MOBILE LEGENDS: BANG BANG 🔥</h1>
        <p>⚡ СЛАБЫЙ ПРОТОТИП ⚡</p>
    </div>

    <div class="game-area">
        {% if not session.get('hero') %}
            <!-- ЭКРАН ВЫБОРА ГЕРОЯ -->
            <h2>👤 ВЫБЕРИТЕ ГЕРОЯ</h2>
            {% for key, hero in heroes.items() %}
                <div style="margin: 15px 0;">
                    <button onclick="location.href='/pick/{{ key }}'">
                        {{ hero.name }} ({{ hero.role }}) <br>
                        ❤️ {{ hero.hp }} | ⚔️ {{ hero.dmg }}
                    </button>
                </div>
            {% endfor %}
            <p style="font-size:12px; color:gray;">Данные сохраняются в сессии браузера</p>
        {% else %}
            <!-- ОСНОВНОЙ ИГРОВОЙ ЭКРАН -->
            <h2>🏆 {{ session['hero_name'] }} | Уровень {{ session['level'] }}</h2>
            <p class="gold">💰 Золото: {{ session['gold'] }}</p>
            
            <div class="stats">
                <b>❤️ HP: {{ session['hp'] }}/{{ session['max_hp'] }}</b>
                <div class="hp-bar">
                    <div class="hp-fill" style="width: {{ (session['hp'] / session['max_hp']) * 100 }}%;"></div>
                </div>
                <b>⚔️ Атака: {{ session['dmg'] }}</b>
            </div>

            {% if session.get('enemy') %}
                <!-- ИДЁТ БОЙ -->
                <div class="stats enemy-stats">
                    <h3>⚡ Враг: {{ session['enemy_name'] }}</h3>
                    <b>❤️ HP врага: {{ session['enemy_hp'] }}</b>
                    <div class="hp-bar">
                        <div class="hp-fill" style="width: {{ (session['enemy_hp'] / session['enemy_max_hp']) * 100 }}%; background: #44aa44;"></div>
                    </div>
                </div>
                <form method="post" action="/attack">
                    <button type="submit" class="danger">⚔️ АТАКОВАТЬ</button>
                    <button type="submit" formaction="/flee" class="success">🏃 СБЕЖАТЬ</button>
                </form>
            {% else %}
                <!-- МИРНЫЙ РЕЖИМ / КАРТА -->
                <h3>🌍 ЛЕГЕНДАРНАЯ КАРТА</h3>
                <form method="post" action="/farm">
                    <button type="submit">🌲 Фармить лес (Крипы)</button>
                </form>
                <form method="post" action="/fight_turtle">
                    <button type="submit">🐢 Битва с Черепахой</button>
                </form>
                <form method="post" action="/fight_lord">
                    <button type="submit" class="danger">👑 БИТВА С ЛОРДОМ</button>
                </form>
                <hr>
                <form method="post" action="/heal">
                    <button type="submit" class="success">💚 Лечиться (50 золота)</button>
                </form>
                <form method="post" action="/reset">
                    <button type="submit" style="background:#555;">🔄 Новый герой</button>
                </form>
            {% endif %}

            <!-- ЛОГ БОЯ -->
            <div class="log">
                {% for msg in session.get('log', []) %}
                    {{ msg }}<br>
                {% endfor %}
            </div>
        {% endif %}
    </div>
    <p style="text-align:center; margin-top:20px;">🔧 MLBB Clone v0.1 — Python Flask</p>
</body>
</html>
'''

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def add_log(message):
    log = session.get('log', [])
    log.append(message)
    if len(log) > 8:  # Держим последние 8 сообщений
        log.pop(0)
    session['log'] = log

def init_enemy(enemy_key):
    enemy = MONSTERS[enemy_key]
    session['enemy'] = enemy_key
    session['enemy_name'] = enemy_key.upper()
    session['enemy_hp'] = enemy['hp']
    session['enemy_max_hp'] = enemy['hp']
    session['enemy_dmg'] = enemy['dmg']
    session['enemy_gold'] = enemy['gold']

# --- МАРШРУТЫ FLASK ---

@app.route('/')
def index():
    # Инициализация сессии если пусто
    if 'hero' not in session:
        session['hero'] = None
    return render_template_string(HTML_TEMPLATE, heroes=HEROES)

@app.route('/pick/<hero_key>')
def pick_hero(hero_key):
    hero = HEROES[hero_key]
    session['hero'] = hero_key
    session['hero_name'] = hero['name']
    session['hp'] = hero['hp']
    session['max_hp'] = hero['hp']
    session['dmg'] = hero['dmg']
    session['gold'] = 100
    session['level'] = 1
    session['log'] = [f"✅ Вы выбрали {hero['name']}!"]
    session['enemy'] = None
    return redirect(url_for('index'))

@app.route('/farm', methods=['POST'])
def farm():
    if session.get('enemy'): return redirect(url_for('index'))
    init_enemy('лесной крип')
    add_log("🌿 Вы наткнулись на лесного крипа! Бой начинается!")
    return redirect(url_for('index'))

@app.route('/fight_turtle', methods=['POST'])
def fight_turtle():
    if session.get('enemy'): return redirect(url_for('index'))
    init_enemy('черепаха')
    add_log("🐢 Огромная Черепаха атакует!")
    return redirect(url_for('index'))

@app.route('/fight_lord', methods=['POST'])
def fight_lord():
    if session.get('enemy'): return redirect(url_for('index'))
    if session['level'] < 2:
        add_log("❌ Лорд слишком силён! Достигните 2 уровня.")
        return redirect(url_for('index'))
    init_enemy('ЛОРД')
    add_log("👑 ЛОРД ПРОБУДИЛСЯ! Это будет тяжёлая битва!")
    return redirect(url_for('index'))

@app.route('/attack', methods=['POST'])
def attack():
    if not session.get('enemy'):
        return redirect(url_for('index'))
    
    # Урон героя
    player_dmg = session['dmg'] + random.randint(-3, 5)
    session['enemy_hp'] -= player_dmg
    add_log(f"⚔️ Вы нанесли {player_dmg} урона!")

    if session['enemy_hp'] <= 0:
        # ПОБЕДА
        gold_reward = session['enemy_gold']
        session['gold'] += gold_reward
        add_log(f"🎉 ПОБЕДА! Получено {gold_reward} золота!")
        
        # Лорд даёт уровень
        if session['enemy'] == 'ЛОРД':
            session['level'] += 1
            session['max_hp'] += 20
            session['hp'] = session['max_hp']
            session['dmg'] += 5
            add_log(f"⬆️ УРОВЕНЬ {session['level']}! HP и урон увеличены!")
        
        session['enemy'] = None
        return redirect(url_for('index'))

    # Ответный удар врага
    enemy_dmg = session['enemy_dmg'] + random.randint(-2, 4)
    session['hp'] -= enemy_dmg
    add_log(f"💥 Враг наносит {enemy_dmg} урона!")

    if session['hp'] <= 0:
        # СМЕРТЬ
        add_log("💀 ВАС УБИЛИ... Вы воскресли на базе с 50% HP.")
        session['hp'] = session['max_hp'] // 2
        session['gold'] = max(0, session['gold'] - 50)
        session['enemy'] = None

    return redirect(url_for('index'))

@app.route('/flee', methods=['POST'])
def flee():
    if session.get('enemy'):
        add_log("🏃 Вы сбежали с поля боя, но потеряли 20 золота.")
        session['gold'] = max(0, session['gold'] - 20)
        session['enemy'] = None
    return redirect(url_for('index'))

@app.route('/heal', methods=['POST'])
def heal():
    if session.get('enemy'):
        add_log("❌ Нельзя лечиться в бою!")
        return redirect(url_for('index'))
    if session['gold'] >= 50:
        session['gold'] -= 50
        session['hp'] = session['max_hp']
        add_log("💚 HP полностью восстановлено!")
    else:
        add_log("❌ Недостаточно золота!")
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('index'))

# --- ЗАПУСК ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
