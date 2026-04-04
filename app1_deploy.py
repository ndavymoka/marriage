from flask import Flask, render_template_string, request, url_for
import csv
from pathlib import Path

app = Flask(__name__)

HOST = "https://your-domain.onrender.com"
RESPONSES_FILE = Path("responses.csv")

guests = {
    "love-artem": "Артём и Любовь",
    "irina-raisa": "Ирина и Раиса",
    "taras-tatyana": "Тарас и Татьяна",
    "mihail-viktoria": "Михаил и Виктория",
    "daria-serozh": "Дария и Серож",
    "kseniya-matvey": "Ксения и Матвей",
    "viktoria": "Виктория",
    "yulia-ilya": "Юлия и Илья",
    "valeria": "Валерия",
    "vladimir": "Владимир",
    "vladislav-olga": "Владислав и Ольга",
    "nikita1": "Никита",
    "nikita2": "Никита",
    "maksim1": "Максим",
    "maksim2": "Максим",
    "ekaterina": "Екатерина",
    "roman": "Роман",
}

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Приглашение</title>
  <style>
    body { margin:0; font-family:Arial,sans-serif; background:#f4efe8; }
    .container { max-width:720px; margin:0 auto; padding:40px 16px; }
    .card { background:rgba(255,255,255,.95); border-radius:24px; padding:32px; text-align:center; }
    .button { display:inline-block; margin-top:20px; background:#5a3e2b; color:#fff; text-decoration:none; padding:12px 20px; border-radius:10px; }
    .links { margin-top:20px; text-align:left; word-break:break-all; }
    .links a { color:#5a3e2b; }
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>{{ name }}</h1>
      <p><b>22 августа 2026</b></p>
      <p><b>Регистрация в ЗАГС:</b> 10:00</p>
      <p><b>Сбор гостей:</b> 16:00</p>
      <p><b>ЗАГС:</b> г. Белгород, ул. Попова, д.14</p>
      <p><b>Ресторан:</b> Тоскана, г. Белгород, ул. Парковая, 10</p>
      <p>Ваше присутствие — лучший подарок 🤍</p>
    </div>
  </div>
</body>
</html>
"""

@app.route('/')
def home():
    links = [(guestid, name, url_for('invite', guestid=guestid, _external=True)) for guestid, name in guests.items()]
    items = ''.join(f'<li><a href="{u}">{name}</a> — {u}</li>' for guestid, name, u in links)
    return f'<h2>Ссылки для гостей</h2><ul>{items}</ul>'

@app.route('/<guestid>')
def invite(guestid):
    if guestid not in guests:
        return "Not found", 404
    return render_template_string(HTML, name=guests[guestid], guestid=guestid)

@app.route('/submit/<guestid>', methods=['POST'])
def submit(guestid):
    data = request.get_json(silent=True) or {}
    ans = data.get('answer', '')
    RESPONSES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RESPONSES_FILE.open('a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([guests.get(guestid, guestid), ans])
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
