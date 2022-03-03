import requests

class Senders(object):

    def __init__(self):
        url = "http://127.0.0.1:5000/"
        self.sendFile = url + "fileCheck3d/"
        self.getFarmId = url + "farm/getfarmid"
        self.deviceid = ""
        self.deviceid_data = {'device_id': 4}
        # Add RFID tag

    def sendFile(self,path):
        response_farmid = requests.post(self.sendFile, headers={"X-Api-Key": "ZgDaEwHgZideHuGp5My83g",
                                                                "Content-Type": "application/json"}, json=self.deviceid_data)
        data_farmid = {"farm_id": response_farmid.json()["farm_id"]}
        files = {'file': open(path, 'rb')}
        response = requests.put(self.sendFile(), headers={"X-Api-Key": "ZgDaEwHgZideHuGp5My83g", "enctype": "multipart/form-data"},
                                data=data_farmid, files=files)
        return response.json()