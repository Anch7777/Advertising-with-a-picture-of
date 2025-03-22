from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def mission_title():
    return "Миссия Колонизация Марса"


@app.route('/index')
def mission_slogan():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    promotion_text = """
    Человечество вырастает из детства.<br>
    Человечеству мала одна планета.<br>
    Мы сделаем обитаемыми безжизненные пока планеты.<br>
    И начнем с Марса!<br>
    Присоединяйся!
    """
    return promotion_text


@app.route('/promotion_image')
def promotion_image():
    return render_template('promotion_image.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')