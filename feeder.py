'''
Automated feeder. A servo activates after an adjustable delay.
The delay can be increased or decreased using the buttons.
Matthew Oppenheim 2020
delay not saving to persistent file
v1.0 First working version.
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

       
def delay_initialise(filename=DELAY_FILE, delay=DELAY_MINUTES):
    ''' Initialise the delay file if it does not already exist. '''
    try:
        delay = delay_readfile(filename)
        print('delay file {} already exists with value {}'.format(
            filename, delay))
    except Exception as e:
        print('could not read from {}\nerror {}\n'.format(
            filename, e))
        print('creating file with value: {}'.format(delay))
        delay_writefile(delay)
    if delay < DELAY_MINUTES:
        delay_writefile(DELAY_MINUTES)

def delay_decrease():
    ''' Decrease the value in the delay file. '''
    delay = delay_readfile()
    delay -= MINUTES_PER_LED
    if delay < 0:
        delay = 0
    delay_writefile(delay)

def delay_get_min():
    return int(delay_readfile())
    
def delay_get_ms():
    ''' Get the delay in ms. '''
    delay_min = delay_get_min()
    delay_ms = delay_min * 60000
    return delay_ms

def delay_increase():
    ''' Increase the value in the delay file. '''
    delay = delay_readfile(DELAY_FILE)
    delay += MINUTES_PER_LED
    if delay > MAX_DELAY_MINUTES:
        delay = MAX_DELAY_MINUTES
    delay_writefile(delay)

def delay_readfile(filename=DELAY_FILE):
    ''' Read from the file on the microbit. '''
    with open(filename, 'r') as my_file:
        content = my_file.read()
    # print('read: {} from: {}'.format(content, filename))
    return int(content)

def delay_writefile(delay):
    ''' Write to the file on the microbit. '''
    with open(DELAY_FILE, 'w') as my_file:
        my_file.write(str(delay))
        print('written {} to {}'.format(delay, DELAY_FILE))


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


def button_a_pressed():
    ''' Increase the time delay. '''
    print('button a press detected')
    display.show('-')
    sleep(20)
    display.clear()
    delay_decrease()
    display_show_delay(delay_get_min())


def button_b_pressed():
    ''' Decrease the time delay. '''
    print('button b press detected')
    display.show('+')
    sleep(20)
    display.clear()
    delay_increase()
    display_show_delay(delay_get_min())


def display_create_image(num_leds):
    ''' Create the leds_image of num_leds. '''
    leds_string = BRIGHT * num_leds
    leds_string = ":".join(leds_string[i:i+5]
        for i in range(0, len(leds_string), 5))
    leds_image = Image(leds_string + ':')
    return leds_image


def display_show_delay(delay_in_minutes):
    ''' Display the remaining delay. '''
    num_leds = minutes_to_leds(delay_in_minutes)
    display.show(display_create_image(num_leds))


def minutes_to_leds(minutes):
    ''' How many LEDS to light to represent minutes of time. '''
    # add 0.5 as int always rounds down
    num_leds = int(minutes/MINUTES_PER_LED+0.5)
    if num_leds < 1:
        num_leds = 1
    return num_leds 


def ms_to_min(ms):
    ''' Convert ms to minutes. '''
    return ms/60000


# setup servo on pin0
# Creates repeated pulses in a 20ms time window.
pin0.set_analog_period(20)
servo_set_degree(0, pin0)
delay_initialise()

start_tick = time.ticks_ms()
print('start_tick: {}'.format(start_tick))
target_ticks = delay_get_ms() + start_tick
display_show_delay(delay_get_min())

while time.ticks_diff(delay_get_ms()+start_tick, time.ticks_ms()) > 0:
#    ticks_left = ticks_diff(delay_file.get_delay_ms(), start_tick)
#    print('remaining ticks:'.format(ticks_left))
    sleep(100)
    # elapsed_ticks = time.ticks_ms() - start_tick
    remaining_tics = time.ticks_diff(delay_get_ms()+start_tick, time.ticks_ms())
    # add 0.5 as int always rounds down
    remaining_minutes = int(ms_to_min(remaining_tics)+0.5)
    # print('remaining_minutes: {}'.format(remaining_minutes))
    display_show_delay(remaining_minutes)

    if button_a.was_pressed() and not button_b.was_pressed():
       button_a_pressed()

    if button_b.was_pressed() and not button_a.was_pressed():
       button_b_pressed()

servo_set_degree(180, pin0)
display.clear()


