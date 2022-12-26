import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
XMAX=400
YMAX=400
# 读取彩色图片,注意，这里一定要是彩色图片，不然会报 ：function takes exactly 1 argument (3 given) 的错误

image = np.zeros((600,800,3), dtype=np.uint8)
print(image.shape)
# 定义宋体路径
fontpath = 'simsun.ttc'
font = ImageFont.truetype(fontpath, 50)
img_pil = Image.fromarray(image)

text2 = '你好，中国'
draw = ImageDraw.Draw(img_pil)
text2_width, text2_height = draw.textsize(text2, font=font)
text2_x = XMAX // 2 
text2_y = YMAX // 2 - text2_width // 2
text2_org = (text2_x, text2_y)
        
draw.text(text2_org, text2, font=font, fill=(255, 255, 255))


save_image = np.array(img_pil)

img = cv2.cvtColor(save_image, cv2.COLOR_BGR2GRAY)
cv2.imshow('image', img)

cv2.waitKey()

cv2.destroyAllWindows()