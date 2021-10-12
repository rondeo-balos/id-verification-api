import cv2
import numpy as np
import base64
from PIL import Image

def data_uri_to_cv2_img(uri):
    print('Converting URI')
    encoded_data = uri.split(',')[1]
    numpy_parsing = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(numpy_parsing, cv2.IMREAD_COLOR)
    print('URI CONVERTED')
    return img

def imge_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    
    bas64Str = data.decode('utf-8')
    print(bas64Str)
    file = open('base64String.txt', "w")
    file.write(bas64Str)
    
    print('Completed')

if __name__ == '__main__':
    '''
    with open('img.txt','r') as file:
        data_uri = file.read()
    img = data_uri_to_cv2_img(data_uri)
    cv2.imshow('frame',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    
    imge_to_base64('/home/ai/Pictures/driverLicense/aliya_front_id.jpg')