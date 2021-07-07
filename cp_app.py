import time
import random
import osdp
import time

buzzer_cmd = {
    "command": osdp.CMD_BUZZER,
    "reader": 0,
    "control_code": 2,
    "on_count": 10,
    "off_count": 10,
    "rep_count": 1
}

led_cmd = {
    "command": osdp.CMD_LED,
    "reader": 0,
    "led_number": 0,
    "control_code": 2,
    "on_count": 10,
    "off_count": 10,
    "on_color": osdp.LED_COLOR_RED | osdp.LED_COLOR_BLUE,
    "off_color": osdp.LED_COLOR_NONE,
    "timer_count": 10,
    "temporary": True
}

pd_info = [
    # PD_0 info
    {
        "address": 2, # address you configured in PDM
        "flags": 0, # osdp.FLAG_ENFORCE_SECURE
        "channel_type": "uart",
        "channel_speed": 9600,
        "channel_device": '/dev/tty.usbserial-14320', # fill your device name here
    },
    # PD_1 info
    {
        "address": 4,# address you configured in PDM
        "flags": 0, # osdp.FLAG_ENFORCE_SECURE
        "channel_type": "uart",
        "channel_speed": 9600,
        "channel_device": '/dev/tty.usbserial-14320', # fill your device name here
    }
]

key = bytes([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

commands = [ led_cmd, buzzer_cmd ]

def event_handler(address, event):
    print("PD Address: ", address)
    for k, v in event.items():
        if k == "data":
            print ("{}: {}".format(k, v.hex()))
        else:
            print ("{}: {}".format(k, v))

osdp.set_loglevel(7)

cp = osdp.ControlPanel(pd_info, master_key=key)
cp.set_event_callback(event_handler)

count = 0  # loop counter
PD_0 = 0   # PD offset number
PD_1 = 1   # PD offset number
r = 0
while True:
    cp.refresh()

    if (count % 100) == 99 and cp.sc_active(PD_0):
        r=(r+1)%2
        cp.send_command(r, commands[r])

    count += 1
    time.sleep(0.020) #sleep for 20ms
