from flask import Flask, render_template

app = Flask(__name__)

@app.route('/carousel')
def index():
    images = [
        "img.png",
        "img_1.png",
        "img_2.png"
    ]
    return render_template('index.html', images=images)

if __name__ == '__main__':
    app.run(port=5080, host='127.0.0.1')