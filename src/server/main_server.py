import socket
import threading
import csv
import requests
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

cap_threshold = 200 
cloth_threshold = 8
window = 20

cloth_cnt = 0
cloth_flag = False
rain_flag = False
motor_flag = False
loop = 0

bind_ip = '0.0.0.0'
bind_port = 12344

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)
print('listen {}:{}'.format(bind_ip, bind_port))

client1 = None  

def handle_client(client_socket):
    global cloth_cnt, cloth_flag, rain_flag, motor_flag, loop, client1
    
    if client1 is None:
        raddr = client_socket.getpeername()
        client1 = raddr[0]
        print(f"Clinet1 set: {client1}")
    
    bufsize=1024
    request = client_socket.recv(bufsize)
       
    message = request.decode()
    print('recv: {}' .format(message))
    m_list = message.split(",")
    
    if message.startswith("GET"):
        lines = message.split("\r\n")
        parts = lines[0].split(" ")
        if len(parts) >= 2:
            path = parts[1]  
            if path == "/MOTOR":
                if client1:
                    motor_flag = True
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nCommand sent to Client1"
                    client_socket.send(response.encode())
                    print("MOTOR_FLAG ON")
                else:
                    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nClient1 not connected"
                    client_socket.send(response.encode())
                    print("Client1 not connected")
            else:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nInvalid request"
                client_socket.send(response.encode())
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMalformed HTTP request"
            client_socket.send(response.encode())        
    elif (len(m_list) == 2):
        try:
            time = float(m_list[0])
            cap = float(m_list[1])
        except ValueError:
            client_socket.send(b'ERROR\r\n')
        else: 
            loop += 1
            if cap <= cap_threshold:
                cloth_cnt += 1           
            if (loop >= window):
                rain_water = receive_weather()
                if (rain_flag == False) and (rain_water != 0.0):
                    client_socket.send(b'MOTOR\r\n')
                    send_line_notify('\nWarning!\n雨が降り始めました。洗濯物を回収してください。')
                    rain_flag = True
                elif (cloth_flag == False) and (cloth_cnt >= cloth_threshold):
                    client_socket.send(b'OK\r\n')
                    send_line_notify('洗濯物が乾きました。洗濯物を回収できます。')
                    cloth_flag = True
                else:
                    client_socket.send(b'OK\r\n')               
                cloth_cnt = 0
                loop = 0                  
            elif (motor_flag == True and addr[0] == client1):
                client_socket.send(b"MOTOR\r\n")
                send_line_notify('洗濯物が守られました。')
                print("MOTOR command sent to Client1")
                motor_flag = False                
            else:
                client_socket.send(b'OK\r\n')               
            with open('Capacity.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([loop, cap])
    else: 
        client_socket.send(b'ERROR\r\n')

def send_line_notify(message):
    line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'{message}'}
    requests.post(line_notify_api, headers = headers, data = data)
    
def receive_weather():
    now = datetime.datetime.now()
    yahoo_url = "https://map.yahooapis.jp/weather/V1/place?appid={appid}&coordinates={lat_lon}&output={output}&date={date}"
    yahoo_url = yahoo_url.format(appid=os.environ['YAHOO_APPID'], lat_lon=os.environ['YAHOO_COORDINATES'], output="json",
                             date=now.strftime("%Y%m%d%H%M"))
    yahoo_json = requests.get(yahoo_url).json()
    yahoo_rainfall = yahoo_json["Feature"][0]["Property"]["WeatherList"]["Weather"][0]["Rainfall"]
    return yahoo_rainfall
    
while True:
    client, addr = server.accept()
    print('connected from: {}:{}'.format(addr[0],addr[1]))
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()