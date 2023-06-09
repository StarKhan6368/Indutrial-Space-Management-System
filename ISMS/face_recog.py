import face_recognition, requests, datetime
from urllib.request import urlretrieve
import numpy as np

class Camera:
    
    def __init__(self, url):
        self.url = url
    
    def capture(self, filename=None, intensity=50):
        filename = filename or  f"face_recon/{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.flash(intensity)
        filename, headers = urlretrieve(f"{self.url}/capture", f"{filename}.jpg")
        self.flash(0)
        return filename
        
    def flash(self, intensity):
        requests.get(f"{self.url}/control?var=lamp&val={intensity}")
        
    def face_compare(self, known_encodings, filename):
        image = face_recognition.load_image_file(filename)
        encoded_image = face_recognition.face_encodings(image)
        if encoded_image:
            result = face_recognition.compare_faces(known_encodings, encoded_image[0])
            if result: return True, filename
            else: return False, filename
        else:
            print("Face Not Found in the Image...")
            return False, filename
        
    def recognize(self, known_encodings, intensity=50):
        filename = self.capture(intensity=intensity)
        known_encodings = np.fromstring(known_encodings, sep=",", dtype=float)
        return self.face_compare([known_encodings], filename)
    
    def find_and_encode(self, filename: str):
        image = face_recognition.load_image_file(filename)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            encode = np.array2string(encoding[0], separator=",", max_line_width=float("inf"))[1:-1]
            return encode
        else:
            False