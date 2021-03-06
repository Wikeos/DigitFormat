import requests
import datetime
import json
import credentials as cred
from notifypy import Notify


def postRequest(token, startTime, endTime, slot):

    # Date du jour
    date = str(datetime.datetime.now())[0:10]

    url = "https://app.digiforma.com/api/v1/graphql"
    headers = {'Host': 'app.digiforma.com', 
            'Connection': 'keep-alive', 
            'accept': '*/*',
            'content-type': 'application/json',
            'authorization': 'Bearer ' + token,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://cefim.digiforma.net',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://cefim.digiforma.net/',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Length': '20561'}
    data = json.dumps({"operationName" : "sign_one_attendance",
    "query" : "mutation sign_one_attendance($id: ID!, $date: TrainingSessionDateInput!, $signature: String!, $on_behalf: ID) {\n  sign_one_attendance(id: $id, date: $date, signature: $signature, on_behalf: $on_behalf)\n}\n",
    "variables" : {
    "date" : {
            "date" : date,
            "end_time" : endTime,
            "slot" : slot,
            "start_time" : startTime
            },
    "id" : cred.idUtilisateur,
    "on_behalf" : None,
    "signature" : cred.signature}})

    results = requests.post(url=url, data=data, headers=headers)
    print(results.text)
    if(results.text.find('{"sign_one_attendance":true}') != -1): 
        notification.message = "L'émargement a bien été signé"
    else:
        notification.icon = "utils/wrong.png"
        notification.message = "Echec de la signature"
    notification.send()


# DEBUT DU SCRIPT
notification = Notify()
notification.title = "DigiFormat"
notification.icon = "utils/notification.png"

# Date du jour
heure = int(str(datetime.datetime.now())[11:13])
if(heure < 14):
    startTime = "09:00:00"
    endTime = "12:30:00"
    slot = "morning"
else:
    startTime = "14:00:00"
    endTime = "17:30:00"
    slot = "afternoon"

# Requête POST
postRequest(cred.token, startTime, endTime, slot)