from __future__ import print_function

import os
import re
import sys
import json
regx='CI-[0-9]'
regex=re.compile(regx)
#import api
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            os.pardir
        )
    )

    import apiai


# demo agent acess token: pratik's client tok : 0dd45e4dcd204c8c80490094894daf11  old token : 37b54074655048acbf2ff81fbf39d1a1

CLIENT_ACCESS_TOKEN = '0dd45e4dcd204c8c80490094894daf11'

def create_ticket(info_list):
    import requests


    url = 'https://dev23984.service-now.com/api/now/table/incident'
    user = 'admin'
    pwd = 'Tusharbhatt92'


    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    #info_list=json.loads(info_list)

    response = requests.post(url, auth=(user, pwd), headers=headers,data=json.dumps(info_list))


    if response.status_code != 201:
        #print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        print("\n"+"  your ticket has been generated and your ticket no is  ")
        exit()

    data = response.json()
    #data1=json.dump(data)
    #print(data)

    # with open("test_json.json",'w+') as fout:
    #     fout.write(str(data))


def main():
    info_list={}
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    chat_list=[]
    while True:
        print(u"> ", end=u"")
        user_message = input()

        if user_message == u"exit":
            break

        request = ai.text_request()
        request.query = user_message
        #chat_list.append(user_message)
        #res=request.getresponse()
        #print(type(res))
        response = json.loads(request.getresponse().read().decode('utf-8'))
        #print(type(response))
        # with open('test_jason.json','w+') as fin:
        #     fin.write(str(response))
        #     fin.close()


        #print(response)
        #result = response['result']
        # pram=response['parameters']
        # if pram is not None:
        #     name=(response['intentName'],response['parameter[0]'])
        #
        #

        # action = result.get('action')
        # actionIncomplete = result.get('actionIncomplete', False)
        #
        intent_name = response['result']['metadata']['intentName']
        # print(intent_name)
        if intent_name == 'get_name':
            first_name = response['result']['parameters']['cust_name']
            #print(first_name[0])
            #info_list.append(temp)
            last_name = response['result']['parameters']['last_name']
            #print(type(last_name))
            name=first_name[0]+" "+ last_name[0]
            #print(name)

            info_list['caller_id']=name
        if intent_name == 'Issues':
            temp=response['result']['resolvedQuery']
            info_list["short_description"]=temp.strip()
        if intent_name == 'CIs':
            temp=response['result']['resolvedQuery']
            info_list['cmdb_ci']=temp.strip()

        print(u"< %s" % response['result']['fulfillment']['speech'])

    # print(info_list)
    # print(json.dumps(info_list))
    print("\n\n\n")
    create_ticket(info_list)

if __name__ == '__main__':
    main()