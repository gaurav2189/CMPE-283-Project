from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *
import openstack
application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.MachineData

@application.route('/testApp',methods=['POST'])
def testApp():
    try:      
		#reply = openstack.listOfFlavors();
		#reply = openstack.createNewServer("fromAPI2");
		#reply = openstack.startInstance("57360fe3-f771-433a-ad6b-bc38c9a6eac7");
		#reply = openstack.listOfProjects();
		return json.dumps(reply);
    except Exception, e:
        return str(e);

@application.route("/addMachine",methods=['POST'])
def addMachine():
    try:		
        json_data = request.json['info']
        deviceName = json_data['device']
        ipAddress = json_data['ip']
        userName = json_data['username']
        password = json_data['password']
        portNumber = json_data['port']	
	openstack.createNewServer(deviceName)
	#openstack.listOfServer()

        db.Machines.insert_one({
            'device':deviceName,'ip':ipAddress,'username':userName,'password':password,'port':portNumber
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
        machines = db.Machines.find()
#		openstack.createNewServer(deviceName)
	serverList = openstack.listOfServer();
        machineList = []
		
	for server in serverList['servers']:
		print server
		machineItem = {
				'device':server['name'],
				'ip':server['status'],
				'username':server['OS-SRV-USG:launched_at'],
				'password':server['OS-EXT-AZ:availability_zone'],
				'port':server['OS-DCF:diskConfig'],
				'id': server['OS-EXT-SRV-ATTR:host']
				}
		machineList.append(machineItem)
			
        # for machine in machines:
            # print machine
            # machineItem = {
                    # 'device':machine['device'],
                    # 'ip':machine['ip'],
                    # 'username':machine['username'],
                    # 'password':machine['password'],
                    # 'port':machine['port'],
                    # 'id': str(machine['_id'])
                    # }
            # machineList.append(machineItem)
    except Exception,e:
        return str(e)
    return json.dumps(machineList)

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
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))
#added by abhijeet (remove cocmment later on)

@application.route("/resumemachine",methods=['POST'])
def resumeMachine():
    try:
        machineId = request.json['id']
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')


    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/suspendmachine",methods=['POST'])
def suspendMachine():
    try:
        machineId = request.json['id']
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')


    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/unpausemachine",methods=['POST'])
def unpauseMachine():
    try:

        machineId = request.json['id']
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')


    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/pausemachine",methods=['POST'])
def pauseMachine():
    try:

        machineId = request.json['id']
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')


    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/stopmachine",methods=['POST'])
def stopMachine():
    try:

        machineId = request.json['id']
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')


    except Exception, e:
        return jsonify(status='ERROR',message=str(e))


@application.route("/startmachine",methods=['POST'])
def startMachine():
    try:

        machineId = request.json['id']
        db.Machines.remove({'_id':ObjectId(machineId)})
        return jsonify(status='OK',message='deletion successful')


    except Exception, e:
        return jsonify(status='ERROR',message=str(e))





if __name__ == "__main__":
    application.run(host='127.0.0.1', port= 5010)

