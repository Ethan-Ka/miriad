from flask import Flask
from threading import Thread

app = Flask('')

lobster_bot_website = "<center><a href='https://example.com'>myriad bot website</a></center>"



@app.route('/')
def main():
    return lobster_bot_website

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
