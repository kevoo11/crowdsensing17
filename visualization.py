import socketserver
import sqlite3
import datetime
import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

#style.use('fivethirtyeight')

conn = sqlite3.connect('crowdsensing.db', check_same_thread=False)
c = conn.cursor()
#c.execute('CREATE TABLE IF NOT EXISTS sensorsData(deviceID REAL, deviceIP TEXT, temperature REAL, humidity REAL, ozone REAL, CO REAL, NO2 REAL, NH3 REAL, date TEXT, gps REAL)' )



def pullDatabase(id):
    #c.execute('SELECT * FROM(SELECT * FROM sensorsData WHERE deviceID=1 ORDER BY sortfield ASC limit 20) ORDER BY sortfield DESC')
    c.execute('SELECT * FROM (SELECT * FROM capsFair Where deviceID=? order by date DESC limit 30) order by date ASC', (id,))
    #print(c.fetchmany(20))
    temp, hum, ozone = [],[],[]
    co = []
    no2 = []
    nh3 = []
    date = []
    for row in c.fetchall():
        no2.append(row[6])
        nh3.append(row[7])
        co.append(row[5])
        ozone.append(row[4])
        hum.append(row[3])
        temp.append(row[2])
        date.append(datetime.datetime.strptime(row[8], "%Y-%m-%d %H:%M:%S"))
    return temp, hum, ozone, co, no2, nh3, date

def graphTable(i, id):
    temp, hum, ozone, co, no2, nh3, date =  pullDatabase(id)
    sub1.clear()
    sub1.plot_date(date,temp, "-", linewidth=2)
    sub1.set_title('temperature')
    #sub1.set_xlabel('time')
    sub1.set_ylabel('degree Celcius')
    sub1.axes.get_xaxis().set_visible(False)

    sub2.clear()
    sub2.plot_date(date,hum, "-", linewidth=2)
    sub2.set_title('humidity')
    #sub2.set_xlabel('time')
    sub2.set_ylabel('unit')
    sub2.axes.get_xaxis().set_visible(False)

    sub3.clear()
    sub3.plot_date(date, ozone, "-", linewidth=2)
    sub3.set_title('ozone')
    #sub3.set_xlabel('time')
    sub3.set_ylabel('ppb')
    sub3.axes.get_xaxis().set_visible(False)

    sub4.clear()
    sub4.plot_date(date, co, "-", linewidth=2,color='b')
    sub4.set_title('CO')
    #sub4.set_xlabel('time')
    sub4.set_ylabel('ppm')
    sub4.axes.get_xaxis().set_visible(False)

    sub5.clear()
    sub5.plot_date(date, no2, "-", linewidth =2, color='m')
    sub5.set_title('NO2')
    sub5.set_xlabel('time')
    sub5.set_ylabel('ppm')

    sub6.clear()
    sub6.plot_date(date, nh3, "-", linewidth =2, color='c')
    sub6.set_title('NH3')
    sub6.set_xlabel('time')
    sub6.set_ylabel('ppm')

deviceID = input("Which device you would like to graph ?")

fig = plt.figure()
fig.suptitle('Sensors reading', fontsize=28, fontweight='bold')

sub1 = fig.add_subplot(3,2,1) #temperature

sub2 = fig.add_subplot(3,2,2) #humidity

sub3 = fig.add_subplot(3,2,3) #ozone

sub4 = fig.add_subplot(3,2,4) #the rest with ppm

sub5 = fig.add_subplot(3,2,5)

sub6 = fig.add_subplot(3,2,6)

ani = animation.FuncAnimation(fig,graphTable, fargs=deviceID ,interval=1000)
#graphTable()
plt.show()
c.close()
conn.close()
