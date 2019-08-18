#!/usr/bin/python

from flask import Flask, render_template, redirect, url_for, request
import pyautogui
import webbrowser

app = Flask(__name__)
app.secret_key = "Not Random. Oh Noes"
# It doesn't matter because im not storing passwords or anything

HOME_OPEN_NETFLIX_STRING = "Open Netflix"
HOME_OPEN_HULU_STRING = "Open Hulu"
HOME_OPEN_FILE_STRING = "Open Local File"
HOME_OPEN_YOUTUBE_STRING = "Open Youtube"

CTRLR_REQUEST_FORM_MOUSE = "mouse"
CTRLR_REQUEST_FORM_KEYBOARD = "keyboard"

@app.route('/')
def start():
    return redirect(url_for('home'))


@app.route('/Home', methods=['GET'])
def home():
    return render_template("MainPage.html", openNetflixString=HOME_OPEN_NETFLIX_STRING,
                           openHuluString=HOME_OPEN_HULU_STRING, openFileString=HOME_OPEN_FILE_STRING,
                           openYoutubeString=HOME_OPEN_YOUTUBE_STRING)


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
    else:
        # logic for something
        return redirect(url_for('home'))


@app.route('/MouseAndKeyboardCtrlr', methods=['GET'])
def ctrlr():
    return render_template("MouseAndKeyboardCtrlr.html", reqFormMouse=CTRLR_REQUEST_FORM_MOUSE,
                           reqFormKeyboard=CTRLR_REQUEST_FORM_KEYBOARD)


def ctrlrMouse(mouseRequest):
    duration = 0.2

    if mouseRequest == "^^^":
        pyautogui.move(None, -200, duration=duration)
    elif mouseRequest == "^^":
        pyautogui.move(None, -100, duration=duration)
    elif mouseRequest == "^":
        pyautogui.move(None, -50, duration=duration)
    elif mouseRequest == "v":
        pyautogui.move(None, 50, duration=duration)
    elif mouseRequest == "vv":
        pyautogui.move(None, 100, duration=duration)
    elif mouseRequest == "vvv":
        pyautogui.move(None, 200, duration=duration)
    elif mouseRequest == ">>>":
        pyautogui.move(200, None, duration=duration)
    elif mouseRequest == ">>":
        pyautogui.move(100, None, duration=duration)
    elif mouseRequest == ">":
        pyautogui.move(50, None, duration=duration)
    elif mouseRequest == "<":
        pyautogui.move(-50, None, duration=duration)
    elif mouseRequest == "<<":
        pyautogui.move(-100, None, duration=duration)
    elif mouseRequest == "<<<":
        pyautogui.move(-200, None, duration=duration)
    elif mouseRequest == "Center":
        screenWidth, screenHeight = pyautogui.size()
        pyautogui.moveTo(screenWidth/2, screenHeight/2, duration=duration)
    elif mouseRequest == "0":
        pyautogui.click()
    elif mouseRequest == "Double Click":
        pyautogui.doubleClick()
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
    else:
        return


@app.route('/MouseAndKeyboardCtrlr', methods=['POST'])
def ctrlrPost():
    if CTRLR_REQUEST_FORM_KEYBOARD in request.form:
        ctrlrKeyboard(request.form[CTRLR_REQUEST_FORM_KEYBOARD])
    elif CTRLR_REQUEST_FORM_MOUSE in request.form:
        ctrlrMouse(request.form[CTRLR_REQUEST_FORM_MOUSE])

    return redirect(url_for('ctrlr'))


if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0')