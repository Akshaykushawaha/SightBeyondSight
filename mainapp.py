import cohere
import openai
import io
import os

import bs4
import urllib
import requests
import image_extraction
import speech_recognition as sr
# Import the Google Cloud client library
from google.cloud import vision
from google.cloud.vision_v1 import types
# Set up the credentials for the client

openai.api_key = "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"


def extr1(URL):

    #cl = cohere.Client(api_key="oVlWuiwtuqQMzgwC036yy65HjKlBQ3pdgDWd2kQS")

    htmldata = bs4.BeautifulSoup(
        urllib.request.urlopen(URL), features='html.parser')
    soup = htmldata
    data = ''
    data1 = ''
    for data in soup.find_all("p"):
        data1 += data.get_text()

    prompt = (f"Please summarize the following text:\n\n{data1}\n\nSummary:")
    params = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    # Make the API request
    response = openai.Completion.create(**params)

    # Print the summary
    summary = response.choices[0].text.strip()
    #summary = cl.summarize(str(data1))
    print(summary)
    return summary


def extr2(URL):
    img_desc = ""
    count = image_extraction.main(URL)
    # print(count)
    if count != -1:
        for i in range(2):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./analog-memento-378717-70bbf05aff2d.json"
            # Instantiate a client
            client = vision.ImageAnnotatorClient()
            with open(f"./images/z{i+1}.jpg", "rb") as image_file:
                content = image_file.read()
                # Convert the image data to a Vision API readable format
                image = types.Image(content=content)
                # Perform label detection on the image
                res = client.label_detection(image=image)
                labels = res.label_annotations
                # Print the generated labels/descriptions

                label1 = ""
                for label in labels:
                    label1 += label.description + ", "

                prompt = """  
                This program generates a meaningful sentence given the features identified from an image.
                    
                Labels: snow, lake, mountain, tree, blue, sky 
                Sentence: The scene features a mountain range, a blue sky, and clouds in the distance.
                        
                --  
                Labels: plants, person, casual, building
                Sentence:  a person is standing in front of a building, with several potted plants placed nearby dressed in casual clothing and appears to be in a relaxed pose.
                        
                --  
                Labels: red, building, car, street 
                Sentence:  There is a red car parked on the street in front of the building.
                        
                -- 
                Labels:  pasta, wine, fork, table
                Sentence:  The picture displays a plate of pasta, a glass of wine, and a fork on a table.
                        
                -- 
                Labels:  """+label1+"""
                Sentence: """

                # response = cl.generate(
                # model='xlarge',
                #prompt = prompt,
                # max_tokens=100,
                # temperature=0.6,
                # stop_sequences=["--"])

                #sentence = response.generations[0].text
                ######################################################
                params = {
                    "model": "text-davinci-003",
                    "prompt": prompt,
                    "temperature": 0.5,
                    "max_tokens": 60,
                    "top_p": 1,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }

                # Make the API request
                response = openai.Completion.create(**params)

                # Print the summary
                sentence = response.choices[0].text.strip()
                print("\n\nPrinting sentence from image here:\n\n")
                print(sentence)
                img_desc += str(i)+"). "+sentence + "\n\n"
    else:
        img_desc = "0"
    return img_desc


def extr3(summary, user_input, valid):

    print("what is summary ", summary)
    if (valid == 1):
        prompt = (
            f"{summary}\n\nin context to the given paragraph, solve the query :{user_input}")
        params = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 1000,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        # Make the API request
        response = openai.Completion.create(**params)

        # Print the summary
        summary = response.choices[0].text.strip()
        #summary = cl.summarize(str(data1))
        print(summary, "from voice")
        return summary
    if (valid == 0):
        return user_input


# def voice_control(summary, request):
#     # Initialize SpeechRecognition object
#     r = sr.Recognizer()

#     # Get audio from request
#     audio = sr.AudioData(request.data, sample_rate=16000)

#     print("Recognizing...")

#     # Use SpeechRecognition to recognize speech
#     try:
#         print("Recognized try: ")
#         text = r.recognize_google(audio)
#         print(text, "from voice recongnition try")
#         ans = 1
#     except sr.UnknownValueError:
#         text = 'Sorry, I did not understand that.'
#         ans = 0
#     except sr.RequestError:
#         text = 'Sorry, there was an error processing your request.'
#         ans = 0

#     print("going to call extr3")
#     # Return recognized text
#     return extr3(summary, text, ans)

# enter website url
# extr1("https://digit.in")
# extr2("https://digit.in")
# extr3("Digit.in is a popular technology media portal in India that helps users decide what tech products to buy. They do this through testing thousands of products in their two test labs in Noida and Mumbai, providing unbiased buying advice to millions of Indians. Digit is also about leadership and grooming new leaders for the media industry.","what is product testing",1)
