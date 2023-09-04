import wiotp.sdk.application
import time    
import wiotp.sdk.application
import warnings
warnings.filterwarnings('ignore')

options = wiotp.sdk.application.parseConfigFile("application.yaml")
client = wiotp.sdk.application.ApplicationClient(config=options)
client.connect()

while True:
    try:
        data = {
            "time" : time.time(),
            "state": "active"
        }
        client.publishEvent(typeId="RaspberryPi", deviceId="1", eventId="pi_status", msgFormat="json", data={'state':data})
        print(data)
        time.sleep(30)
    except Exception as e:
        print("Exception: ", e)