#!/usr/bin/python

from flask import Flask, render_template, redirect, url_for, request
import pyautogui  # import move, moveTo, click, doubleClick, press, hotkey, size
import webbrowser
from subprocess import PIPE, Popen
import sys
import html

app = Flask(__name__)
app.secret_key = "Not Random. Oh Noes"
# It doesn't matter because im not storing passwords or anything

HOME_OPEN_NETFLIX_STRING = "Open Netflix"
HOME_OPEN_HULU_STRING = "Open Hulu"
HOME_OPEN_FILE_STRING = "Open Local File"
HOME_OPEN_YOUTUBE_STRING = "Open Youtube"
HOME_OPEN_URL_STRING = "Open URL"

CTRLR_REQUEST_FORM_MOUSE = "mouse"
CTRLR_REQUEST_FORM_KEYBOARD = "keyboard"
CTRLR_REQUEST_FORM_TYPE = "type"

TYPE_INPUT_BOX_NAME = "typeInputBox"

MOUSE_MOVE_LARGE = 400
MOUSE_MOVE_MEDIUM = 100
MOUSE_MOVE_SMALL = 25


def getCPUTemp():
    if sys.platform == "linux":
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        output, _error = process.communicate()
        return float(output[output.index('=') + 1:output.rindex("'")])
    else:
        return 53.2  # test


def getCPUData():
    cpuTemp = getCPUTemp()

    if cpuTemp >= 50:
        cpuOverHeat = "True"
    else:
        cpuOverHeat = "False"

    cpuOverHeatMsg = "The CPU temp is at " + str(cpuTemp) + " C. This is very hot."

    return cpuOverHeat, cpuOverHeatMsg


@app.route('/')
def start():
    return redirect(url_for('home'))


@app.route('/Home', methods=['GET'])
def home():
    cpuOverHeat, cpuOverHeatMsg = getCPUData()
    return render_template("MainPage.html", openNetflixString=HOME_OPEN_NETFLIX_STRING,
                           openHuluString=HOME_OPEN_HULU_STRING, openFileString=HOME_OPEN_FILE_STRING,
                           openYoutubeString=HOME_OPEN_YOUTUBE_STRING, cpuOverHeat=cpuOverHeat,
                           cpuOverHeatMsg=cpuOverHeatMsg, openURLString=HOME_OPEN_URL_STRING)


@app.route('/Home', methods=['POST'])
def homePost():
    if request.form["submit"] == HOME_OPEN_NETFLIX_STRING:
        webbrowser.open('https://www.netflix.com')
        return redirect(url_for('ctrlr'))
    elif request.form["submit"] == HOME_OPEN_HULU_STRING:
        webbrowser.open('https://www.hulu.com')
        return redirect(url_for('ctrlr'))
    elif request.form["submit"] == HOME_OPEN_YOUTUBE_STRING:
        webbrowser.open('https://www.youtube.com')
        return redirect(url_for('ctrlr'))
    elif request.form["submit"] == HOME_OPEN_FILE_STRING:
        # open local files logic
        return redirect(url_for('fileSelecter'))
    elif request.form["submit"] == HOME_OPEN_URL_STRING:
        webbrowser.open(request.form["urlInputBox"])
        return redirect(url_for('ctrlr'))
    else:
        # logic for something
        return redirect(url_for('home'))


@app.route('/MouseAndKeyboardCtrlr', methods=['GET'])
def ctrlr():
    cpuOverHeat, cpuOverHeatMsg = getCPUData()
    return render_template("MouseAndKeyboardCtrlr.html", reqFormMouse=CTRLR_REQUEST_FORM_MOUSE,
                           reqFormKeyboard=CTRLR_REQUEST_FORM_KEYBOARD, typeInputBox=TYPE_INPUT_BOX_NAME,
                           reqFormType=CTRLR_REQUEST_FORM_TYPE, cpuOverHeat=cpuOverHeat,
                           cpuOverHeatMsg=cpuOverHeatMsg)


