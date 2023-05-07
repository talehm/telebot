# Telebot

A simple Telegram bot for sending and receiving messages.

## Usage

1. Clone this repository.
2. Create virutal environemnt by `venv\Scripts\activate`.
3. Install the required dependencies: `pip install -r requirements.txt`.
4. Set up a Telegram bot using the [BotFather](https://t.me/botfather).
5. Copy your bot's token and paste it into the `config.py` file.
6. install ngrok on your computer and run  `http ngrok <app_port>` in downloaded folder.
7. copy ngrok public url and paste it into the `bot/bot.py` file. `#WEBHOOK_URL = '<ngrok_public_url>/webhook'`.
9. Connect database.
  - Add local postgres credentials in `webapp/app.py` file. 
  - Initialize database by `flask db init`.
  - Migrate database by `flask db migrate -m "first migration"`.
  - Upgrade database by `flask db upgrade`.
10. Start Bot by `/start` command on your telegram.

## Features

- Send messages to the bot and receive a reply.
- Store messages in a database for later retrieval.
- Support for multiple users and conversations.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue.

## License

This project is licensed under the [MIT License](LICENSE).
