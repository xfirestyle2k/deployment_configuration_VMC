import requests                         # need this for Get/Post/Delete
import configparser                     # parsing config file
import time
import sys
from prettytable import PrettyTable

config = configparser.ConfigParser()
config.read("./config.ini")
strProdURL      = config.get("vmcConfig", "strProdURL")
strCSPProdURL   = config.get("vmcConfig", "strCSPProdURL")
Refresh_Token   = config.get("vmcConfig", "refresh_Token")
ORG_ID          = config.get("vmcConfig", "org_id")
SDDC_ID         = config.get("vmcConfig", "sddc_id")

DEBUG_MODE = True

REFRESH_TOKEN = ''

CSP_URL='https://console.cloud.vmware.com'
VMC_URL='https://vmc.vmware.com'

params = {'refresh_token': REFRESH_TOKEN}
if DEBUG_MODE:
    print ('Params:\n',json.dumps(params))

headers = {'Content-Type': 'application/json'}
if DEBUG_MODE:
    print ('Headers:\n',json.dumps(headers))

url = CSP_URL + '/csp/gateway/am/api/auth/api-tokens/authorize'
if DEBUG_MODE:
    print('Token Auth URL:',url)
    input('\n\nPress any key to continue')

response = requests.post(url,params=params,headers=headers)
jsonResponse = response.json()
if DEBUG_MODE:
    print('\nRaw token JSON:\n',jsonResponse)
    print ('\nFormatted token JSON:\n',json.dumps(jsonResponse,indent=1),'\n\n')
    input('\n\nPress any key to continue')


# Extract the access_token from the JSON into a variable
access_token = jsonResponse['access_token']
if DEBUG_MODE:
    print('\nExtracted access token:', access_token)

# Build the URL to list organizations
url = VMC_URL + '/vmc/api/orgs'
if DEBUG_MODE:
    print('\nOrg list URL:',url)

# Build the headers for the GET request - we're using JSON, we pass the content type and the access token
org_list_headers =  {'Content-Type': 'application/json','csp-auth-token':access_token}
if DEBUG_MODE:
    print('\nOrg list headers: ', org_list_headers)
    input('\n\nPress any key to continue')

# Invoke the API - there are no parameters for this GET request, only headers
response = requests.get(url,headers=org_list_headers)

# Retrieve the JSON response
org_json = response.json()
if DEBUG_MODE:
    print('\nRaw Org JSON:', org_json)
    print('\nFormatted Org JSON',json.dumps(org_json,indent=2))
    # This code writes the JSON to a file for easier reading
    with open('orgs.json','w') as outfile:
        json.dump(org_json,outfile,indent=2)
    input('\n\nPress any key to continue')

# Print out the display_name for every org
print('Organization display names: ')
for org in org_json:
    print(org['display_name'])