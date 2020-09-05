'''
Automated feeder. A servo activates after an adjustable delay.
The delay can be increased or decreased using the buttons.
Matthew Oppenheim 2020
delay not saving to persistent file
v0.1
'''

# from microbit import button_a, button_b, display, Image, pin0, time
from microbit import *
import time as time

BRIGHT = '7'
DELAY_FILE = 'delay_minutes.txt'
# delay in minutes until the feeder activates
DELAY_MINUTES = 12
# maximum number of LEDs on the board
LEDS = 25
# maximum number of LEDs to use
MAX_DELAY_LEDS = 25
# maximum delay
MAX_DELAY_MINUTES = 300
# how many minutes delay an active LED represents
MINUTES_PER_LED = 12

class DelayFile:
    ''' Handle the file containing the delay time on the microbit. '''
    def __init__(self, filename=DELAY_FILE, delay=DELAY_MINUTES):
        self.filename = filename
        try:
            self.delay = self.readfile(filename)
            print('delay file {} already exists with value {}'.format(
                filename, self.delay))
        except Exception as e:
            print('could not read from {}\nerror {}\n'.format(
                self.filename, e))
            print('creating file with value: {}'.format(delay))
            self.writefile(delay)
            self.delay = delay
        

    def decrease_delay(self):
        ''' Decrease the value in the delay file. '''
        self.delay -= MINUTES_PER_LED
        if self.delay < 0:
            self.delay = 0
        self.writefile(self.delay)

    def get_delay_min(self):
        return self.delay
        
    def get_delay_ms(self):
        ''' Get the delay in ms. '''
        return self.delay * 60 * 1000

    def increase_delay(self):
        ''' Increase the value in the delay file. '''
        self.delay += MINUTES_PER_LED
        if self.delay > MAX_DELAY_MINUTES:
            self.delay = MAX_DELAY_MINUTES
        self.writefile(self.delay)

    def readfile(self, filename):
        ''' Read from the file on the microbit. '''
        with open(filename, 'r') as my_file:
            content = my_file.read()
        return content 

    def writefile(self, value):
        ''' Write to the file on the microbit. '''
        with open(self.filename, 'w') as my_file:
            my_file.write(str(value))
            print('written {} to {}'.format(value, self.filename))


def servo_set_ms_pulse(ms_on, pin):
        # pin.write_analog(1023) is constant on pulse
        # (1023 * ms_on / 20) gives a pulse of length ms_on
        # pulse sets the servo angle
        pin.write_analog(1023 * ms_on / 20)


def servo_set_degree(degrees, pin):
    ''' Set servo position in degrees. '''
    # 180 degrees = 1.0 ms pulse, 0 degrees = 2.0 ms pulse
    servo_set_ms_pulse(2 + (-degrees / 180), pin)
    print('servo set to {} degrees'.format(degrees))



def button_a_pressed(delay_file):
    ''' Increase the time delay. '''
    print('button a press detected')
    display.show('-')
    sleep(20)
    display.clear()
    delay_file.decrease_delay()
    display_show_delay()

def button_b_pressed(delay_file):
    ''' Decrease the time delay. '''
    print('button b press detected')
    display.show('+')
    sleep(20)
    display.clear()
    delay_file.increase_delay()
    display_show_delay()


def display_create_image(num_leds):
    ''' Create the leds_image of num_leds. '''
    leds_string = BRIGHT * num_leds
    leds_string = ":".join(leds_string[i:i+5]
        for i in range(0, len(leds_string), 5))
    leds_image = Image(leds_string + ':')
    return leds_image


def display_show_delay():
    ''' Display the remaining delay. '''
    num_leds = minutes_to_leds(delay_file.get_delay_min())
    display.show(display_create_image(num_leds))


def minutes_to_leds(minutes):
    ''' How many LEDS to light to represent minutes of time. '''
    return int(minutes / MINUTES_PER_LED)


# setup servo on pin0
# Creates repeated pulses in a 20ms time window.
pin0.set_analog_period(20)
servo_set_degree(0, pin0)
delay_file = DelayFile(DELAY_FILE, DELAY_MINUTES)

start_tick = time.ticks_ms()
print('start_tick: {}'.format(start_tick))
target_ticks = delay_file.get_delay_ms() + start_tick
display_show_delay()

while time.ticks_diff(delay_file.get_delay_ms()+start_tick, time.ticks_ms()) > 0:
#    ticks_left = ticks_diff(delay_file.get_delay_ms(), start_tick)
#    print('remaining ticks:'.format(ticks_left))
    sleep(100)
    elapsed_ticks = time.ticks_ms() - start_tick
    remaining_tics = time.ticks_diff(delay_file.get_delay_ms()+start_tick, time.ticks_ms())
    # print('remaining_ticks {}'.format(remaining_tics)) 

    if button_a.was_pressed() and not button_b.was_pressed():
       button_a_pressed(delay_file)

    if button_b.was_pressed() and not button_a.was_pressed():
       button_b_pressed(delay_file)

servo_set_degree(180, pin0)


