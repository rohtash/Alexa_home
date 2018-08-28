import fauxmo
import logging
import time
import sys
import RPi.GPIO as GPIO ## Import GPIO library
 
from debounce_handler import debounce_handler
 
logging.basicConfig(level=logging.DEBUG)
 
class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    
    TRIGGERS = {"abc": 52001,"doha": 52017, "london": 51000, "paris": 53000, "pearl": 52002,"all devices":52025}

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address)
        
        if name=="abc":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(7), state)   ## State is true/false
        elif name =="doha":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(12), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(12), state) ## State is true/false
        elif name =="london":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(11), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(11), state) ## State is true/false
        elif name =="paris":
            GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
            GPIO.setup(int(13), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(13), state) ## State is true/false
        elif name == "pearl":
            GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
            GPIO.setup(int(15), GPIO.OUT)  ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(15), state)  ## State is true/false
        elif name == "all devices":
            GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
            GPIO.setup(int(11), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(11), state) ## State is true/false
            GPIO.setup(int(12), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(12), state) ## State is true/false
            GPIO.setup(int(13), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(13), state) ## State is true/false
            GPIO.setup(int(15), GPIO.OUT)  ## Setup GPIO Pin to OUTPUT
            GPIO.output(int(15), state)  ## State is true/false
        else:
            print("Device not found!")

        return True
       
if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
 
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)
 
    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: "+ e.args  )
            break
