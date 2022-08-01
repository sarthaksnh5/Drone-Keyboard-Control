import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import cv2
from real_time_object_detection import getLocation
import keyboard

print("[INFO] starting video stream...")
cap = cv2.VideoCapture(0)
roll = 1500
yaw = 1500
pitch = 1500
throttle = 1500

time.sleep(2.0)

try:
    vehicle = connect('127.0.0.1:14550', wait_ready=True)
    vehicle.armed = True

    def visionMode():
        print("Entering in Vision Mode")
        vehicle.mode = VehicleMode('FBWB')
        vehicle.channels.overrides = {'2': 1500}
        while True:
            centerX, centerY = getLocation(cap)            
            if centerX < 218:
                vehicle.channels.overrides = {'4': 1000}
                print('Left')
            if centerX > 218 and centerX < 369:
                vehicle.channels.overrides = {'4': 1500}
                print('Center')
            if centerX > 369:
                vehicle.channels.overrides = {'4': 2000}
                print('Right')

            if centerY < 174:
                vehicle.channels.overrides = {'3': 2000}
                print('Up')
            if centerY > 174 and centerY < 304:
                vehicle.channels.overrides = {'3': 1500}
                print('center')
            if centerY > 304:
                vehicle.channels.overrides = {'3': 1000}
                print('Down')
            

            if keyboard.is_pressed('q'):
                print('Exiting vision mode')
                vehicle.mode = VehicleMode('CIRCLE')
                cv2.destroyAllWindows()
                break

    def takeoff():
        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        vehicle.mode = VehicleMode('STABILIZE')
        print("Vehicle taking off")
        vehicle.mode = VehicleMode('LOITER')

        while not vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)
        
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
                vehicle.mode = VehicleMode('CIRCLE')
                break

            vehicle.channels.overrides = {
                '1': int(roll),
                '2': int(pitch),
                '3': int(throttle),
                '4': int(yaw)
            }


    takeoff()

    while True:
        if keyboard.is_pressed('v'):
            visionMode()

        if keyboard.is_pressed('m'):
            manualMode()

        if keyboard.is_pressed('e'):
            print("Enter in RTL Mode")
            vehicle.mode = VehicleMode('RTL')
            vehicle.close()
            cap.release()
            cv2.destroyAllWindows
            break

    # Close vehicle object before exiting script
    # print("Close vehicle object")
    # vehicle.close()

except Exception as e:
    vehicle.mode = VehicleMode('RTL')
    vehicle.close()
    print(e)
