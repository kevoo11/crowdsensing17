import socketserver
import sqlite3
import datetime
import math
import time
#import matplotlib.pyplot as plot
import threading
import socket

conn = sqlite3.connect('crowdsensing.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS sensorsData(deviceID REAL, deviceIP TEXT, temperature REAL, humidity REAL, ozone REAL, CO REAL, NO2 REAL, NH3 REAL, date TEXT)' )
lock = threading.Lock()

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        print('Connection from {}'.format(self.client_address[0]))
        #self.data = self.request.recv(1024)
        #the client's ip
        print("{}\nConnection successful".format(ord(c)) for c in self.data)
        while True:

            self.data = self.request.recv(1024)
            data = self.data
            if data[0] == 0:
                deviceID = self.f(data[0],data[1])
                deviceIP = self.client_address[0]
    
                #current received date
                unix = time.time()
                date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))

                command = self.data[2]
                if command == 68:
                    value = self.updateSensors(data)
                    self.put_database(deviceID, deviceIP, date, value)

    #def graphData(self):
    #    c.execute("SELECT * FROM")

    #function that appends 2 int values
    def f(self, x, y):
        a = math.floor(math.log10(y))
        return int(x * 10 ** (1 + a) + y)

    #function to put necessary data: device id, device ip, date
    def put_database(self, id, ip, date, r):

        try:
            lock.acquire(True)
            c.execute(
                "INSERT INTO sensorsData(deviceID, deviceIP, temperature, humidity, ozone, CO, NO2, NH3, date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                (id, ip, r[0], r[1], r[2], r[3], r[4], r[5], date))
            conn.commit()
        finally:
            lock.release()

    #function that update the sensors value
    def updateSensors(self, data):
        values = []
        for a in range(0, 6):
            sensor_type = data[3 + a * 2] >> 2
            high_byte = (data[3 + a * 2]) & 3
            data_value = data[4 + a * 2] | high_byte << 8 #raw ADC value

            if sensor_type == 1: #temperature sensor
                temp_volt = (3.3 / 1024) * data_value
                temperature = (temp_volt * 1000 - 500) / 10
                #temperature = 24.5


                #window.addstr(0,0,"TEMP", curses.A_BOLD)
                #print("temperature: {} celcius ,".format(nh3_rs))
                values.append(temperature)

            elif sensor_type == 2: #humidity sensor
                #PUT EQUATION HERE
                hum_volt = (3.3/1024) * data_value
                humidity = ((hum_volt/3.3) - 0.1515)/0.00636
                hum_real = humidity/(1.0546- 0.00216 * temperature)

                if hum_real > 100:
                    hum_real = 100
                elif hum_real < 0:
                    hum_real = 0

                #print("humidity: {} % ,".format(hum_real))
                values.append(hum_real)

            elif sensor_type == 3: #ozone sensor
                #PUT EQUATION HERE
                o3_volt = (3.3/1024) * data_value
                o3_rs = 10000 * ((3.3/o3_volt) - 1)
                o3_ro = 38333
                o3_x = o3_rs / o3_ro #ratio
                o3_ppb = pow(10,2.0638) * pow(o3_x, 1.0071)

                if o3_ppb >= 1000:
                    o3_ppb = 1000
                elif o3_ppb <= 10:
                    o3_ppb = 10

                print("O3_rs {} ".format(o3_rs))
                print("ozone: {} ppb ,".format(o3_ppb))
                values.append(o3_ppb)

            elif sensor_type == 4: #CO sensor
                #PUT EQUATION HERE
                co_volt = (3.3/1024) * data_value
                co_rs = 1000000 * ((3.3 / co_volt) - 1)
                co_ro = 237142
                co_x = co_rs / co_ro  # ratio
                co_ppm = pow(10, 0.6519) * pow(co_x, -1.1863)

                if co_ppm >= 1000:
                    co_ppm = 1000
                elif co_ppm <= 1:
                    co_ppm = 1

                print("CO_rs {} ".format(co_rs))
                print("CO: {} ppm ,".format(co_ppm))
                values.append(co_ppm)

            elif sensor_type == 5: #NO2 sensor
                #PUT EQUATION HERE
                no2_volt = (3.3 / 1024) * data_value
                no2_rs = 10000 * ((3.3 / no2_volt) - 1)
                no2_ro = 27000
                no2_x = no2_rs / no2_ro  # ratio
                no2_ppm = pow(10, -0.8171) * pow(no2_x, 1.0072)

                if no2_ppm >= 10:
                    no2_ppm = 10
                elif no2_ppm <= 0.05:
                    no2_ppm = 0.05

                print("NO2_rs {} ".format(no2_rs))
                print("NO2: {} ppm ,".format(no2_ppm))
                values.append(no2_ppm)

            elif sensor_type == 6: #NH3 sensor
                #PUT EQUATION HERE
                nh3_volt = (3.3 / 1024) * data_value
                nh3_rs = 1000000 * ((3.3 / nh3_volt) - 1)
                nh3_ro = 1250000
                nh3_x = nh3_rs / nh3_ro  # ratio
                nh3_ppm = pow(10, -0.1616) * pow(nh3_x, -1.8111)

                if nh3_ppm >= 500:
                    nh3_ppm = 500
                elif nh3_ppm <= 1:
                    nh3_ppm = 1

                print("NH3_rs {} ".format(nh3_rs))
                print("NH3: {} ppm,\n".format(nh3_ppm))
                values.append(nh3_ppm)
        return values

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = 'ec2-13-58-130-73.us-east-2.compute.amazonaws.com' , 1012 #uw's ip
    #HOST, PORT = '192.168.1.8', 888

    # Create the server, binding to localhost on port 8888
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    with server:
        ip, port = server.server_address

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        server.serve_forever()