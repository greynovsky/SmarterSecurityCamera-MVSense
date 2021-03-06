# SmarterSecurityCamera-MVSense
A proof of concept program for filtering person detection data from the MVSense API on Meraki smart security cameras. Intended for setups with one main camera to observe.

By remembering a few network / bluetooth devices that you usually take with you when you leave the house, the program can check if you are likely home or not when it sees a 'person'

This program works with the "person detection" feature available in the MVSense API. A similar functionality could be accomplished using a webhooks endpoint, but this implementation eliminates the need for any third party services. 

## Setup
The program will guide you through setup, but you need to do a few things first:
1. Enable Meraki API access, store your api key somewhere safe.  https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API
2. Enable MVSense for the target camera. Record the cameras serial. (If your camera supports MVSense, you should have 10 free licenses.)
3. Run monitorMV.py

## Output
The program simply writes to a .log file, 'motionData.log', when a person is detected, and it determines you are away from home. The main purpose of the program is to provide the actual filtering of data in such a way that allows the end user to take whatever actions they may want using the data. <br><br>


## Future plans
* A different version of this idea implemented with a GUI and Webhooks for overall motion detection from dashboard. 
- I did this! https://github.com/andrewbluepiano/SmarterMVMotionWebhookAlerts
