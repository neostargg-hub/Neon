# app.py — Mobile Legends Bang Bang прототип v2.0
from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# --- РАСШИРЕННЫЕ ДАННЫЕ ГЕРОЕВ MLBB ---
HEROES = {
    "alusard": {"name": "Алукард", "hp": 120, "dmg": 28, "role": "Fighter", "skill": "Разрез"},
    "miya": {"name": "Мия", "hp": 85, "dmg": 40, "role": "Marksman", "skill": "Град стрел"},
    "tigreal": {"name": "Тигрил", "hp": 170, "dmg": 18, "role": "Tank", "skill": "Священный удар"},
    "eudora": {"name": "Эвдора", "hp": 75, "dmg": 50, "role": "Mage", "skill": "Молния"}
}

# --- ПРЕДМЕТЫ (можно купить за золото) ---
ITEMS = {
    "blade": {"name": "Меч Отчаяния", "cost": 150, "dmg_bonus": 15, "hp_bonus": 0},
    "armor": {"name": "Кираса", "cost": 120, "dmg_bonus": 0, "hp_bonus": 40},
    "boots": {"name": "Сапоги скорости", "cost": 80, "dmg_bonus": 5, "hp_bonus": 10},
    "blood": {"name": "Кровожадность", "cost": 200, "dmg_bonus": 20, "hp_bonus": 25}
}

# --- МОНСТРЫ (разных уровней) ---
MONSTERS = {
    "лесной крип": {"hp": 35, "dmg": 6, "gold": 50, "exp": 20},
    "большой крип": {"hp": 50, "dmg": 10, "gold": 80, "exp": 35},
    "черепаха": {"hp": 80, "dmg": 15, "gold": 150, "exp": 60},
    "ЛОРД": {"hp": 150, "dmg": 25, "gold": 350, "exp": 150}
}

# --- СИСТЕМА УРОВНЕЙ ---
LEVELS = {
    1: {"exp_needed": 0},
    2: {"exp_needed": 100},
    3: {"exp_needed": 250},
    4: {"exp_needed": 450},
    5: {"exp_needed": 700}
}

