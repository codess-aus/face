from io import BytesIO
import os
from PIL import Image, ImageDraw
import requests
from dotenv import load_dotenv

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials

from azure.cognitiveservices.vision.face.models import APIErrorException


#Load the environment variables
load_dotenv()
'''
This example detects faces from 2 different images, then returns information about their facial features.
The features can be set to a variety of properties, see the SDK for all available options.    

Prequisites:
Install the Face SDK: pip install --upgrade azure-cognitiveservices-vision-face

References:
Face SDK: https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-vision-face/?view=azure-python
Face documentation: https://docs.microsoft.com/en-us/azure/cognitive-services/face/
Face API: https://docs.microsoft.com/en-us/azure/cognitive-services/face/apireference
'''

'''
Authenticate the Face service
'''
# This key will serve all examples in this document.
KEY = os.environ["VISION_KEY"]

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ["VISION_ENDPOINT"]

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

'''
Detect face(s) with attributes in a URL image
'''
image_url = "https://cdn.geekwire.com/wp-content/uploads/2014/04/SatyaNadella.jpg"
detected_faces = face_client.face.detect_with_url(
    url=image_url, 
    return_face_id=False, 
    return_face_landmarks=False, 
    recognition_model="recognition_01", 
    detection_model="detection_01"
)

# Image of face(s)
#face1_url = 'https://upload.wikimedia.org/wikipedia/commons/f/f2/Kristofer_Hivju_%28Cropped%2C_2015%29.jpg'
face1_url = 'https://images.prismic.io/wellcomecollection/39c8ff2c560005fd3c0fab625d4ac7ac62d80a6c_tf_190405_3780183.jpg'
face1_name = os.path.basename(face1_url)
#face2_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/The_famous_mustache_and_goatee.jpg/220px-The_famous_mustache_and_goatee.jpg'
face2_url = 'https://i.pinimg.com/originals/33/eb/c3/33ebc3e9183eba0c1f7d5712bd6d41d9.jpg'
face2_name = os.path.basename(face2_url)
face3_url = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/c830bb5f-ac81-4b1c-ba22-ff7992a1e210/d9va57t-4ca427f8-97bc-4ecb-aedd-59e8dddefda7.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi9jODMwYmI1Zi1hYzgxLTRiMWMtYmEyMi1mZjc5OTJhMWUyMTAvZDl2YTU3dC00Y2E0MjdmOC05N2JjLTRlY2ItYWVkZC01OWU4ZGRkZWZkYTcuanBnIn1dXX0.aCQUX7uPxh03F-FJV1rLZRF3Zqr4NHrn_UleObznAlg"
face3_name = os.path.basename(face3_url)
face4_url = "https://img.rasset.ie/001a8615-1500.jpg"
face4_name = os.path.basename(face4_url)

# List of url images
url_images = [face1_url, face2_url, face3_url, face4_url]

# Attributes you want returned with the API call, a list of FaceAttributeType enum (string format)
face_attributes = ['headPose', 'glasses']

try:
    # Your code that makes API requests goes here
    detected_faces = face_client.face.detect_with_url(url=image_url, return_face_attributes=face_attributes)
except APIErrorException as e:
    print(e)

# Detect a face with attributes, returns a list[DetectedFace]
for image in url_images:
    try:
        detected_faces = face_client.face.detect_with_url(
            url=image, 
            return_face_id=True, 
            return_face_landmarks=True, 
            return_face_attributes=face_attributes,
            recognition_model="recognition_01", 
            detection_model="detection_01"
        )
    except APIErrorException as e:
        print(e)
        continue

    if not detected_faces:
        raise Exception(
            'No face detected from image {}'.format(os.path.basename(image)))

    # Rest of your code...

# # Detect a face with attributes, returns a list[DetectedFace]
# for image in url_images:
#     detected_faces = face_client.face.detect_with_url(url=image, return_face_attributes=face_attributes)
#     if not detected_faces:
#         raise Exception(
#             'No face detected from image {}'.format(os.path.basename(image)))

    '''
    Display the detected face with attributes and bounding box
    '''
    # Face IDs are used for comparison to faces (their IDs) detected in other images.
    for face in detected_faces:
        print()
        print('Detected face ID from', os.path.basename(image), ':')
        # ID of detected face
        print(face.face_id)
        # Show all facial attributes from the results
        print()
        #print('Facial attributes detected:')
       # print('Age: ', face.face_attributes.age)
        #print('Gender: ', face.face_attributes.gender)
        print('Head pose: ', face.face_attributes.head_pose)
        #print('Smile: ', face.face_attributes.smile)
        #print('Facial hair: ', face.face_attributes.facial_hair)
        # print('Glasses: ', face.face_attributes.glasses)
        # print('Emotion: ')
        # print('\tAnger: ', face.face_attributes.emotion.anger)
        # print('\tContempt: ', face.face_attributes.emotion.contempt)
        # print('\tDisgust: ', face.face_attributes.emotion.disgust)
        # print('\tFear: ', face.face_attributes.emotion.fear)
        # print('\tHappiness: ', face.face_attributes.emotion.happiness)
        # print('\tNeutral: ', face.face_attributes.emotion.neutral)
        # print('\tSadness: ', face.face_attributes.emotion.sadness)
        # print('\tSurprise: ', face.face_attributes.emotion.surprise)
        # print()

    # Convert width height to a point in a rectangle
    def getRectangle(faceDictionary):
        rect = faceDictionary.face_rectangle
        left = rect.left
        top = rect.top
        right = left + rect.width
        bottom = top + rect.height

        return ((left, top), (right, bottom))

    # Download the image from the url, so can display it in popup/browser
    response = requests.get(image)
    img = Image.open(BytesIO(response.content))

    # For each face returned use the face rectangle and draw a red box.
    print('Drawing rectangle around face... see popup for results.')
    print()
    draw = ImageDraw.Draw(img)
    for face in detected_faces:
        draw.rectangle(getRectangle(face), outline='red')

    # Display the image in the users default image browser.
    img.show()