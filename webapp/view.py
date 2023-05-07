@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://027a-84-134-18-115.ngrok-free.app/' + TOKEN)
    return "!", 200