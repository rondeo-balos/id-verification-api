import json
import time
import sys
import io
from io import BytesIO
import cv2
from requests import get, post
from PIL import Image, ImageDraw, ImageFont


def parse_response(response):
    res_dict = {}
    for key, value in response.items():
        for k,v in value.items():
            if 'value' in k:
                res_dict[key] = v
    
    return res_dict

def getConfidenceScore(wds):
	score = 0
	for w in wds:
		score = score+ w['confidence']
	avg = score/len(wds)
	#print("AVERAGE {}".format(avg))
	return avg
	

def getAzureOcr(image):
	# Endpoint URL
	endpoint = r"https://ocr-id-verification.cognitiveservices.azure.com/"
	apim_key = "dc7dd77aecf34a08ba66718e2c954317"
	post_url = endpoint + "formrecognizer/v2.1/prebuilt/idDocument/analyze"
	#source = r"/home/ai/plastkRepos/ocr/demoWebApp/receipts/teaetc.jpg"
	get_url = None

	headers = {
	# Request headers
	'Content-Type': 'image/jpeg',
	'Ocp-Apim-Subscription-Key': apim_key,
	}

	params = {
	"includeTextDetails": True
	}
	pil_im = Image.fromarray(image)
	stream = io.BytesIO()
	pil_im.save(stream, 'jpeg')	
	#image=Image.open(stream)
	data_bytes = stream.getvalue()	


	try:
		resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
		if resp.status_code != 202:
			print("POST analyze failed:\n%s" % resp.text)
			quit()
		print("POST analyze succeeded:\n")
		print(resp.text)
		get_url = resp.headers["operation-location"]
	except Exception as e:
		print("POST analyze failed:\n%s" % str(e))
		quit()

	print("Moving ahead..")
	print(get_url)
	#Analyze the receipt from retrieved URL
	n_tries = 10
	n_try = 0
	wait_sec = 6
	resp_json = None
	while n_try < n_tries:
		try:
			resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
			resp_json = json.loads(resp.text)
			if resp.status_code != 200:
				print("GET Receipt results failed:\n%s" % resp_json.read)
				quit()
			status = resp_json["status"]
			print(status)
			if status == "succeeded":
				#print("Receipt Analysis succeeded:\n%s" % resp_json)
				print('Got the response!')
				break
			if status == "failed":
				print("Analysis failed:\n%s" % resp_json)
				quit()
			# Analysis still running. Wait and retry.
			time.sleep(wait_sec)
			n_try += 1     
		except Exception as e:
			msg = "GET analyze results failed:\n%s" % str(e)
			print(msg)
			quit()
   
	fields = resp_json['analyzeResult']['documentResults'][0]['fields']['MachineReadableZone']['valueObject']
	parsed_res = parse_response(fields)
	return parsed_res

	'''
	lines = resp_json['analyzeResult']['readResults'][0]['lines']
	#print(lines)
	res_list = []
	overall_scores = 0
	count = 0

	for line in lines:
		words = line['words']
		score = getConfidenceScore(words)*100
		if score < 80:
			count = count+1
		overall_scores = overall_scores + score
		res_list.append(line['text'])
		#res_list.append(line['text']+"  {:.2f}".format(score)+"%")
	print(res_list)
	accuracy = overall_scores/len(lines)
	return res_list, accuracy, count
	'''
 
 
if __name__ == '__main__':
	img1_path = '/home/farhan/fiverr/saAbdulHamid/imgs/test2.jpg'
	img = cv2.imread(img1_path)
	#results, accuracy, count = getAzureOcr(img)
	res = getAzureOcr(img)	
	print (res)
	
