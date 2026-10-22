import math, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from config import WIDTH, HEIGHT, FPS, DURATION, SCENES, CACHE
W,H=1920,1080
BG=(4,7,18)
def font(size,bold=False):
    candidates=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"]
    for p in candidates:
        try:return ImageFont.truetype(p,size)
        except:pass
    return ImageFont.load_default()
def draw_center(d,xy,text,f,fill,anchor="mm"):
    d.text(xy,text,font=f,fill=fill,anchor=anchor,stroke_width=0)
def render_frame(sec, size):
    w,h=size; im=Image.new("RGB",size,BG); d=ImageDraw.Draw(im,"RGBA")
    # Moving procedural starfield / particles.
    seed=42; rng=random.Random(seed)
    for i in range(150):
        x=(rng.random()*w + sec*(8+i%9))%w; y=(rng.random()*h + math.sin(sec*.3+i)*18)%h
        r=1+(i%3==0)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(28,150,255,75+(i%150)))
    scene=next((s for s in SCENES if s[0]<=sec<s[1]),SCENES[-1])
    idx=SCENES.index(scene); local=(sec-scene[0])/max(1,scene[1]-scene[0])
    # Network visualization changes with time and scene.
    pts=[]
    for i in range(46):
        a=i*2.399+sec*.08; rad=(0.12+(i%7)*.055)*min(w,h)
        x=w*.5+math.cos(a)*rad; y=h*.48+math.sin(a)*rad*.72
        pts.append((x,y))
    for i,(x,y) in enumerate(pts):
        for j in range(i+1,min(i+5,len(pts))):
            x2,y2=pts[j]
            if (x-x2)**2+(y-y2)**2<(w*.18)**2:
                d.line((x,y,x2,y2),fill=(0,170,255,32),width=1)
    for i,(x,y) in enumerate(pts):
        r=3+(i%4)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(0,220,255,180))
    # Scene-specific meaningful diagrams.
    if idx==2: # token flow into network
        for k,word in enumerate(["The","future","is","being","built"]):
            x=w*.18+k*w*.13; y=h*.34+math.sin(sec*2+k)*12
            d.rounded_rectangle((x-55,y-25,x+55,y+25),12,outline=(0,220,255,210),width=2)
            draw_center(d,(x,y),word,font(24,True),(230,250,255,255))
            d.line((x+55,y,x+95,y+30),fill=(120,80,255,180),width=2)
    elif idx==3: # attention matrix
        cell=min(38,int(w*.025))
        for r in range(6):
            for c in range(6):
                val=int(30+200*(0.5+0.5*math.sin(sec*2+r*1.2+c*.8)))
                x=w*.36+c*(cell+4); y=h*.3+r*(cell+4)
                d.rounded_rectangle((x,y,x+cell,y+cell),4,fill=(0,val,255,100+val//2))
        draw_center(d,(w*.5,h*.25),"SELF-ATTENTION: CONTEXTUAL LINKS",font(25,True),(180,235,255,255))
    elif idx==4:
        draw_center(d,(w*.28,h*.34),"TRAINING",font(36,True),(0,225,255,255))
        draw_center(d,(w*.28,h*.42),"LEARNING PARAMETERS",font(22),(210,230,255,255))
        draw_center(d,(w*.72,h*.34),"INFERENCE",font(36,True),(170,115,255,255))
        draw_center(d,(w*.72,h*.42),"GENERATING OUTPUTS",font(22),(210,230,255,255))
        d.line((w*.43,h*.35,w*.57,h*.35),fill=(255,255,255,190),width=3)
    elif idx==5:
        labels=["USER GOAL","PLANNING","TOOL SEARCH","OBSERVE","VERIFY","RESULT"]
        x0=w*.12; y=h*.35; step=w*.15
        for i,label in enumerate(labels):
            x=x0+i*step
            d.rounded_rectangle((x-60,y-40,x+60,y+40),12,fill=(4,24,52,230),outline=(0,205,255,220),width=2)
            draw_center(d,(x,y),label,font(16,True),(220,245,255,255))
            if i<len(labels)-1:d.line((x+62,y,x+step-62,y),fill=(120,90,255,220),width=3)
        tasks=["Break goal into tasks","Select search tool","Simulated results received","Compare evidence","Find missing details","Draft + check report"]
        k=min(5,int(local*6))
        draw_center(d,(w*.5,h*.58),tasks[k],font(27,True),(0,235,255,255))
        draw_center(d,(w*.5,h*.66),"SIMULATED DEMONSTRATION — NO LIVE WEB RESEARCH",font(18),(255,190,90,255))
        d.rounded_rectangle((w*.36,h*.73,w*.64,h*.82),14,outline=(255,190,90,230),width=3)
        draw_center(d,(w*.5,h*.775),"HUMAN PERMISSION CHECKPOINT",font(19,True),(255,220,160,255))
    elif idx==6:
        for k,label in enumerate(["TEXT","IMAGE","AUDIO","VIDEO"]):
            x=w*(.2+k*.2); y=h*.38+math.sin(sec*2+k)*15
            d.rounded_rectangle((x-65,y-40,x+65,y+40),12,fill=(10,25,60,230),outline=(0,220,255,220),width=2)
            draw_center(d,(x,y),label,font(23,True),(220,245,255,255))
            d.line((x,y+45,w*.5,h*.62),fill=(140,90,255,150),width=2)
        draw_center(d,(w*.5,h*.7),"MODEL  +  APPLICATION  +  API  +  TOOLS",font(26,True),(180,210,255,255))
    elif idx==7:
        draw_center(d,(w*.32,h*.4),"AGI",font(88,True),(0,225,255,255))
        draw_center(d,(w*.32,h*.49),"DEBATED CONCEPT",font(24,True),(220,240,255,255))
        draw_center(d,(w*.68,h*.4),"ASI",font(88,True),(170,115,255,255))
        draw_center(d,(w*.68,h*.49),"HYPOTHETICAL",font(24,True),(220,240,255,255))
        for k,label in enumerate(["SCIENCE","MATH","ENGINEERING","LANGUAGE","PLANNING"]):
            x=w*.16+k*w*.17; y=h*.68+math.sin(sec+k)*8
            draw_center(d,(x,y),label,font(16,True),(170,210,255,230))
    elif idx==8:
        for k,(label,col) in enumerate([("UNCHECKED ACTION",(255,100,110,255)),("VERIFY + APPROVE",(0,235,180,255))]):
            x=w*(.28+.44*k)
            d.rounded_rectangle((x-170,h*.32,x+170,h*.48),18,fill=(20,20,38,230),outline=col,width=3)
            draw_center(d,(x,h*.4),label,font(24,True),col)
        draw_center(d,(w*.5,h*.59),"LIMITED PERMISSIONS  •  VERIFICATION  •  HUMAN OVERSIGHT",font(22),(220,240,255,255))
    elif idx==9:
        labels=["AI","NEURAL NETWORKS","LLMs","AI AGENTS","AGI CONCEPT","ASI HYPOTHESIS"]
        for k,label in enumerate(labels):
            x=w*(.08+k*.168); y=h*.47+math.sin(sec*1.5+k)*18
            d.rounded_rectangle((x-65,y-34,x+65,y+34),10,fill=(6,20,48,230),outline=(0,205,255,220),width=2)
            draw_center(d,(x,y),label,font(14,True),(225,245,255,255))
            if k<5:d.line((x+66,y,x+0.168*w-66,y),fill=(130,90,255,210),width=2)
    # Header / title and chapter label.
    draw_center(d,(w*.5,h*.10),scene[2],font(max(18,int(w*.018)),True),(0,220,255,255))
    if idx==0:
        draw_center(d,(w*.5,h*.78),scene[3],font(max(24,int(w*.035)),True),(245,250,255,255))
        draw_center(d,(w*.5,h*.86),scene[4],font(max(16,int(w*.018)),False),(130,200,255,255))
    else:
        draw_center(d,(w*.5,h*.18),scene[3],font(max(20,int(w*.027)),True),(245,250,255,255))
        draw_center(d,(w*.5,h*.91),scene[4],font(max(12,int(w*.012)),False),(160,195,235,255))
    # cinematic vignette
    arr=np.asarray(im).astype(np.float32)
    yy,xx=np.mgrid[0:h,0:w]; dist=((xx-w/2)/(w*.75))**2+((yy-h/2)/(h*.8))**2
    vign=np.clip(1-dist*.45,.45,1)
    arr*=vign[:,:,None]
    im=Image.fromarray(np.uint8(np.clip(arr,0,255)))
    return im
def render_video(quality):
    size=(1920,1080) if quality=="final" else (960,540)
    frames=CACHE/f"frames_{quality}"; frames.mkdir(parents=True,exist_ok=True)
    total=DURATION*FPS
    for i in range(total):
        path=frames/f"frame_{i:06d}.png"
        if path.exists(): continue
        render_frame(i/FPS,size).save(path,optimize=False)
        if i%300==0: print(f"Rendering frames: {i}/{total}")
