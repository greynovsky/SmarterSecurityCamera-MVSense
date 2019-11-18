# Author: Andrew Afonso
# Github: https://github.com/andrewbluepiano/SmarterSecurityCamera-MVSense
import requests
import os
import time
import logging
import json
import sys
#pprint used for debugging
#import pprint

def main():
    config = {}
    config["trusted"] = []
#    pp = pprint.PrettyPrinter(indent=4)
    LOG_FILENAME = 'motionData.log'
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename=LOG_FILENAME, format=FORMAT)
    
    if not os.path.isfile('config.json'):
        print("First time?\n Lets get things set up. \n")
        config["apikey"] = input('Enter your API Key: ')
        config["cameraSerial"] = input('Enter the target MV camera\'s serial: ')
        config["networkID"] = input('Enter the target network\'s ID: ')
        print("Enter on-person device's MAC addresses, one per line. Press enter when done.\n")
        while True:
            newtrust = input('MAC: ').lower()
            if newtrust == "":
                break
            else:
                config["trusted"].append(newtrust)
        with open('config.json', 'w') as newConfig:
            json.dump(config, newConfig)
    else:
        configFile = open('config.json', 'r')
        config = json.load(configFile)
#        pp.pprint(config)
        configFile.close()
    
    while 1==1:
        try:
            zones = requests.get( 'https://api.meraki.com/api/v0/devices/' + config["cameraSerial"] + '/camera/analytics/live',
                headers={'x-cisco-meraki-api-key': config["apikey"], 'Accept': 'application/json'}
            )
            
            people = json.loads(zones.text)
            
#            print(zones.url)
#            pp.pprint(people)

            for values in people["zones"]:
                #If a person is detected
                if int(people["zones"][values]["person"]) > 0:
                    wificlientsget = requests.get(
                        'https://api.meraki.com/api/v0/networks/' + config["networkID"] + '/clients',
                        headers={'x-cisco-meraki-api-key': config["apikey"], 'Accept': 'application/json'},
                        params={'timespan' : '1800'}
                    )
                    bluetoothclientsget = requests.get(
                        'https://api.meraki.com/api/v0/networks/' + config["networkID"] + '/bluetoothClients',
                        headers={'x-cisco-meraki-api-key': config["apikey"], 'Accept': 'application/json'},
                        params={'timespan' : '60'}
                    )
                    
                    
                    wifiClients = json.loads(wificlientsget.text)
                    bluetoothClients = json.loads(bluetoothclientsget.text)
                    
#                    print(wificlientsget.url)
#                    print(wificlientsget.text)
#                    pp.pprint(wifiClients)
#                    pp.pprint(bluetoothClients)
                    
                    notify = 1
                    
                    for client in wifiClients:
#                        print(client["mac"])
                        if client["status"] != "Offline" and client["mac"] in config["trusted"]:
#                            pp.pprint(client)
                            notify = 0
                    
                    for client in bluetoothClients:
#                        print(client["mac"])
                        if client["mac"] in config["trusted"]:
#                            pp.pprint(client)
                            notify = 0
                    
                    if notify == 1:
                        logging.warning('Warnable Person Detected')
                        print("Warnable Person Detected")
        except KeyError as e:
            print("Oops, but not really (KeyError): " + str(e))



if __name__ == "__main__":
    main()
