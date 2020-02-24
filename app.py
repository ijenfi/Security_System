from flask import Flask, render_template, redirect, url_for, request
import telepot
from telepot.loop import MessageLoop
from watson_developer_cloud import VisualRecognitionV3
from time import sleep
import time, datetime
import json
from picamera import PiCamera
from ctypes import *

# create the application object



now = datetime.datetime.now()
telegram_bot = telepot.Bot('991598288:AAHKA1sccDKeigCreN_-X64_IFMXl0Ff2VE')

camera = PiCamera()
IMAGE = 'image.jpg'

so_file = "/home/pi/watson/blink.so"
blink = CDLL(so_file)


app = Flask(__name__)

def recognize_image():
    visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey='szq2kcHpQpxh6luBuuY7SNUgSKy_ZhPH9n09WZo5ApaY')
    with open(IMAGE, 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file,
            threshold='0.6',
        classifier_ids='default').get_result()
    result_str = json.dumps(classes, indent=2)
    result_json = json.loads(result_str)

    print(result_str)
    result_classes = result_json["images"][0]["classifiers"][0]["classes"]

    return result_classes

def parse_result(result):
    scores = []
    for item in result:
        score = item["score"]
        image_class = item["class"]
        #print("This is the image class:{}".format(image_class))
        if "color" not in image_class:
            scores.append(score)
    return scores

def get_best_image(result, best_score):
    best_image = None
    for item in result:
        score = item["score"]
        image_class = item["class"]
        if score == best_score:
            best_image = image_class
    return best_image

def call_camera_bot():
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/watson/image.jpg')
    camera.stop_preview()

    json_result = recognize_image()
    scores = parse_result(json_result)
    best_score = max(scores)
    image_result = get_best_image(json_result, best_score)

    message_for_bot = "Looks like some {} is trying to hack your device!".format(image_result)
    return message_for_bot


def action(message):
    hacked = True
    message_for_bot = call_camera_bot()
    chat_id = message['chat']['id']
    command = message['text']
    if command == '/hi':
        telegram_bot.sendMessage(chat_id, text="hi")
    if hacked:
        telegram_bot.sendPhoto(chat_id, photo=open(IMAGE))
        telegram_bot.sendMessage(chat_id, text=message_for_bot)

    #telegram_bot.sendPhoto(chat_id, photo=open(IMAGE))
    
    #print("Received %s" % command)

    response = telegram_bot.getUpdates()
    print(response)


@app.route('/home')
def home():
    return "<h1>The safe will open shortly</h1>"

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != '2020':
            error = 'Invalid Username/Password. A picture of you has been taken to prove your identity !'
            blink.blink(0)

            print(telegram_bot.getMe())

            MessageLoop(telegram_bot, action).run_as_thread()
            print("Up and Running.....")
#            while 1:
#                time.sleep(10)
        else:
            blink.blink(1)
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
