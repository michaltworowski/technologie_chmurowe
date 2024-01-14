import cv2
import os
import requests
from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

app = Flask(__name__)
api = Api(app)


class PeopleCounterStatic(Resource):
    def get(self):
        # load image
        image = cv2.imread('grupa_osob.jpg')
        image = cv2.resize(image, (700, 400))

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        return {'peopleCount': len(rects)}


class PeopleCounterDynamicUrl(Resource):
    def get(self):
        url = request.args.get('url')
        # This statement requests the resource at the given link, extracts its contents and saves it in a variable
        data = requests.get(url).content

        # Opening a new file named img with extension .jpg This file would store the data of the image file
        f = open('img.jpg','wb')

        # Storing the image data inside the data variable to the file
        f.write(data)
        f.close()

        image = cv2.imread('img.jpg')
        image = cv2.resize(image, (700, 400))

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        return {'people count dynamic from url': len(rects)}


class PeopleCounterDynamicForm(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('form.html'),200, headers)

    @app.route('/success', methods = ['POST'])
    def post(self):
        headers = {'Content-Type': 'text/html'}
        f = request.files['file']
        f.save(f.filename)
        try:
            os.rename(f.filename, 'img.jpg')
        except WindowsError:
            os.remove('img.jpg')
            os.rename(f.filename, 'img.jpg')

        image = cv2.imread('img.jpg')
        image = cv2.resize(image, (700, 400))

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        return {'people count dynamic from url': len(rects)}

api.add_resource(PeopleCounterStatic, '/')
api.add_resource(PeopleCounterDynamicUrl, '/dynamic')
api.add_resource(PeopleCounterDynamicForm, '/form')

if __name__ == '__main__':
    app.run(debug=True)
