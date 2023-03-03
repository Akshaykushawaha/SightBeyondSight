import cohere
import openai
import io
import os

import bs4
import urllib
import requests
import image_extraction

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
            with open(f"./images/images{i+1}.jpg", "rb") as image_file:
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

# enter website url
# extr1("https://digit.in")
# extr2("https://digit.in")
