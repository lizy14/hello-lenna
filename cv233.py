import cv2

def load(filename):
    return cv2.imread(filename)

def save(img, filename):
    cv2.imwrite(filename, img)

def rotate(img, degree):
    rows, cols, _ = img.shape
    mat = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1)
    return cv2.warpAffine(img, mat, (cols, rows))

def flip(img, direction):
    cv2.flip(img, direction, img)
    return img
    
def transpose(img):
    cv2.transpose(img, img)
    return img
