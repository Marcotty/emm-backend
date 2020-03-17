# coding=utf-8

from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import tools
# creating the Flask application
app = Flask(__name__)
#Enable Cross Origin Resource Sharing
CORS(app)

testClient = {
    "entreprise":"enterprises/LC0430y1qm",
    "key":"GOOGLE_APPLICATION_CREDENTIALS"
}
APIs = []
def CreationAPI():
    print('Creation API')
    global APIs
    APIs.insert(0, tools.getAPI(testClient["entreprise"], testClient["key"]))
    
def getAPI(ent):
    if ent == testClient["entreprise"]:
        return APIs[0]
    return None
@app.route('/')
def home():
    return render_template("home.html")
#GET /entreprise/devices pour retourner liste des devices d'une certaine entreprise
@app.route('/<enterprise>/<enterpriseNumber>/devices')
def get_devices(enterprise, enterpriseNumber):
    if APIs == []:
        CreationAPI()
    ent_name = enterprise + "/" + enterpriseNumber
    print('Fetch devices from' + ent_name)
    devices = tools.getDevicesEnterprise(ent_name, getAPI(ent_name))
    #print(tools.ObjetToJson(devices))
    return jsonify(devices)

@app.route('/<enterprise>/<enterpriseNumber>/devices/<deviceId>', methods = ['POST', 'DELETE'])
def post_device(enterprise, enterpriseNumber, deviceId):
    if APIs == []:
        CreationAPI()
    ent_name = enterprise + "/" + enterpriseNumber
    device_name = enterprise + "/" + enterpriseNumber + "/devices/" + deviceId
    
    if request.method == 'POST':
        print('Update device for' + device_name)
        response = tools.updateDevice(device_name, getAPI(ent_name), request.json)
        #print(tools.ObjetToJson(response))
        return jsonify(response)
    
    elif request.method == 'DELETE':
        response = tools.deleteDevice(device_name, getAPI(ent_name))
        #print(tools.ObjetToJson(response))
        return jsonify(response)
    
@app.route('/<enterprise>/<enterpriseNumber>/policies')
def get_policies(enterprise, enterpriseNumber):
    if APIs == []:
        CreationAPI()
    ent_name = enterprise + "/" + enterpriseNumber
    print('Fetch policies from ' + ent_name)
    policies = tools.getPoliciesEnterprise(ent_name, getAPI(ent_name))
    #print(tools.ObjetToJson(devices))
    return jsonify(policies)
@app.route('/<enterprise>/<enterpriseNumber>/policies/<policyId>/inscription')
def inscriptionPolicy(enterprise, enterpriseNumber, policyId):
    if APIs == []:
        CreationAPI()
        
    ent_name = enterprise + "/" + enterpriseNumber
    pol_name = enterprise + "/" + enterpriseNumber + "/policies/" + policyId
    qr_code_url = tools.inscriptionPolicy(ent_name, pol_name, getAPI(ent_name))
    return jsonify(qr_code_url)

@app.route('/<enterprise>/<enterpriseNumber>/policies/<policyId>', methods = ['POST', 'DELETE'])
def post_policies(enterprise, enterpriseNumber, policyId):
    if APIs == []:
        CreationAPI()
        
    ent_name = enterprise + "/" + enterpriseNumber
    pol_name = enterprise + "/" + enterpriseNumber + "/policies/" + policyId
    
    if request.method == 'POST':
        response = tools.UpdatePoliciesEnterprise(pol_name, getAPI(ent_name), request.json)
        #print(tools.ObjetToJson(response))
        return jsonify(response)
    
    elif request.method == 'DELETE':
        response = tools.DeletePolicy(pol_name, getAPI(ent_name))
        #print(tools.ObjetToJson(response))
        return jsonify(response)
    
@app.route('/<enterprise>/<enterpriseNumber>/policies/<policyId>/new', methods = ['POST'])
def new_policy(enterprise, enterpriseNumber, policyId):
    if APIs == []:
        CreationAPI()
        
    ent_name = enterprise + "/" + enterpriseNumber
    pol_name = enterprise + "/" + enterpriseNumber + "/policies/" + policyId
    response = tools.UpdatePoliciesEnterprise(pol_name, getAPI(ent_name), request.json)
    return jsonify(response)

@app.route('/<enterprise>/<enterpriseNumber>')
def get_enterprise(enterprise, enterpriseNumber):
    if APIs == []:
        CreationAPI()
    ent_name = enterprise + "/" + enterpriseNumber
    print('Fetch policies from' + ent_name)
    enterprise = tools.getEnterprise(ent_name, getAPI(ent_name))
    #print(tools.ObjetToJson(devices))
    return jsonify(enterprise)

if __name__ == "__main__":
    print('start')
    CreationAPI()
    app.run(debug=True)
    #app.run(host='172.17.11.50', port=5000, debug=True)

    