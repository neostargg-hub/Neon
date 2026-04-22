from flask import Flask

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes, viewport-fit=cover">
  <title>Витамины · Еда</title>
  <!-- Красивые шрифты: Inter (основной) + вторичный -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300..700&display=swap" rel="stylesheet">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: "Inter", -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, sans-serif;
      background: #f2f2f7;
      color: #1c1c1e;
      line-height: 1.45;
      -webkit-font-smoothing: antialiased;
      padding-bottom: 30px;
    }

    html {
      scroll-behavior: smooth;
    }

    .container {
      max-width: 680px;
      margin: 0 auto;
      padding: 22px 16px 10px;
    }

    /* Hero с красивым шрифтом */
    .hero {
      margin-bottom: 28px;
      padding-top: 8px;
    }

    .hero .eyebrow {
      font-family: "Inter", sans-serif;
      font-weight: 500;
      font-size: 15px;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      color: #8e8e93;
      margin-bottom: 6px;
    }

    .hero h1 {
      font-family: "Inter", sans-serif;
      font-weight: 700;
      font-size: 38px;
      letter-spacing: -0.8px;
      color: #1c1c1e;
      line-height: 1.1;
    }

    .hero h1 span {
      font-weight: 400;
      color: #8e8e93;
    }

    /* Карточки — стекло iOS */
    .card {
      background: rgba(255, 255, 255, 0.75);
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
      border-radius: 24px;
      padding: 22px 18px;
      margin-bottom: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03), 0 2px 8px rgba(0, 0, 0, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.5);
      transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.3s;
      opacity: 0;
      transform: translateY(20px);
      animation: cardFadeIn 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
    }

    .card:hover {
      box-shadow: 0 24px 40px rgba(0, 0, 0, 0.06);
      transform: scale(1.002) translateY(-3px);
    }

    @keyframes cardFadeIn {
      0% { opacity: 0; transform: translateY(20px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    .card:nth-of-type(1) { animation-delay: 0.03s; }
    .card:nth-of-type(2) { animation-delay: 0.1s; }
    .card:nth-of-type(3) { animation-delay: 0.17s; }
    .card:nth-of-type(4) { animation-delay: 0.24s; }
    .card:nth-of-type(5) { animation-delay: 0.31s; }
    .card:nth-of-type(6) { animation-delay: 0.38s; }

    /* Картинки продуктов */
    .card-img {
      width: 100%;
      height: 170px;
      object-fit: cover;
      border-radius: 18px;
      margin-bottom: 18px;
      background-color: #e9e9ef;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }

    .card-header {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 8px;
    }

    .vitamin-name {
      font-family: "Inter", sans-serif;
      font-weight: 650;
      font-size: 26px;
      letter-spacing: -0.5px;
      color: #1c1c1e;
    }

    .vitamin-sub {
      font-family: "Inter", sans-serif;
      font-weight: 400;
      font-size: 17px;
      color: #8e8e93;
    }

    .desc {
      font-family: "Inter", sans-serif;
      color: #3a3a3c;
      font-size: 15px;
      font-weight: 400;
      margin-bottom: 14px;
    }

    .food-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px 10px;
    }

    .food-tag {
      background: rgba(120, 120, 128, 0.08);
      padding: 8px 16px;
      border-radius: 40px;
      font-family: "Inter", sans-serif;
      font-weight: 500;
      font-size: 15px;
      color: #1c1c1e;
      backdrop-filter: blur(5px);
      -webkit-backdrop-filter: blur(5px);
      border: 0.5px solid rgba(60, 60, 67, 0.06);
      transition: background 0.2s;
    }

    .food-tag:hover {
      background: rgba(100, 100, 110, 0.14);
    }

    .footer-note {
      text-align: center;
      margin-top: 32px;
      font-family: "Inter", sans-serif;
      font-weight: 400;
      font-size: 14px;
      color: #8e8e93;
      letter-spacing: 0.2px;
    }

    @media (max-width: 480px) {
      .container { padding: 16px 12px; }
      .hero h1 { font-size: 32px; }
      .card-img { height: 150px; }
    }
  </style>
</head>
<body>
<div class="container">
  <div class="hero">
    <div class="eyebrow">питание · польза</div>
    <h1>Витамины<br><span>в продуктах</span></h1>
  </div>

  <!-- Карточка 1: Витамин A -->
  <div class="card">
    <img class="card-img" src="https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Морковь и овощи" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин A</span>
      <span class="vitamin-sub">ретинол</span>
    </div>
    <div class="desc">Для зрения, кожи и иммунитета. Лучше усваивается с жирами.</div>
    <div class="food-list">
      <span class="food-tag">🥕 Морковь</span>
      <span class="food-tag">🍠 Батат</span>
      <span class="food-tag">🥬 Шпинат</span>
      <span class="food-tag">🧈 Печень</span>
      <span class="food-tag">🥚 Яйца</span>
    </div>
  </div>

  <!-- Карточка 2: Витамин C -->
  <div class="card">
    <img class="card-img" src="https://images.pexels.com/photos/209555/pexels-photo-209555.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Цитрусовые и киви" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин C</span>
      <span class="vitamin-sub">аскорбиновая</span>
    </div>
    <div class="desc">Мощный антиоксидант, поддерживает коллаген и сосуды.</div>
    <div class="food-list">
      <span class="food-tag">🍊 Апельсин</span>
      <span class="food-tag">🥝 Киви</span>
      <span class="food-tag">🍓 Клубника</span>
      <span class="food-tag">🫑 Перец</span>
      <span class="food-tag">🥦 Брокколи</span>
    </div>
  </div>

  <!-- Карточка 3: Витамин D -->
  <div class="card">
    <img class="card-img" src="https://images.pexels.com/photos/4109937/pexels-photo-4109937.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Лосось и рыба" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин D</span>
      <span class="vitamin-sub">кальциферол</span>
    </div>
    <div class="desc">«Солнечный» витамин. Укрепляет кости и иммунитет.</div>
    <div class="food-list">
      <span class="food-tag">🐟 Лосось</span>
      <span class="food-tag">🐠 Скумбрия</span>
      <span class="food-tag">🥫 Печень трески</span>
      <span class="food-tag">🍄 Грибы</span>
      <span class="food-tag">🥛 Молоко</span>
    </div>
  </div>

  <!-- Карточка 4: Витамин E -->
  <div class="card">
    <img class="card-img" src="https://images.pexels.com/photos/5945811/pexels-photo-5945811.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Орехи и авокадо" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин E</span>
      <span class="vitamin-sub">токоферол</span>
    </div>
    <div class="desc">Защищает клетки от старения, важен для кожи.</div>
    <div class="food-list">
      <span class="food-tag">🌰 Миндаль</span>
      <span class="food-tag">🥑 Авокадо</span>
      <span class="food-tag">🌻 Семечки</span>
      <span class="food-tag">🫒 Оливковое масло</span>
      <span class="food-tag">🌿 Шпинат</span>
    </div>
  </div>

  <!-- Карточка 5: Витамин K -->
  <div class="card">
    <img class="card-img" src="https://images.pexels.com/photos/533360/pexels-photo-533360.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Зелень и брокколи" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин K</span>
      <span class="vitamin-sub">филлохинон</span>
    </div>
    <div class="desc">Отвечает за свёртываемость крови и здоровье костей.</div>
    <div class="food-list">
      <span class="food-tag">🥬 Капуста кейл</span>
      <span class="food-tag">🥦 Брокколи</span>
      <span class="food-tag">🌱 Петрушка</span>
      <span class="food-tag">🥗 Шпинат</span>
      <span class="food-tag">🫘 Фасоль</span>
    </div>
  </div>

  <!-- Карточка 6: Витамины группы B -->
  <div class="card">
    <img class="card-img" src="https://images.pexels.com/photos/128420/pexels-photo-128420.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Цельнозерновые и бобовые" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Группа B</span>
      <span class="vitamin-sub">B₁, B₂, B₆, B₁₂</span>
    </div>
    <div class="desc">Энергия, нервная система и обмен веществ.</div>
    <div class="food-list">
      <span class="food-tag">🥩 Мясо</span>
      <span class="food-tag">🥚 Яйца</span>
      <span class="food-tag">🌾 Овсянка</span>
      <span class="food-tag">🫘 Чечевица</span>
      <span class="food-tag">🥛 Молочные</span>
    </div>
  </div>

  <div class="footer-note">
    свежие продукты — источник здоровья
  </div>
</div>
</body>
</html>"""

@app.route('/')
def index():
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
