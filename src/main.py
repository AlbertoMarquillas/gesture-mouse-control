import cv2 #For capturing the video from the camera
import time as t #For calculating the frame rate
import hand_tracking_module as htm #Import the hand tracking module
import math #For calculating the length of the line between the thumb and the index finger
from comtypes import CLSCTX_ALL #For the audio control
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume #For the audio control
import numpy as np #For the volume control


#define with and height of the camera
wCam, hCam = 640, 480

# Create the object for the hand tracking
hand_tracker = htm.HandTrackingModule(maxHands=1, detectionCon=0.75, trackCon=0.75)

#The audio control
devices = AudioUtilities.GetSpeakers() # Get the speakers
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None) # Get the audio interface
volume = interface.QueryInterface(IAudioEndpointVolume) # Get the audio
# volume.GetMute()  # To get the current mute state
# volume.GetMasterVolumeLevel() # To get the current volume level


volRange = volume.GetVolumeRange() # Get the volume range
minVol = volRange[0] # Minimum volume
maxVol = volRange[1] # Maximum volume


# Set the frame rate
previousTime = 0 # Previous time
currentTime = 0 # Current time

# Create the object for the camera
cap = cv2.VideoCapture(0)

vol = 0
volBar = 400

while cap.isOpened():
    # Read the frame from the camera
    success, img = cap.read()
    
    # Find the hand landmarks
    img = hand_tracker.findHands(img)
    
    # Find the position of the hand landmarks
    landMarkList, bbox = hand_tracker.findPosition(img, draw=False)
    
    if len(landMarkList) != 0:
           
        x1, y1 = landMarkList[4][1], landMarkList[4][2] # x and y coordinates of the thumb
        x2, y2 = landMarkList[8][1], landMarkList[8][2] # x and y coordinates of the index finger
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # x and y coordinates of the center of the line between the thumb and the index finger
    
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) # Draw a circle at the thumb
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED) # Draw a circle at the index finger
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) # Draw a circle at the center of the line between the thumb and the index finger, color purple
        #Draw a line between the thumb and the index finger
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        
        # Calculate the length of the line between the thumb and the index finger
        length = math.hypot(x2 - x1, y2 - y1)
        # x2 - x1 = the length of the line in the x-axis
        # y2 - y1 = the length of the line in the y-axis
        
        #Hand range 50 - 300
        #Volume range -65.25 - 0
        
        vol = np.interp(length, [50, 300], [minVol, maxVol]) # Interpolate the volume
        volBar = np.interp(length, [50, 300], [400, 150]) # Interpolate the volume
        volPer = np.interp(length, [50, 300], [0, 100])
        #np.interp(value, [min1, max1], [min2, max2])
        #value = the value to interpolate
        #[min1, max1] = the range of the value
        #[min2, max2] = the range of the interpolated value
        
        
        #print(int(length), volume)
        volume.SetMasterVolumeLevel(vol, None)
        
        if length < 50: # If the length of the line is less than 50, at the minimum volume
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED) # Draw a circle at the center of the line between the thumb and the index finger, color green

        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        
        #Add percentage
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        
        
    
    # Calculate the frame rate
    currentTime = t.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    
    # Display the frame rate
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    
    # Display the image
    cv2.imshow("Image", img)
    
    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Release the camera and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()