from flask import Flask, request, render_template
from random import randint
app = Flask(__name__)

ch1 = randint (0,10)
ch2 = randint (0,10)
answer = ch1 + ch2


@app.route("/")
def hello():


    return '<form action="/echo" method="GET">'+str(ch1)+'+'+str(ch2)+' = <input name="text"><input type="submit" value="Ответ"></form>'

@app.route("/echo")
def echo():

    x = int(request.args.get('text', ''))
    if x == answer:
        return "Правильный ответ - "+str(answer)+', ваш ответ - ' + request.args.get('text', '')
    else:
        return "Неправильный ответ, правильный ответ - "+str(answer)+', ваш ответ - '  + request.args.get('text', '')


if __name__ == "__main__":
    app.run()