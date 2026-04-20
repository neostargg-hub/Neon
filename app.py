# app.py — Mobile Legends Bang Bang прототип v3.0 — ГРАФИЧЕСКАЯ MOBA
from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
import random
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# --- ГЕРОИ (улучшенные характеристики) ---
HEROES = {
    "alusard": {"name": "Алукард", "hp": 150, "dmg": 30, "speed": 4, "color": "#ff4444", "role": "Fighter"},
    "miya": {"name": "Мия", "hp": 100, "dmg": 45, "speed": 3, "color": "#44ff44", "role": "Marksman"},
    "tigreal": {"name": "Тигрил", "hp": 200, "dmg": 20, "speed": 2, "color": "#4444ff", "role": "Tank"},
    "eudora": {"name": "Эвдора", "hp": 90, "dmg": 55, "speed": 3, "color": "#ff44ff", "role": "Mage"}
}

# --- HTML С CANVAS И JAVASCRIPT ДЛЯ ИГРЫ ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>MLBB v3.0 — Графическая MOBA</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: #0a0a0a;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Arial', sans-serif;
        }
        #gameContainer {
            background: #1a1a2e;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 0 50px rgba(0,100,255,0.3);
        }
        canvas { 
            border: 3px solid #4a6fa5;
            border-radius: 10px;
            display: block;
            background: linear-gradient(135deg, #0f1a2c, #1a2a4a);
            cursor: crosshair;
        }
        #ui {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
            color: white;
        }
        .stats {
            background: rgba(0,0,0,0.7);
            padding: 10px;
            border-radius: 10px;
            border-left: 4px solid gold;
        }
        button {
            background: #2a3a5c;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            border: 1px solid #6a8cff;
        }
        button:hover { background: #3a5a8c; }
        .danger { background: #6b2a2a; }
        .success { background: #2a5a3a; }
        #minimap {
            width: 150px;
            height: 150px;
            background: #0a0f1e;
            border: 2px solid gold;
            border-radius: 10px;
            margin-left: 20px;
        }
        .flex-row {
            display: flex;
            align-items: center;
        }
        .log {
            background: black;
            color: #aaffaa;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
            max-width: 300px;
            overflow: hidden;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        {% if not session.get('hero') %}
            <!-- ЭКРАН ВЫБОРА ГЕРОЯ -->
            <div style="color: white; padding: 30px;">
                <h1 style="color: gold; text-align: center;">⚔️ ВЫБЕРИТЕ ГЕРОЯ ⚔️</h1>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 30px;">
                    {% for key, hero in heroes.items() %}
                    <div style="background: {{ hero.color }}20; padding: 20px; border-radius: 15px; border: 2px solid {{ hero.color }};">
                        <h2 style="color: {{ hero.color }};">{{ hero.name }}</h2>
                        <p>❤️ {{ hero.hp }} | ⚔️ {{ hero.dmg }}</p>
                        <p>🏃 Скорость: {{ hero.speed }}</p>
                        <p>🎭 {{ hero.role }}</p>
                        <button onclick="location.href='/pick/{{ key }}'" 
                                style="background: {{ hero.color }}; width: 100%; margin-top: 10px;">
                            ВЫБРАТЬ
                        </button>
                    </div>
                    {% endfor %}
                </div>
            </div>
        {% else %}
            <!-- ИГРОВОЙ ЭКРАН С CANVAS -->
            <div class="flex-row">
                <canvas id="gameCanvas" width="800" height="500"></canvas>
                <div style="margin-left: 20px;">
                    <div id="minimap">
                        <canvas id="miniCanvas" width="150" height="150"></canvas>
                    </div>
                    <div class="stats" style="margin-top: 20px;">
                        <h3 id="heroName">{{ session['hero_name'] }}</h3>
                        <p>❤️ HP: <span id="hpDisplay">{{ session['hp'] }}</span>/{{ session['max_hp'] }}</p>
                        <p>💰 Золото: <span id="goldDisplay">{{ session['gold'] }}</span></p>
                        <p>⭐ Уровень: <span id="levelDisplay">{{ session['level'] }}</span></p>
                        <p>🗡️ Убийств: <span id="killsDisplay">0</span></p>
                    </div>
                    <div class="log" id="logDisplay">
                        Игра началась!
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 15px; justify-content: center;">
                <button onclick="gameAction('attack')" class="danger">⚔️ АТАКА</button>
                <button onclick="gameAction('skill')">✨ СКИЛЛ</button>
                <button onclick="gameAction('move_up')">⬆️ ВВЕРХ</button>
                <button onclick="gameAction('move_down')">⬇️ ВНИЗ</button>
                <button onclick="gameAction('move_left')">⬅️ ВЛЕВО</button>
                <button onclick="gameAction('move_right')">➡️ ВПРАВО</button>
                <button onclick="gameAction('heal')" class="success">💚 ЛЕЧЕНИЕ</button>
                <button onclick="location.href='/reset'">🔄 СБРОС</button>
            </div>
        {% endif %}
    </div>

    {% if session.get('hero') %}
    <script>
        // ИГРОВЫЕ ДАННЫЕ ИЗ СЕССИИ
        let gameState = {
            hero: {
                name: "{{ session['hero_name'] }}",
                hp: {{ session['hp'] }},
                maxHp: {{ session['max_hp'] }},
                dmg: {{ session['dmg'] }},
                x: 400,
                y: 250,
                color: "{{ session.get('color', '#ff4444') }}",
                speed: {{ session.get('speed', 3) }}
            },
            enemies: [],
            gold: {{ session['gold'] }},
            level: {{ session['level'] }},
            kills: 0,
            log: ["Игра началась! Используйте кнопки для управления."]
        };

        // Генерация мобов
        function spawnEnemy() {
            if (gameState.enemies.length < 5) {
                gameState.enemies.push({
                    x: Math.random() * 700 + 50,
                    y: Math.random() * 400 + 50,
                    hp: 40,
                    maxHp: 40,
                    dmg: 10,
                    type: "крип",
                    color: "#88ff88",
                    targetX: Math.random() * 700 + 50,
                    targetY: Math.random() * 400 + 50
                });
            }
        }

        // Спавн каждые 5 секунд
        setInterval(spawnEnemy, 5000);
        spawnEnemy();
        spawnEnemy();

        // Отрисовка игры
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const miniCanvas = document.getElementById('miniCanvas');
        const miniCtx = miniCanvas.getContext('2d');

        function drawGame() {
            // Очистка
            ctx.clearRect(0, 0, 800, 500);
            
            // Рисуем линии (топ, мид, бот)
            ctx.strokeStyle = "#ffffff30";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, 150); ctx.lineTo(800, 150);
            ctx.moveTo(0, 350); ctx.lineTo(800, 350);
            ctx.stroke();
            
            // Рисуем башни
            ctx.fillStyle = "#ffaa00";
            ctx.beginPath();
            ctx.arc(100, 150, 25, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#00aaff";
            ctx.beginPath();
            ctx.arc(700, 350, 25, 0, Math.PI * 2);
            ctx.fill();
            
            // Текст башен
            ctx.fillStyle = "white";
            ctx.font = "bold 12px Arial";
            ctx.fillText("🔥 TOP", 75, 145);
            ctx.fillText("💧 BOT", 675, 345);

            // Рисуем врагов
            gameState.enemies.forEach(enemy => {
                // Движение врагов
                if (Math.random() < 0.02) {
                    enemy.targetX = Math.random() * 700 + 50;
                    enemy.targetY = Math.random() * 400 + 50;
                }
                
                // Преследование героя если близко
                const dx = gameState.hero.x - enemy.x;
                const dy = gameState.hero.y - enemy.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist < 100) {
                    enemy.targetX = gameState.hero.x;
                    enemy.targetY = gameState.hero.y;
                }
                
                // Движение к цели
                if (Math.abs(enemy.x - enemy.targetX) > 2) {
                    enemy.x += enemy.targetX > enemy.x ? 0.5 : -0.5;
                }
                if (Math.abs(enemy.y - enemy.targetY) > 2) {
                    enemy.y += enemy.targetY > enemy.y ? 0.5 : -0.5;
                }
                
                // Отрисовка врага
                ctx.fillStyle = enemy.color;
                ctx.beginPath();
                ctx.arc(enemy.x, enemy.y, 18, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // HP бар врага
                ctx.fillStyle = "#ff0000";
                ctx.fillRect(enemy.x - 20, enemy.y - 30, 40, 5);
                ctx.fillStyle = "#00ff00";
                ctx.fillRect(enemy.x - 20, enemy.y - 30, 40 * (enemy.hp / enemy.maxHp), 5);
                
                // Текст
                ctx.fillStyle = "white";
                ctx.font = "10px Arial";
                ctx.fillText(`${Math.floor(enemy.hp)}/${enemy.maxHp}`, enemy.x - 15, enemy.y - 35);
            });

            // Рисуем героя
            ctx.fillStyle = gameState.hero.color;
            ctx.shadowColor = gameState.hero.color;
            ctx.shadowBlur = 20;
            ctx.beginPath();
            ctx.arc(gameState.hero.x, gameState.hero.y, 22, 0, Math.PI * 2);
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 3;
            ctx.stroke();
            
            // Имя героя
            ctx.fillStyle = "white";
            ctx.font = "bold 14px Arial";
            ctx.fillText(gameState.hero.name, gameState.hero.x - 30, gameState.hero.y - 35);
            
            // HP бар героя
            ctx.fillStyle = "#ff0000";
            ctx.fillRect(gameState.hero.x - 30, gameState.hero.y - 25, 60, 8);
            ctx.fillStyle = "#00ff00";
            ctx.fillRect(gameState.hero.x - 30, gameState.hero.y - 25, 60 * (gameState.hero.hp / gameState.hero.maxHp), 8);

            // Мини-карта
            miniCtx.clearRect(0, 0, 150, 150);
            miniCtx.fillStyle = "#0a0f1e";
            miniCtx.fillRect(0, 0, 150, 150);
            
            // Герой на миникарте
            miniCtx.fillStyle = gameState.hero.color;
            miniCtx.beginPath();
            miniCtx.arc(gameState.hero.x / 800 * 150, gameState.hero.y / 500 * 150, 5, 0, Math.PI * 2);
            miniCtx.fill();
            
            // Враги на миникарте
            miniCtx.fillStyle = "#ff4444";
            gameState.enemies.forEach(enemy => {
                miniCtx.beginPath();
                miniCtx.arc(enemy.x / 800 * 150, enemy.y / 500 * 150, 3, 0, Math.PI * 2);
                miniCtx.fill();
            });

            // Обновление UI
            document.getElementById('hpDisplay').textContent = Math.floor(gameState.hero.hp);
            document.getElementById('goldDisplay').textContent = gameState.gold;
            document.getElementById('levelDisplay').textContent = gameState.level;
            document.getElementById('killsDisplay').textContent = gameState.kills;
            
            const logDiv = document.getElementById('logDisplay');
            logDiv.innerHTML = gameState.log.slice(-3).join('<br>');
        }

        // Игровые действия
        function gameAction(action) {
            fetch('/game_action', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    action: action,
                    hero_x: gameState.hero.x,
                    hero_y: gameState.hero.y,
                    enemies: gameState.enemies
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    gameState.hero.hp = data.hero_hp;
                    gameState.hero.maxHp = data.hero_max_hp;
                    gameState.gold = data.gold;
                    gameState.level = data.level;
                    gameState.kills = data.kills;
                    gameState.log = data.log;
                    
                    // Обновление врагов
                    if (data.enemies) {
                        gameState.enemies = data.enemies;
                    }
                    
                    // Движение
                    const speed = gameState.hero.speed || 3;
                    if (action === 'move_up') gameState.hero.y = Math.max(30, gameState.hero.y - speed * 5);
                    if (action === 'move_down') gameState.hero.y = Math.min(470, gameState.hero.y + speed * 5);
                    if (action === 'move_left') gameState.hero.x = Math.max(30, gameState.hero.x - speed * 5);
                    if (action === 'move_right') gameState.hero.x = Math.min(770, gameState.hero.x + speed * 5);
                    
                    if (gameState.hero.hp <= 0) {
                        alert('💀 ВАС УБИЛИ! Воскрешение...');
                        gameState.hero.hp = gameState.hero.maxHp / 2;
                        gameState.hero.x = 400;
                        gameState.hero.y = 250;
                    }
                }
                drawGame();
            });
        }

        // Авто-обновление каждые 100мс
        setInterval(() => {
            gameState.enemies = gameState.enemies.filter(e => e.hp > 0);
            drawGame();
        }, 100);

        // Запуск отрисовки
        drawGame();
    </script>
    {% endif %}
</body>
</html>
'''

# --- FLASK МАРШРУТЫ ДЛЯ ГРАФИЧЕСКОЙ ИГРЫ ---

@app.route('/')
def index():
    if 'hero' not in session:
        session['hero'] = None
    return render_template_string(HTML_TEMPLATE, heroes=HEROES)

@app.route('/pick/<hero_key>')
def pick_hero(hero_key):
    hero = HEROES[hero_key]
    session.clear()
    session['hero'] = hero_key
    session['hero_name'] = hero['name']
    session['hp'] = hero['hp']
    session['max_hp'] = hero['hp']
    session['dmg'] = hero['dmg']
    session['speed'] = hero['speed']
    session['color'] = hero['color']
    session['gold'] = 200
    session['level'] = 1
    session['exp'] = 0
    session['kills'] = 0
    session['log'] = ["✅ Герой выбран!", "🎮 Используйте WASD или кнопки"]
    return redirect(url_for('index'))

@app.route('/game_action', methods=['POST'])
def game_action():
    data = request.json
    action = data.get('action')
    hero_x = data.get('hero_x', 400)
    hero_y = data.get('hero_y', 250)
    enemies = data.get('enemies', [])
    
    hero_hp = session.get('hp', 100)
    hero_max_hp = session.get('max_hp', 100)
    hero_dmg = session.get('dmg', 30)
    gold = session.get('gold', 0)
    level = session.get('level', 1)
    kills = session.get('kills', 0)
    log = session.get('log', [])
    
    # Обработка действий
    if action == 'attack' or action == 'skill':
        dmg_multiplier = 2.0 if action == 'skill' else 1.0
        attack_range = 80
        
        for enemy in enemies:
            dx = enemy['x'] - hero_x
            dy = enemy['y'] - hero_y
            dist = (dx**2 + dy**2)**0.5
            
            if dist < attack_range:
                dmg = int(hero_dmg * dmg_multiplier + random.randint(-5, 10))
                enemy['hp'] -= dmg
                log.append(f"⚔️ Нанесено {dmg} урона!")
                
                if enemy['hp'] <= 0:
                    gold += 50
                    kills += 1
                    log.append(f"🎉 Крип убит! +50💰")
                else:
                    # Ответный удар
                    hero_hp -= enemy['dmg']
                    log.append(f"💥 Крип наносит {enemy['dmg']} урона")
                break
    
    elif action == 'heal':
        if gold >= 100:
            gold -= 100
            hero_hp = hero_max_hp
            log.append("💚 Полное исцеление!")
        else:
            log.append("❌ Недостаточно золота!")
    
    # Удаление мёртвых врагов
    enemies = [e for e in enemies if e['hp'] > 0]
    
    # Сохранение в сессию
    session['hp'] = hero_hp
    session['gold'] = gold
    session['kills'] = kills
    session['log'] = log[-10:]
    
    # Проверка смерти героя
    if hero_hp <= 0:
        hero_hp = hero_max_hp // 2
        gold = max(0, gold - 100)
        log.append("💀 Смерть! Потеряно 100💰")
        session['hp'] = hero_hp
        session['gold'] = gold
    
    return jsonify({
        'success': True,
        'hero_hp': hero_hp,
        'hero_max_hp': hero_max_hp,
        'gold': gold,
        'level': level,
        'kills': kills,
        'log': log[-5:],
        'enemies': enemies
    })

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
