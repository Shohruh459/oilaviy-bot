#!/usr/bin/env python3
"""assets/images/sN.jpg yo'q bo'lsa, faqat PREVIEW uchun iliq gradient o'rinbosar yaratadi (placeholder_*.jpg)."""
import os
from PIL import Image, ImageFilter
import numpy as np
R = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')
pal = {1:((196,142,92),(92,52,38)),2:((214,170,120),(110,70,50)),3:((180,150,110),(70,60,52)),
       4:((205,160,105),(80,48,36)),5:((222,184,130),(120,80,56)),6:((200,150,100),(60,40,34))}
H, W = 2880, 1620
for n, (c1, c2) in pal.items():
    if any(os.path.exists(os.path.join(R, f's{n}.{e}')) for e in ('jpg','jpeg','png','mp4')): continue
    y = np.linspace(0, 1, H)[:, None, None]; x = np.linspace(-1, 1, W)[None, :, None]
    g = np.array(c1)*(1-y) + np.array(c2)*y
    glow = np.exp(-(((x+0.3*(-1)**n)**2)*3 + ((y-0.35)**2)*8))*40
    img = np.clip(g + glow, 0, 255).astype('uint8')
    Image.fromarray(img).filter(ImageFilter.GaussianBlur(2)).save(os.path.join(R, f'placeholder_s{n}.jpg'), quality=92)
