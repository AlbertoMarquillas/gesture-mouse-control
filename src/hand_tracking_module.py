import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='google.protobuf.symbol_database')

import cv2 # OpenCV library for computer vision to capture and process images
import mediapipe as mp # MediaPipe library for hand tracking to detect landmarks
import time as t # To calculate the frame rate
import math # To calculate the distance between landmarks

#create a class to handle the hand tracking
class HandTrackingModule():
    
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5, webcam=0):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.webcam = webcam

        # Create the object for hand tracking
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands, min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)
        # Create the object to draw the landmarks
        self.mpDraw = mp.solutions.drawing_utils
        
        self.tipIds = [4, 8, 12, 16, 20] # List of the landmarks of the tips of the fingers

    def findHands(self, img, draw=True):
        # Convert the frame to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # MediaPipe accepts RGB images

        # Process the frame to detect the landmarks
        self.results = self.hands.process(imgRGB) # results contains the landmarks
        # results is a dictionary with the following keys: 'multi_hand_landmarks', 'multi_handedness' 

        #print(self.results.multi_hand_landmarks) #Detect if there are hands in the frame

        if self.results.multi_hand_landmarks: # If there are hands in the frame
            for handLandmarks in self.results.multi_hand_landmarks: # For each hand detected      
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS, self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                               self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
                    
                    #img: original image
                    #handLandmarks: landmarks detected of a single hand
                    #HAND_CONNECTIONS: connections between the landmarks
                    #DrawingSpec: specifications of the drawing
                    #color: color of the lines
                    #thickness: thickness of the lines
                    #circle_radius: radius of the circles

        return img

    #img: original image
    #handNo: number of the hand to detect
    #draw: draw the landmarks on the image
    def findPosition(self, img, handNo=0, draw=True):
        
        xList = [] # List to store the x-coordinates of the landmarks
        yList = [] # List to store the y-coordinates of the landmarks
        bbox = [] # List to store the bounding box of the hand
        
        self.landMarkList = [] # List to store the landmarks

        if self.results.multi_hand_landmarks: # If there are hands in the frame
            hand = self.results.multi_hand_landmarks[handNo] # Get the landmarks of the handNo hand
            for id, lm in enumerate(hand.landmark):
                # id: id of the landmark
                # lm: landmark
                h, w, c = img.shape # Height, width, and channels of the image
                #channels are the colors of the image
                cx, cy = int(lm.x*w), int(lm.y*h) # Coordinates of the landmark
                #print(id, cx, cy) # Print the id and the coordinates of the landmark

                xList.append(cx) # Append the x-coordinate to the list
                yList.append(cy) # Append the y-coordinate to the list

                self.landMarkList.append([id, cx, cy]) # Append the id and the coordinates of the landmark to the list
                #landMarkList: list of landmarks
                #id: id of the landmark
                #cx: x-coordinate of the landmark
                #cy: y-coordinate of the landmark
                
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    #img: original image
                    #(cx, cy): coordinates of the landmark
                    #15: radius of the circle
                    #(255, 0, 255): color of the circle
                    #cv2.FILLED: fill the circle


            xmin, xmax = min(xList), max(xList) # Minimum and maximum x-coordinates of the landmarks
            ymin, ymax = min(yList), max(yList) # Minimum and maximum y-coordinates of the landmarks
            bbox = xmin, ymin, xmax, ymax # Bounding box of the hand
            
            
            if draw:
                cv2.rectangle(img, (bbox[0] -20, bbox[1] -20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)
                
            
                # Draw a circle on the landmarks
                #if id == 0: # If the landmark is the first one
                    #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    #img: original image
                    #(cx, cy): coordinates of the landmark
                    #15: radius of the circle
                    #(255, 0, 255): color of the circle
                    #cv2.FILLED: fill the circle
            
        return self.landMarkList, bbox

    # Create a function to detect thumb up
    def thumbUp(self):
        return self.landMarkList[self.tipIds[0]][2] < self.landMarkList[0][2]
                
    
    # Create a function to detect thumb down
    def thumbDown(self):
        return self.landMarkList[self.tipIds[0]][2] > self.landMarkList[0][2]
    
    # Create a function to detect the number of fingers up
    def fingersUp(self):
        #create a list to store the fingers up
        fingers = []
        
        #Get the thumb
        if self.landMarkList[self.tipIds[0]][1] < self.landMarkList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
            
        #Get the other fingers
        for id in range(1, 5):
            if self.landMarkList[self.tipIds[id]][2] < self.landMarkList[self.tipIds[id] - 2][2]:
                # If the y-coordinate of the finger tip is less than the y-coordinate of the finger IP
                #finger tip: tip of the finger
                #finger IP: finger interphalangeal joint
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers
    
    #A function to find distance between two landmarks
    #p1: first landmark
    #p2: second landmark
    #img: image
    #draw: draw the line between the landmarks
    #r: radius of the circle
    #t: thickness of the line
    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.landMarkList[p1][1:] 
        x2, y2 = self.landMarkList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            
        length = math.hypot(x2 - x1, y2 - y1)
        
        return length, img,  [x1, y1, y2, cx, cy]
            


def main():
    # Initialize the frame rate calculation
    previousTime = 0
    currentTime = 0
    
    #Create an object of the HandTrackingModule class
    handTracking = HandTrackingModule()
    
    # Initialize the video capture object
    cap = cv2.VideoCapture(handTracking.webcam)
    # Create the loop to capture the video
    while cap.isOpened():
        # Read the frame from the webcam
        success, img = cap.read()
        
        img = handTracking.findHands(img)
        
        landMarkList, bbox = handTracking.findPosition(img, draw=False)
        
        if len(landMarkList) != 0:
            
            length, img, info = handTracking.findDistance(8, 12, img)
        
        
        if not success:
            print("No se pudo leer el frame de la cámara")
            break
        # Calculate the frame rate
        currentTime = t.time()
        fps = 1/(currentTime - previousTime) # Calculate the frame rate
        #fps: 1 / time taken to process the frame
        previousTime = currentTime
        
        # Display the frame rate on the image
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        #img: original image
        #str(int(fps)): frame rate
        #(10, 70): position of the text
        #cv2.FONT_HERSHEY_PLAIN: font style
        #3: font size
        #(255, 0, 255): color of the text
        #3: thickness of the text
            
        # Display the frame
        cv2.imshow("Image", img)

        # Wait for the user to press the 'q' key to exit the loop
        # cv2.waitKey(1) returns a 32-bit integer corresponding to the pressed key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()        
        
        
        
        
if __name__ == "__main__":
    main()