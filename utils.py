import cv2 as cv
import numpy as np
import IPython
import html
import base64
from ipywidgets import IntSlider


def show(*images, enlarge_small_images = True, max_per_row = -1, font_size = 0):
    if len(images) == 2 and type(images[1])==str:
        images = [(images[0], images[1])]

    def convert(imgOrTuple):
        try:
            img, title = imgOrTuple
            if type(title)!=str:
                img, title = imgOrTuple, ''
        except ValueError:
            img, title = imgOrTuple, ''        
        if type(img)==str:
            data = img
        else:
            img = convert_for_display(img)
            if enlarge_small_images:
                REF_SCALE = 400
                h, w = img.shape[:2]
                if h<REF_SCALE or w<REF_SCALE:
                    scale = max(1, min(REF_SCALE//h, REF_SCALE//w))
                    img = cv.resize(img,(w*scale,h*scale), interpolation=cv.INTER_NEAREST)
            data = 'data:image/png;base64,' + base64.b64encode(cv.imencode('.png', img)[1]).decode('utf8')
        return data, title
    
    if max_per_row == -1:
        max_per_row = len(images)
    
    rows = [images[x:x+max_per_row] for x in range(0, len(images), max_per_row)]
    font = f"font-size: {font_size}px;" if font_size else ""
    
    html_content = ""
    for r in rows:
        l = [convert(t) for t in r]
        html_content += "".join(["<table><tr>"] 
                + [f"<td style='text-align:center;{font}'>{html.escape(t)}</td>" for _,t in l]    
                + ["</tr><tr>"] 
                + [f"<td style='text-align:center;'><img src='{d}'></td>" for d,_ in l]
                + ["</tr></table>"])
    IPython.display.display(IPython.display.HTML(html_content))

def convert_for_display(img):
    if img.dtype!=np.uint8:
        a, b = img.min(), img.max()
        if a==b:
            offset, mult, d = 0, 0, 1
        elif a<0:
            offset, mult, d = 128, 127, max(abs(a), abs(b))
        else:
            offset, mult, d = 0, 255, b
        img = np.clip(offset + mult*(img.astype(float))/d, 0, 255).astype(np.uint8)
    return img
        
def center_text(img, text, center, color, fontFace = cv.FONT_HERSHEY_PLAIN, fontScale = 1, thickness = 1, lineType = cv.LINE_AA, max_w = -1):
    while True:
        (w, h), _ = cv.getTextSize(text, fontFace, fontScale, thickness)
        if max_w<0 or w<max_w or fontScale<0.2:
            break
        fontScale *= 0.8
    pt = (center[0]-w//2, center[1]+h//2)
    cv.putText(img, text, pt, fontFace, fontScale, color, thickness, lineType)

    
def draw_hist(hist, height = 192, back_color = (160,225,240), border = 5):
    size = hist.size
    img = np.full((height, size+border*2, 3), back_color, dtype=np.uint8)
    nh = np.empty_like(hist, dtype=np.int32)
    cv.normalize(hist, nh, 0, height-1-border*2, cv.NORM_MINMAX, cv.CV_32S)
    for i in range(size):
        img[-border-nh[i]:-border,border+i,0:3] = i
    return img