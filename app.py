from flask import Flask, render_template, redirect, url_for, Response, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from gtts import gTTS
from datetime import datetime
import shutil
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from mainapp import extr1, extr2, extr3
import pyttsx3
from playsound import playsound
import redis
import speech_recognition as sr

engine = pyttsx3.init("dummy")

app = Flask(__name__)
global voice_summary
voice_summary = ""

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used


class NameForm(FlaskForm):
    name = StringField('', validators=[DataRequired()], render_kw={
                       "placeholder": "Enter the link here", "class": "form-control my-input-field"})
    submit = SubmitField('Submit', render_kw={
                         "class": "btn btn-primary", "onclick": "preloader()"})


# Redis configuration
r = redis.Redis(
    host='redis-17173.c23738.us-east-1-mz.ec2.cloud.rlrcp.com',
    port=17173,
    password='ZEAC3jbH4ka0FYM6qRwFCoJI9zaZ6skx')
DEFAULT_EXPIRATION = 10800  # 3 hours for cache


# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html

    form = NameForm()
    if form.validate_on_submit():
        # print(form.name.data)
        # string and image description is returned here

        if r.get(form.name.data):
            summary = r.get(form.name.data).decode('utf-8')
            img_desc = r.get(form.name.data+"img").decode('utf-8')
            print("From cache")
        else:
            summary = extr1(form.name.data)
            img_desc = extr2(form.name.data)
            r.set(form.name.data, summary, ex=DEFAULT_EXPIRATION)
            r.set(form.name.data+"img", img_desc, ex=DEFAULT_EXPIRATION)
            print("From web")

        with open("summary.txt", "w") as f:
            f.write(summary)

        if img_desc == "0":
            img_desc = "Images could not be extracted from the given link"
        else:
            img_desc = "The images on the webpage are: "+img_desc

        time = datetime.now().strftime("_%H_%M_%S")
        nm = "test"+time+".mp3"

        summary = summary + " " + img_desc + " " + \
            "Now you can ask me questions about the webpage by pressing spacebar once and speaking."

    # saving audio file for summary, to be played on webpage
        gTTS(summary).save("./static/"+"sum.mp3")
        # shutil.move(nm,"./static/"+nm)
        audio_summary = "./static/"+"sum.mp3"

        # saving audio file for image descriptions, to be played on webpage
        gTTS(img_desc).save("./images/"+"img1.mp3")
        # shutil.move(nm,"./static/"+nm)
        audio_img = "./images/"+"img1.mp3"
        # print(audio_img, "from app.py")

        return render_template('index.html', form=form, sum=summary, img=img_desc, audio=audio_summary)
    else:
        return render_template('index.html', form=form)


@app.route('/voice-input', methods=['POST'])
def voice_input():
    # Initialize SpeechRecognition object
    r = sr.Recognizer()
    valid = 0
    text = ""
    form = NameForm()

    print(request.data, "from app.py data")
    # Get audio from request
    audio = sr.AudioData(request.data, sample_rate=16000, sample_width=2)

    print(audio, "from app.py audio")
    # Use SpeechRecognition to recognize speech
    try:
        text = request.data
        valid = 1
    except sr.UnknownValueError:
        text = 'Sorry, I did not understand that.'
        valid = 0
    except sr.RequestError:
        text = 'Sorry, there was an error processing your request.'
        valid = 0

    file = open("summary.txt", "r")
    info = file.read()
    print("voice summary", info)
    text = extr3(info, text, valid)

    print("from app.py text end return", text)

    file.close()
    # Return recognized text
    return text


# keep this as is
if __name__ == '__main__':
    app.run()