def ctrlrMouse(mouseRequest):
    duration = 0.2

    if mouseRequest == "^^^":
        pyautogui.move(None, -MOUSE_MOVE_LARGE, duration=duration)
    elif mouseRequest == "^^":
        pyautogui.move(None, -MOUSE_MOVE_MEDIUM, duration=duration)
    elif mouseRequest == "^":
        pyautogui.move(None, -MOUSE_MOVE_SMALL, duration=duration)
    elif mouseRequest == "v":
        pyautogui.move(None, MOUSE_MOVE_SMALL, duration=duration)
    elif mouseRequest == "vv":
        pyautogui.move(None, MOUSE_MOVE_MEDIUM, duration=duration)
    elif mouseRequest == "vvv":
        pyautogui.move(None, MOUSE_MOVE_LARGE, duration=duration)
    elif mouseRequest == ">>>":
        pyautogui.move(MOUSE_MOVE_LARGE, None, duration=duration)
    elif mouseRequest == ">>":
        pyautogui.move(MOUSE_MOVE_MEDIUM, None, duration=duration)
    elif mouseRequest == ">":
        pyautogui.move(MOUSE_MOVE_SMALL, None, duration=duration)
    elif mouseRequest == "<":
        pyautogui.move(-MOUSE_MOVE_SMALL, None, duration=duration)
    elif mouseRequest == "<<":
        pyautogui.move(-MOUSE_MOVE_MEDIUM, None, duration=duration)
    elif mouseRequest == "<<<":
        pyautogui.move(-MOUSE_MOVE_LARGE, None, duration=duration)
    elif mouseRequest == "Center":
        screenWidth, screenHeight = pyautogui.size()
        pyautogui.moveTo(screenWidth/2, screenHeight/2, duration=duration)
    elif mouseRequest == "0":
        pyautogui.click()
    elif mouseRequest == "Double Click":
        pyautogui.doubleClick()
    elif mouseRequest == "Right Click":
        pyautogui.rightClick()
    else:
        return


def ctrlrKeyboard(keyboardRequest):
    if keyboardRequest == "PgDn":
        pyautogui.press('pgdn')
    elif keyboardRequest == "PgUp":
        pyautogui.press('pgup')
    elif keyboardRequest == "Enter":
        pyautogui.press('enter')
    elif keyboardRequest == "Tab":
        pyautogui.press('tab')
    elif keyboardRequest == "Space":
        pyautogui.press('space')
    elif keyboardRequest == "Close":
        pyautogui.hotkey('ctrl', 'w')
    elif keyboardRequest == html.unescape('&uarr;'):  # up arrow
        pyautogui.press('up')
    elif keyboardRequest == html.unescape('&larr;'):
        pyautogui.press('left')
    elif keyboardRequest == html.unescape('&rarr;'):
        pyautogui.press('right')
    elif keyboardRequest == html.unescape('&darr;'):
        pyautogui.press('down')
    elif keyboardRequest == html.unescape('F11'):
        pyautogui.press('f11')
    elif keyboardRequest == html.unescape('F5'):
        pyautogui.press('f5')
    elif keyboardRequest == html.unescape('Esc'):
        pyautogui.press('esc')
    else:
        return


@app.route('/MouseAndKeyboardCtrlr', methods=['POST'])
def ctrlrPost():
    if CTRLR_REQUEST_FORM_KEYBOARD in request.form:
        ctrlrKeyboard(request.form[CTRLR_REQUEST_FORM_KEYBOARD])
    elif CTRLR_REQUEST_FORM_MOUSE in request.form:
        ctrlrMouse(request.form[CTRLR_REQUEST_FORM_MOUSE])
    elif CTRLR_REQUEST_FORM_TYPE in request.form:
        if request.form[CTRLR_REQUEST_FORM_TYPE] == "Type":
            pyautogui.write(request.form[TYPE_INPUT_BOX_NAME])

    return redirect(url_for('ctrlr'))


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0')