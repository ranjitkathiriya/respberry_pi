import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

string_tagid = "S123457345"
url = 'http://127.0.0.1:5000/fileCheck3d/'+ string_tagid
url_getfarmid = "http://127.0.0.1:5000/farm/getfarmid"

data = {'device_id': 4}

response_farmid = requests.post(url_getfarmid, headers={"X-Api-Key": "ZgDaEwHgZideHuGp5My83g","Content-Type":"application/json"},json=data)

data_farmid = {"farm_id":response_farmid.json()["farm_id"]}

files = {'file': open('Data/lod_100.off','rb')}

response = requests.put(url, headers={"X-Api-Key": "ZgDaEwHgZideHuGp5My83g","enctype":"multipart/form-data"},data=data_farmid,files=files)
print(response.json())