# Telegram Bot Sales Demo

## 🎯 Célkitűzés
Ez egy átfogó Telegram bot demo, amely bemutatja a Telegram botok főbb képességeit potenciális ügyfelek számára.

## ✨ Funkciók

### 1. Bemutatkozás és Főmenü
- Üdvözlő üzenet
- Interaktív inline billentyűzet
- Áttekinthető menürendszer

### 2. Média Kezelés
- **Videó küldés**: Demonstrálja a videó megosztás képességét
- **Hang küldés**: Hangfájlok és zene küldése
- **Kép küldés**: Fotók és grafikai elemek megosztása

### 3. Interaktív Funkciók
- **Inline gombok**: Azonnali válaszok és navigáció
- **ConversationHandler**: Többlépcsős beszélgetés (regisztráció)
- **Echo funkció**: Üzenet visszaküldés

### 4. Időzítés
- **Job Queue**: Emlékeztetők és időzített üzenetek
- 30 másodperces demo emlékeztető

### 5. Adatkezelés
- Felhasználói adatok tárolása (user_data)
- Bot szintű statisztikák (bot_data)
- Statisztikák megjelenítése

### 6. Hibaelhárítás
- Komplex error handler
- Logging minden műveletnél

## 🚀 Telepítés

### 1. Python Telegram Bot telepítése
```bash
pip install python-telegram-bot --upgrade
```

### 2. Bot Token megszerzése
1. Keresd meg a @BotFather-t Telegram-on
2. Küld neki: `/newbot`
3. Kövesd az utasításokat
4. Másold le a kapott tokent

### 3. Token beállítása
Nyisd meg a `telegram_bot_demo.py` fájlt és cseréld le:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

A saját bot tokenedre.

## ▶️ Indítás

```bash
python telegram_bot_demo.py
```

## 📋 Használat

### Alapvető Parancsok
- `/start` - Bot indítása és főmenü megnyitása
- `/help` - Elérhető parancsok listája
- `/regisztracio` - Interaktív regisztráció indítása
- `/cancel` - Regisztráció megszakítása
- `/info` - Bot és felhasználói információk

### Demo Flow
1. **Indítsd el a botot** a `/start` paranccsal
2. **Navigálj a menüben** az inline gombok segítségével:
   - Próbáld ki a videó/hang küldést
   - Nézd meg a statisztikákat
   - Állíts be emlékeztetőt
   - Olvasd el az információkat
3. **Kezdj regisztrációt** a `/regisztracio` paranccsal
4. **Írj bármit** a botnak - visszaküldi echo funkcióként

## 🎨 Demo Prezentáció Tippek

### Sales Szemszögből
1. **Kezdd a főmenüvel**: Mutasd meg a tiszta, professzionális felületet
2. **Demonstráld a gombokat**: Kattints végig az opciókon
3. **Futtasd a regisztrációt**: Mutasd meg a többlépcsős folyamatot
4. **Állíts be emlékeztetőt**: Várj 30 másodpercet a demo alatt
5. **Mutasd a statisztikákat**: Demonstráld az adatkezelést

### Kiemelhető Előnyök
- ✅ Gyors válaszidő
- ✅ Felhasználóbarát interface
- ✅ Gazdag média támogatás
- ✅ Intelligens beszélgetéskezelés
- ✅ Automatizálható folyamatok
- ✅ Skálázható architektúra

## 🔧 Testreszabás

### Videó/Hang Hozzáadása
Ha valódi médiát szeretnél küldeni, a callback funkcióban cseréld le:

```python
# Videónál:
await context.bot.send_video(
    chat_id=query.message.chat_id, 
    video="VIDEO_FILE_ID_VAGY_URL"
)

# Hangnál:
await context.bot.send_audio(
    chat_id=query.message.chat_id, 
    audio="AUDIO_FILE_ID_VAGY_URL"
)
```

### További Funkciók
- Képek küldése: `send_photo()`
- Dokumentumok: `send_document()`
- Helyszín: `send_location()`
- Kontakt: `send_contact()`

## 📊 Technikai Részletek

- **Framework**: python-telegram-bot v22.5+
- **Async/Await**: Teljes aszinkron működés
- **Handler típusok**: CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler
- **Job Queue**: Időzített feladatok
- **Context adatok**: user_data, bot_data
- **Error handling**: Komplex hibakezelés

## 🤝 Bővítési Lehetőségek

A demo könnyen bővíthető:
- Adatbázis integráció
- API kapcsolatok
- Webhook működés
- Admin funkciók
- Fizetési integráció
- Ütemezett hírlevelek
- Chatbot AI integráció

## 📝 Megjegyzések

- A bot token SOHA ne kerüljön verziókezelőbe!
- Használj környezeti változókat production környezetben
- A demo egyszerűsített - éles környezetben bővebb hibakezelés szükséges