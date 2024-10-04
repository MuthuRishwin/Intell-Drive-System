import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # Use 0 for the default camera

def draw_parallelogram(frame):
    height, width = frame.shape[:2]

    # Define the four corners of the parallelogram
    top_left = (int(width * 0.4), int(height * 0.6))
    top_right = (int(width * 0.6), int(height * 0.6))
    bottom_left = (int(width * 0.1), height)
    bottom_right = (int(width * 0.9), height)

    # Create a numpy array of points for the parallelogram
    pts = np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.int32)

    # Create a mask for the parallelogram region
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)

    # Apply the mask to the frame to keep only the parallelogram region
    parallelogram_region = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert the parallelogram region to the HSV color space for color detection
    hsv_frame = cv2.cvtColor(parallelogram_region, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    # Create a mask for detecting green color in the parallelogram region
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    # Find contours of green objects in the green_mask
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour is detected
    if len(contours) > 0:
        # Iterate through the contours and replace green color with red only within the parallelogram
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Change this threshold according to your requirements
                cv2.drawContours(parallelogram_region, [contour], 0, (0, 0, 255), -1)
        cv2.putText(parallelogram_region, "Detecting some Obstacles", (int(width * 0.4), int(height * 0.55)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 25, 255), 2)
    else:
        # If no object is detected, keep the parallelogram green
        parallelogram_region = cv2.fillPoly(parallelogram_region, [pts], (0, 255, 0))
        cv2.putText(parallelogram_region, "You can park here", (int(width * 0.4), int(height * 0.55)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Combine the modified parallelogram region with the original frame
    frame = cv2.add(frame, parallelogram_region)

    return frame

while True:
    ret, frame = cap.read()  # Read a frame from the camera

    if not ret:
        break
    frame = draw_parallelogram(frame)  # Draw the parallelogram and replace color within it

    cv2.imshow('Camera', frame)  # Display the frame with the parallelogram and modified color

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all windows