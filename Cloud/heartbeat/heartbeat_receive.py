import wiotp.sdk.application
import time

def myEventCallback(event):
    status = event.data['state']
    print(status)
    with open('/var/www/FlaskApp/FlaskApp/heartbeat/pi_active.csv', 'a') as f:
            f.write(f"\n{status['time']},{status['state']}")
            f.close()

path = "application.yaml"
options = wiotp.sdk.application.parseConfigFile(path)
client = wiotp.sdk.application.ApplicationClient(config=options)
client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(eventId="pi_status")


if __name__ == "__main__":
    while True:
        time.sleep(0.2)
