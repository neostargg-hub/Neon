from flask import Flask

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes, viewport-fit=cover">
  <title>Витамины · Презентация</title>
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
      font-family: "Inter", -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
      background: linear-gradient(145deg, #e8e8ed 0%, #f2f2f7 100%);
      color: #1c1c1e;
      line-height: 1.45;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }

    /* Контейнер-слайдер */
    .presentation {
      max-width: 720px;
      width: 100%;
      margin: 0 auto;
    }

    /* Титульный слайд — отдельный стиль */
    .title-slide {
      background: rgba(255, 255, 255, 0.82);
      backdrop-filter: blur(30px);
      -webkit-backdrop-filter: blur(30px);
      border-radius: 36px;
      padding: 48px 32px;
      margin-bottom: 24px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08), 0 4px 14px rgba(0, 0, 0, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.6);
      text-align: center;
      opacity: 0;
      transform: scale(0.96) translateY(10px);
      animation: titleAppear 0.8s cubic-bezier(0.23, 1, 0.32, 1) forwards;
    }

    @keyframes titleAppear {
      0% { opacity: 0; transform: scale(0.96) translateY(10px); }
      100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    .title-slide .topic-label {
      font-size: 15px;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: #8e8e93;
      margin-bottom: 16px;
    }

    .title-slide h1 {
      font-size: 48px;
      font-weight: 700;
      letter-spacing: -1.2px;
      color: #1c1c1e;
      line-height: 1.15;
      margin-bottom: 32px;
    }

    .title-slide h1 span {
      display: block;
      font-size: 28px;
      font-weight: 400;
      color: #6c6c70;
      margin-top: 8px;
    }

    .title-slide .author {
      margin-top: 48px;
      padding-top: 32px;
      border-top: 1px solid rgba(60, 60, 67, 0.1);
    }

    .title-slide .author-name {
      font-size: 22px;
      font-weight: 650;
      color: #1c1c1e;
      margin-bottom: 4px;
    }

    .title-slide .teacher-name {
      font-size: 18px;
      font-weight: 400;
      color: #6c6c70;
    }

    .title-slide .teacher-name strong {
      font-weight: 600;
      color: #1c1c1e;
    }

    /* Карточки-слайды — плавное появление с эффектом перелистывания */
    .slide-card {
      background: rgba(255, 255, 255, 0.78);
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
      border-radius: 28px;
      padding: 28px 24px;
      margin-bottom: 20px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.04), 0 2px 8px rgba(0, 0, 0, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.5);
      transition: transform 0.3s ease, box-shadow 0.3s;
      opacity: 0;
      transform: translateX(-12px) translateY(8px);
      animation: slideFadeIn 0.55s cubic-bezier(0.23, 1, 0.32, 1) forwards;
    }

    @keyframes slideFadeIn {
      0% { opacity: 0; transform: translateX(-12px) translateY(8px); }
      100% { opacity: 1; transform: translateX(0) translateY(0); }
    }

    /* Эффект перелистывания — задержки создают каскад */
    .slide-card:nth-of-type(1) { animation-delay: 0.05s; }
    .slide-card:nth-of-type(2) { animation-delay: 0.12s; }
    .slide-card:nth-of-type(3) { animation-delay: 0.19s; }
    .slide-card:nth-of-type(4) { animation-delay: 0.26s; }
    .slide-card:nth-of-type(5) { animation-delay: 0.33s; }
    .slide-card:nth-of-type(6) { animation-delay: 0.40s; }
    .slide-card:nth-of-type(7) { animation-delay: 0.47s; }
    .slide-card:nth-of-type(8) { animation-delay: 0.54s; }

    .slide-card:hover {
      box-shadow: 0 24px 45px rgba(0, 0, 0, 0.08);
      transform: scale(1.002) translateY(-3px);
    }

    /* Изображения */
    .card-img {
      width: 100%;
      height: 170px;
      object-fit: cover;
      border-radius: 20px;
      margin-bottom: 20px;
      background: #e9e9ef;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
      transition: opacity 0.2s;
    }

    .card-header {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 10px;
    }

    .vitamin-name {
      font-size: 26px;
      font-weight: 650;
      letter-spacing: -0.5px;
      color: #1c1c1e;
    }

    .vitamin-sub {
      font-size: 17px;
      font-weight: 400;
      color: #8e8e93;
    }

    .desc {
      color: #3a3a3c;
      font-size: 15px;
      font-weight: 400;
      margin-bottom: 16px;
      line-height: 1.5;
    }

    .food-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px 10px;
      margin-bottom: 12px;
    }

    .food-tag {
      background: rgba(120, 120, 128, 0.08);
      padding: 8px 16px;
      border-radius: 40px;
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

    /* Блок статистики / информации */
    .info-block {
      background: rgba(0, 122, 255, 0.06);
      border-radius: 18px;
      padding: 16px 18px;
      margin-top: 16px;
      border-left: 4px solid #007aff;
    }

    .info-block p {
      font-size: 15px;
      color: #1c1c1e;
      margin-bottom: 6px;
    }

    .info-block .highlight {
      font-weight: 700;
      color: #007aff;
    }

    .stat-row {
      display: flex;
      justify-content: space-between;
      margin-top: 12px;
      gap: 12px;
    }

    .stat-item {
      background: white;
      border-radius: 16px;
      padding: 12px 14px;
      flex: 1;
      text-align: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .stat-number {
      font-size: 28px;
      font-weight: 700;
      color: #1c1c1e;
    }

    .stat-label {
      font-size: 13px;
      color: #8e8e93;
      margin-top: 4px;
    }

    .world-russia-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin: 16px 0 8px;
    }

    .market-card {
      background: white;
      border-radius: 18px;
      padding: 16px;
    }

    .market-card h4 {
      font-size: 17px;
      font-weight: 650;
      margin-bottom: 8px;
    }

    .market-card .value {
      font-size: 26px;
      font-weight: 700;
      color: #007aff;
    }

    .footer-note {
      text-align: center;
      margin-top: 28px;
      font-size: 14px;
      color: #8e8e93;
      letter-spacing: 0.2px;
      opacity: 0;
      animation: fadeInLate 0.5s ease 0.8s forwards;
    }

    @keyframes fadeInLate {
      to { opacity: 1; }
    }

    @media (max-width: 480px) {
      body { padding: 10px; }
      .title-slide { padding: 32px 20px; }
      .title-slide h1 { font-size: 36px; }
      .card-img { height: 140px; }
      .stat-number { font-size: 22px; }
      .world-russia-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
<div class="presentation">

  <!-- ТИТУЛЬНЫЙ ЛИСТ -->
  <div class="title-slide">
    <div class="topic-label">Презентация</div>
    <h1>Витамины<br><span>в продуктах питания</span></h1>
    <div class="author">
      <div class="author-name">Турсунбаев Амин</div>
      <div class="teacher-name">Преподаватель: <strong>Вадим Казанбеков</strong></div>
    </div>
    <div style="margin-top: 36px; display: flex; justify-content: center; gap: 8px;">
      <span style="background: #007aff; width: 8px; height: 8px; border-radius: 4px;"></span>
      <span style="background: #c6c6c8; width: 8px; height: 8px; border-radius: 4px;"></span>
      <span style="background: #c6c6c8; width: 8px; height: 8px; border-radius: 4px;"></span>
    </div>
  </div>

  <!-- СЛАЙД 2: Мировой рынок витаминов (новая информация) -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">🌍 Мировой рынок</span>
      <span class="vitamin-sub">2024–2029</span>
    </div>
    <div class="desc">
      Глобальный рынок витаминов и добавок активно растёт: в 2024 году его объём составил <strong>$167 млрд</strong>, к 2029 году достигнет <strong>$272 млрд</strong> [citation:3].
    </div>
    <div class="world-russia-grid">
      <div class="market-card">
        <h4>📊 Северная Америка</h4>
        <div class="value">37%</div>
        <div style="font-size: 14px; color: #6c6c70;">крупнейший рынок</div>
      </div>
      <div class="market-card">
        <h4>📈 Азиатско-Тихоокеанский</h4>
        <div class="value">+10.5%</div>
        <div style="font-size: 14px; color: #6c6c70;">самый быстрорастущий [citation:4]</div>
      </div>
    </div>
    <div class="info-block">
      <p><span class="highlight">Тренды:</span> персонализированное питание, ДНК-тесты для подбора витаминов, растительные формулы и clean-label [citation:7].</p>
    </div>
  </div>

  <!-- СЛАЙД 3: Ситуация в России + статистика дефицита -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">🇷🇺 Россия: рынок и дефицит</span>
      <span class="vitamin-sub">2025–2026</span>
    </div>
    <div class="desc">
      Российский рынок БАД в 2025 году — почти <strong>280 млрд руб.</strong>, рост в 5 раз за 10 лет [citation:6].
    </div>
    <div class="stat-row">
      <div class="stat-item">
        <div class="stat-number">70%</div>
        <div class="stat-label">россиян испытывают дефицит витаминов группы B [citation:6]</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">75-85%</div>
        <div class="stat-label">детей с круглогодичной нехваткой витаминов [citation:6]</div>
      </div>
    </div>
    <div class="info-block" style="margin-top: 12px;">
      <p><span class="highlight">Спрос в январе 2026:</span> общее падение на 15%, но витамин E вырос на 23% [citation:2]. Потребители переходят на натуральные источники.</p>
    </div>
  </div>

  <!-- СЛАЙД 4: Витамин A -->
  <div class="slide-card">
    <img class="card-img" src="https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Морковь" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин A</span>
      <span class="vitamin-sub">ретинол</span>
    </div>
    <div class="desc">Суточная норма: 1 мг. Поддерживает зрение, кожу, иммунитет. Дефицит — у 17% детей в России [citation:6].</div>
    <div class="food-list">
      <span class="food-tag">🥕 Морковь</span>
      <span class="food-tag">🍠 Батат</span>
      <span class="food-tag">🥬 Шпинат</span>
      <span class="food-tag">🧈 Печень</span>
      <span class="food-tag">🥚 Яйца</span>
    </div>
  </div>

  <!-- СЛАЙД 5: Витамин C -->
  <div class="slide-card">
    <img class="card-img" src="https://images.pexels.com/photos/209555/pexels-photo-209555.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Цитрусовые" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин C</span>
      <span class="vitamin-sub">аскорбиновая</span>
    </div>
    <div class="desc">Норма: 70-100 мг. Мощный антиоксидант. В январе 2026 спрос на витамин C в России упал на 29% — люди переходят на фрукты [citation:10].</div>
    <div class="food-list">
      <span class="food-tag">🍊 Апельсин</span>
      <span class="food-tag">🥝 Киви</span>
      <span class="food-tag">🍓 Клубника</span>
      <span class="food-tag">🫑 Перец</span>
      <span class="food-tag">🥦 Брокколи</span>
    </div>
  </div>

  <!-- СЛАЙД 6: Витамин D -->
  <div class="slide-card">
    <img class="card-img" src="https://images.pexels.com/photos/4109937/pexels-photo-4109937.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Лосось" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин D</span>
      <span class="vitamin-sub">кальциферол</span>
    </div>
    <div class="desc">Норма: 2.5 мкг. Для костей и иммунитета. ~10% взрослых россиян страдают остеопорозом из-за нехватки D и кальция [citation:6].</div>
    <div class="food-list">
      <span class="food-tag">🐟 Лосось</span>
      <span class="food-tag">🐠 Скумбрия</span>
      <span class="food-tag">🥫 Печень трески</span>
      <span class="food-tag">🍄 Грибы</span>
      <span class="food-tag">🥛 Молоко</span>
    </div>
  </div>

  <!-- СЛАЙД 7: Витамин E -->
  <div class="slide-card">
    <img class="card-img" src="https://images.pexels.com/photos/5945811/pexels-photo-5945811.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Орехи" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Витамин E</span>
      <span class="vitamin-sub">токоферол</span>
    </div>
    <div class="desc">Норма: 12-15 мг. Антиоксидант для кожи и сосудов. Единственный витамин, спрос на который в России вырос (+23%) в 2026 [citation:2].</div>
    <div class="food-list">
      <span class="food-tag">🌰 Миндаль</span>
      <span class="food-tag">🥑 Авокадо</span>
      <span class="food-tag">🌻 Семечки</span>
      <span class="food-tag">🫒 Оливковое масло</span>
      <span class="food-tag">🌿 Шпинат</span>
    </div>
  </div>

  <!-- СЛАЙД 8: Группа B -->
  <div class="slide-card">
    <img class="card-img" src="https://images.pexels.com/photos/128420/pexels-photo-128420.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Зерновые" loading="lazy">
    <div class="card-header">
      <span class="vitamin-name">Группа B</span>
      <span class="vitamin-sub">B₁, B₂, B₆, B₁₂, B₉</span>
    </div>
    <div class="desc">Энергия, нервная система, кроветворение. <strong>До 70% россиян</strong> испытывают дефицит одного или нескольких витаминов группы B [citation:6].</div>
    <div class="food-list">
      <span class="food-tag">🥩 Мясо</span>
      <span class="food-tag">🥚 Яйца</span>
      <span class="food-tag">🌾 Овсянка</span>
      <span class="food-tag">🫘 Чечевица</span>
      <span class="food-tag">🥛 Молочные</span>
    </div>
    <div class="info-block" style="margin-top: 14px;">
      <p>📌 Фолиевая кислота (B₉) особенно важна беременным — 400-600 мкг/сутки. Содержится в зелени, бобовых, печени [citation:5].</p>
    </div>
  </div>

  <div class="footer-note">
    свежие продукты — источник здоровья • данные 2025-2026
  </div>
</div>
</body>
</html>"""

@app.route('/')
def index():
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
