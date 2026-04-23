from flask import Flask

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes, viewport-fit=cover">
  <title>Витамины · Презентация 15 минут</title>
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
      padding: 20px 16px;
    }

    .presentation {
      max-width: 820px;
      margin: 0 auto;
    }

    /* АНИМАЦИИ ПОЯВЛЕНИЯ */
    @keyframes slideFadeIn {
      0% { opacity: 0; transform: translateY(25px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    /* ТИТУЛЬНЫЙ СЛАЙД */
    .title-slide {
      background: rgba(255, 255, 255, 0.82);
      backdrop-filter: blur(30px);
      -webkit-backdrop-filter: blur(30px);
      border-radius: 36px;
      padding: 48px 32px;
      margin-bottom: 24px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.6);
      text-align: center;
      opacity: 0;
      animation: slideFadeIn 0.7s ease forwards;
    }

    .title-slide .topic-label {
      font-size: 15px;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: #007aff;
      margin-bottom: 16px;
    }

    .title-slide h1 {
      font-size: 48px;
      font-weight: 700;
      letter-spacing: -1.2px;
      color: #1c1c1e;
      line-height: 1.15;
      margin-bottom: 16px;
    }

    .title-slide h1 span {
      display: block;
      font-size: 24px;
      font-weight: 400;
      color: #6c6c70;
      margin-top: 8px;
    }

    .title-slide .author {
      margin-top: 40px;
      padding-top: 30px;
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

    /* КАРТОЧКИ-СЛАЙДЫ */
    .slide-card {
      background: rgba(255, 255, 255, 0.78);
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
      border-radius: 28px;
      padding: 28px 24px;
      margin-bottom: 20px;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.5);
      opacity: 0;
      animation: slideFadeIn 0.6s ease forwards;
      transition: box-shadow 0.3s ease;
    }

    .slide-card:nth-child(2) { animation-delay: 0.1s; }
    .slide-card:nth-child(3) { animation-delay: 0.2s; }
    .slide-card:nth-child(4) { animation-delay: 0.3s; }
    .slide-card:nth-child(5) { animation-delay: 0.4s; }
    .slide-card:nth-child(6) { animation-delay: 0.5s; }
    .slide-card:nth-child(7) { animation-delay: 0.6s; }
    .slide-card:nth-child(8) { animation-delay: 0.7s; }
    .slide-card:nth-child(9) { animation-delay: 0.8s; }
    .slide-card:nth-child(10) { animation-delay: 0.9s; }
    .slide-card:nth-child(11) { animation-delay: 1.0s; }

    .slide-card:hover {
      box-shadow: 0 24px 45px rgba(0, 122, 255, 0.08);
    }

    .card-header {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 16px;
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

    /* ИНТЕРАКТИВНЫЕ КАРТОЧКИ-РАСКЛАДУШКИ */
    .interactive-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }

    .flip-item {
      cursor: pointer;
    }

    .flip-image {
      width: 100%;
      aspect-ratio: 1 / 1;
      object-fit: cover;
      border-radius: 20px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .flip-item:hover .flip-image {
      transform: scale(1.02);
      box-shadow: 0 12px 24px rgba(0, 122, 255, 0.12);
    }

    .flip-content {
      max-height: 0;
      opacity: 0;
      overflow: hidden;
      background: rgba(0, 122, 255, 0.04);
      border-radius: 16px;
      margin-top: 8px;
      padding: 0 16px;
      transition: max-height 0.5s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease, padding 0.3s ease, margin 0.3s ease;
      border-left: 3px solid transparent;
    }

    .flip-item.active .flip-content {
      max-height: 500px;
      opacity: 1;
      padding: 16px;
      margin-top: 12px;
      border-left-color: #007aff;
    }

    .flip-content p {
      font-size: 15px;
      color: #3a3a3c;
      margin-bottom: 8px;
    }

    .flip-content ul {
      padding-left: 20px;
      color: #3a3a3c;
      font-size: 14px;
    }

    .flip-content li {
      margin-bottom: 4px;
    }

    .flip-label {
      text-align: center;
      margin-top: 8px;
      font-weight: 500;
      color: #1c1c1e;
      font-size: 16px;
    }

    /* ТАБЛИЦЫ */
    .content-table {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
      font-size: 14px;
    }

    .content-table th {
      text-align: left;
      padding: 12px 8px;
      background: rgba(0, 122, 255, 0.08);
      font-weight: 650;
      border-radius: 12px 12px 0 0;
    }

    .content-table td {
      padding: 12px 8px;
      border-bottom: 1px solid rgba(60, 60, 67, 0.08);
    }

    /* БЛОКИ С ИНФОРМАЦИЕЙ */
    .info-block {
      background: rgba(0, 122, 255, 0.05);
      border-radius: 18px;
      padding: 16px 18px;
      margin-top: 16px;
      border-left: 4px solid #007aff;
    }

    .highlight {
      font-weight: 700;
      color: #007aff;
    }

    .stat-row {
      display: flex;
      gap: 12px;
      margin: 16px 0;
    }

    .stat-item {
      background: white;
      border-radius: 16px;
      padding: 16px;
      flex: 1;
      text-align: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .stat-number {
      font-size: 32px;
      font-weight: 700;
      color: #1c1c1e;
    }

    .stat-label {
      font-size: 13px;
      color: #8e8e93;
      margin-top: 4px;
    }

    .badge {
      display: inline-block;
      background: #007aff;
      color: white;
      font-size: 13px;
      font-weight: 600;
      padding: 4px 12px;
      border-radius: 20px;
      margin-right: 8px;
      margin-bottom: 8px;
    }

    .footer-note {
      text-align: center;
      margin-top: 32px;
      font-size: 14px;
      color: #8e8e93;
      opacity: 0;
      animation: slideFadeIn 0.5s ease 1.5s forwards;
    }

    @media (max-width: 480px) {
      .title-slide { padding: 32px 20px; }
      .title-slide h1 { font-size: 36px; }
      .interactive-grid { grid-template-columns: 1fr 1fr; }
    }
  </style>
</head>
<body>
<div class="presentation">

  <!-- ТИТУЛЬНЫЙ ЛИСТ -->
  <div class="title-slide">
    <div class="topic-label">Презентация · 15 минут</div>
    <h1>Витамины<br><span>от истории до тарелки</span></h1>
    <div class="author">
      <div class="author-name">Турсунбаев Амин</div>
      <div class="teacher-name">Преподаватель: <strong>Вадим Казанбеков</strong></div>
    </div>
    <div style="margin-top: 24px; font-size: 14px; color: #8e8e93;">
      Нажмите на картинки — узнайте больше
    </div>
  </div>

  <!-- СЛАЙД 1: ИСТОРИЯ ОТКРЫТИЯ ВИТАМИНОВ -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">📜 История открытия</span>
      <span class="vitamin-sub">1880-1948</span>
    </div>
    <div style="margin-bottom: 16px; color: #3a3a3c;">
      <p style="margin-bottom: 12px;">В 1880 году русский врач <strong>Николай Лунин</strong> провёл эксперимент: кормил мышей искусственной смесью из белков, жиров, углеводов и минералов. Мыши погибали. Добавление натурального молока спасало их. Лунин сделал вывод: в пище есть «незаменимые факторы питания».</p>
      <p>В 1912 году польский биохимик <strong>Казимир Функ</strong> выделил кристаллы, излечивающие бери-бери, и назвал их «витаминами» (vita — жизнь, amine — азот). К 1948 году были открыты все 13 витаминов.</p>
    </div>
    <div class="interactive-grid">
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Nikolai_Lunin.jpg/440px-Nikolai_Lunin.jpg" alt="Николай Лунин" loading="lazy">
        <div class="flip-label">Николай Лунин</div>
        <div class="flip-content">
          <p><strong>1854-1937</strong> — русский педиатр. В 1880 году в диссертации «О значении неорганических солей для питания животных» доказал существование витаминов за 30 лет до их открытия.</p>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Casimir_Funk_01.jpg/440px-Casimir_Funk_01.jpg" alt="Казимир Функ" loading="lazy">
        <div class="flip-label">Казимир Функ</div>
        <div class="flip-content">
          <p><strong>1884-1967</strong> — польский биохимик. В 1912 году выделил витамин B1 и придумал термин «витамин». Предсказал существование других витаминов.</p>
        </div>
      </div>
    </div>
    <div class="info-block">
      <p><span class="highlight">Нобелевские премии за витамины:</span> 1929 — Христиан Эйкман (B1), 1937 — Альберт Сент-Дьёрдьи (C), 1943 — Хенрик Дам (K).</p>
    </div>
  </div>

  <!-- СЛАЙД 2: ЭКСПЕРИМЕНТЫ И ОПЫТЫ -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">🧪 Эксперименты</span>
      <span class="vitamin-sub">как открывали витамины</span>
    </div>
    <div class="interactive-grid">
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/3683074/pexels-photo-3683074.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Цинга" loading="lazy">
        <div class="flip-label">Цинга и лимоны</div>
        <div class="flip-content">
          <p>В 1747 году шотландский врач <strong>Джеймс Линд</strong> провёл первый клинический эксперимент: разделил 12 моряков с цингой на группы и давал разные добавки. Те, кто получал лимоны и апельсины, выздоравливали за 6 дней.</p>
          <p>Так был найден витамин C, хотя само вещество выделили только в 1928 году.</p>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/3683060/pexels-photo-3683060.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Бери-бери" loading="lazy">
        <div class="flip-label">Бери-бери и рис</div>
        <div class="flip-content">
          <p>В 1897 году голландский врач <strong>Христиан Эйкман</strong> заметил, что куры, которых кормили полированным рисом, заболевали параличом (бери-бери). Добавление рисовых отрубей излечивало их.</p>
          <p>Из отрубей позже выделили витамин B1 (тиамин). Эйкман получил Нобелевскую премию.</p>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Рахит" loading="lazy">
        <div class="flip-label">Рахит и солнце</div>
        <div class="flip-content">
          <p>В 1919 году <strong>Эдвард Мелланби</strong> доказал, что рахит у собак излечивается рыбьим жиром. Позже выяснили, что ультрафиолет также лечит рахит — так открыли витамин D.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- СЛАЙД 3: ЧТО ГДЕ СОДЕРЖИТСЯ — ИНТЕРАКТИВ -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">🥗 Что где содержится</span>
      <span class="vitamin-sub">нажмите на продукты</span>
    </div>
    <div class="interactive-grid">
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Морковь">
        <div class="flip-label">🥕 Морковь</div>
        <div class="flip-content">
          <p><strong>Витамин A:</strong> 835 мкг на 100 г (83% нормы)</p>
          <p><strong>Витамин K:</strong> 13 мкг</p>
          <p><strong>Витамин C:</strong> 6 мг</p>
          <p>Бета-каротин превращается в витамин A только в присутствии жиров.</p>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/209555/pexels-photo-209555.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Апельсин">
        <div class="flip-label">🍊 Апельсин</div>
        <div class="flip-content">
          <p><strong>Витамин C:</strong> 53 мг на 100 г (60% нормы)</p>
          <p><strong>Фолаты (B9):</strong> 30 мкг</p>
          <p><strong>Витамин B1:</strong> 0,09 мг</p>
          <p>Один апельсин содержит почти суточную норму витамина C.</p>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/4109937/pexels-photo-4109937.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Лосось">
        <div class="flip-label">🐟 Лосось</div>
        <div class="flip-content">
          <p><strong>Витамин D:</strong> 11 мкг на 100 г (73% нормы)</p>
          <p><strong>Витамин B12:</strong> 3 мкг (125% нормы)</p>
          <p><strong>Витамин B6:</strong> 0,8 мг</p>
          <p>Дикий лосось содержит в 4 раза больше витамина D, чем фермерский.</p>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/5945811/pexels-photo-5945811.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Миндаль">
        <div class="flip-label">🌰 Миндаль</div>
        <div class="flip-content">
          <p><strong>Витамин E:</strong> 26 мг на 100 г (173% нормы)</p>
          <p><strong>Витамин B2:</strong> 1,1 мг (85% нормы)</p>
          <p><strong>Витамин B7 (биотин):</strong> 50 мкг</p>
          <p>Всего 30 г миндаля покрывают 50% суточной нормы витамина E.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- СЛАЙД 4: ТАБЛИЦА СОДЕРЖАНИЯ ВИТАМИНОВ -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">📊 Таблица содержания</span>
      <span class="vitamin-sub">мг/мкг на 100 г продукта</span>
    </div>
    <table class="content-table">
      <tr><th>Продукт</th><th>Витамин</th><th>Содержание</th><th>% нормы</th></tr>
      <tr><td>Печень говяжья</td><td>A</td><td>9000 мкг</td><td>900%</td></tr>
      <tr><td>Шиповник</td><td>C</td><td>650 мг</td><td>720%</td></tr>
      <tr><td>Петрушка</td><td>K</td><td>1640 мкг</td><td>1366%</td></tr>
      <tr><td>Подсолнечное масло</td><td>E</td><td>44 мг</td><td>293%</td></tr>
      <tr><td>Печень трески</td><td>D</td><td>250 мкг</td><td>1666%</td></tr>
      <tr><td>Чечевица</td><td>B9 (фолаты)</td><td>479 мкг</td><td>120%</td></tr>
      <tr><td>Красный перец</td><td>C</td><td>128 мг</td><td>142%</td></tr>
      <tr><td>Яичный желток</td><td>B12</td><td>2 мкг</td><td>83%</td></tr>
    </table>
    <div class="info-block">
      <p><span class="highlight">Интересно:</span> Печень трески — абсолютный рекордсмен по витамину D (250 мкг/100 г). Достаточно 5 г в день для покрытия суточной нормы.</p>
    </div>
  </div>

  <!-- СЛАЙД 5: ВИТАМИН A -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">🥕 Витамин A (ретинол)</span>
      <span class="vitamin-sub">жирорастворимый</span>
    </div>
    <div class="interactive-grid">
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/143133/pexels-photo-143133.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Морковь">
        <div class="flip-label">Источники</div>
        <div class="flip-content">
          <ul>
            <li>Печень (9000 мкг/100г)</li>
            <li>Морковь (835 мкг)</li>
            <li>Батат (709 мкг)</li>
            <li>Шпинат (469 мкг)</li>
            <li>Сливочное масло (684 мкг)</li>
          </ul>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/3683074/pexels-photo-3683074.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Функции">
        <div class="flip-label">Функции</div>
        <div class="flip-content">
          <ul>
            <li>Зрение (синтез родопсина)</li>
            <li>Иммунитет</li>
            <li>Рост и развитие клеток</li>
            <li>Здоровье кожи и слизистых</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="info-block">
      <p><span class="highlight">Норма:</span> 1 мг (3300 МЕ). Дефицит — куриная слепота. Избыток токсичен (поражение печени). Бета-каротин из растений безопасен.</p>
    </div>
  </div>

  <!-- СЛАЙД 6: ВИТАМИН C -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">🍊 Витамин C (аскорбиновая)</span>
      <span class="vitamin-sub">водорастворимый</span>
    </div>
    <div class="interactive-grid">
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/209555/pexels-photo-209555.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Источники C">
        <div class="flip-label">Источники</div>
        <div class="flip-content">
          <ul>
            <li>Шиповник (650 мг/100г)</li>
            <li>Красный перец (128 мг)</li>
            <li>Киви (93 мг)</li>
            <li>Брокколи (89 мг)</li>
            <li>Апельсин (53 мг)</li>
          </ul>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Эксперимент">
        <div class="flip-label">Эксперимент</div>
        <div class="flip-content">
          <p>Лайнус Полинг (дважды нобелевский лауреат) принимал 3000 мг витамина C ежедневно и прожил 93 года. Он утверждал, что высокие дозы предотвращают простуду и рак.</p>
        </div>
      </div>
    </div>
    <div class="info-block">
      <p><span class="highlight">Норма:</span> 75-90 мг. Курильщикам +35 мг. Разрушается при нагреве. Безопасный предел — 2000 мг.</p>
    </div>
  </div>

  <!-- СЛАЙД 7: ВИТАМИН D -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">☀️ Витамин D (кальциферол)</span>
      <span class="vitamin-sub">жирорастворимый</span>
    </div>
    <div class="interactive-grid">
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/4109937/pexels-photo-4109937.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Лосось">
        <div class="flip-label">Источники</div>
        <div class="flip-content">
          <ul>
            <li>Печень трески (250 мкг)</li>
            <li>Лосось дикий (11 мкг)</li>
            <li>Скумбрия (16 мкг)</li>
            <li>Яичный желток (5 мкг)</li>
            <li>Грибы (облучённые УФ)</li>
          </ul>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/3683060/pexels-photo-3683060.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Солнце">
        <div class="flip-label">Синтез на солнце</div>
        <div class="flip-content">
          <p>15-20 минут на солнце с открытыми руками и лицом дают 10000-20000 МЕ витамина D. В России с октября по март синтез практически отсутствует.</p>
        </div>
      </div>
    </div>
    <div class="info-block">
      <p><span class="highlight">Норма:</span> 15-20 мкг (600-800 МЕ). 80% россиян испытывают дефицит. Безопасный предел — 100 мкг.</p>
    </div>
  </div>

  <!-- СЛАЙД 8: ВИТАМИН E -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">🌰 Витамин E (токоферол)</span>
      <span class="vitamin-sub">жирорастворимый</span>
    </div>
    <div class="interactive-grid">
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/5945811/pexels-photo-5945811.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Орехи">
        <div class="flip-label">Источники</div>
        <div class="flip-content">
          <ul>
            <li>Масло зародышей пшеницы (149 мг)</li>
            <li>Подсолнечное масло (44 мг)</li>
            <li>Миндаль (26 мг)</li>
            <li>Авокадо (2 мг)</li>
            <li>Шпинат (2 мг)</li>
          </ul>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Функции">
        <div class="flip-label">Функции</div>
        <div class="flip-content">
          <ul>
            <li>Мощный антиоксидант</li>
            <li>Защита клеточных мембран</li>
            <li>Здоровье кожи и волос</li>
            <li>Репродуктивная функция</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="info-block">
      <p><span class="highlight">Норма:</span> 15 мг. «Витамин молодости». Безопасный предел — 1000 мг.</p>
    </div>
  </div>

  <!-- СЛАЙД 9: ВИТАМИНЫ ГРУППЫ B -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">⚡ Витамины группы B</span>
      <span class="vitamin-sub">комплекс из 8 витаминов</span>
    </div>
    <table class="content-table">
      <tr><th>Витамин</th><th>Норма</th><th>Основные источники</th></tr>
      <tr><td>B1 (тиамин)</td><td>1,2-2,1 мг</td><td>Свинина, крупы, бобовые</td></tr>
      <tr><td>B2 (рибофлавин)</td><td>1,5-3 мг</td><td>Молоко, яйца, печень</td></tr>
      <tr><td>B3 (ниацин)</td><td>14-20 мг</td><td>Мясо, рыба, арахис</td></tr>
      <tr><td>B5 (пантотеновая)</td><td>5-10 мг</td><td>Печень, яйца, авокадо</td></tr>
      <tr><td>B6 (пиридоксин)</td><td>1,5-3 мг</td><td>Мясо, рыба, бананы</td></tr>
      <tr><td>B7 (биотин)</td><td>30-100 мкг</td><td>Яйца, орехи, соя</td></tr>
      <tr><td>B9 (фолиевая)</td><td>400 мкг</td><td>Зелень, печень, бобовые</td></tr>
      <tr><td>B12 (кобаламин)</td><td>2-3 мкг</td><td>Печень, рыба, яйца, сыр</td></tr>
    </table>
    <div class="info-block">
      <p><span class="highlight">Важно:</span> B12 содержится только в животных продуктах. Веганам необходимы добавки или обогащённые продукты.</p>
    </div>
  </div>

  <!-- СЛАЙД 10: ВИТАМИН K -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">🥬 Витамин K (филлохинон)</span>
      <span class="vitamin-sub">жирорастворимый</span>
    </div>
    <div class="interactive-grid">
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/533360/pexels-photo-533360.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Зелень">
        <div class="flip-label">Источники</div>
        <div class="flip-content">
          <ul>
            <li>Петрушка (1640 мкг)</li>
            <li>Капуста кейл (817 мкг)</li>
            <li>Шпинат (483 мкг)</li>
            <li>Брокколи (102 мкг)</li>
            <li>Соевое масло (183 мкг)</li>
          </ul>
        </div>
      </div>
      <div class="flip-item" onclick="this.classList.toggle('active')">
        <img class="flip-image" src="https://images.pexels.com/photos/3683074/pexels-photo-3683074.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Функции">
        <div class="flip-label">Функции</div>
        <div class="flip-content">
          <ul>
            <li>Свёртывание крови</li>
            <li>Здоровье костей</li>
            <li>Синтез остеокальцина</li>
            <li>Частично синтезируется в кишечнике</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="info-block">
      <p><span class="highlight">Норма:</span> 90-120 мкг. Название от немецкого «Koagulationsvitamin». Людям на антикоагулянтах нужно контролировать потребление.</p>
    </div>
  </div>

  <!-- СЛАЙД 11: ИТОГИ И РЕКОМЕНДАЦИИ -->
  <div class="slide-card">
    <div class="card-header">
      <span class="vitamin-name">✅ Итоги и рекомендации</span>
      <span class="vitamin-sub">как быть здоровым</span>
    </div>
    <div class="stat-row">
      <div class="stat-item">
        <div class="stat-number">5</div>
        <div class="stat-label">порций овощей/фруктов в день</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">13</div>
        <div class="stat-label">незаменимых витаминов</div>
      </div>
    </div>
    <div style="margin: 20px 0;">
      <span class="badge">Разнообразное питание</span>
      <span class="badge">Сезонные продукты</span>
      <span class="badge">Витамин D зимой</span>
      <span class="badge">Меньше термообработки</span>
      <span class="badge">Анализы перед добавками</span>
      <span class="badge">Сочетать жиры с A, D, E, K</span>
    </div>
    <div class="info-block">
      <p>📌 <span class="highlight">Главный вывод:</span> Лучший источник витаминов — разнообразная свежая пища. Добавки нужны только при доказанном дефиците и по назначению врача.</p>
    </div>
  </div>

  <div class="footer-note">
    Презентация 15 минут · Турсунбаев Амин · Вадим Казанбеков
  </div>
</div>

<script>
  // Закрываем другие открытые карточки при открытии новой (опционально)
  document.querySelectorAll('.flip-item').forEach(item => {
    item.addEventListener('click', function(e) {
      // Можно раскомментировать для аккордеон-эффекта
      // document.querySelectorAll('.flip-item').forEach(i => {
      //   if (i !== this) i.classList.remove('active');
      // });
    });
  });
</script>
</body>
</html>"""

@app.route('/')
def index():
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
