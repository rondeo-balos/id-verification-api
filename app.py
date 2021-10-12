from verifyFaces import getFaceVerifiedByAzure
from azureOCR import getAzureOcr
from flask import (Flask, request, jsonify, render_template)
import cv2
import numpy as np
from base64ToJpg import data_uri_to_cv2_img
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



@app.route('/verifyuser', methods = ['GET', 'POST'])
def upload_images():
    if request.method == 'POST':
        passport_image = request.files['passport']
        selfie = request.form.get('selfie')
    try:
        print(passport_image)
        raw_image_passport = cv2.imdecode(np.fromstring(passport_image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        selfie_image = data_uri_to_cv2_img(selfie)
        #raw_image_selfie = cv2.imdecode(np.fromstring(selfie.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        print('\n***EXRACTING DATA FROM PASSPORT...****\n')
        res_dict = {}
        ocr_res = getAzureOcr(raw_image_passport)
        print('\n****VERIFYING FACES...****\n')
        face_verify_res = getFaceVerifiedByAzure(raw_image_passport, selfie_image)
        print('\nVerification is completed, getting the final results...\n')
        res_dict['user_details'] = ocr_res
        if(face_verify_res['isIdentical']):
            myDict = {'message': 'Faces and details are verified', 'status': face_verify_res['isIdentical']}
            print(myDict)
            res_Dict = {'message': 'USER IS VERIFIED', 'status': face_verify_res['isIdentical']}
            
        else:
            myDict = {'message': 'Faces are not verified', 'status': face_verify_res['isIdentical']}
            res_Dict = {'message': 'USER IS NOT VERIFIED', 'status': face_verify_res['isIdentical']}
        res_dict['results_of_face_verfication'] = myDict
        res_dict['final_result'] = res_Dict

        
        return jsonify(res_dict)
        
    except Exception as e:
        json_response = {'status':False, 'message':'Something went wrong, please try again.'}
        print('something went wrong', e)
        return json_response, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, threaded=True, debug=True)