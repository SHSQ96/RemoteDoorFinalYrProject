from flask import Flask, render_template, request,send_from_directory
from time import sleep
from urllib.request import urlopen
import json


app = Flask(__name__)


READ_API_KEY='EUBLAYYE4IRCKO2L'
CHANNEL_ID=1314542



CHANNEL_ID_DOOR=1336510
DOOR_CHANNEL_WRITE_API_KEY='I97YZCF8GPKC39TG'

def readSpeak():
    conn = urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (CHANNEL_ID,READ_API_KEY))
    response = conn.read()
    print("http status code=%s" % (conn.getcode()))
    data=json.loads(response)
    print(data['field1'],"created at ",data['created_at'])        
    conn.close()
    # sleep(16)
    return data['field1']

def writeSpeak(api_key, value):
    baseURL = f"http://api.thingspeak.com/update?api_key={api_key}&field1="
    f = urlopen(baseURL +str(value))
    f.read()
    f.close()
    print(f"Sent the value {value}")
    return 0    

@app.route('/openDoor',methods=["POST"])
def openDoor():
    '''
    simply open the door
    '''
    print("Going to write to thingspeak")
    value=1
    status=writeSpeak(DOOR_CHANNEL_WRITE_API_KEY,value)
    dicnry={}
    if status==0:
        dicnry["door_opened"]=1
        data=readSpeak()
        if data==-1:
            print("No data returned")
        print(data)
        
        dicnry["data"]=data
        return render_template("index.html",data=dicnry)
    else:
        return "Some problem in sending command to open the door"




@app.route('/readDoor')
def readDoor():
    print("Some one called read door")
    data=readSpeak()
    if data==-1:
        print("No data returned")
    print(data)
    dicnry={}
    dicnry["data"]=data
    return render_template("index.html",data=dicnry)


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)

