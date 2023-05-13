import face_recognition, requests, datetime
from urllib.request import urlretrieve
from numpy import fromstring

class Camera:
    
    def __init__(self, url):
        self.url = url
    
    def capture(self, filename=None):
        filename = filename or  f"face_recon/{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        filename, headers = urlretrieve(f"{self.url}/capture", f"{filename}.jpg")
        return filename
        
    def flash(self, intensity):
        requests.get(f"{self.url}/control?var=lamp&val={intensity}")
        
    def face_compare(self, known_encodings, filename):
        image = face_recognition.load_image_file(filename)
        encoded_image = face_recognition.face_encodings(image)
        if encoded_image:
            for faces in encoded_image:
                result = face_recognition.compare_faces(known_encodings, faces)
                if result: return True
        else: 
            return False
        
    def recognize(self, known_encodings, intensity=50):
        self.flash(intensity)
        filename = self.capture()
        self.flash(0)
        known_encodings = fromstring(known_encodings, sep=",", dtype=float)
        return self.face_compare([known_encodings], filename)
    
if __name__ == "__main__":
    import numpy as np
    import os
    camera = Camera("http://192.168.0.123")
    done = False
    while not done:
        camera.flash(50)
        filename = camera.capture(filename="test")
        camera.flash(0)
        image = face_recognition.load_image_file(filename)
        encoded_image = face_recognition.face_encodings(image)
        resp = input("Confirm this image (Y, y, Yes, yes): ").lower()
        if encoded_image and resp in ["yes", "y"]:
            with open("enc.txt", "w") as file:
                file.write(np.array2string(encoded_image[0], separator=",", max_line_width=float("inf")))
            done = True
        elif resp in ["yes", "y"] and not encoded_image:
            print("No face detected")
            os.remove("test.jpg")
        else:
            print("Picture discarded due to user demand")
            os.remove("test.jpg")