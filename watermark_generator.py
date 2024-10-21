import cv2
import hashlib
import hmac
import numpy as np

IMG_WIDTH = 1200
IMG_HEIGHT = 800
WATERMARK_WIDTH = 256
WATERMARK_HEIGHT = 256

IMG_SIZE = IMG_HEIGHT * IMG_WIDTH
WATERMARK_SIZE = WATERMARK_HEIGHT * WATERMARK_WIDTH

KEY = 1001
THRESH = 75

def secure_seeded_random_points(seed, img_size, watermark_size):
    seed_bytes = str(seed).encode('utf-8')  # Convert seed to bytes
    points = []
    
    for i in range(watermark_size):
        # Create a new HMAC using the seed and index as the message
        h = hmac.new(seed_bytes, str(i).encode('utf-8'), hashlib.sha256)
        # Convert the HMAC to an integer and scale it to img_size
        point = int(h.hexdigest(), 16) % img_size
        points.append(point)
    
    return points

def xor(x ,y):
    if x == 0 and y == 0:
        return 0
    elif x == 0 and y != 0:
        return 255
    elif x != 0 and y == 0:
        return 255
    elif x !=0 and y != 0:
        return 0

secure_random_points = secure_seeded_random_points(KEY, IMG_SIZE, WATERMARK_SIZE)


owner_img = cv2.imread('images\owner_img.jpg', 0)

for k in range(0, 7):
    master_img = cv2.imread('images\master_images\master_img_'+str(k)+'.jpg', 0)
    watermark_img = np.zeros((WATERMARK_WIDTH, WATERMARK_HEIGHT, 1), np.uint8)

    i = 0
    j = 0

    for i in range(0, WATERMARK_HEIGHT):
        for j in range(0, WATERMARK_WIDTH):
            watermark_img[i, j] = xor(master_img[i, j], owner_img[i, j])

    watermark_img = (255-watermark_img)
    kernel = np.ones((4,4),np.uint8)
    watermark_img = cv2.medianBlur(watermark_img, 3)
    watermark_img = cv2.morphologyEx(watermark_img, cv2.MORPH_OPEN, kernel)
    watermark_img = cv2.morphologyEx(watermark_img, cv2.MORPH_CLOSE, kernel)
    watermark_img = (255-watermark_img)

    cv2.imwrite('images\\regenerated_watermarks\\watermark_img_'+str(k)+'.jpg', watermark_img)
    print(k)
print("Done")