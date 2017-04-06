import socketserver
import sqlite3
connect = sqlite3.connect('crowdsensing.db')
c = connect.cursor()

#TCP connection
class CrowdSensingHandler(socketserver.BaseRequestHandler):

    def handle (self):
        #self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print ("yo".format(self.client_address[0]))
        print (self.data)

        #to send back the data
        self.request.sendall(self.data)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8888

    server = socketserver.TCPServer((HOST, PORT), CrowdSensingHandler)

    #Keeping the server to run until Ctrl-C is called
    server.serve_forever()

class Crowdsensing:

    #initialize variables
    def __init__(self):
        self.DeviceID = ""
        self.DeviceIP = ""
        self.Ro = [0.0,0.0,0.0,0.0,0.0]
        self.Sensors = [1,2,3,4,5,6]
        self.GPSLoc = 0.0
        self.DateInitialized = ""
        self.SensorsSize =

    def UpdateRo(self):
        if CrowdSensingHandler.data[2] == "R": #command for Ro; for loop


    def database(self):


    def UpdateSensors(self):
        if CrowdSensingHandler.data[2] == "S": #command to update sensors; for loop


    def Decode(self, CrowdSensingHandler): #formula for calibaration


    def FormatData(self):

    def UpdateGPS (self):
        self.GPSLoc = 123456 #some float from data

    def UpdateDeviceID (self):
        self.DeviceID = {CrowdSensingHandler.data[0], CrowdSensingHandler[1]}

