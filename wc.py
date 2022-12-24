from gpiozero import AngularServo
from gpiozero import Button
from time import sleep
import requests
import json
from gpiozero.pins.pigpio import PiGPIOFactory
pigpio_factory = PiGPIOFactory()

button1 = Button(19)
button2 = Button(26)

servo =AngularServo(18, min_angle=0, max_angle = 180, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=pigpio_factory)

servo.angle = 0 # Cerrado
url = 'http://dev.relred.com/soldix/api/transactions'


while True:
    user = input('Scan QR\n')
    payload = { 'u_id': user, 'p_id': 'p6368e1c90d9bc' }
    response = requests.post(url, json=payload)
    print(response.url)
				
    if response.status_code == 200:
        result = response.json()
        if result['message'] == 'SUCCESS':
            print("Transaccion exitosa, abriendo puerta")
            servo.angle = 90 # Abierto
            button1.wait_for_release()
            button1.wait_for_press()
            print("Cerrando puerta")
            servo.angle = 0 # Cerrado
            button2.wait_for_press()
            print("Abriendo puerta")
            servo.angle = 90 # Abierto
            button1.wait_for_release()
            button1.wait_for_press()
            print("Cerrando puerta\n")
            servo.angle = 0 # Cerrado
        if result['message'] == 'FAIL':
            print("Fondos Insuficientes\n")
            continue
