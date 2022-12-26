import cv2
import numpy as np
import random
import threading
from tqdm import tqdm
import imageio
from gradient import generateGradient
from PIL import Image, ImageDraw, ImageFont

XMAX = 125
YMAX = 285
BORDER = 5

global lock
global all_frames
global text_recs
global grid_rec
lock = threading.Lock()

def checkAdjacent(x,y):
    if np.sum(grid[x-1:x+2,y-1:y+2]) > 0:
        return True
    else: return False
    
def randomWalk(x,y):
    # walks in a random direction with step size 1 2 or 3
    dir = random.choice(directions)
    step_size = random.choice([1,2,3])
    x += dir[0]*step_size
    y += dir[1]*step_size
    
    if x < 0:
        x = XMAX - 1
    if x > XMAX - 1:
        x = 0
    if y < 0:
        y = YMAX - 1
    if y > YMAX - 1:
        y = 0
        
    return x,y

# def generateRandomInRange(min1,max1,min2,max2):
#     a = np.random.rand()
#     if a > 0.5:
#         x = random.randint(min1,max1)
#     else:
#         x = random.randint(min2,max2)
#     return x

# def generateStartCoordinates():
#     if np.random.rand() > 0.5:
#         x = generateRandomInRange(BORDER,XMAX-2*BORDER,BORDER,XMAX-2*BORDER)
#         y = generateRandomInRange(BORDER,2*BORDER,YMAX-2*BORDER,YMAX-BORDER)
#     else:
#         x = generateRandomInRange(BORDER,2*BORDER,XMAX-2*BORDER,XMAX-BORDER)
#         y = generateRandomInRange(BORDER,YMAX-2*BORDER,BORDER,YMAX-2*BORDER)
        
#     return (x,y)

def select_point(outer_rec, inner_recs):
    # outer_rec: dictionary with keys x1,y1,x2,y2
    # inner_recs: list of dictionaries of rectangles
    # randomly selects a point that is inside the outer rec but not contained in any of the inner recs
    while True:
        # Generate a random x coordinate within the range of x1 and x2
        x = random.uniform(outer_rec['x1'], outer_rec['x2'])
        # Generate a random y coordinate within the range of y1 and y2
        y = random.uniform(outer_rec['y1'], outer_rec['y2'])
        # Check if the point is not contained in the smaller rectangles
        inside = False
        for r in inner_recs:
            if x<r['x2'] and x>r['x1'] and y<r['y2'] and y>r['y1']:
                inside = True
                break
        if not inside:        
            return int(x), int(y)

def stickToSnowflake():

    global all_frames
    global lock
    global grid
    global text_recs
    global grid_rec
    # x,y = generateStartCoordinates()
    
    
    x,y = select_point(grid_rec,text_recs)

    while not checkAdjacent(x,y):
        x,y = randomWalk(x,y)
    with lock:
        grid[x,y] = 255
        all_frames.append(np.uint8(grid.copy()))

# add all dictionary of names and e for english, c for chinese
cards = {
    'You':'e',
    '你':'c'
}  

# select the output type
# type = 'gif'
type = 'mp4'    

for n,t in cards.items():
    print(f'making {type} card for {n} ...')
    all_frames = []
    grid = np.zeros((XMAX,YMAX))
    all_frames.append(np.uint8(grid.copy()))

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = 255
    thickness = 2
    
    
    if t == 'e':
        text = f"To: {n},"
        (text_width, text_height), _ = cv2.getTextSize(text, font, fontScale, thickness)
        
        # Calculate the coordinates of the bottom-left corner of the text
        text_x = XMAX // 2 
        text_y = YMAX // 2 - text_width // 2
        org = (text_y, text_x)
        grid = cv2.putText(grid, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    
        text2 = f"Merry Xmas!!"
        (text2_width, text2_height), _ = cv2.getTextSize(text2, font, fontScale, thickness)

        text2_x = XMAX // 2 + text2_height +text2_height//4
        text2_y = YMAX // 2 - text2_width // 2
        text2_org = (text2_y, text2_x)
        grid = cv2.putText(grid, text2, text2_org, font, fontScale, color, thickness, cv2.LINE_AA)
    elif t == 'c':
        image = np.zeros((grid.shape[0],grid.shape[1],3), dtype=np.uint8)

        # 定义宋体路径
        fontpath = 'bold_cn.ttf'
        font_cn = ImageFont.truetype(fontpath, 35)
        img_pil = Image.fromarray(image)

        text2 = '圣诞快乐!!'
        draw = ImageDraw.Draw(img_pil)
        text2_width, text2_height = draw.textsize(text2, font=font_cn)
        text2_x = XMAX // 2 +text2_height//4
        text2_y = YMAX // 2 - text2_width // 2
        text2_org = (text2_y, text2_x)
                
        draw.text(text2_org, text2, font=font_cn, fill=(255, 255, 255))
        
        text = f'祝 {n}'
        draw = ImageDraw.Draw(img_pil)
        text_width, text_height = draw.textsize(text, font=font_cn)
        text_x = XMAX // 2 -text_height
        text_y = YMAX // 2 - text_width // 2
        text_org = (text_y, text_x)
                
        draw.text(text_org, text, font=font_cn, fill=(255, 255, 255))


        save_image = np.array(img_pil)

        grid = cv2.cvtColor(save_image, cv2.COLOR_BGR2GRAY)
    

        
    directions = [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,1),(-1,0),(-1,-1)]

    text_recs = [
        {'x1':text2_y,'y1':text2_x,'x2':text2_y+text2_width,'y2':text2_x - text2_height},
        {'x1':text_y,'y1':text_x,'x2':text_y+text_width,'y2':text_x - text_height},
    ]
    grid_rec = {'x1':0,'y1':0,'x2':XMAX,'y2':YMAX}

        
        
    for i in tqdm(range(1)):
        threads = []
        for j in range(4000):
            t = threading.Thread(target=stickToSnowflake)
            t.start()
            threads.append(t)
            
        for t in threads:
            t.join()

    processed_frames = []
    for f in all_frames[::20]:
        f = cv2.resize(f,(YMAX*3,XMAX*3))
        blur = cv2.GaussianBlur(f,(45,45),0)
        sharp = cv2.subtract(f, blur)
        # gradient = generateGradient(width)
        background = generateGradient(f.shape[1],f.shape[0])
        for c in range(background.shape[-1]):
            background[:,:,c][sharp>0] = 0
        
        sharp = np.where(sharp>0,sharp+50,sharp)
        sharp = np.clip(sharp,0,255)

        background += cv2.cvtColor(sharp,cv2.COLOR_GRAY2RGB)
        processed_frames.append(background)

    for i in range(25):
        processed_frames.append(background)
    
    if type == 'gif':
        imageio.mimsave(f"cards/{n}.gif", processed_frames, duration=0.1)

    elif type == 'mp4':
        video_writer = imageio.get_writer(f'cards/{n}.mp4', fps=30)
        for image in processed_frames:
            video_writer.append_data(image)
        video_writer.close()





