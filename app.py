from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *
import openstack
application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.MachineData
mytoken = openstack.getAdminToken()

#following API are available

# def getToken(userName, password, projectName):
# def getAdminToken():
# def getUserToken(userName, password, projectName = "admin"):

# def listOfServer(mytoken):
# def listOfFlavors(mytoken):
# def listOfImages(mytoken):
# def listOfProjects(mytoken):
# def listOfUsers(mytoken):
# def listOfNetworks(mytoken):

# def createNewProject(mytoken, projectName, projectDescription):
# def createNewUser(mytoken, userName, password):
# def createNewServer(mytoken, vmName):

# def instanceAction(mytoken, instanceId, action):

# def startInstance(mytoken, instanceId):
# def stopInstance(mytoken, instanceId):
# def pauseInstance(mytoken, instanceId):
# def unpauseInstance(mytoken, instanceId):
# def suspendInstance(mytoken, instanceId):
# def resumeInstance(mytoken, instanceId):
# def deleteInstance(mytoken, instanceId):

@application.route('/testApp',methods=['POST'])
def testApp():
    try:      
        #reply = openstack.listOfFlavors();
        #reply = openstack.createNewServer("fromAPI2");
        #reply = openstack.startInstance("57360fe3-f771-433a-ad6b-bc38c9a6eac7");
        #reply = openstack.listOfProjects();
        mytoken = openstack.getAdminToken();
        reply = openstack.listOfServer(mytoken);
        return json.dumps(reply);
    except Exception, e:
        return str(e);

@application.route("/addMachine",methods=['POST'])
def addMachine():
    try:		
        json_data = request.json['info']
        instanceName = json_data['instanceName']
        flavorId = json_data['flavor']['id']
        imageId = json_data['image']['id']
        networkId = json_data['network']['id']
        print instanceName
        print flavorId
        print imageId
        print networkId
        openstack.createNewServer(mytoken, instanceName, flavorId, imageId, networkId)
        db.Machines.insert_one({
            'device':instanceName,'ip':flavorId,'username':imageId,'password':networkId,'port':networkId
            })
        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))


@application.route('/')
def showMachineList():	
#	return 'hello world'
    return render_template('index.html')
@application.route('/list')
def showMachineList1():	
#	return 'hello world'
    return render_template('instances.html')
    
@application.route('/index')
def showMachineList2():	
#	return 'hello world'
    return render_template('index.html')
    
@application.route('/getMachine',methods=['POST'])
def getMachine():
    try:
        machineId = request.json['id']
        machine = db.Machines.find_one({'_id':ObjectId(machineId)})
        machineDetail = {
                'device':machine['device'],
                'ip':machine['ip'],
                'username':machine['username'],
                'password':machine['password'],
                'port':machine['port'],
                'id':str(machine['_id'])
                }
        return json.dumps(machineDetail)
    except Exception, e:
        return str(e)

@application.route('/updateMachine',methods=['POST'])
def updateMachine():
    try:
        machineInfo = request.json['info']
        machineId = machineInfo['id']
        device = machineInfo['device']
        ip = machineInfo['ip']
        username = machineInfo['username']
        password = machineInfo['password']
        port = machineInfo['port']

        db.Machines.update_one({'_id':ObjectId(machineId)},{'$set':{'device':device,'ip':ip,'username':username,'password':password,'port':port}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getMachineList",methods=['POST'])
def getMachineList():
    try:
        serverInfo = openstack.listOfServer(mytoken)
        flavorInfo = openstack.listOfFlavors(mytoken)
        imageInfo = openstack.listOfImages(mytoken)
        networkInfo = openstack.listOfNetworks(mytoken)
        machineList = []
        flavorList = []
        imageList = []
        networkList = []
        for server in serverInfo['servers']:
            machineItem = {
                'name':server['name'],
                'image_name':server['image']['id'],
                'ip_address':server['OS-SRV-USG:launched_at'],
                'flavor':server['flavor']['id'],
                'status':server['status'],
                'zone': server['OS-EXT-AZ:availability_zone'],
                'task': server['OS-EXT-STS:task_state'],
                'id': server['id']
                }
            machineList.append(machineItem)
			
        for flavor in flavorInfo['flavors']:
            flavorItem = {'name':flavor['name'], 'id': flavor['id']}
            flavorList.append(flavorItem)

        for image in imageInfo['images']:
			imageItem = {'name':image['name'], 'id': image['id']}
			imageList.append(imageItem)

        for network in networkInfo['networks']:
            networkItem = {'name':network['name'], 'id': network['id']}
            networkList.append(networkItem)

        stackInfo = {'servers':machineList, 'flavors':flavorList, 'images':imageList, 'networks':networkList}
    except Exception,e:
            return str(e)
    return json.dumps(stackInfo)

@application.route("/execute",methods=['POST'])
def execute():
    try:
        machineInfo = request.json['info']
        ip = machineInfo['ip']
        username = machineInfo['username']
        password = machineInfo['password']
        command = machineInfo['command']
        isRoot = machineInfo['isRoot']
        
        env.host_string = username + '@' + ip
        env.password = password
        resp = ''
        with settings(warn_only=True):
            if isRoot:
                resp = sudo(command)
            else:
                resp = run(command)

        return jsonify(status='OK',message=resp)
    except Exception, e:
        print 'Error is ' + str(e)
        return jsonify(status='ERROR',message=str(e))

@application.route("/deleteMachine",methods=['POST'])
def deleteMachine():
    try:
        machineId = request.json['id']
        print machineId     
        response = openstack.deleteInstance(mytoken, machineId)
        return jsonify(response)
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/resumemachine",methods=['POST'])
def resumeMachine():
    try:
        machineId = request.json['id']
        print machineId      
        response = openstack.resumeInstance(mytoken, machineId)
        return jsonify(response)
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/suspendmachine",methods=['POST'])
def suspendMachine():
    try:
        machineId = request.json['id']
        print machineId
        response = openstack.suspendInstance(mytoken, machineId)
        return jsonify(response)
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/unpausemachine",methods=['POST'])
def unpauseMachine():
    try:
        machineId = request.json['id']
        print machineId
        response = openstack.unpauseInstance(mytoken, machineId)
        return jsonify(response)
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/pausemachine",methods=['POST'])
def pauseMachine():
    try:
        machineId = request.json['id']
        print machineId       
        response = openstack.pauseInstance(mytoken, machineId)
        return jsonify(response)
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/stopmachine",methods=['POST'])
def stopMachine():
    try:
        machineId = request.json['id']
        print machineId
        response = openstack.stopInstance(mytoken, machineId)
        return jsonify(response)
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/startmachine",methods=['POST'])
def startMachine():
    try:
        machineId = request.json['id']
        print machineId
        response = openstack.startInstance(mytoken, machineId)
        return jsonify(response)
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))





if __name__ == "__main__":
    application.run(host='127.0.0.1', port= 5010)

