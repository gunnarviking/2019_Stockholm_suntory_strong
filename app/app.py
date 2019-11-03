import os
from flask import Flask
from flask import render_template
from common	import data

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	entries = data.get_entries()
	print(entries)
	return render_template('index.html', entries=entries)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=5002)