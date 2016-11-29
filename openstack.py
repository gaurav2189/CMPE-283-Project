
#!/usr/bin/env python


############# These libraries are required ###########
import urllib2
import json
from flask import jsonify

############### Configuration Section ################
############### Enter your own values ################
# OpenStack server address
# Can be IP address or DNS name
# Can be 127.0.0.1  (localhost) but usually isn't
# hostIP="192.168.1.106"
hostIP="localhost"

# Domain, User, Password
mydomainname= "default"
myusername=   "admin"
mypassword=   "admin_user_secret"


############### OpenStack API ports ########
# Make sure that these ports are open in the Control Node
# and that VirtualBox Port Forwarding (if used) is properly set
# Note that keystone administration port 35357 is no longer needed in v3,
# it is only there for backward compatibility with v2.
# All Keystone operations now go through port 5000
NOVAport         = "8774"
CINDERport       = "8776"
CEILOMETERport   = "8777"
GLANCEport       = "9292"
NEUTRONport      = "9696"
AWSport          = "8000"
HEATport         = "8004"
KEYSTONEport     = "5000"


################## Sample code logic starts here #######################################

def getToken(userName, password, projectName):
	print
	print
	print "********************************************"
	print "* Obtain authorization token from Keystone *"
	print "********************************************"
	print "" ; print ""


	print "Build the request headers, URL and body and POST everything      "
	print"--------------------------------------------------------------------------"


	#### Build the request headers
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json'
			   }
	print "REQUEST HEADERS:" ; print headers

	#### Build the request URL
	CMDpath="/v3/auth/tokens"
	APIport=KEYSTONEport
	url="http://"+hostIP+":"+APIport+CMDpath
	print "REQUEST URL:" ; print url

	#### Build the request body
	#body='{"auth":{"identity":{"methods":["password"],"password":{"user":{"name":"'+myusername+'","domain":{"name":"'+mydomainname+'"},"password":"'+mypassword+'"}}}}}'

	body = ('{'
	'   "auth": {'
	'       "identity": {'
	'           "methods": ['
	'               "password"'
	'           ],'
	'           "password": {'
	'               "user": {'
	'                   "domain": {'
	'                       "name": "default"'
	'                   },'
	'                   "name": "'+ userName +'",'
	'                   "password": "'+ password + '"'
	'               }'
	'           }'
	'       },'
	'       "scope": {'
	'           "project": {'
	'               "domain": {'
	'                   "name": "default"'
	'               },'
	'               "name": "' + projectName +'"'
	'           }'
	'       }'
	'   }'
	'}')

	print "REQUEST BODY:" ; print body
	print"--------------------------------------------------------------------------"
	print "" ; print ""

	#### Send the  POST request
	req = urllib2.Request(url, body, headers)

	##quit()


	print "Read the response headers and body"
	print"--------------------------------------------------------------------------"

	#### Read the response header
	header = urllib2.urlopen(req).info()
	print "RESPONSE HEADER" ; print "===============" ; print header


	#### Read the response body
	response = urllib2.urlopen(req).read()
	print "RESPONSE BODY" ; print"=============" ; print response
	print"--------------------------------------------------------------------------"
	print ""
	print ""

	#quit()

	print "Decode the response header and body"
	print"------------------------------------"

	mytoken = header.getheader('X-Subject-Token')
	print "KEYSTONE TOKEN (X-Subject-Token)" ; print "================================" ; print mytoken ; print ""


	#### Convert response body to pretty print format
	decoded = json.loads(response.decode('utf8'))
	pretty = json.dumps(decoded,sort_keys=True,indent=3)
	print "RESPONSE BODY IN PRETTY FORMAT" ; print "==============================" ; print pretty ; print "" ; print ""


	#### Parse JSON formatted data for token issue date
	issued = decoded['token']['issued_at']
	print "TOKEN WAS ISSUED" ; print "================" ; print issued ; print "" ; print ""


	#### Parse JSON formatted data for token expiration date
	expires = decoded['token']['expires_at']
	print "TOKEN WILL EXPIRE" ; print "=================" ; print expires ; print "" ; print ""
	print "" ; print ""
	return mytoken;
	
##quit()

def getAdminToken():
	print "----------------Admin Token-------------------"; print ""; print ""	
	return getToken("admin", "admin_user_secret", "admin");

def getUserToken(userName, password, projectName = "admin"):
	print "----------------User Token-------------------"; print ""; print ""	
	return getToken(userName, password, projectName);


