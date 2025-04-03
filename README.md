# 🧩 WhatsApp Riddle Game

This is a fun and interactive WhatsApp-based riddle game powered by Twilio Conversations API. Users can receive riddles, ask for hints, and respond — all through WhatsApp.

## ✨ Features

- Twilio WhatsApp integration  
- Riddle engine with multiple riddle types (math, logic, word)  
- Dynamic conversations using the Conversations API  
- Hint system and response feedback  
- Conversation memory via JSON storage  
- Fun ASCII-style messages to enhance experience

## 📦 Tech Stack

- Python 3  
- Twilio Conversations API  
- `.env` for secrets  
- JSON file for tracking riddles and responses  
- `pytest` for unit testing

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/whatsapp_riddle_game.git
cd whatsapp_riddle_game


## Create a new .env File
API_KEY_SID=your_twilio_api_key
API_KEY_SECRET=your_twilio_api_key_secret
ACC_SID=your_account_sid
SVC_ID=your_conversation_service_sid
PERSONAL_NUM=whatsapp:+your_verified_whatsapp_number
MASTERSHOOL_NUM=whatsapp:+your_twilio_whatsapp_number
