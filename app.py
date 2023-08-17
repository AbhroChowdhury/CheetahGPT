from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redditGPT')
def redditGPT():
    return render_template('redditGPT.html')

@app.route('/youtubeGPT')
def youtubeGPT():
    return render_template('youtubeGPT.html')

@app.route('/wikipediaGPT')
def wikipediaGPT():
    return render_template('wikipediaGPT.html')

@app.route('/csvGPT')
def csvGPT():
    return render_template('csvGPT.html')

@app.route('/documentGPT')
def documentGPT():
    return render_template('documentGPT.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
