import websocket
import json
import threading
import time
import requests
import os


def send_json_request(ws, request):
    ws.send(json.dumps(request))


def receive_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)


def heartbeat(interval, ws):
    print("heartbeat begin")
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")


ws = websocket.WebSocket()
ws.connect("wss://gateway.discord.gg/?v=6&encording=json")
event = receive_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval']/1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = "OTUwMzExMTUxMTc3MTkxNDU2.YiXHDg.lVO7l0IeKOVw0rXrFYDOlJRR9vY"

payload = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": "pc"
        }
    }
}

header = {
    'authorization': token,
}

send_json_request(ws, payload)

while True:
    event = receive_json_response(ws)

    try:
        username = event['d']['author']['username']
        content = event['d']['content']
        channel_id = event['d']['channel_id']

        f = open("log.csv", "a")
        f.write(channel_id+","+username+","+content+"\n")
        f.close()

        if ".decode" in content:
            content = content.lower()
            a = content.split("$")
            dc = ""
            for char in a:
                if char == " ":
                    dc += " "
                else:
                    dc += str(int(char)-int('a'))+"-"
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={
                              "content": dc"})

        if username == "i have no brain" and content == ".log":
            files = {
                "file": ("./log.csv", open("./log.csv", 'rb'))
            }

            r = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, files=files)
        elif username == "i have no brain" and content == ".status":
            r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={
                              "content": "Looking good, if I can survive until 1/4, this method will work fine, discord forget to fix bug, hopefully :D"})
        elif username == "i have no brain" and content == ".clear":
            os.remove("log.csv")
            f = open("log.csv", "a")
            f.write("channel_id,author,message_content\n")
            f.close()
            r = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=header, data={"content": "Done!"})

        op_code = event("op")
        if op_code == 11:
            print("heartbeat received")
    except:
        pass
