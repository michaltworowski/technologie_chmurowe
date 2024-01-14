import cv2

# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Reading the Image
img = cv2.imread('grupa_osob.jpg')
img = cv2.resize(img, (700,400))

# Detecting all the regions in the
# Image that has a pedestrians inside it
(rects, weights) = hog.detectMultiScale(img,
									winStride=(4, 4),
									padding=(8, 8),
									scale=1.15)

# Drawing the regions in the Image
for (x, y, w, h) in rects:
	cv2.rectangle(img, (x, y),
				(x + w, y + h),
				(0, 0, 255), 2)

print(f'Found {len(rects)} humans')

# Showing the output Image
cv2.imshow("Image", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
