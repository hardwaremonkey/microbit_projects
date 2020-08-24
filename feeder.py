''' Positional servo controller.
'''

from microbit import button_a, button_b, display, pin0, sleep

DELAY_FILE = 'delay_minutes.txt'
DELAY_MINUTES = 2

class DelayFile:
    def __init__(self, filename=DELAY_FILE):
        self.filename = filename

    def read(self):
        try:
            with open(filename, 'r') as my_file:
                read_value = my_file.read()
        except Exception as e:
            print('could not read from {}\nerror {}\n'.format(filename, e))
            print('creating file with default value: {}'.format(DELAY_MINUTES))
            self.write(DELAY_MINUTES)
            return DELAY_MINUTES
        return read_value


    def write(self, value):
        with open(filename, 'w') as my_file:
            my_file.write(str(value))
            print('written {} to {}'.format(value, filename))
            my_file.close()

class Servo:
    ''' Creates repeated pulses in a 20ms time window. '''
    def __init__(self, servo_pin=pin0):
        self.pin = servo_pin
        # 20ms gives 50Hz, standard servo signal frequencyinfo2
        print('starting Servo')
        self.pin.set_analog_period(20)


    def set_ms_pulse(self, ms_on):
        # pin.write_analog(1023) is constant on
        # (1023 * ms_on / 20) gives a ms_on pulse
        self.pin.write_analog(1023 * ms_on / 20)


    def set_ms_pulse_invert(self, ms_on):
        ''' Gives inverted logic servo control pulse. '''
        self.pin.write_analog(1023 - 1023 * (ms_on / 20))


    def set_degree(self, deg):
        ''' Set position in degrees. '''
        self.degrees = deg
        # 180 degrees = 1.0 ms pulse, 0 degrees = 2.0 ms pulse
        self.set_ms_pulse(2 + (-self.degrees / 180))
        print('servo set to {} degrees'.format(deg))


    def rotate_clockwise(self):
        new_deg = min(180, self.degrees + 1)
        self.set_degree(new_deg)


    def rotate_counterclockwise(self):
        new_deg = max(0, self.degrees - 1)
        self.set_degree(new_deg)




servo1 = Servo()
delay = DelayFile()

while True:
    sleep(20)
    display.set_pixel(4,0,0)
    display.set_pixel(0,0,0)
    display.set_pixel(2,2,5)

    if button_a.is_pressed() and not button_b.is_pressed():
        display.set_pixel(4,0,0)
        display.set_pixel(0,0,7)
        servo1.set_degree(0)

    if button_b.is_pressed() and not button_a.is_pressed():
        display.set_pixel(0,0,0)
        display.set_pixel(4,0,7)
        servo1.set_degree(180)