# def getToken():
	# print
	# print
	# print "********************************************"
	# print "* Obtain authorization token from Keystone *"
	# print "********************************************"
	# print "" ; print ""


	# print "Build the request headers, URL and body and POST everything      "
	# print"--------------------------------------------------------------------------"


	# #### Build the request headers
	# headers = {
			  # 'Content-Type'   :   'application/json',
			  # 'Accept'         :   'application/json'
			   # }
	# print "REQUEST HEADERS:" ; print headers

	# #### Build the request URL
	# CMDpath="/v3/auth/tokens"
	# APIport=KEYSTONEport
	# url="http://"+hostIP+":"+APIport+CMDpath
	# print "REQUEST URL:" ; print url

	# #### Build the request body
	# #body='{"auth":{"identity":{"methods":["password"],"password":{"user":{"name":"'+myusername+'","domain":{"name":"'+mydomainname+'"},"password":"'+mypassword+'"}}}}}'

	# body = ('{'
	# '   "auth": {'
	# '       "identity": {'
	# '           "methods": ['
	# '               "password"'
	# '           ],'
	# '           "password": {'
	# '               "user": {'
	# '                   "domain": {'
	# '                       "name": "default"'
	# '                   },'
	# '                   "name": "admin",'
	# '                   "password": "admin_user_secret"'
	# '               }'
	# '           }'
	# '       },'
	# '       "scope": {'
	# '           "project": {'
	# '               "domain": {'
	# '                   "name": "default"'
	# '               },'
	# '               "name": "admin"'
	# '           }'
	# '       }'
	# '   }'
	# '}')
	# print "REQUEST BODY:" ; print body
	# print"--------------------------------------------------------------------------"
	# print "" ; print ""

	# #### Send the  POST request
	# req = urllib2.Request(url, body, headers)

	# ##quit()


	# print "Read the response headers and body"
	# print"--------------------------------------------------------------------------"

	# #### Read the response header
	# header = urllib2.urlopen(req).info()
	# print "RESPONSE HEADER" ; print "===============" ; print header


	# #### Read the response body
	# response = urllib2.urlopen(req).read()
	# print "RESPONSE BODY" ; print"=============" ; print response
	# print"--------------------------------------------------------------------------"
	# print ""
	# print ""

	# #quit()

	# print "Decode the response header and body"
	# print"------------------------------------"

	# mytoken = header.getheader('X-Subject-Token')
	# print "KEYSTONE TOKEN (X-Subject-Token)" ; print "================================" ; print mytoken ; print ""


	# #### Convert response body to pretty print format
	# decoded = json.loads(response.decode('utf8'))
	# pretty = json.dumps(decoded,sort_keys=True,indent=3)
	# print "RESPONSE BODY IN PRETTY FORMAT" ; print "==============================" ; print pretty ; print "" ; print ""


	# #### Parse JSON formatted data for token issue date
	# issued = decoded['token']['issued_at']
	# print "TOKEN WAS ISSUED" ; print "================" ; print issued ; print "" ; print ""


	# #### Parse JSON formatted data for token expiration date
	# expires = decoded['token']['expires_at']
	# print "TOKEN WILL EXPIRE" ; print "=================" ; print expires ; print "" ; print ""
	# print "" ; print ""
	# return mytoken;
	
# ##quit()

############# List the NOVA API-v2 details #######
def listOfServer():
	mytoken = getAdminToken()
	print "*****************************************"
	print "*  Get list of the NOVA API-v2 details  *"
	print "*****************************************"
	print ""

	print "Build the request headers, URL and body and GET everything"
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""


	#### Build the URL
	CMDpath="/v2.1/servers/detail"
	APIport=NOVAport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "URL" ; print "===" ; print url1 ; print "" ; print ""


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, None, headers)

	#### Read the response
	response1 = urllib2.urlopen(req1).read()

	#### Convert to JSON format
	decoded1 = json.loads(response1.decode('utf8'))

	#### Make it look pretty and indented
	pretty1 = json.dumps(decoded1,sort_keys=True,indent=3)
	print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""
	
	print "---------------------------------------"; print ""; print "" 
	for i in decoded1['servers']:
		print i['name'], i['status'];
	print""; print "-------------------------------------------"
	return decoded1;

	