# --- HTML ШАБЛОН (улучшенный интерфейс) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MLBB v2.0 — Эволюция</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }
        body { 
            background: linear-gradient(135deg, #0a0f1e 0%, #1a0f2e 100%);
            color: #f0e68c; 
            font-family: 'Arial', sans-serif; 
            max-width: 600px; 
            margin: 20px auto; 
            padding: 15px;
            text-shadow: 1px 1px 2px black;
            min-height: 100vh;
        }
        .header {
            background: linear-gradient(45deg, #2c1a4d, #1a0f2e);
            padding: 15px;
            border-radius: 15px 15px 0 0;
            border: 2px solid gold;
            text-align: center;
            margin-bottom: 15px;
        }
        .version-badge {
            background: gold;
            color: black;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .game-area {
            background: rgba(26, 31, 46, 0.95);
            border: 2px solid #4a6fa5;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 30px rgba(78, 114, 255, 0.3);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }
        .stat-card {
            background: #0d111c;
            padding: 12px;
            border-radius: 10px;
            border-left: 4px solid #ff4444;
        }
        .stat-card.enemy { border-left-color: #44ff44; }
        .hp-bar {
            width: 100%;
            height: 20px;
            background: #3a1a1a;
            border-radius: 10px;
            margin: 8px 0;
            border: 1px solid #555;
        }
        .hp-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff4444, #ff6666);
            border-radius: 10px;
            transition: width 0.3s;
        }
        .exp-bar {
            height: 8px;
            background: #1a3a1a;
            border-radius: 5px;
            margin: 5px 0;
        }
        .exp-fill {
            height: 100%;
            background: linear-gradient(90deg, #44aaff, #88ccff);
            border-radius: 5px;
        }
        button {
            background: #2a3a5c;
            color: white;
            border: none;
            padding: 12px 18px;
            margin: 5px;
            border-radius: 25px;
            font-weight: bold;
            box-shadow: 0 4px 0 #0f1a2c;
            cursor: pointer;
            transition: 0.15s;
            border: 1px solid #6a8cff;
            font-size: 14px;
        }
        button:hover { 
            background: #3a5a8c; 
            transform: translateY(-2px); 
            box-shadow: 0 6px 0 #0f1a2c; 
        }
        button:active { 
            transform: translateY(2px); 
            box-shadow: 0 2px 0 #0f1a2c; 
        }
        button:disabled {
            opacity: 0.5;
            transform: none;
            box-shadow: 0 4px 0 #0f1a2c;
            cursor: not-allowed;
        }
        .danger { background: #6b2a2a; border-color: #ff6666; }
        .success { background: #2a5a3a; border-color: #66ff66; }
        .shop { background: #5a4a2a; border-color: #ffcc66; }
        .log {
            background: #000000;
            padding: 12px;
            height: 160px;
            overflow-y: auto;
            border-radius: 8px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            color: #aaffaa;
            border: 1px inset #666;
            font-size: 13px;
        }
        .inventory {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin: 10px 0;
        }
        .item-badge {
            background: #2a3a5c;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            border: 1px solid gold;
        }
        .gold { color: #FFD700; font-weight: bold; font-size: 18px; }
        .shop-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin: 15px 0;
        }
        .shop-item {
            background: #1a1f2e;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #4a6fa5;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 MOBILE LEGENDS: BANG BANG 🔥</h1>
        <span class="version-badge">⚡ ВЕРСИЯ 2.0 — ПРЕДМЕТЫ И ОПЫТ ⚡</span>
    </div>

    <div class="game-area">
        {% if not session.get('hero') %}
            <!-- ЭКРАН ВЫБОРА ГЕРОЯ (улучшенный) -->
            <h2>👤 ВЫБЕРИТЕ ГЕРОЯ</h2>
            <div style="display: grid; gap: 10px;">
            {% for key, hero in heroes.items() %}
                <div style="background: #0d111c; padding: 15px; border-radius: 10px; border: 1px solid #4a6fa5;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <h3 style="margin:0;">{{ hero.name }}</h3>
                            <span style="color: #aaa;">{{ hero.role }}</span>
                        </div>
                        <div style="text-align: right;">
                            <div>❤️ {{ hero.hp }}</div>
                            <div>⚔️ {{ hero.dmg }}</div>
                        </div>
                    </div>
                    <div style="margin-top: 10px;">
                        <b>🎯 Скилл:</b> {{ hero.skill }}
                    </div>
                    <button onclick="location.href='/pick/{{ key }}'" style="width: 100%; margin-top: 10px;">
                        ВЫБРАТЬ {{ hero.name.upper() }}
                    </button>
                </div>
            {% endfor %}
            </div>
        {% else %}
            <!-- ОСНОВНОЙ ИГРОВОЙ ЭКРАН v2.0 -->
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="margin:0;">🏆 {{ session['hero_name'] }}</h2>
                <div class="gold">💰 {{ session['gold'] }}</div>
            </div>
            
            <!-- Опыт и уровень -->
            <div style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between;">
                    <span>⭐ Уровень {{ session['level'] }}</span>
                    <span>{{ session['exp'] }}/{{ session['exp_needed'] }} EXP</span>
                </div>
                <div class="exp-bar">
                    <div class="exp-fill" style="width: {{ (session['exp'] / session['exp_needed']) * 100 }}%;"></div>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <b>{{ session['hero_name'] }}</b>
                    <div>❤️ HP: {{ session['hp'] }}/{{ session['max_hp'] }}</div>
                    <div class="hp-bar">
                        <div class="hp-fill" style="width: {{ (session['hp'] / session['max_hp']) * 100 }}%;"></div>
                    </div>
                    <div>⚔️ Атака: {{ session['dmg'] }}</div>
                    <div>🛡️ Роль: {{ session['role'] }}</div>
                </div>
                
                {% if session.get('enemy') %}
                <div class="stat-card enemy">
                    <b>{{ session['enemy_name'] }}</b>
                    <div>❤️ HP: {{ session['enemy_hp'] }}/{{ session['enemy_max_hp'] }}</div>
                    <div class="hp-bar">
                        <div class="hp-fill" style="width: {{ (session['enemy_hp'] / session['enemy_max_hp']) * 100 }}%; background: #44aa44;"></div>
                    </div>
                    <div>⚔️ Атака: {{ session['enemy_dmg'] }}</div>
                </div>
                {% else %}
                <div class="stat-card">
                    <b>📊 Статистика</b>
                    <div>⚔️ Убито мобов: {{ session.get('kills', 0) }}</div>
                    <div>💀 Смертей: {{ session.get('deaths', 0) }}</div>
                </div>
                {% endif %}
            </div>

            <!-- Инвентарь -->
            {% if session.get('inventory') %}
            <div>
                <b>🎒 Инвентарь:</b>
                <div class="inventory">
                    {% for item in session['inventory'] %}
                        <span class="item-badge">{{ item }}</span>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            {% if session.get('enemy') %}
                <!-- РЕЖИМ БОЯ -->
                <form method="post" action="/attack">
                    <button type="submit" class="danger">⚔️ АТАКОВАТЬ (обычная)</button>
                    <button type="submit" formaction="/skill" class="danger" style="background:#8a4a2a;">
                        ✨ {{ session.get('skill', 'СКИЛЛ') }}
                    </button>
                    <button type="submit" formaction="/flee" class="success">🏃 СБЕЖАТЬ</button>
                </form>
            {% else %}
                <!-- МИРНЫЙ РЕЖИМ -->
                <h3>🌍 КАРТА БОЯ</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <form method="post" action="/farm_small">
                        <button type="submit" style="width:100%;">🌿 Малый крип</button>
                    </form>
                    <form method="post" action="/farm_big">
                        <button type="submit" style="width:100%;">🌳 Большой крип</button>
                    </form>
                    <form method="post" action="/fight_turtle">
                        <button type="submit" style="width:100%;">🐢 Черепаха</button>
                    </form>
                    <form method="post" action="/fight_lord">
                        <button type="submit" class="danger" style="width:100%;">👑 ЛОРД</button>
                    </form>
                </div>
                
                <!-- МАГАЗИН -->
                <h3 style="margin-top: 20px;">🏪 МАГАЗИН</h3>
                <div class="shop-grid">
                    {% for key, item in items.items() %}
                    <div class="shop-item">
                        <b>{{ item.name }}</b><br>
                        <span class="gold">{{ item.cost }}💰</span><br>
                        <small>⚔️+{{ item.dmg_bonus }} ❤️+{{ item.hp_bonus }}</small>
                        <form method="post" action="/buy/{{ key }}" style="margin-top:5px;">
                            <button type="submit" class="shop" style="padding:5px; width:100%;">КУПИТЬ</button>
                        </form>
                    </div>
                    {% endfor %}
                </div>
                
                <hr>
                <div style="display: flex; gap: 5px;">
                    <form method="post" action="/heal" style="flex:1;">
                        <button type="submit" class="success" style="width:100%;">💚 Лечение (80💰)</button>
                    </form>
                    <form method="post" action="/reset" style="flex:1;">
                        <button type="submit" style="background:#555; width:100%;">🔄 Сброс</button>
                    </form>
                </div>
            {% endif %}

            <!-- ЛОГ СОБЫТИЙ -->
            <div class="log">
                {% for msg in session.get('log', []) %}
                    {{ msg }}<br>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def add_log(message):
    log = session.get('log', [])
    log.append(message)
    if len(log) > 10:
        log.pop(0)
    session['log'] = log

def check_level_up():
    current_level = session['level']
    current_exp = session['exp']
    
    for level, data in LEVELS.items():
        if level > current_level and current_exp >= data['exp_needed']:
            session['level'] = level
            session['max_hp'] += 25
            session['hp'] = session['max_hp']
            session['dmg'] += 8
            add_log(f"🎉 УРОВЕНЬ {level}! HP +25, Атака +8!")
            session['exp_needed'] = LEVELS.get(level + 1, {"exp_needed": 9999})['exp_needed']
            return True
    return False

def init_enemy(enemy_key):
    enemy = MONSTERS[enemy_key]
    session['enemy'] = enemy_key
    session['enemy_name'] = enemy_key.upper()
    session['enemy_hp'] = enemy['hp']
    session['enemy_max_hp'] = enemy['hp']
    session['enemy_dmg'] = enemy['dmg']
    session['enemy_gold'] = enemy['gold']
    session['enemy_exp'] = enemy['exp']

def calculate_damage(base_dmg, is_skill=False):
    if is_skill:
        return int(base_dmg * 1.8 + random.randint(-5, 10))
    return base_dmg + random.randint(-3, 8)

# --- МАРШРУТЫ FLASK v2.0 ---

@app.route('/')
def index():
    if 'hero' not in session:
        session['hero'] = None
    return render_template_string(HTML_TEMPLATE, heroes=HEROES, items=ITEMS)

@app.route('/pick/<hero_key>')
def pick_hero(hero_key):
    hero = HEROES[hero_key]
    session.clear()
    session['hero'] = hero_key
    session['hero_name'] = hero['name']
    session['role'] = hero['role']
    session['skill'] = hero['skill']
    session['hp'] = hero['hp']
    session['max_hp'] = hero['hp']
    session['dmg'] = hero['dmg']
    session['gold'] = 150
    session['level'] = 1
    session['exp'] = 0
    session['exp_needed'] = LEVELS[2]['exp_needed']
    session['kills'] = 0
    session['deaths'] = 0
    session['inventory'] = []
    session['log'] = [f"✅ Вы выбрали {hero['name']}!", f"🎯 Скилл: {hero['skill']}"]
    session['enemy'] = None
    return redirect(url_for('index'))

@app.route('/buy/<item_key>', methods=['POST'])
def buy_item(item_key):
    if session.get('enemy'):
        add_log("❌ Нельзя покупать в бою!")
        return redirect(url_for('index'))
    
    item = ITEMS.get(item_key)
    if not item:
        return redirect(url_for('index'))
    
    if session['gold'] >= item['cost']:
        session['gold'] -= item['cost']
        session['dmg'] += item['dmg_bonus']
        session['max_hp'] += item['hp_bonus']
        session['hp'] += item['hp_bonus']
        inventory = session.get('inventory', [])
        inventory.append(item['name'])
        session['inventory'] = inventory
        add_log(f"🛒 Куплено: {item['name']}! +{item['dmg_bonus']} атаки, +{item['hp_bonus']} HP")
    else:
        add_log(f"❌ Недостаточно золота для {item['name']}!")
    
    return redirect(url_for('index'))

# Фарм разных мобов
@app.route('/farm_small', methods=['POST'])
def farm_small():
    if session.get('enemy'): return redirect(url_for('index'))
    init_enemy('лесной крип')
    add_log("🌿 Вы напали на лесного крипа!")
    return redirect(url_for('index'))

@app.route('/farm_big', methods=['POST'])
def farm_big():
    if session.get('enemy'): return redirect(url_for('index'))
    init_enemy('большой крип')
    add_log("🌳 Большой крип рычит на вас!")
    return redirect(url_for('index'))

@app.route('/fight_turtle', methods=['POST'])
def fight_turtle():
    if session.get('enemy'): return redirect(url_for('index'))
    init_enemy('черепаха')
    add_log("🐢 Древняя Черепаха просыпается!")
    return redirect(url_for('index'))

@app.route('/fight_lord', methods=['POST'])
def fight_lord():
    if session.get('enemy'): return redirect(url_for('index'))
    if session['level'] < 2:
        add_log("❌ Лорд слишком силён! Нужен 2 уровень.")
        return redirect(url_for('index'))
    init_enemy('ЛОРД')
    add_log("👑 ЛОРД ВЫХОДИТ НА АРЕНУ!")
    return redirect(url_for('index'))

@app.route('/attack', methods=['POST'])
def attack():
    if not session.get('enemy'):
        return redirect(url_for('index'))
    
    # Атака игрока
    player_dmg = calculate_damage(session['dmg'])
    session['enemy_hp'] -= player_dmg
    add_log(f"⚔️ Вы нанесли {player_dmg} урона!")

    if session['enemy_hp'] <= 0:
        # ПОБЕДА
        gold_reward = session['enemy_gold']
        exp_reward = session['enemy_exp']
        session['gold'] += gold_reward
        session['exp'] += exp_reward
        session['kills'] = session.get('kills', 0) + 1
        add_log(f"🎉 ПОБЕДА! +{gold_reward}💰 +{exp_reward} EXP!")
        
        if session['enemy'] == 'ЛОРД':
            session['exp'] += 100  # Бонус за Лорда
            add_log("👑 ЛОРД ПОВЕРЖЕН! +100 бонусного опыта!")
        
        if check_level_up():
            pass  # Уровень уже поднят в функции
        
        session['enemy'] = None
        return redirect(url_for('index'))

    # Ответ врага
    enemy_dmg = calculate_damage(session['enemy_dmg'])
    session['hp'] -= enemy_dmg
    add_log(f"💥 {session['enemy_name']} наносит {enemy_dmg} урона!")

    if session['hp'] <= 0:
        session['deaths'] = session.get('deaths', 0) + 1
        add_log(f"💀 ВАС УБИЛИ... Потеряно 75 золота.")
        session['hp'] = session['max_hp'] // 2
        session['gold'] = max(0, session['gold'] - 75)
        session['enemy'] = None

    return redirect(url_for('index'))

@app.route('/skill', methods=['POST'])
def use_skill():
    if not session.get('enemy'):
        return redirect(url_for('index'))
    
    # Усиленная атака скиллом
    skill_dmg = calculate_damage(session['dmg'], is_skill=True)
    session['enemy_hp'] -= skill_dmg
    add_log(f"✨ СКИЛЛ: {session['skill']}! Нанесено {skill_dmg} урона!")
    
    if session['enemy_hp'] <= 0:
        return redirect(url_for('attack'))  # Перенаправляем на логику победы
    
    # Ответ врага (усиленный)
    enemy_dmg = calculate_damage(session['enemy_dmg']) + 5
    session['hp'] -= enemy_dmg
    add_log(f"💢 Контратака! {session['enemy_name']} наносит {enemy_dmg} урона!")
    
    if session['hp'] <= 0:
        session['deaths'] = session.get('deaths', 0) + 1
        add_log(f"💀 Смерть после использования скилла...")
        session['hp'] = session['max_hp'] // 2
        session['gold'] = max(0, session['gold'] - 75)
        session['enemy'] = None
    
    return redirect(url_for('index'))

@app.route('/flee', methods=['POST'])
def flee():
    if session.get('enemy'):
        if random.random() < 0.7:  # 70% шанс побега
            add_log("🏃 Успешный побег! -20💰")
            session['gold'] = max(0, session['gold'] - 20)
            session['enemy'] = None
        else:
            add_log("❌ Не удалось сбежать!")
            enemy_dmg = calculate_damage(session['enemy_dmg'])
            session['hp'] -= enemy_dmg
            add_log(f"💥 Враг наносит {enemy_dmg} урона при побеге!")
            if session['hp'] <= 0:
                session['deaths'] = session.get('deaths', 0) + 1
                session['hp'] = session['max_hp'] // 2
                session['gold'] = max(0, session['gold'] - 75)
                session['enemy'] = None
    return redirect(url_for('index'))

@app.route('/heal', methods=['POST'])
def heal():
    if session.get('enemy'):
        add_log("❌ Нельзя лечиться в бою!")
        return redirect(url_for('index'))
    if session['gold'] >= 80:
        session['gold'] -= 80
        session['hp'] = session['max_hp']
        add_log("💚 Полное исцеление!")
    else:
        add_log("❌ Нужно 80 золота!")
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
