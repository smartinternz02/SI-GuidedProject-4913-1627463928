# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 16:27:07 2021

@author: hp
"""
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
#importing the inputScript file used to analyze the URL
import inputScript
#Deployment
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "VnVcQSTp2Ao1ylm62iMnaaZ98hn2iBqZkn1sRbJJlaS7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



#load model
app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl', 'rb'))


#Redirects to the page to give the user iput URL.
@app.route('/predict')
def predict():
   return render_template('trial_project_temp.html')

#Fetches the URL given by the URL and passes to inputScript
@app.route('/y_predict',methods=['POST'])
def y_predict():
   '''
   For rendering results on HTML GUI
   '''
   url = request.form['URL']
   checkprediction = inputScript.main(url)
   payload_scoring = {"input_data": [{"field": [['having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL', 'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report', 'Result']], 
                                   "values": checkprediction}]}

   response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a9b8c738-6c18-4f16-90d8-2844868549a3/predictions?version=2021-07-29',
                                     json=payload_scoring, 
                                     headers={'Authorization': 'Bearer ' + mltoken})
   print("Scoring response")
   predict=response_scoring.json()
   print(predict)
   output=predict['predictions'][0]['values'][0][0]
   if(output==1):
       pred="Your are safe!!  This is a Legitimate Website."
       
   else:
       pred="You are on the wrong site. Be cautious!"
   return render_template('trial_project_temp.html', prediction_text='{}'.format(pred),url=url)

#Takes the input parameters fetched from the URL by inputScript and returns the predictions
@app.route('/predict_api',methods=['POST'])
def predict_api():
   '''
   For direct API calls trought request
   '''
   data = request.get_json(force=True)
   prediction = model.y_predict([np.array(list(data.values()))])

   output = prediction[0]
   return jsonify(output)

if __name__ == "__main__":
   app.run(debug=True)

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)