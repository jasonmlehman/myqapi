from botocore.vendored import requests

class myqapi:
	#Constants
        device_list_endpoint = "api/v4/UserDeviceDetails/Get"
        device_set_endpoint = "api/v4/DeviceAttribute/PutDeviceAttribute"
        uri = "myqexternal.myqdevice.com"
        endpoint = "api/v4/User/Validate"
	#MyQ username and password
        username = "username"
        password = "password"

	# appid For liftmaster
        app_id = "Vj8pQggXLhLy0WHahglCD4N1nAkkXQtGYpq2HrHD7H1nvmbT55KqtN6RSF4ILB/i"

	# appid for chamberlain
	#app_id = "OA9I/hgmPHFp9RYKJqCKfwnhh28uqLJzZ9KOJf1DXoo8N2XAaVX6A1wcLYyWsnnv"

	# appid for craftsman
	#app_id = "YmiMRRS1juXdSd0KWsuKtHmQvh5RftEp5iewHdCvsNB77FnQbY+vjCVn2nMdIeN8"

	# appid for merlin
	#app_id = "3004cac4e920426c823fa6c2ecf0cc28ef7d4a7b74b6470f8f0d94d6c39eb718"

        def __init__(self):
		# Get the security token used to authenticate to myq API
                params = {
                    'username': self.username,
                    'password': self.password
                }
                login = requests.post(
                        'https://{host_uri}/{login_endpoint}'.format(
                            host_uri=self.uri,
                            login_endpoint=self.endpoint),
                            json=params,
                            headers={
                                'MyQApplicationId': self.app_id
                            }
                    )

                auth = login.json()
                self.security_token = auth['SecurityToken']

        def get_devices(self):
		# Gets all devices within your myQ account
                devices = requests.get(
                    'https://{host_uri}/{device_list_endpoint}'.format(
                        host_uri=self.uri,
                        device_list_endpoint=self.device_list_endpoint),
                        headers={
                            'MyQApplicationId': self.app_id,
                            'SecurityToken': self.security_token
                        }
                )

                devices = devices.json()['Devices']
                return devices

        def get_garagedeviceid(self, description):
		# This gets the device id for the garage door state will be set on
                devices = self.get_devices()
                deviceid = None
                garagedoors = [x for x in devices if x['MyQDeviceTypeName'] == 'GarageDoorOpener']

                for garagedoor in garagedoors:
                        for attrib in garagedoor['Attributes']:
                                if attrib['Value'] == description:
                                        deviceid = garagedoor['MyQDeviceId']
                if deviceid == None:
                        return "Liftmaster device name not found"
                else:
                        return deviceid

        def get_state(self, description):
		# This gets the state of a garage door
                deviceid = self.get_garagedeviceid(description)
                devices = self.get_devices()
                garagedoors = [x for x in devices if x['MyQDeviceTypeName'] == 'GarageDoorOpener']
                garagedoor = garagedoors[0]['Attributes']
                state = [x['Value'] for x in garagedoor if x['AttributeDisplayName'] == "doorstate"]

                return state[0]

        def set_state(self, description):
		# This function assumes the door is either open or closed.  It will toggle it to the other state (if closed, then open)
                state = self.get_state(description)
                device_id = self.get_garagedeviceid(description)
                if state == "1":
                        new_state = "2"
                elif state == "2":
                        new_state = "1"
                print(new_state)

                payload = {
                    'attributeName': 'desireddoorstate',
                    'myQDeviceId': device_id,
                    'AttributeValue': new_state,
                }
                device_action = requests.put(
                    'https://{host_uri}/{device_set_endpoint}'.format(
                        host_uri=self.uri,
                        device_set_endpoint=self.device_set_endpoint),
                        data=payload,
                        headers={
                            'MyQApplicationId': self.app_id,
                            'SecurityToken': self.security_token
                        }
                )

                return device_action.status_code == 200

def lambda_handler(event, context):
	# This is the name of the garage door as listed in the MYQ application, change to whatever suits your needs.  
	x = myqapi()
	x.set_state("GarageDoor")
