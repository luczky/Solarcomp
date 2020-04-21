#!/usr/bin/python

# scrypt do odczytu po rs485 ze sterownika Solarcomp 951
import time
import serial
import requests

# tutaj trzeba poprawic na swoj numer idx czujnika
poz1 = 27   # poz1-panel solarny
poz2 = 28   #poz2-zasobnik-dol
poz3 = 29   #poz3-zasobnik gora
poz4 = 30   #poz4-pompa
poz5 = 33   #poz5 moc chwilowa i moc dzien (2 wartosci)

while True:
    ser = serial.Serial(
        port='/dev/ttyUSB0',    #moze trzeba zmienic
        baudrate = 4800,            #ustawic ten sam co w sterowniku
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    znakodczyt = bytearray(b'\x01\x01\x02\x03\x0a\x0b\x0c')
    data = bytearray(b'\x81\x54\x01\x5A\x78\x78\x01\x78\x78\x78\x23')
    def zapytanie(wartosc):
        nrodczyt = wartosc
        data[6] = znakodczyt[nrodczyt]
        #print data[6]
        ser.write(data)
    def odpowiedz(idx, dzielnik):
        x = []
        x=ser.read(11)
        znak = x[7]
        numer1 = x[8]
        numer2 = x[9]
        temperatura = []
        temperatura.append(znak)
        temperatura.append(ord(numer1))
        temperatura.append(ord(numer2))
        if temperatura[2] < 10:
            temperatura[2] = str(temperatura[2])
            temperatura[2] = ('0' +temperatura[2])
            temp = (str(temperatura[1]) +temperatura[2])
        else:
            temp = (str(temperatura[1])) + (str(temperatura[2]))
        temp = float(temp)/dzielnik
        requests.post('http://192.168.1.38:8084/json.htm?type=command&param=udevice&idx=' +(str(idx)) +'&svalue=' +(str(temp)))
        #print temp
        time.sleep(1)

    zapytanie(1)
    odpowiedz(poz1, 10)

    zapytanie(2)
    odpowiedz(poz2, 10)

    zapytanie(3)
    odpowiedz(poz3, 10)

    zapytanie(4)
    odpowiedz(poz4,1)
#
    def pytmoc():
        moc = []
        moc=ser.read(11)
        znak = moc[7]
        numer1 = moc[8]
        numer2 = moc[9]
        temperatura = []
        temperatura.append(znak)
        temperatura.append(ord(numer1))
        temperatura.append(ord(numer2))
        global mocpyt
        mocpyt = (str(temperatura[1])) + (str(temperatura[2]))

    zapytanie(5)
    pytmoc()
    mocw = float(mocpyt)*100

    time.sleep(1)
#
    zapytanie(6)
    pytmoc()

    mocd = (mocpyt)
#
    ser.close()
    requests.post('http://192.168.1.38:8084/json.htm?type=command&param=udevice&idx=' +(str(poz5)) +'&svalue=' +(str(mocw)) +';' +(str(mocd)))
    #print mocw
    #print mocd
    time.sleep(30)
# jak dziala to mozna wszystkie "print" usunac lub zahashowac
