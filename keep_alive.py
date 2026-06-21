import os
from threading import Thread

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Bot ishlayapti! ✅"


def _run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    """Render kabi platformalarda botni 'web service' sifatida
    tirik ushlab turish uchun fon rejimida oddiy http server ishga tushiradi.
    UptimeRobot shu manzilga muntazam so'rov yuborib, botni uxlab
    qolishdan saqlaydi."""
    t = Thread(target=_run)
    t.daemon = True
    t.start()
