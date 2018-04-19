from flask import Flask, render_template, session, redirect, url_for, request
from flask import Flask
from flask_bootstrap import Bootstrap
import explorer

app = Flask(__name__)
bootstrap = Bootstrap(app)

data = explorer.foods

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
	return render_template('menu.html')

@app.route('/rate/<int:ind>')
def rate(ind):
	#ind is the index (list of JSON documents)
	this_food = data[ind]
	return render_template('rate.html', food=this_food)

@app.route('/view_ratings')
def view_ratings():
	return render_template('view_ratings.html')

@app.route('/training') #Button to train a model
def train():
	return render_template('index.html')

if __name__ =='__main__':
	app.config.update(
		DEBUG = True,
		TEMPLATES_AUTO_RELOAD=True
		)
	app.run(port=8000)