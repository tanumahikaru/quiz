from flask import Flask, render_template, request

import random
import db

app = Flask(__name__)

# レイアウトサンプル
@app.route('/')
def sample_top():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