def listOfFlavors():
	mytoken = getAdminToken()
	print "*****************************************"
	print "*  Get list of the Images details  *"
	print "*****************************************"
	print ""

	print "Build the request headers, URL and body and GET everything"
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""


	#### Build the URL
	CMDpath="/v2.1/flavors/detail"
	APIport=NOVAport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "URL" ; print "===" ; print url1 ; print "" ; print ""


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, None, headers)
	print req1
	#### Read the response
	response1 = urllib2.urlopen(req1).read()
	
	#### Convert to JSON format
	decoded1 = json.loads(response1.decode('utf8'))

	#### Make it look pretty and indented
	pretty1 = json.dumps(decoded1,sort_keys=True,indent=3)
	#print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""
	
	print "---------------------------------------"; print ""; print "" 
	for i in decoded1['flavors']:
		print i['name'], i['id'];
	print""; print "-------------------------------------------"
	return decoded1;


def listOfImages():
	mytoken = getAdminToken()
	print "*****************************************"
	print "*  Get list of the Images details  *"
	print "*****************************************"
	print ""

	print "Build the request headers, URL and body and GET everything"
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""


	#### Build the URL
	#http://localhost:9292/v2/images
	CMDpath="/v2/images"
	APIport=GLANCEport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "URL" ; print "===" ; print url1 ; print "" ; print ""


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, None, headers)

	#### Read the response
	response1 = urllib2.urlopen(req1).read()

	#### Convert to JSON format
	decoded1 = json.loads(response1.decode('utf8'))

	#### Make it look pretty and indented
	pretty1 = json.dumps(decoded1,sort_keys=True,indent=3)
	print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""
	
	print "---------------------------------------"; print ""; print "" 
	for i in decoded1['images']:
		print i['name'], i['id'];
	print""; print "-------------------------------------------"
	return decoded1;

def listOfProjects():
	mytoken = getAdminToken()
	print "*****************************************"
	print "*  Get list of the Images details  *"
	print "*****************************************"
	print ""

	print "Build the request headers, URL and body and GET everything"
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""

	#### Build the request URL
	CMDpath="/v3/projects"
	APIport=KEYSTONEport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "REQUEST URL:" ; print url1


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, None, headers)
	#### Read the response
	response1 = urllib2.urlopen(req1).read()
	
	#### Convert to JSON format
	decoded1 = json.loads(response1.decode('utf8'))

	#### Make it look pretty and indented
	pretty1 = json.dumps(decoded1,sort_keys=True,indent=3)
	#print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""
	
	print "---------------------------------------"; print ""; print "" 
	for i in decoded1['projects']:
		print i['name'], i['id'];
	print""; print "-------------------------------------------"
	return decoded1;

## create a new project
def createNewProject(projectName, projectDescription):
	mytoken = getAdminToken()
	
	print "Build the request headers, URL and body and GET everything"
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""
	
	body = ('{'
    '"project": {'
    '    "description": "'+ projectDescription +'",'
    '    "domain_id": "3295977a1c9a4dde8540e9ec5eae80d0",'
    '    "enabled": true,'
    '    "is_domain": false,'
    '    "name": "'+ projectName +'"'
    '}'
	'}')
	

	#### Build the request URL
	CMDpath="/v3/projects"
	APIport=KEYSTONEport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "REQUEST URL:" ; print url1


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, body, headers)

	#### Read the response
	response1 = urllib2.urlopen(req1).read()

	#### Convert to JSON format
	decoded1 = json.loads(response1.decode('utf8'))

	#### Make it look pretty and indented
	pretty1 = json.dumps(decoded1,sort_keys=True,indent=3)
	print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""
	return decoded1;


def listOfUsers():
	mytoken = getAdminToken()
	
	print "Build the request headers, URL and body and GET everything"
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""

	#### Build the request URL
	CMDpath="/v3/users"
	APIport=KEYSTONEport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "REQUEST URL:" ; print url1


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, None, headers)
	#### Read the response
	response1 = urllib2.urlopen(req1).read()
	
	#### Convert to JSON format
	decoded1 = json.loads(response1.decode('utf8'))

	#### Make it look pretty and indented
	pretty1 = json.dumps(decoded1,sort_keys=True,indent=3)
	#print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""
	
	print "---------------------------------------"; print ""; print "" 
	for i in decoded1['users']:
		print i['name'], i['id'];
	print""; print "-------------------------------------------"
	return decoded1;


