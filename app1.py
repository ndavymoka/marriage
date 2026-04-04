from flask import Flask, render_template_string, request
import csv

app = Flask(__name__)

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
    "roman": "Роман"
}

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400&display=swap" rel="stylesheet">

<style>
body{
margin:0;
font-family:Roboto,sans-serif;
background:url('https://images.pexels.com/photos/5704203/pexels-photo-5704203.jpeg?auto=compress&cs=tinysrgb&w=2000')
center/cover no-repeat fixed;
overflow-x:hidden;
}

body::after{
content:"";
position:fixed;
inset:0;
background:rgba(0,0,0,0.45);
}

.container{
max-width:720px;
margin:auto;
padding:60px 20px;
position:relative;
z-index:2;
}

.card{
background:rgba(255,255,255,0.92);
border-radius:24px;
padding:50px;
text-align:center;
box-shadow:0 25px 60px rgba(0,0,0,0.25);
}

.timer{
display:flex;
justify-content:center;
gap:10px;
margin:20px 0;
}

.box{
background:#fff;
padding:10px;
border-radius:10px;
width:65px;
box-shadow:0 8px 20px rgba(0,0,0,0.1);
}

.button{
margin-top:15px;
background:#5a3e2b;
color:#fff;
border:none;
padding:12px 20px;
border-radius:10px;
cursor:pointer;
width:100%;
}

.colors{
display:flex;
justify-content:center;
gap:8px;
flex-wrap:wrap;
margin-top:10px;
}

.circle{
width:35px;
height:35px;
border-radius:50%;
}

.olive{background:#708238;}
.burgundy{background:#6b0f1a;}
.beige{background:#d6c3a3;}
.brown{background:#5a3e2b;}
.mustard{background:#c2a133;}
.black{background:#111;}

.popup{
position:fixed;
inset:0;
display:flex;
align-items:center;
justify-content:center;
background:rgba(0,0,0,0.6);
opacity:0;
pointer-events:none;
transition:.3s;
z-index:10;
}

.popup.active{
opacity:1;
pointer-events:auto;
}

.popup-content{
background:#fff;
padding:30px;
border-radius:18px;
text-align:center;
max-width:90%;
}

canvas{
position:fixed;
inset:0;
pointer-events:none;
z-index:5;
}
</style>
</head>

<body>

<canvas id="fire"></canvas>

<div class="popup" id="popup">
<div class="popup-content">
🎉 Спасибо, будем рады видеть вас на нашей свадьбе!
</div>
</div>

<div class="container">
<div class="card">

<h1>💍 {{ name }}</h1>
<p>приглашаем вас на нашу свадьбу!</p>

<p><b>22 августа 2026</b></p>

<p><b>Регистрация в ЗАГС:</b> 10:00</p>
<p><b>Сбор гостей:</b> 16:00</p>

<!-- ✅ ТВОЯ ДОБАВЛЕННАЯ СТРОКА -->
<p>
Время между регистрацией и сбором гостей можете использовать с пользой, будем ждать вас в самом лучшем настроении в ресторане!
</p>

<p><b>ЗАГС:</b> г. Белгород, ул. Попова, д.14</p>

<p>
<b>Ресторан:</b> Тоскана<br>
г. Белгород, ул. Парковая, 10<br>
<a href="https://yandex.ru/maps/-/CPfJ4DN9" target="_blank">Открыть карту</a>
</p>

<div class="timer" id="timer"></div>

<p style="font-size:13px;opacity:.8;">
Ваше присутствие — лучший подарок 🤍<br>
С благодарностью примем только денежные подарки.
</p>

<b>Дресс-код</b>
<div class="colors">
<div class="circle olive"></div>
<div class="circle burgundy"></div>
<div class="circle beige"></div>
<div class="circle brown"></div>
<div class="circle mustard"></div>
<div class="circle black"></div>
</div>

</div>
</div>

<script>

const d=new Date("2026-08-22T16:00:00");

setInterval(()=>{
let n=new Date();
let t=d-n;

let dd=Math.floor(t/86400000);
let hh=Math.floor(t/3600000%24);
let mm=Math.floor(t/60000%60);

document.getElementById("timer").innerHTML=
`<div class="box">${dd}<br>д</div>
<div class="box">${hh}<br>ч</div>
<div class="box">${mm}<br>м</div>`;
},1000);

const c=document.getElementById("fire");
const ctx=c.getContext("2d");
c.width=innerWidth;
c.height=innerHeight;

let p=[];

function boom(){
for(let i=0;i<80;i++){
p.push({
x:innerWidth/2,
y:innerHeight/2,
dx:(Math.random()-0.5)*10,
dy:(Math.random()-0.5)*10,
life:60
});
}
}

function anim(){
ctx.clearRect(0,0,c.width,c.height);
p.forEach(a=>{
a.x+=a.dx;
a.y+=a.dy;
a.life--;
ctx.fillRect(a.x,a.y,2,2);
});
p=p.filter(a=>a.life>0);
requestAnimationFrame(anim);
}
anim();

function send(){
let ans=document.querySelector('input[name="ans"]:checked').value;

fetch("/submit/{{ guest_id }}",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({answer:ans})
});

document.getElementById("popup").classList.add("active");
boom();
}

</script>

</body>
</html>
"""

@app.route("/<guest_id>")
def invite(guest_id):
    if guest_id not in guests:
        return "Ошибка"
    return render_template_string(
        HTML,
        name=guests[guest_id],
        guest_id=guest_id
    )

@app.route("/submit/<guest_id>", methods=["POST"])
def submit(guest_id):
    data = request.get_json()
    ans = data.get("answer","")

    with open("responses.csv","a",newline="",encoding="utf-8") as f:
        csv.writer(f).writerow([guests.get(guest_id), ans])

    return "OK"

if __name__=="__main__":
    app.run(debug=True)