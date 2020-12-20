import blynklib

from sense_hat import SenseHat

sense = SenseHat()

sense.clear()

BLYNK_AUTH = '39GdI0DcuPiMwH-zf0vlmojtrdZqB0Ae'

blynk = blynklib.Blynk(BLYNK_AUTH)

# register handler for virtual pin V1(temperature) reading
@blynk.handle_event('read V1')
def read_virtual_pin_handler(pin):
    temp=round(sense.get_temperature(),2)
    humidity=round(sense.get_humidity(),2)
    print('V1 Read: ' + str(temp))  # print temp to console
    print('V2 Reed: ' + str(humidity))   
    blynk.virtual_write(1, temp)
    blynk.virtual_write(2, humidity)


while True:
    blynk.run()
    