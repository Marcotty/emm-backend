import requests
import json
import os
import webbrowser
import urllib.request
from google.oauth2 import service_account
from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
from urllib.parse import urlencode

def test() :
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'
    entreprises = androidmanagement.enterprises().get(name = enterprise_name).execute()
    names = entreprises['name']
    print('Entreprise name : ' + names)
    
    response = androidmanagement.enterprises().devices().list(parent = enterprise_name).execute()
    txt = json.dumps(response, indent=4)
    print(txt)
    devices = response['devices']
    for device in devices:
        print('Name: ' + device['name'])

# Méthode permettant de créer les crédits d'authentification depuis le compte de service
# Permet de ne pas avoir à autoriser l'application à accéder à l'API à chaque exécution.
def CreationCredits(path) :
    print('Creation credits autorisations')
    credentials = service_account.Credentials.from_service_account_file(
    #filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    filename=os.environ[path],
    scopes=['https://www.googleapis.com/auth/androidmanagement'])
    return credentials

#Méthode pour créer l'API permettant la gestion des objects
def getAPI(client, pathKey):
    print('Creation API pour ' + client)
    #Create credentials
    credentials = CreationCredits(pathKey)
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    if androidmanagement:
        print('Authentication succeeded.')
    return androidmanagement
#M2thode qui retourne les infos de l'entreprise 
#Paramètres [Entreprise_name, AndroidAPI]
def getEnterprise(ent, androidmanagement) :
    print('Retourne infos entreprise de ' + ent)
    if androidmanagement:   
        response = androidmanagement.enterprises().get(name = ent).execute()
        print(ObjetToJson(response))
        return response
    
#Méthode permettant de retourner la liste des politiques d'une entreprise
#Paramètres [Entreprise_name, AndroidAPI]
def getPoliciesEnterprise(ent, androidmanagement) :
    response = androidmanagement.enterprises().policies().list(parent = ent).execute()
    policies = response['policies']
    return policies
#Méthode qui retourne la liste des devices d'une entreprise
#Paramètres [Entreprise_name, AndroidAPI]
def getDevicesEnterprise(ent, androidmanagement):
    print('Retourne la liste des devices de ' + ent)
    response = androidmanagement.enterprises().devices().list(parent = ent).execute()
    if response:
        devices = response['devices']
        return devices
    else:
        print('Aucun device trouvé')
def updateDevice(device_name, androidmanagement, device_body):
    print('Update device ' + device_name)
    response = androidmanagement.enterprises().devices().patch(
        name=device_name,
        body=device_body
    ).execute()
    return response
#Méthode permettant de supprimer un device grâce à son id
def deleteDevice(NomDevice, androidmanagement):
    print('Suppression du device ' + NomDevice)
    response = androidmanagement.enterprises().devices().delete(name = NomDevice).execute()
    if response:
        print('Suppression ok')
    else:
        print('Pas de device portant ce nom : ' + NomDevice)

def UpdatePoliciesEnterprise(pol_name, androidmanagement, pol_body):
    print('Update politique ' + pol_name)
    response = androidmanagement.enterprises().policies().patch(
        name=pol_name,
        body=pol_body
    ).execute()
    return response

#Méthode permettant de supprimer une politique grâce à son id
def DeletePolicy(NomPolitique, androidmanagement):
    print('Suppression de la politique ' + NomPolitique)
    response = androidmanagement.enterprises().policies().delete(name = NomPolitique).execute()
    if response:
        print('Suppression ok')
    else:
        print('Pas de politique portant ce nom : ' + NomPolitique)
        
#Méthode permettant de supprimer TOUS les devices (développement)
def DeleteAllDevices():
    print('Suppression de tous les devices')
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    if androidmanagement:
        print('Authentication succeeded.')
    devices = getDevices()
    for device in devices:
        print('Suppression de ' + device['name'])
        androidmanagement.enterprises().devices().delete(name = device['name']).execute()

#Méthode permettant de supprimer un device grâce à son id
def DeleteDevice(NomDevice):
    print('Suppression du device ' + NomDevice)
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    if androidmanagement:
        print('Authentication succeeded.')
    response = androidmanagement.enterprises().devices().delete(name = NomDevice).execute()
    if response:
        print('Suppression ok')
    else:
        print('Pas de device portant ce nom : ' + NomDevice)

def inscriptionPolicy(ent_name, pol_name, androidmanagement):
    enrollment_token = androidmanagement.enterprises().enrollmentTokens().create(
        parent=ent_name,
        body={"policyName": pol_name}
    ).execute()

    image = {
        'cht': 'qr',
        'chs': '200x200',
        'chl': enrollment_token['qrCode']
    }

    qrcode_url = 'https://chart.googleapis.com/chart?' + urlencode(image)
    return qrcode_url

