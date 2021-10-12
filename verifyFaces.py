#from deepface import DeepFace
import cv2
import http.client, urllib.request, urllib.parse, urllib.error, base64
from requests import get, post
import json 


def verifyImages(img1, img2):
    '''
    processed_img_card = apply_preprocessing(img1)
    print('\nVerifying the faces..')
    results = DeepFace.verify(processed_img_card, img2, model_name='VGG-Face', distance_metric='euclidean_l2')
    print("IsVerified: ", results["verified"])
    return results["verified"]
    '''
    return None
'''
def verifyImagesWithMultipleModels(img1, img2):
    res_list = []
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace"]
    for model in models:
        result = DeepFace.verify(img1, img2, model_name = model, distance_metric='euclidean_l2')
        res_list.append(result)
        res_list.append('\n')

    for res in res_list:
        print(res)
'''    

   
def getAzureFaceID(img1, img2):
    #read data from saved image
    print('Initializing Azure Model..')
    '''
    with open(img1, "rb") as f:
        data_bytes_1 = f.read()
    
    with open(img2, "rb") as f:
        data_bytes_2 = f.read()
    '''

    endpoint = "https://verify-faces-uk.cognitiveservices.azure.com"
    apim_key = "9b7fa1de28344b1ba7460e680fae0e80"
    post_url = endpoint + "/face/v1.0/detect"

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': apim_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
    })

    try:
        final_resp = []
        print('\nProcessing images..')
        resp_img1 = post(url = post_url, data = img1, headers = headers, params = params)
        resp_img2 = post(url = post_url, data = img2, headers = headers, params = params)
        if (resp_img1.status_code != 200) or (resp_img2.status_code != 200):
            print("POST analyze failed here:\n%s" % resp_img1.text)
            return None, None
        #print("POST analyze succeeded:\n%s" % resp_img1.headers)
        get_face_id_1 = json.loads(resp_img1.text)
        get_face_id_2  = json.loads(resp_img2.text)
        return get_face_id_1[0]['faceId'], get_face_id_2[0]['faceId']
        #final_resp = extractText(get_url, source) #demotest
    except Exception as e:
        print("POST analyze failed:", e)
        return None, None

def getFaceVerifiedByAzure(front_img, selfie):
    try:
        img1 = cv2.imencode('.jpg', front_img)[1].tobytes()
        img2 = cv2.imencode('.jpg', selfie)[1].tobytes()
        id1, id2 = getAzureFaceID(img1, img2)
        if(id1 != None):
            
            endpoint = "https://verify-faces-uk.cognitiveservices.azure.com"
            apim_key = "9b7fa1de28344b1ba7460e680fae0e80"
            post_url = endpoint + "/face/v1.0/verify"

            headers = {
                # Request headers
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': apim_key,
            }
            
            body = {"faceId1": id1,"faceId2": id2}
            
            try:
                final_resp = []
                print('Matching faces..\n')
                resp = post(url = post_url, json = body, headers = headers)
                #print(resp.status_code)
                if resp.status_code != 200:
                    print("POST analyze failed here:%s" % resp.text)
                    return None
                #print("POST analyze succeeded:\n%s\n" % resp.headers)
                response = json.loads(resp.text)
                return response
                #final_resp = extractText(get_url, source) #demotest
            except Exception as e:
                print("POST analyze failed here:\n", e)
                return None
        else:
            print('Faces are not found..')
            return None
    except:
        return None

if __name__ == '__main__':
    img1_path = '/home/farhan/fiverr/saAbdulHamid/imgs/passport.jpg'
    img2_path = '/home/farhan/fiverr/saAbdulHamid/imgs/selfie.jpg'
    
    front_img = cv2.imread(img1_path)
    selfie = cv2.imread(img2_path)
    results = getFaceVerifiedByAzure(front_img, selfie)
    print(results)
    if (results['isIdentical']):
        print('\nFACES ARE VERIFIED!\n')
    else:
        print('\nFACES ARE NOT VERIFIED!\n')
    
    #processed_img_card = apply_preprocessing(front_img)
    #cv2.imwrite('processed.jpg', processed_img)
    #a = verifyImages(front_img, selfie)
    #a = verifyImagesWithMultipleModels(front_img, selfie)
    
    #a = getAzureFaceID(img1)
    #b = getAzureFaceID(img2)
    #print(a)
    #print(b)
    #id1 = '89903d27-126d-4d6b-8a68-4ad4cfe4ce29'
    #id2 = '0ea3a33f-75a9-41c9-8ce8-705ad99c9444'  
    #id1, id2 = getAzureFaceID(img1, img2)  