## create a new project
def createNewUser(userName, password):
	mytoken = getAdminToken()
	
	print "Build the request headers, URL and body and GET everything"
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""
	
	body = ('{'
    '"user": {'
    '    "default_project_id": "65a1fb5b49aa49a8a82ee57db2ca38fa",'
    '    "domain_id": "3295977a1c9a4dde8540e9ec5eae80d0",'
    '    "enabled": true,'
    '    "name": "'+ userName +'",'
    '    "password": "'+ password +'"'
    '}'
	'}')
		

	#### Build the request URL
	CMDpath="/v3/users"
	APIport=KEYSTONEport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "REQUEST URL:" ; print url1


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, body, headers)

	#### Read the response
	response1 = urllib2.urlopen(req1).read()

	#### Convert to JSON format
	decoded1 = json.loads(response1.decode('utf8'))

	#### Make it look pretty and indented
	pretty1 = json.dumps(decoded1,sort_keys=True,indent=3)
	print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""
	return decoded1;

	
## create a new server
def createNewServer(vmName):
	mytoken = getAdminToken()
	
	print "Build the request headers, URL and body and GET everything"
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""

	body = ('{'
    '"server": {'
    '   "name": "'+ vmName + '",'
    '    "imageRef": "01cbabf2-6730-4bb2-af9d-6ea43949e966",'
    '    "flavorRef": "1",'
    '    "networks": ['
    '        {'
    '            "uuid": "ab6455b1-f08f-445d-ac83-0be672cb92ac"'
    '        }'
    '    ]'
    '}'
	'}')
	#### Build the URL
	CMDpath="/v2.1/servers"
	APIport=NOVAport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "URL" ; print "===" ; print url1 ; print "" ; print ""


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, body, headers)

	#### Read the response
	response1 = urllib2.urlopen(req1).read()

	#### Convert to JSON format
	decoded1 = json.loads(response1.decode('utf8'))

	#### Make it look pretty and indented
	pretty1 = json.dumps(decoded1,sort_keys=True,indent=3)
	print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""
	return decoded1;


def instanceAction(instanceId, action):
	mytoken = getAdminToken()
	print "-----------------------------------------------------------"

	#### Build the headers
	
	headers = {
			  'Content-Type'   :   'application/json',
			  #'Accept'         :   'application/json',
			  'X-Auth-Token'   :    mytoken
			   }
	print "REQUEST HEADERS" ; print "================" ; print headers ; print "" ; print ""

	body = ('{'
    '"'+action+'":null'
	'}')
	
	
	print "REQUEST BODY:" ; print body
	print"--------------------------------------------------------------------------"
	print "" ; print ""

	
	#### Build the URL
	#http://localhost:8774/v2.1/servers/6269d835-bee0-49b7-ba1c-f348aac88d1c/action
	CMDpath="/v2.1/servers/"+instanceId+"/action"
	APIport=NOVAport
	url1="http://"+hostIP+":"+APIport+CMDpath
	print "URL" ; print "===" ; print url1 ; print "" ; print ""


	#### Send the GET request
	# Note that the second parameter which normally carries the body data
	# is "None", making the request a "GET" instead of a "POST"
	req1 = urllib2.Request(url1, body, headers)

	try:		
		response1 = urllib2.urlopen(req1).read()	
		print "action execution successful"
		return {"status":"OK", "message":"success"};
	except Exception,e:
		print "This is an exception"
		print str(e)
		return {"status":"ERROR", "message":str(e)};	

def startInstance(instanceId):
	print "start instance"
	return instanceAction(instanceId, "os-start");
	
def stopInstance(instanceId):
	print "stop instance"
	return instanceAction(instanceId, "os-stop");

def pauseInstance(instanceId):
	print "pause instance"
	return instanceAction(instanceId, "pause");

def unpauseInstance(instanceId):
	print "unpause instance"
	return instanceAction(instanceId, "unpause");

def suspendInstance(instanceId):
	print "suspend instance"
	return instanceAction(instanceId, "suspend");

def resumeInstance(instanceId):
	print "resume instance"
	return instanceAction(instanceId, "resume");

def deleteInstance(instanceId):
	print "forceDelete instance"
	return instanceAction(instanceId, "forceDelete");

	
def myTry():
	print "-----------------------------------"; print ""; print ""	
	print "trying to call a method"
	print ""; print "---------------------------"
	return;
	
	
## This is test region	
# jreply = listOfServer()
# # for server in jreply:
	# # print server;

# for server in jreply['servers']:
	# print server
	# print ""
	
#createNewServer("funcName")
#listOfServer()
#listOfFlavors()
#listOfImages()
#myTry()
#deleteInstance("de5eedb2-8bb5-4c5e-bfe3-ec6aa59c7cc1")
#stopInstance("89ece6c4-1629-4984-be0e-f1a402b277f0")
#createNewProject("testproject8", "This is a new project")
#listOfProjects()
#createNewUser("abc", "gaurav")
#listOfUsers()
print "This is open stack"
##quit()
