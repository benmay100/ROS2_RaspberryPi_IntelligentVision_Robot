import cv2
import sys # Import sys module to exit gracefully

img = cv2.imread('/home/ben-may/ROS_Workspaces/luqman_course_ws/src/vision_rpi_bot/assets/left.png')

if img is None:
    print("Error: Could not load image. Check the path.")
    sys.exit(1) # Exit if image not found

decoder = cv2.QRCodeDetector()
data, points, _ = decoder.detectAndDecode(img)
print("Result of QR code = ", data)

cv2.imshow('Detected QR code is ', img)

# Loop to wait for a key press and allow for graceful exit
while True:
    key = cv2.waitKey(1) & 0xFF # Wait for 1ms and get key code
    if key == ord('q'): # Press 'q' to quit
        break
    # You can add other conditions here, e.g., if you have ROS subscribers
    # if rospy.is_shutdown(): # For ROS 1
    # if rclpy.ok() is False: # For ROS 2
    #    break

cv2.destroyAllWindows()
print("Exiting application.")