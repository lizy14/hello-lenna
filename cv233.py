def rotate(img, degree):
    return img


def vertical_flip(img):
    return img[::-1]


def horizontal_flip(img):
    return [i[::-1] for i in img]


def transpose(img):
    return list(map(list, zip(*img)))
