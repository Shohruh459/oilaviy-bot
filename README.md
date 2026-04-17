# 🌙 Oilaviy Bilim O'yini — Telegram Bot

بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ

Oilani birlashtiruvchi, ilmga muhabbat uyg'otuvchi islomiy-psixologik quiz bot.

---

## 📁 Fayl tuzilmasi

```
oilaviy_bot/
├── bot.py           ← Asosiy bot (barcha handler'lar)
├── questions.py     ← 50 ta savol banki (3 qatlam)
├── database.py      ← SQLite: ball, statistika, reyting
├── requirements.txt ← Python kutubxonalar
├── Procfile         ← Railway deploy uchun
└── README.md        ← Shu fayl
```

---

## 🚀 Ishga tushirish (Railway)

### 1-qadam — Bot tokeni olish
1. Telegramda [@BotFather](https://t.me/BotFather) ga boring
2. `/newbot` yozing
3. Nomini bering: `Oilaviy Bilim Oyini`
4. Username: `oilaviy_bilim_bot` (yoki boshqa)
5. Token nusxalab oling

### 2-qadam — GitHub'ga yuklash
```bash
git init
git add .
git commit -m "Bismillah — birinchi commit"
git remote add origin https://github.com/SIZNING_USERNAME/oilaviy-bot.git
git push -u origin main
```

### 3-qadam — Railway deploy
1. [railway.app](https://railway.app) ga kiring
2. "New Project" → "Deploy from GitHub"
3. Repozitoriyangizni tanlang
4. **Variables** bo'limiga o'ting:
   ```
   BOT_TOKEN = sizning_tokeningiz
   ```
5. Deploy tugadi! 🎉

---

## 🎮 O'yin imkoniyatlari

| Xususiyat | Holati |
|-----------|--------|
| 50 ta savol | ✅ Tayyor |
| 4 ta kategoriya | ✅ Tayyor |
| 3 qatlam tizimi | ✅ Tayyor |
| Ball tizimi | ✅ Tayyor |
| Reyting (leaderboard) | ✅ Tayyor |
| Shaxsiy statistika | ✅ Tayyor |
| Har savol hadis/oyat | ✅ Tayyor |

---

## 🌱 Kelajakdagi rejalar (2-bosqich)

- [ ] Oilaviy guruh rejimi
- [ ] Haftalik musobaqa
- [ ] Taklif (invite) tizimi
- [ ] 200+ ta savol
- [ ] PostgreSQL (katta baza uchun)
- [ ] Admin panel

---

## 📿 Hadis

> "Ilm izlash har bir musulmonga farzdir"
> — Ibn Moja rivoyati

---

وَتَعَاوَنُوا عَلَى الْبِرِّ وَالتَّقْوَىٰ
*"Yaxshilik va taqvo yo'lida bir-biringizga yordam bering"*
— Al-Ma'ida surasi, 2-oyat
