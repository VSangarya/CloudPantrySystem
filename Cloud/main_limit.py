import wiotp.sdk.application
import time

client = None
status = None

def myEventCallback(event):
    status = event.data['state']
    print(status)
    ts = int(time.time())
    milk = status["Milk"]
    sugar = status["Sugar"]
    cp = status["Coffee powder"]
    tp = status["Tea powder"]
    with open('/var/www/FlaskApp/FlaskApp/response.csv', 'a') as f:
            f.write(f"\n{ts},{milk},{sugar},{cp},{tp}")
            f.close()


path = "application.yaml"
options = wiotp.sdk.application.parseConfigFile(path)
client = wiotp.sdk.application.ApplicationClient(config=options)
client.connect()
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents(eventId="weight_status")


if __name__ == "__main__":
    with open('/var/www/FlaskApp/FlaskApp/response.csv', 'w') as f:
        f.write(f"{'Time'},{'Milk'},{'Sugar'},{'Coffee_powder'},{'Tea_powder'}")
        f.close()
        pass
    while True:
        time.sleep(0.2)