#Méthode permettant de convertir un objet python en objet json
def ObjetToJson(objet):
    device_json = json.dumps(objet, indent=4)
    return device_json

def getDevices(ent, num):
    print('Retourne la liste des devices')
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    if androidmanagement:
        print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'
    response = androidmanagement.enterprises().devices().list(parent = enterprise_name).execute()
    if response:
        devices = response['devices']
        return devices
    else:
        print('Aucun device trouvé')

#Méthode qui permet d'afficher dans la console la liste des devices appartenant à l'organisation
def AffListDevices() :
    print('Affichage des devices')
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    if androidmanagement:
        print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'    
    response = androidmanagement.enterprises().devices().list(parent = enterprise_name).execute()
    if response:
        devices = response['devices']
        i=0
        for device in devices:
            i+=1
            print('\nDevice n°{} :'.format(i))
            print('Name: ' + device['name'])
            print('Politique: ' + device['policyName'])
            print('UserName: ' + device['userName'])
            print('ManagementMode: ' + device['managementMode'])
            print('Date inscription: ' + device['enrollmentTime'])
            if 'softwareInfo' in device:
                softwareInfo = device['softwareInfo']
                #print('Marque: ' + softwareInfo['brand'])
                print('Version Android: ' + softwareInfo['androidVersion'])
                print('Langage Systeme: ' + softwareInfo['primaryLanguageCode'])
            if 'hardwareInfo' in device:
                hardwareInfo = device['hardwareInfo']
                print('Marque: ' + hardwareInfo['brand'])
                print('Modèle: ' + hardwareInfo['model']) 
            # Afficher l'objet en JSON
            print(ObjetToJson(device))
    else:
        print('Aucun device trouvé')
def ListPolicies() :
    print('Affichage des politiques')
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    if androidmanagement:
        print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'    
    response = androidmanagement.enterprises().policies().list(parent = enterprise_name).execute()
    policies = response['policies']
    return policies
    
def AffListPolicies() :
    print('Affichage des politiques')
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    if androidmanagement:
        print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'    
    response = androidmanagement.enterprises().policies().list(parent = enterprise_name).execute()
    policies = response['policies']
    i=0
    for policy in policies:
        i+=1
        print('\Politique n°{} :'.format(i))
        print(ObjetToJson(policy))
        

def InscriptionQR(NomPolitique):
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)

    print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'
    
    #Creation du token d'inscription
    enrollment_token = androidmanagement.enterprises().enrollmentTokens().create(
        parent=enterprise_name,
        body={"policyName": NomPolitique}
    ).execute()

    image = {
        'cht': 'qr',
        'chs': '500x500',
        'chl': enrollment_token['qrCode']
    }

    qrcode_url = 'https://chart.googleapis.com/chart?' + urlencode(image)
    
    print('Please visit this URL to scan the QR code:', qrcode_url)
    print('Ouverture auto')
    #url = urllib.request.urlopen(qrcode_url)
    #print('result code : ' + str(url.getcode()))
    webbrowser.open_new(qrcode_url)
    
#Méthode qui charge une(toutes?) politique depuis un fichier
def ChargerPolitique():
    print('Charger Politique')
    with open('policies.json') as json_data:
        data_dict = json.load(json_data)
        return data_dict
def UpdatePolitiqueTest():
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)
    enterprise_name = 'enterprises/LC0430y1qm'
    politique = ChargerPolitique()
    policy_name = enterprise_name + politique['name']
    politique_str = ObjetToJson(politique)
    androidmanagement.enterprises().policies().patch(
        name=policy_name,
        body=json.loads(politique_str)
    ).execute()
#Méthode permettant de mettre à jour une politique
# politique hardcodée dans le code => fichier chargé
def UpdatePolitique(politique_name):
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)

    print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'

    policy_name = enterprise_name + '/policies/policy1'

    policy_json = '''
    {
      "applications": [
        {
          "packageName": "com.android.chrome",
          "installType": "KIOSK",
          "defaultPermissionPolicy": "PROMPT"
        }
      ],
      "kioskCustomization": {
          "powerButtonActions" : "POWER_BUTTON_AVAILABLE",
          "deviceSettings" : "SETTINGS_ACCESS_BLOCKED",
          "statusBar": "NOTIFICATIONS_AND_SYSTEM_INFO_ENABLED",
          "systemNavigation" : "NAVIGATION_ENABLED"
        },
      "systemUpdate": {
          "type" : "AUTOMATIC"
      },
      "advancedSecurityOverrides": {
          "untrustedAppsPolicy": "ALLOW_INSTALL_DEVICE_WIDE"
      },
      "debuggingFeaturesAllowed": true,
      "bluetoothDisabled": true,
      "statusReportingSettings": {
        "applicationReportsEnabled": true,
        "deviceSettingsEnabled": true,
        "softwareInfoEnabled": true,
        "memoryInfoEnabled": true,
        "networkInfoEnabled": true,
        "displayInfoEnabled": true,
        "powerManagementEventsEnabled": true,
        "hardwareStatusEnabled": true,
        "systemPropertiesEnabled": true,
        "applicationReportingSettings": {
            "includeRemovedApps": true
        }
      },
       "appAutoUpdatePolicy": "ALWAYS"
    }
    '''
    #Creation politique a partir du json
    androidmanagement.enterprises().policies().patch(
        name=policy_name,
        body=json.loads(policy_json)
    ).execute()
