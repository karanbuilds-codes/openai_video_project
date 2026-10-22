from config import OUT, CACHE, SCENES, NARRATION
def stamp(sec):
    ms=round(sec*1000); h=ms//3600000; ms%=3600000; m=ms//60000; ms%=60000; s=ms//1000; ms%=1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
def make_srt():
    OUT.mkdir(exist_ok=True)
    path=OUT/"subtitles.srt"
    # Scene-aligned subtitles split into readable chunks, timed proportionally to words.
    lines=[]
    for idx,((start,end,*_),script) in enumerate(zip(SCENES,NARRATION),1):
        words=script.split()
        # 12-word captions, proportional scene timing; capped within the scene.
        groups=[words[i:i+12] for i in range(0,len(words),12)]
        total=sum(len(g) for g in groups); cursor=start
        for j,g in enumerate(groups):
            dur=(end-start)*len(g)/max(total,1)
            a=cursor; b=min(end,cursor+dur)
            lines.append(f"{idx*100+j}\\n{stamp(a)} --> {stamp(b)}\\n{' '.join(g)}")
            cursor=b
    path.write_text("\\n\\n".join(lines)+"\\n",encoding="utf-8")
    return path
