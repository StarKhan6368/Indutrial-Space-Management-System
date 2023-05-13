import face_recognition, requests
from urllib.request import urlretrieve

class Camera:
    
    def __init__(self, url):
        self.url = url
        self.image_file = "image.jpg"
    
    def capture(self):
        urlretrieve(f"{self.url}/capture", "image.jpg")
        
    def flash(self, intensity):
        requests.get(f"{self.url}/control?var=lamp&val={intensity}")
        
    def face_compare(self, known_encodings):
        image = face_recognition.load_image_file(self.image_file)
        encoded_image = face_recognition.face_encodings(image)
        if encoded_image:
            for faces in encoded_image:
                result = face_recognition.compare_faces(known_encodings, faces)
                if result: return True
        else: 
            return False
        
    def recognize(self, known_encodings, intensity=50):
        self.flash(intensity)
        self.capture()
        self.flash(0)
        return self.face_compare(known_encodings)
    
if __name__ == "__main__":
    import numpy as np
    camera = Camera("http://192.168.0.123")
    camera.flash(50)
    camera.capture()
    camera.flash(0)
    image = face_recognition.load_image_file("image.jpg")
    encoded_image = face_recognition.face_encodings(image)
    print(encoded_image)
    if encoded_image and input() in ["yes", "y", "Y"]:
        with open("enc.txt", "w") as file:
            file.write(np.array2string(encoded_image[0], separator=",", max_line_width=float("inf")))