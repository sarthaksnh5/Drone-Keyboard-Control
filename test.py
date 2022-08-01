import time
from dronekit import connect, VehicleMode
import keyboard

roll = 1500
yaw = 1500
pitch = 1500
throttle = 1500

time.sleep(2.0)

try:
    vehicle = connect('/dev/ttyACM0', wait_ready=True)      

    def takeoff():
        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        vehicle.mode = VehicleMode('STABILIZE')
        print("Vehicle taking off")
        vehicle.mode = VehicleMode('LOITER')

        while not vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        vehicle.armed = True  
        
        # time.sleep(20)
        # print('Entering in circle mode')
        # vehicle.mode = VehicleMode('CIRCLE')

    def manualMode():
        print('Enter in manual mode')
        global roll, yaw, throttle, pitch
        vehicle.mode = VehicleMode('LOITER')
        thresh = 200

        while True:
            roll = 1500
            yaw = 1500
            throttle = 1500
            pitch = 1500

            if keyboard.is_pressed('s'):
                pitch = 1500 + thresh

            if keyboard.is_pressed('w'):
                pitch = 1500 - thresh

            if keyboard.is_pressed('d'):
                roll = 1500 + thresh  

            if keyboard.is_pressed('a'):
                roll = 1500 - thresh                                 
            
            if keyboard.is_pressed('up'):
                throttle = 1500 + thresh

            if keyboard.is_pressed('down'):
                throttle = 1500 - thresh

            if keyboard.is_pressed('right'):
                yaw = 1500 + thresh 

            if keyboard.is_pressed('left'):
                yaw = 1500 - thresh          

                

            
            if keyboard.is_pressed('q'):
                vehicle.mode = VehicleMode('RTL')
                break

            vehicle.channels.overrides = {
                '1': int(roll),
                '2': int(pitch),
                '3': int(throttle),
                '4': int(yaw)
            }


    takeoff()

    while True:

        if keyboard.is_pressed('m'):
            manualMode()

        if keyboard.is_pressed('e'):
            print("Enter in RTL Mode")
            vehicle.mode = VehicleMode('RTL')
            vehicle.close()
            break

    # Close vehicle object before exiting script
    # print("Close vehicle object")
    # vehicle.close()

except Exception as e:
    vehicle.mode = VehicleMode('RTL')
    vehicle.close()
    print(e)
