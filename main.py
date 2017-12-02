import numpy as np
import cv2

fileName = "12da1dc4adab6e00952790c8e363a9a62e945fd3"
extn = ".jpg"
# Read and convert the image to Grayscale
src = cv2.imread(fileName + extn, cv2.IMREAD_GRAYSCALE)

cv2.startWindowThread()
# See what you have got
cv2.imshow("Original Image", src)

# Initialize parameters
height, width = src.shape
blockSize = 5
C = -7

# Apply Adaptive Mean Thresholding
amtImage = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
cv2.imwrite(fileName + '-after-thresholding' + extn, amtImage)
cv2.imshow("After Thresholding", amtImage)

# Find image contours
_, contours, hierarchy = cv2.findContours(amtImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Initialize numpy array, will be used to export the image with labels
labeledImage = np.zeros((height, width, 1), np.uint8)
color = (255, 255, 255)
scale = 1
count = 0

# Header
print('number,length')

for contour in contours:
    arcLen = cv2.arcLength(contour, False)
    
    # Ignore small contours; will help to reduce noise
    if arcLen > 20:
        cv2.drawContours(labeledImage, [contour * scale], -1, color, -2)
        count += 1
        countLabel = str(count)
        x = contour[0][0][0]
        y = contour[0][0][1]
        
        # Print label on image
        cv2.putText(labeledImage, countLabel, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 180, 1, True)
        print(countLabel + ',' + str(arcLen))

# Write to file and see the output
cv2.imwrite(fileName + '-with-labels' + extn, labeledImage)
cv2.imshow("Final Image", labeledImage)

# Cleanup
cv2.waitKey(0)
cv2.destroyAllWindows()