#Méthode permettant d'inscrire les devices en utilisant un qr code
def Inscription_QR() : 
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)

    print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'

    policy_name = enterprise_name + '/policies/policy2'

    policy_json = '''
    {
      "applications": [
        {
          "packageName": "com.android.chrome",
          "installType": "KIOSK",
          "defaultPermissionPolicy": "PROMPT"
        }
      ],
      "kioskCustomization": {
          "powerButtonActions" : "POWER_BUTTON_AVAILABLE",
          "deviceSettings" : "SETTINGS_ACCESS_BLOCKED",
          "statusBar": "NOTIFICATIONS_AND_SYSTEM_INFO_ENABLED",
          "systemNavigation" : "NAVIGATION_ENABLED"
        },
      "systemUpdate": {
          "type" : "AUTOMATIC"
      },
      "advancedSecurityOverrides": {
          "untrustedAppsPolicy": "ALLOW_INSTALL_DEVICE_WIDE"
      },
      "debuggingFeaturesAllowed": true,
      "bluetoothDisabled": true
    }
    '''
    #Creation politique a partir du json
    androidmanagement.enterprises().policies().patch(
        name=policy_name,
        body=json.loads(policy_json)
    ).execute()
    #Creation du token d'inscription
    enrollment_token = androidmanagement.enterprises().enrollmentTokens().create(
        parent=enterprise_name,
        body={"policyName": policy_name}
    ).execute()

    image = {
        'cht': 'qr',
        'chs': '500x500',
        'chl': enrollment_token['qrCode']
    }

    qrcode_url = 'https://chart.googleapis.com/chart?' + urlencode(image)
    
    print('Please visit this URL to scan the QR code:', qrcode_url)
    print('Ouverture auto')
    #url = urllib.request.urlopen(qrcode_url)
    #print('result code : ' + str(url.getcode()))
    webbrowser.open_new(qrcode_url)   

#méthode qui retourne un code QR
def getQRLien():
    # Paste your project ID here.
    cloud_project_id = 'projettest-268014'
    
    #Create credentials
    credentials = CreationCredits()
    # Create the API client.
    androidmanagement = build('androidmanagement', 'v1', credentials=credentials)

    print('Authentication succeeded.')
    enterprise_name = 'enterprises/LC0430y1qm'

    policy_name = enterprise_name + '/policies/policy1'

    policy_json = '''
    {
      "applications": [
        {
          "packageName": "com.android.chrome",
          "installType": "KIOSK",
          "defaultPermissionPolicy": "PROMPT"
        }
      ],
      "kioskCustomization": {
          "powerButtonActions" : "POWER_BUTTON_AVAILABLE",
          "deviceSettings" : "SETTINGS_ACCESS_BLOCKED",
          "statusBar": "NOTIFICATIONS_AND_SYSTEM_INFO_ENABLED",
          "systemNavigation" : "NAVIGATION_ENABLED"
        },
      "systemUpdate": {
          "type" : "AUTOMATIC"
      },
      "advancedSecurityOverrides": {
          "untrustedAppsPolicy": "ALLOW_INSTALL_DEVICE_WIDE"
      },
      "debuggingFeaturesAllowed": true,
      "bluetoothDisabled": true
    }
    '''
    #Creation politique a partir du json
    androidmanagement.enterprises().policies().patch(
        name=policy_name,
        body=json.loads(policy_json)
    ).execute()
    #Creation du token d'inscription
    enrollment_token = androidmanagement.enterprises().enrollmentTokens().create(
        parent=enterprise_name,
        body={"policyName": policy_name}
    ).execute()

    image = {
        'cht': 'qr',
        'chs': '500x500',
        'chl': enrollment_token['qrCode']
    }

    qrcode_url = 'https://chart.googleapis.com/chart?' + urlencode(image)
    return qrcode_url
