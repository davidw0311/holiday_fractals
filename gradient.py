import random
from PIL import Image, ImageDraw
import numpy as np
import cv2

def generateGradient(width, height, start_color=(158, 194, 255), end_color=(33, 42, 165)):

    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # Generate a gradient fill from the starting color to the ending color
    for y in range(height):
        color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * y / height) for i in range(3))
        draw.line((0, y, width, y), fill=color)

    # Convert the image to a NumPy array
    gradient = np.array(image)
    return gradient 

