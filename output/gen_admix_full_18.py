# -*- coding: utf-8 -*-
"""AdMix Full Wireframe Suite — 15장 (1440x900 / 390x844)
#1A1F5E Deep Blue  +  #4ADE80 Lime Green
"""
import sys, io, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('C:/Agent/pepper/admix_wireframes')
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1440, 900
MW, MH = 390, 844

BLUE    = (26,  31,  94)
BLUE2   = (45,  55, 145)
BLUE3   = (14,  16,  60)
BLUE_L  = (232, 235, 255)
BLUE_M  = (55,  70, 170)
LIME    = (74,  222, 128)
LIME_L  = (220, 252, 231)
LIME_D  = (22,  163,  74)
WHITE   = (255, 255, 255)
BG      = (246, 248, 255)
CARD    = (255, 255, 255)
BORDER  = (218, 224, 248)
BORDER2 = (198, 208, 240)
TEXT    = (14,  18,  58)
TEXT2   = (72,  84, 130)
TEXT3   = (142, 156, 198)
SUCCESS = (34,  197,  94)
SUCCL   = (218, 252, 231)
WARN    = (234, 179,   8)
WARNL   = (254, 249, 195)
DANGER  = (239,  68,  68)
DANGL   = (254, 226, 226)
PURPLE  = (124,  58, 237)
PURPL   = (234, 224, 255)
SIDE    = (18,  22,  75)
SIDE2   = (32,  40, 110)

_fc = {}
def fnt(sz, bold=False):
    key = (sz, bold)
    if key not in _fc:
        fp = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
        try:   _fc[key] = ImageFont.truetype(fp, sz)
        except: _fc[key] = ImageFont.load_default()
    return _fc[key]

def gv(w, h, c1, c2):
    a = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        t2 = y/max(h-1,1)
        for c in range(3): a[y,:,c] = int(c1[c]*(1-t2)+c2[c]*t2)
    return Image.fromarray(a)

def gh(w, h, c1, c2):
    a = np.zeros((h, w, 3), dtype=np.uint8)
    for x in range(w):
        t2 = x/max(w-1,1)
        for c in range(3): a[:,x,c] = int(c1[c]*(1-t2)+c2[c]*t2)
    return Image.fromarray(a)

def ni(w=W, h=H, bg=BG):
    img = Image.new('RGB', (w, h), bg)
    return img, ImageDraw.Draw(img)

def rr(d, x, y, w, h, fill=None, ol=None, lw=1, r=8):
    if w>0 and h>0:
        d.rounded_rectangle([x,y,x+w,y+h], radius=min(r,w//2,h//2),
                             fill=fill, outline=ol, width=lw)

def t(d, s, x, y, sz, col=None, bold=False):
    d.text((x,y), str(s), font=fnt(sz,bold), fill=col or TEXT)

def tc(d, s, cx, y, sz, col=None, bold=False):
    bb = d.textbbox((0,0), str(s), font=fnt(sz,bold))
    d.text((cx-(bb[2]-bb[0])//2, y), str(s), font=fnt(sz,bold), fill=col or TEXT)

def tw(d, s, sz, bold=False):
    bb = d.textbbox((0,0), str(s), font=fnt(sz,bold))
    return bb[2]-bb[0]

def thh(d, s, sz, bold=False):
    bb = d.textbbox((0,0), str(s), font=fnt(sz,bold))
    return bb[3]-bb[1]

def btn(d, x, y, w, h, lbl, sz=14, fill=LIME, col=BLUE3, r=20, bold=True):
    rr(d, x, y, w, h, fill=fill, r=r)
    tc(d, lbl, x+w//2, y+(h-thh(d,lbl,sz,bold))//2, sz, col=col, bold=bold)

def btn_ghost(d, x, y, w, h, lbl, sz=13, ol=None, col=None, r=20):
    rr(d, x, y, w, h, ol=ol or (160,180,240), lw=2, r=r)
    tc(d, lbl, x+w//2, y+(h-thh(d,lbl,sz))//2, sz, col=col or (190,210,255))

def pill(d, x, y, lbl, sz=11, fill=None, col=None, r=12):
    f = fnt(sz)
    bb = d.textbbox((0,0), lbl, font=f)
    pw = bb[2]-bb[0]+18; ph = 24
    rr(d, x, y, pw, ph, fill=fill or BORDER, r=r)
    t(d, lbl, x+9, y+5, sz, col=col or TEXT2)
    return pw

def sbadge(d, x, y, status):
    cfg = {'집행중':(SUCCL,SUCCESS),'완료':(BORDER,TEXT3),
           '일시정지':(WARNL,WARN),'검토중':(BLUE_L,BLUE_M),'대기':(WARNL,WARN)}
    bg, col = cfg.get(status,(BORDER,TEXT3))
    pw = tw(d,status,11)+16
    rr(d, x, y, pw, 22, fill=bg, r=11)
    t(d, status, x+8, y+4, 11, col=col, bold=True)
    return pw

# ── Shared: top nav ───────────────────────────────────────────
def nav(img, d, active=''):
    g = gh(W, 60, BLUE3, BLUE)
    img.paste(g, (0,0))
    d = ImageDraw.Draw(img)
    t(d,'Ad', 28,17,22,col=LIME,bold=True)
    t(d,'Mix',60,17,22,col=WHITE,bold=True)
    d.ellipse([88,26,96,34], fill=(55,70,155))
    t(d,'광고 플랫폼',104,22,12,col=(135,158,220))
    items=['대시보드','캠페인','매체','소재','리포트']
    nx=280
    for item in items:
        is_a = item==active
        t(d,item,nx,22,13,col=WHITE if is_a else (165,188,230))
        if is_a:
            bb=d.textbbox((nx,22),item,font=fnt(13))
            d.rectangle([nx,56,bb[2]+2,60],fill=LIME)
        nx+=106
    rr(d,W-216,14,170,32,fill=LIME,r=16)
    tc(d,'+ 캠페인 만들기',W-216+85,21,12,col=BLUE3,bold=True)
    d.ellipse([W-44,13,W-10,47],fill=BLUE2)
    tc(d,'재',W-27,23,13,col=WHITE,bold=True)

# ── Shared: sidebar ───────────────────────────────────────────
def sidebar(img, d, active='대시보드'):
    d.rectangle([0,60,220,H], fill=SIDE)
    d.line([(220,60),(220,H)], fill=(32,40,110), width=1)
    d.rectangle([0,60,220,100], fill=BLUE3)
    t(d,'Ad',24,70,18,col=LIME,bold=True)
    t(d,'Mix',54,70,18,col=WHITE,bold=True)
    items = [
        ('대시보드','🏠'),('캠페인 관리','📋'),('캠페인 만들기','➕'),
        ('소재 라이브러리','🖼'),('매체 목록','📺'),
        ('리포트','📊'),('청구 & 정산','💳'),('설정','⚙'),
    ]
    for i,(item,icon) in enumerate(items):
        iy = 112+i*48
        is_a = active in item or item in active
        if is_a:
            d.rectangle([0,iy-4,220,iy+38],fill=SIDE2)
            d.rectangle([0,iy-4,4,iy+38],fill=LIME)
        t(d,item,36,iy+8,13,col=WHITE if is_a else (135,158,218),bold=is_a)

# ── Shared: KPI card ─────────────────────────────────────────
def kpi(d, x, y, w, h, lbl, val, chg, up=True, acc=LIME):
    rr(d,x,y,w,h,fill=CARD,ol=BORDER,r=10)
    rr(d,x,y,w,4,fill=acc,r=2)
    t(d,lbl,x+16,y+16,11,col=TEXT3)
    t(d,val,x+16,y+34,26,col=TEXT,bold=True)
    bc=SUCCL if up else DANGL; tc2=SUCCESS if up else DANGER
    lbl2=f'{"▲" if up else "▼"} {chg}'
    pw=tw(d,lbl2,11)+14
    rr(d,x+16,y+h-34,pw,20,fill=bc,r=10)
    t(d,lbl2,x+23,y+h-30,11,col=tc2,bold=True)

# ── Shared: line chart ────────────────────────────────────────
def linechart(d, x, y, w, h, data, col=LIME, bg=CARD, title='', data2=None, col2=BLUE2):
    rr(d,x,y,w,h,fill=bg,ol=BORDER,r=10)
    if title: t(d,title,x+16,y+14,12,col=TEXT2,bold=True)
    PL,PR,PT,PB=52,20,44,36
    CX,CY,CW,CH=x+PL,y+PT,w-PL-PR,h-PT-PB
    days=['4/21','4/22','4/23','4/24','4/25','4/26','4/27']
    n=len(days)
    for i,day in enumerate(days):
        px=CX+i*CW//(n-1)
        t(d,day,px-tw(d,day,10)//2,y+h-PB+4,10,col=TEXT3)
        d.line([(px,CY),(px,CY+CH)],fill=(225,229,250),width=1)
    for i in range(5):
        gy=CY+i*CH//4
        d.line([(CX,gy),(CX+CW,gy)],fill=(225,229,250),width=1)
    def draw_series(dat,c,filled=True):
        if len(dat)<2: return
        mn,mx=min(dat),max(dat); rng=max(mx-mn,1)
        pts=[]
        for i,v in enumerate(dat):
            px=CX+i*CW//(n-1)
            py=CY+CH-int((v-mn)/rng*CH*0.85)-6
            pts.append((px,py))
        if filled:
            fp=[(pts[0][0],CY+CH)]+pts+[(pts[-1][0],CY+CH)]
            fc=tuple(int(0.88*255+0.12*c[k]) for k in range(3))
            d.polygon(fp,fill=fc)
        for i in range(len(pts)-1): d.line([pts[i],pts[i+1]],fill=c,width=3)
        for px,py in pts: d.ellipse([px-4,py-4,px+4,py+4],fill=CARD,outline=c,width=2)
    if data2: draw_series(data2,col2,False)
    draw_series(data,col)

# ── Shared: step wizard bar ────────────────────────────────────
def stepbar(img, d, steps, active):
    d.rectangle([0,60,W,120],fill=WHITE)
    d.line([(0,120),(W,120)],fill=BORDER,width=1)
    sw = W//len(steps)
    for i,slbl in enumerate(steps):
        sx=i*sw+sw//2; done=i<active; cur=i==active
        fc=SUCCESS if done else (BLUE if cur else (200,208,238))
        d.ellipse([sx-16,78,sx+16,110],fill=fc)
        tc(d,'✓' if done else str(i+1),sx,86,13,col=WHITE,bold=True)
        lc2=BLUE if cur else (SUCCESS if done else TEXT3)
        tc(d,slbl,sx,114,11,col=lc2,bold=cur)
        if i<len(steps)-1:
            lc3=SUCCESS if done else (208,215,245)
            d.line([(sx+16,94),(sx+sw-16,94)],fill=lc3,width=2)

# ── Shared: sidebar (media portal) ────────────────────────────
def media_sidebar(d, active='인벤토리'):
    d.rectangle([0,0,220,MH if False else H],fill=BLUE3)
    d.line([(220,0),(220,H)],fill=(30,36,100),width=1)
    t(d,'Ad',20,14,18,col=LIME,bold=True); t(d,'Mix',50,14,18,col=WHITE,bold=True)
    t(d,'매체사 포털',20,38,11,col=(140,160,215))
    items=[('인벤토리 관리','📦'),('광고 신청 목록','📋'),
           ('정산 내역','💰'),('설정','⚙')]
    for i,(item,icon) in enumerate(items):
        iy=80+i*52
        is_a=active in item
        if is_a:
            d.rectangle([0,iy-4,220,iy+40],fill=(24,30,90))
            d.rectangle([0,iy-4,4,iy+40],fill=LIME)
        t(d,item,30,iy+8,13,col=WHITE if is_a else (135,155,215),bold=is_a)

# ── Shared: bar chart (vertical) ─────────────────────────────
def barchart_v(d, x, y, w, h, data, col=LIME, bg=CARD, title=''):
    rr(d,x,y,w,h,fill=bg,ol=BORDER,r=10)
    if title: t(d,title,x+16,y+14,12,col=TEXT2,bold=True)
    PT,PB,PL,PR=44,36,52,16
    n=len(data); bw=(w-PL-PR-8*(n-1))//n
    mx=max(v for _,v in data) if data else 1
    CY=y+PT; CH=h-PT-PB
    for i,(lbl,val) in enumerate(data):
        bx=x+PL+i*(bw+8)
        bh=max(int(CH*val/mx*0.88),4)
        by=CY+CH-bh
        rr(d,bx,by,bw,bh,fill=col,r=5)
        tc(d,lbl,bx+bw//2,CY+CH+4,10,col=TEXT3)
        tc(d,f'{val:,}',bx+bw//2,by-18,10,col=TEXT2,bold=True)

# ── Shared: horizontal bar chart ─────────────────────────────
def barchart_h(d, x, y, w, h, data, col=LIME, bg=CARD, title=''):
    rr(d,x,y,w,h,fill=bg,ol=BORDER,r=10)
    if title: t(d,title,x+16,y+14,12,col=TEXT2,bold=True)
    ITEM_H=36; GAP=10; PL=130; PY=y+44; BW=w-PL-60
    mx=max(v for _,v in data) if data else 1
    for i,(lbl,val) in enumerate(data):
        iy=PY+i*(ITEM_H+GAP)
        t(d,lbl,x+16,iy+9,12,col=TEXT2)
        bw=max(int(BW*val/mx),4)
        rr(d,x+PL,iy,bw,ITEM_H,fill=col,r=6)
        t(d,f'{val:,}',x+PL+bw+8,iy+9,12,col=TEXT2,bold=True)


# ══════════════════════════════════════════════════════════════
# 01 — 메인 랜딩 히어로
# ══════════════════════════════════════════════════════════════
def s01():
    img, d = ni()
    hero_h = 580
    img.paste(gv(W, hero_h, BLUE3, BLUE2), (0,0))
    d = ImageDraw.Draw(img)
    # Decorative
    import random; random.seed(3)
    for _ in range(70):
        rx=random.randint(0,W); ry=random.randint(0,hero_h)
        rs=random.randint(1,3); gc=random.randint(35,60)
        d.ellipse([rx-rs,ry-rs,rx+rs,ry+rs], fill=(gc,gc+8,gc+38))
    d.ellipse([W-250,-80,W+50,220], fill=(35,45,118))
    d.ellipse([-80,320,160,560], fill=(20,26,80))
    # Nav
    nav(img, d)
    d = ImageDraw.Draw(img)
    # Pill
    rr(d,W//2-160,86,320,34,fill=(40,52,124),r=17)
    tc(d,'⚡  B2B 버티컬 광고 플랫폼 — AdMix',W//2,94,13,col=LIME)
    # H1
    tc(d,'버티컬 매체 광고,',W//2,138,58,col=WHITE,bold=True)
    tc(d,'하나의 플랫폼에서',W//2,202,58,col=LIME,bold=True)
    # Subtitle
    tc(d,'맘카페·인벤 등 틈새 버티컬 매체에 광고를 직접 집행하세요. 소재 AI 자동 편집 포함.',W//2,280,16,col=(172,194,238))
    tc(d,'대행사 수수료 0% — 셀프서브로 직접, 더 저렴하게.',W//2,308,16,col=(145,170,220))
    # CTA
    btn(d,W//2-210,356,202,52,'무료로 시작하기',sz=17,r=26)
    btn_ghost(d,W//2+8,356,178,52,'데모 보기',sz=15,r=26)
    # Stats
    for i,(val,lbl) in enumerate([('500+','파트너 매체'),('2.4M+','월 도달 UV'),('380%','평균 ROAS')]):
        sx=W//2-300+i*300
        tc(d,val,sx,434,26,col=LIME,bold=True)
        tc(d,lbl,sx,468,13,col=(158,180,225))
        if i<2: d.line([(sx+120,442),(sx+120,480)],fill=(50,65,130),width=1)
    # Partners
    tc(d,'함께하는 버티컬 매체',W//2,hero_h+24,14,col=TEXT2)
    partners=[('맘카페',LIME_L,LIME_D),('인벤',BLUE_L,BLUE_M),('뽐뿌',BLUE_L,BLUE_M),
              ('클리앙',BLUE_L,BLUE_M),('베이비뉴스',LIME_L,LIME_D),('82cook',BLUE_L,BLUE_M),('루리웹',BLUE_L,BLUE_M)]
    bx=W//2-510
    for pn,pbg,ptc2 in partners:
        pw=tw(d,pn,13,True)+34
        rr(d,bx,hero_h+52,pw,36,fill=pbg,ol=BORDER,r=18)
        tc(d,pn,bx+pw//2,hero_h+61,13,col=ptc2,bold=True)
        bx+=pw+14
    # Features row
    FY=hero_h+108
    rr(d,40,FY,W-80,200,fill=CARD,ol=BORDER,r=14)
    tc(d,'AdMix가 다른 이유',W//2,FY+18,17,col=TEXT,bold=True)
    feats=[('🎯 버티컬 매체 특화','맘카페·게임·IT 등\n틈새 매체만을 위한 플랫폼',LIME),
           ('🤖 AI 소재 자동 편집','매체 사이즈에 맞게\nAI가 자동 최적화',BLUE2),
           ('📊 실시간 성과 분석','캠페인 성과를\n실시간으로 확인',SUCCESS),
           ('💸 대행사 수수료 0%','셀프서브 집행으로\n비용 절감',WARN)]
    fx=W//2-500
    for icon_title,desc,fc in feats:
        tc(d,icon_title,fx,FY+52,14,col=fc,bold=True)
        for li,line in enumerate(desc.split('\n')):
            tc(d,line,fx,FY+78+li*20,12,col=TEXT2)
        fx+=340
    fp=str(OUT/'01_landing_hero.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 01_landing_hero.png')


# ══════════════════════════════════════════════════════════════
# 02 — 서비스 소개
# ══════════════════════════════════════════════════════════════
def s02():
    img, d = ni()
    nav(img, d)
    d = ImageDraw.Draw(img)
    # Header band
    img.paste(gv(W, 140, BLUE, BLUE2), (0,60))
    d = ImageDraw.Draw(img)
    tc(d,'버티컬 매체 & 광고 유형',W//2,84,24,col=WHITE,bold=True)
    tc(d,'맞춤형 버티컬 매체에 다양한 형식의 광고를 집행하세요',W//2,120,14,col=(170,192,235))
    # Category filter
    CATS_Y=210; cats=[('전체',True),('육아/맘',False),('게임',False),('IT/테크',False),('생활정보',False),('뷰티',False),('금융',False)]
    cx3=80
    for clbl,csel in cats:
        cw=tw(d,clbl,13)+24
        rr(d,cx3,CATS_Y,cw,30,fill=BLUE if csel else CARD,ol=BLUE if csel else BORDER,r=15)
        tc(d,clbl,cx3+cw//2,CATS_Y+7,13,col=WHITE if csel else TEXT2,bold=csel)
        cx3+=cw+12
    # Media cards grid (4 cols)
    medias=[
        ('맘카페','육아/맘 커뮤니티','2,400만 UV/월','CPM ₩3,200','배너·네이티브·팝업',LIME_L,LIME_D),
        ('인벤','게이머 전문 미디어','1,820만 UV/월','CPM ₩2,800','배너·비디오·오버레이',BLUE_L,BLUE_M),
        ('뽐뿌','쇼핑 정보 커뮤니티','952만 UV/월','CPM ₩2,100','배너·네이티브',BLUE_L,BLUE_M),
        ('클리앙','IT/테크 커뮤니티','678만 UV/월','CPM ₩3,800','배너·네이티브·스폰서',BLUE_L,BLUE_M),
        ('베이비뉴스','육아 전문 미디어','428만 UV/월','CPM ₩4,200','배너·기사형 광고',LIME_L,LIME_D),
        ('82cook','주부 라이프스타일','380만 UV/월','CPM ₩3,500','배너·네이티브',LIME_L,LIME_D),
        ('루리웹','게임 전문 미디어','542만 UV/월','CPM ₩2,600','배너·비디오',BLUE_L,BLUE_M),
        ('보배드림','자동차/남성 커뮤니티','490만 UV/월','CPM ₩2,900','배너·네이티브',BLUE_L,BLUE_M),
    ]
    MCW=(W-100-3*18)//4; MCH=164; MX=50
    for mi,(mname,mcat,muv,mcpm,mtypes,mbg,mtc2) in enumerate(medias):
        col_i=mi%4; row_i=mi//4
        mx2=MX+col_i*(MCW+18); my2=250+row_i*(MCH+14)
        rr(d,mx2,my2,MCW,MCH,fill=CARD,ol=BORDER,r=10)
        rr(d,mx2,my2,MCW,4,fill=LIME if mbg==LIME_L else BLUE_M,r=2)
        d.ellipse([mx2+16,my2+18,mx2+60,my2+62],fill=mbg)
        tc(d,mname[0],mx2+38,my2+28,20,col=mtc2,bold=True)
        t(d,mname,mx2+72,my2+18,16,col=TEXT,bold=True)
        t(d,mcat,mx2+72,my2+42,11,col=TEXT3)
        t(d,muv,mx2+16,my2+MCH-62,11,col=TEXT3)
        t(d,mcpm,mx2+16,my2+MCH-44,14,col=TEXT,bold=True)
        t(d,mtypes,mx2+16,my2+MCH-22,10,col=TEXT3)
    # Ad types section
    AT_Y=624
    t(d,'지원 광고 유형',50,AT_Y,16,col=TEXT,bold=True)
    ad_types=[('디스플레이 배너','728×90, 300×250\n160×600, 320×100',LIME),
              ('네이티브 광고','기사형, 피드형\n브랜딩 콘텐츠',BLUE2),
              ('동영상 광고','프리롤, 미드롤\n아웃스트림',PURPLE),
              ('팝업 / 오버레이','전면팝업, 하단바\n사이드팝',SUCCESS)]
    aw=(W-100-3*16)//4
    for ai,(aname,adesc,acc) in enumerate(ad_types):
        ax=50+ai*(aw+16)
        rr(d,ax,AT_Y+30,aw,130,fill=CARD,ol=BORDER,r=10)
        rr(d,ax,AT_Y+30,aw,4,fill=acc,r=2)
        t(d,aname,ax+16,AT_Y+50,14,col=TEXT,bold=True)
        for li,line in enumerate(adesc.split('\n')):
            t(d,line,ax+16,AT_Y+76+li*22,12,col=TEXT2)
    fp=str(OUT/'02_service_intro.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 02_service_intro.png')


# ══════════════════════════════════════════════════════════════
# 03 — 요금제/플랜
# ══════════════════════════════════════════════════════════════
def s03():
    img, d = ni()
    nav(img, d)
    d = ImageDraw.Draw(img)
    img.paste(gv(W, 150, BLUE, BLUE2), (0,60))
    d = ImageDraw.Draw(img)
    tc(d,'투명한 요금제',W//2,84,26,col=WHITE,bold=True)
    tc(d,'대행사 수수료 없이 집행 금액의 일정 비율만 플랫폼 수수료로 납부',W//2,126,14,col=(168,190,232))
    # Toggle
    rr(d,W//2-80,222,160,32,fill=BLUE_L,r=16)
    rr(d,W//2-76,226,72,24,fill=BLUE,r=12)
    tc(d,'월간',W//2-40,230,12,col=WHITE,bold=True)
    tc(d,'연간',W//2+40,230,12,col=TEXT3)
    # 3 pricing cards
    plans=[
        ('Starter','스타트업·소상공인','무료','- 월 최대 5개 캠페인\n- 기본 매체 10개\n- 소재 자동 편집 기본\n- 이메일 지원',False),
        ('Growth','성장하는 마케터','₩99,000/월','- 무제한 캠페인\n- 전체 매체 500+\n- AI 후킹 문구 생성\n- 실시간 성과 분석\n- 전화 & 채팅 지원',True),
        ('Enterprise','대형 광고주·대행사','문의','- 전용 계정 매니저\n- 맞춤형 매체 패키지\n- 화이트라벨 대시보드\n- API 연동\n- SLA 99.9%',False),
    ]
    PCW=370; PCY=270
    for pi,(pname,ptag,pprice,pfeats,phigh) in enumerate(plans):
        px=W//2-580+pi*600
        ph_h=480 if phigh else 440
        ph_y=PCY if not phigh else PCY-20
        if phigh:
            rr(d,px-4,ph_y-4,PCW+8,ph_h+8,fill=LIME,r=14)
        rr(d,px,ph_y,PCW,ph_h,fill=WHITE if not phigh else (250,255,250),ol=LIME if phigh else BORDER,r=12,lw=2 if phigh else 1)
        if phigh:
            rr(d,px+PCW//2-52,ph_y-14,104,26,fill=LIME,r=13)
            tc(d,'가장 인기',px+PCW//2,ph_y-7,12,col=BLUE3,bold=True)
        t(d,pname,px+24,ph_y+24,20,col=BLUE if phigh else TEXT,bold=True)
        t(d,ptag,px+24,ph_y+52,12,col=TEXT3)
        d.line([(px+24,ph_y+74),(px+PCW-24,ph_y+74)],fill=BORDER,width=1)
        t(d,pprice,px+24,ph_y+88,28,col=LIME_D if phigh else TEXT,bold=True)
        for fi,feat in enumerate(pfeats.split('\n')):
            t(d,feat,px+24,ph_y+136+fi*34,13,col=TEXT2)
        btn_lbl='무료로 시작' if '무료'==pprice else ('시작하기' if phigh else '문의하기')
        btn(d,px+24,ph_y+ph_h-58,PCW-48,40,btn_lbl,sz=14,
            fill=LIME if phigh else BLUE_L,col=BLUE3 if phigh else BLUE,r=20)
    # FAQ teaser
    t(d,'자주 묻는 질문',50,H-80,14,col=TEXT,bold=True)
    t(d,'계약 없이 언제든지 해지 가능  ·  한국어 지원  ·  부가세 별도',50,H-54,12,col=TEXT3)
    fp=str(OUT/'03_pricing.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 03_pricing.png')


# ══════════════════════════════════════════════════════════════
# 04 — 대시보드 홈
# ══════════════════════════════════════════════════════════════
def s04():
    img, d = ni()
    nav(img, d, '대시보드')
    d = ImageDraw.Draw(img)
    sidebar(img, d, '대시보드')
    MX=240; MY=76
    t(d,'안녕하세요, 재우님 👋',MX,MY,22,col=TEXT,bold=True)
    t(d,'오늘의 캠페인 성과 요약',MX,MY+32,13,col=TEXT3)
    btn(d,W-220,MY-2,172,34,'+ 캠페인 만들기',sz=13,r=17)
    # KPIs
    KW=(W-MX-40-3*14)//4; KY=MY+72
    kpi_data=[('총 노출수','2,481,300','12.4%',True,LIME),('총 클릭수','48,204','8.1%',True,BLUE_M),
              ('전환율','3.82 %','0.5%p',True,SUCCESS),('집행 예산','₩32.9M','4.2%',False,WARN)]
    for i,(lbl,val,chg,up,acc) in enumerate(kpi_data):
        kpi(d,MX+i*(KW+14),KY,KW,100,lbl,val,chg,up,acc)
    # Chart + mini bar
    CH_Y=KY+116; CH_H=216
    CW_L=int((W-MX-40)*0.62); CW_R=W-MX-40-CW_L-16
    linechart(d,MX,CH_Y,CW_L,CH_H,
              [28400,32100,35800,41200,44800,46100,48204],
              col=LIME,title='일별 클릭수 추이 (최근 7일)',
              data2=[25000,27000,30000,35000,38000,40000,42000],col2=BLUE_L)
    barchart_h(d,MX+CW_L+16,CH_Y,CW_R,CH_H,
               [('맘카페',18600000),('인벤',8300000),('클리앙',4200000),('뽐뿌',1800000)],
               col=LIME,title='매체별 예산 집행')
    # Campaign cards
    CAM_Y=CH_Y+CH_H+18
    t(d,'진행 중인 캠페인',MX,CAM_Y,16,col=TEXT,bold=True)
    cams=[('맘카페 유아식품','집행중','₩8.4M','72',LIME),
          ('인벤 게이밍 광고','집행중','₩5.2M','53',LIME),
          ('클리앙 테크 제품','일시정지','₩2.8M','56',WARN),
          ('+ 새 캠페인',None,None,None,None)]
    CW=(W-MX-40-3*14)//4; CARDY=CAM_Y+34
    for ci,(cname,cstat,cbudget,cpct,cacc) in enumerate(cams):
        cx=MX+ci*(CW+14)
        rr(d,cx,CARDY,CW,H-CARDY-20,fill=CARD,ol=BORDER,r=10)
        if cacc is None:
            tc(d,'+',cx+CW//2,CARDY+80,36,col=BORDER2,bold=True)
            tc(d,'새 캠페인',cx+CW//2,CARDY+130,14,col=TEXT3)
            continue
        rr(d,cx,CARDY,CW,5,fill=cacc,r=2)
        sbadge(d,cx+14,CARDY+18,cstat)
        t(d,cname,cx+14,CARDY+50,14,col=TEXT,bold=True)
        t(d,'예산',cx+14,CARDY+80,11,col=TEXT3)
        t(d,cbudget,cx+14,CARDY+96,16,col=TEXT,bold=True)
        rr(d,cx+14,CARDY+H-CARDY-50,CW-28,8,fill=(230,234,252),r=4)
        rr(d,cx+14,CARDY+H-CARDY-50,int((CW-28)*int(cpct)/100),8,fill=cacc,r=4)
        t(d,f'{cpct}%',cx+CW-44,CARDY+H-CARDY-54,11,col=TEXT3)
    fp=str(OUT/'04_dashboard_home.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 04_dashboard_home.png')


# ══════════════════════════════════════════════════════════════
# 05 — 캠페인 생성 Step1: 매체 선택
# ══════════════════════════════════════════════════════════════
def s05():
    img, d = ni()
    nav(img, d, '캠페인')
    d = ImageDraw.Draw(img)
    STEPS=['매체 선택','소재 업로드','사이즈 조정','예산 & 일정']
    stepbar(img,d,STEPS,0); d=ImageDraw.Draw(img)
    MX=48; BODY_Y=128
    t(d,'어떤 매체에 광고하시겠어요?',MX,BODY_Y,20,col=TEXT,bold=True)
    t(d,'버티컬 카테고리별로 최적의 매체를 선택하세요',MX,BODY_Y+30,13,col=TEXT3)
    # Filter + search
    rr(d,MX,BODY_Y+72,280,36,fill=CARD,ol=BORDER,r=18)
    t(d,'🔍  매체 검색...',MX+18,BODY_Y+81,13,col=TEXT3)
    cats3=[('전체',True),('육아/맘',False),('게임',False),('IT/테크',False),('생활정보',False),('뷰티',False)]
    cx4=MX+300
    for clbl,csel in cats3:
        cw=tw(d,clbl,12)+22
        rr(d,cx4,BODY_Y+76,cw,28,fill=BLUE if csel else CARD,ol=BLUE if csel else BORDER,r=14)
        tc(d,clbl,cx4+cw//2,BODY_Y+82,12,col=WHITE if csel else TEXT2,bold=csel)
        cx4+=cw+10
    # Bidding type row
    t(d,'과금 방식',MX,BODY_Y+124,12,col=TEXT3,bold=True)
    for bi,(blbl,bsel) in enumerate([('CPM (노출당)',True),('CPC (클릭당)',False),('예산소진형',False)]):
        bx=MX+bi*200
        rr(d,bx,BODY_Y+142,188,34,fill=BLUE if bsel else CARD,ol=BLUE if bsel else BORDER,r=17)
        tc(d,blbl,bx+94,BODY_Y+149,13,col=WHITE if bsel else TEXT2,bold=bsel)
    # Media grid (3 cols)
    GRID_Y=BODY_Y+192; LW=int((W-MX*2)*0.65)
    MCW2=(LW-2*12)//3; MCH2=148
    medias2=[('맘카페','육아/맘','2,400만','₩3,200',True,True),
             ('인벤','게임','1,820만','₩2,800',True,False),
             ('클리앙','IT/테크','678만','₩3,800',False,True),
             ('뽐뿌','생활정보','952만','₩2,100',False,False),
             ('베이비뉴스','육아/맘','428만','₩4,200',True,True),
             ('루리웹','게임','542만','₩2,600',False,False)]
    for mi,(mn,mc,muv,mcpm,msel,mrec) in enumerate(medias2):
        col_i=mi%3; row_i=mi//3
        mx3=MX+col_i*(MCW2+12); my3=GRID_Y+row_i*(MCH2+12)
        bo=LIME if msel else BORDER; bg3=LIME_L if msel else CARD
        rr(d,mx3,my3,MCW2,MCH2,fill=bg3,ol=bo,lw=2 if msel else 1,r=10)
        if mrec:
            rr(d,mx3+8,my3+8,60,20,fill=WARNL,r=10)
            t(d,'⭐ 추천',mx3+14,my3+11,10,col=WARN)
        cb_f=LIME if msel else (230,234,250)
        rr(d,mx3+MCW2-34,my3+MCH2-36,22,22,fill=cb_f,r=5)
        if msel: tc(d,'✓',mx3+MCW2-23,my3+MCH2-34,12,col=BLUE3,bold=True)
        d.ellipse([mx3+14,my3+30,mx3+58,my3+74],fill=LIME_L if msel else BLUE_L)
        tc(d,mn[0],mx3+36,my3+40,18,col=LIME_D if msel else BLUE_M,bold=True)
        t(d,mn,mx3+68,my3+30,16,col=TEXT,bold=True)
        t(d,mc,mx3+68,my3+52,11,col=TEXT3)
        t(d,'월 UV',mx3+14,my3+MCH2-52,10,col=TEXT3)
        t(d,muv,mx3+14,my3+MCH2-36,13,col=TEXT,bold=True)
        t(d,'CPM',mx3+MCW2//2+10,my3+MCH2-52,10,col=TEXT3)
        t(d,mcpm,mx3+MCW2//2+10,my3+MCH2-36,13,col=TEXT,bold=True)
    # Right panel
    RX=MX+LW+16; RW=W-RX-MX
    rr(d,RX,GRID_Y,RW,H-GRID_Y-20,fill=CARD,ol=BORDER,r=10)
    d.rectangle([RX,GRID_Y,RX+RW,GRID_Y+50],fill=BLUE)
    rr(d,RX,GRID_Y,RW,50,fill=BLUE,r=10)
    d.rectangle([RX,GRID_Y+30,RX+RW,GRID_Y+50],fill=BLUE)
    tc(d,'선택 요약',RX+RW//2,GRID_Y+15,13,col=WHITE,bold=True)
    t(d,'선택 매체: 맘카페, 클리앙',RX+16,GRID_Y+62,12,col=TEXT2)
    t(d,'과금 방식: CPM',RX+16,GRID_Y+82,12,col=TEXT2)
    d.line([(RX+16,GRID_Y+106),(RX+RW-16,GRID_Y+106)],fill=BORDER,width=1)
    t(d,'예상 도달',RX+16,GRID_Y+118,11,col=TEXT3)
    t(d,'3,078만',RX+16,GRID_Y+136,18,col=TEXT,bold=True)
    t(d,'예상 CPM',RX+RW//2,GRID_Y+118,11,col=TEXT3)
    t(d,'₩3,520',RX+RW//2,GRID_Y+136,18,col=TEXT,bold=True)
    btn(d,RX+12,H-60,RW-24,40,'다음: 소재 업로드 →',sz=13,r=20)
    fp=str(OUT/'05_campaign_step1_media.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 05_campaign_step1_media.png')


# ══════════════════════════════════════════════════════════════
# 06 — 캠페인 Step2: 소재 업로드 & AI 자동 편집
# ══════════════════════════════════════════════════════════════
def s06():
    img, d = ni()
    nav(img, d, '소재')
    d = ImageDraw.Draw(img)
    STEPS=['매체 선택 ✓','소재 업로드','사이즈 조정','예산 & 일정']
    stepbar(img,d,STEPS,1); d=ImageDraw.Draw(img)
    # AI banner
    ai_g=gh(W,50,(200,60,0),(255,107,53)); img.paste(ai_g,(0,120)); d=ImageDraw.Draw(img)
    t(d,'✨ AI 후킹 문구 추천:',32,133,13,col=WHITE,bold=True)
    t(d,'"여름 특가! 아기사랑 분유 10% 할인 — 지금 바로!"',250,135,13,col=(255,235,218))
    rr(d,W-184,130,152,30,fill=(210,65,10),r=15)
    tc(d,'✨ 문구 재생성',W-184+76,137,12,col=WHITE,bold=True)
    BODY_Y=176; MX=0
    # 3-panel
    LP_W=280; RP_W=340; CP_W=W-LP_W-RP_W
    # LEFT: source
    d.rectangle([0,BODY_Y,LP_W,H],fill=BLUE3)
    t(d,'원본 소재',18,BODY_Y+14,13,col=(155,175,220),bold=True)
    d.line([(0,BODY_Y+40),(LP_W,BODY_Y+40)],fill=(32,40,110),width=1)
    UY=BODY_Y+50; UH=190
    rr(d,14,UY,LP_W-28,UH,fill=(28,36,92),ol=(45,60,140),r=8)
    tc(d,'🖼',LP_W//2,UY+50,36,col=(55,75,145))
    tc(d,'이미지 드래그 또는 클릭',LP_W//2,UY+110,12,col=(120,145,205))
    tc(d,'PNG · JPG · 최대 10MB',LP_W//2,UY+132,11,col=(85,108,165))
    # Uploaded file
    rr(d,14,UY+UH+10,LP_W-28,72,fill=(28,36,92),r=6)
    t(d,'분유_메인이미지.jpg',22,UY+UH+22,11,col=(190,210,245))
    t(d,'1920×1080  ·  2.4MB',22,UY+UH+40,10,col=(110,135,190))
    rr(d,22,UY+UH+56,60,18,fill=(38,48,118),r=9)
    tc(d,'교체',52,UY+UH+59,10,col=(170,195,240))
    t(d,'AI 편집 설정',18,UY+UH+98,12,col=(155,175,220),bold=True)
    for ci5,(co,csel) in enumerate([('스마트 크롭',True),('중앙',False),('상단',False)]):
        cw5=tw(d,co,11)+14
        rr(d,18+ci5*88,UY+UH+116,cw5,24,fill=LIME if csel else (28,36,92),r=12)
        tc(d,co,(18+ci5*88)+cw5//2,UY+UH+120,11,col=BLUE3 if csel else (140,162,215))
    # File list
    for fi,(fn,fsz) in enumerate([('분유_메인.jpg','2.4MB'),('제품_화이트.png','1.1MB')]):
        fy=BODY_Y+H-BODY_Y-100+fi*48
        rr(d,14,fy,LP_W-28,42,fill=(28,36,92),r=6)
        t(d,fn,24,fy+10,11,col=(190,210,245)); t(d,fsz,24,fy+28,10,col=(100,128,180))
    # CENTER: AI size previews
    CP_X=LP_W
    d.rectangle([CP_X,BODY_Y,CP_X+CP_W,H],fill=BG)
    t(d,'AI 자동 생성 — 매체별 사이즈',CP_X+20,BODY_Y+12,13,col=TEXT2,bold=True)
    rr(d,CP_X+CP_W-180,BODY_Y+8,168,28,fill=LIME_L,ol=LIME,r=14,lw=1)
    tc(d,'5개 사이즈 자동 생성 완료 ✓',CP_X+CP_W-96,BODY_Y+14,11,col=LIME_D,bold=True)
    d.line([(CP_X,BODY_Y+42),(CP_X+CP_W,BODY_Y+42)],fill=BORDER,width=1)
    sizes=[('728×90','리더보드',728,90),('300×250','미디엄 렉탱글',300,250),
           ('320×480','하프 페이지',320,480),('160×600','와이드 스카이',160,600),('320×100','모바일 배너',320,100)]
    SC=0.13; PRV_Y=BODY_Y+52; px_cols=[CP_X+20,CP_X+CP_W//2+10]
    cur_ys=[PRV_Y,PRV_Y]
    for si,(slbl,ssub,sw5,sh5) in enumerate(sizes):
        col_i=si%2; cx6=px_cols[col_i]; cy6=cur_ys[col_i]
        dw6=max(int(sw5*SC),32); dh6=max(int(sh5*SC),14)
        if dh6>100: dh6=100; dw6=max(int(sw5*100/sh5*SC),20)
        card_h=dh6+60
        HW=(CP_W//2-30)
        rr(d,cx6,cy6,HW,card_h,fill=CARD,ol=BORDER,r=8)
        prv_x=cx6+(HW-dw6)//2; prv_y=cy6+8
        rr(d,prv_x,prv_y,dw6,dh6,fill=(215,220,242),ol=BORDER2,r=3)
        rr(d,prv_x+2,prv_y+2,dw6//3,dh6-4,fill=BLUE_L,r=2)
        rr(d,prv_x+dw6-int(30*SC)-10,prv_y+2,int(28*SC)+10,dh6-4,fill=LIME,r=2)
        tc(d,slbl,cx6+HW//2,cy6+card_h-42,11,col=TEXT,bold=True)
        tc(d,ssub,cx6+HW//2,cy6+card_h-24,10,col=TEXT3)
        cur_ys[col_i]+=card_h+10
    # RIGHT: Controls
    RP_X=CP_X+CP_W
    d.rectangle([RP_X,BODY_Y,RP_X+RP_W,H],fill=CARD)
    d.line([(RP_X,BODY_Y),(RP_X,H)],fill=BORDER,width=1)
    t(d,'편집 설정',RP_X+16,BODY_Y+14,14,col=TEXT,bold=True)
    d.line([(RP_X,BODY_Y+42),(RP_X+RP_W,BODY_Y+42)],fill=BORDER,width=1)
    ry=BODY_Y+54
    for lbl4,val4 in [('배경 처리','자동 제거'),('텍스트 오버레이','ON'),('로고 위치','우하단'),('품질','고품질')]:
        t(d,lbl4,RP_X+16,ry,11,col=TEXT3)
        rr(d,RP_X+16,ry+16,RP_W-32,30,fill=BG,ol=BORDER,r=6)
        t(d,val4,RP_X+28,ry+22,12,col=TEXT); ry+=56
    t(d,'AI 후킹 문구 선택',RP_X+16,ry,12,col=TEXT,bold=True); ry+=20
    for ai_p,ai_sel in [('"여름 특가! 아기사랑 분유..."',True),('"지금 바로 시작하는 건강한..."',False)]:
        rr(d,RP_X+16,ry,RP_W-32,38,fill=LIME_L if ai_sel else BG,ol=LIME if ai_sel else BORDER,r=6)
        t(d,ai_p,RP_X+24,ry+10,10,col=LIME_D if ai_sel else TEXT2); ry+=46
    btn(d,RP_X+12,H-56,RP_W-24,38,'다음: 사이즈 조정 →',sz=13,r=19)
    fp=str(OUT/'06_campaign_step2_creative.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 06_campaign_step2_creative.png')


# ══════════════════════════════════════════════════════════════
# 07 — 캠페인 Step3: 사이즈별 세부 조정
# ══════════════════════════════════════════════════════════════
def s07():
    img, d = ni()
    nav(img, d, '소재')
    d = ImageDraw.Draw(img)
    STEPS=['매체 선택 ✓','소재 업로드 ✓','사이즈 조정','예산 & 일정']
    stepbar(img,d,STEPS,2); d=ImageDraw.Draw(img)
    BODY_Y=126
    LP_W=260; RP_W=320; CP_W=W-LP_W-RP_W
    # LEFT: size list
    d.rectangle([0,BODY_Y,LP_W,H],fill=WHITE)
    d.line([(LP_W,BODY_Y),(LP_W,H)],fill=BORDER,width=1)
    t(d,'사이즈 목록',16,BODY_Y+14,13,col=TEXT,bold=True)
    d.line([(0,BODY_Y+40),(LP_W,BODY_Y+40)],fill=BORDER,width=1)
    sizes2=[('728×90','리더보드',True),('300×250','미디엄 렉탱글',False),
            ('320×480','하프 페이지',False),('160×600','와이드 스카이',False),('320×100','모바일 배너',False)]
    for si,(slbl,ssub,ssel) in enumerate(sizes2):
        sy=BODY_Y+50+si*68
        bg4=LIME_L if ssel else WHITE; bo4=LIME if ssel else BORDER
        rr(d,8,sy,LP_W-16,60,fill=bg4,ol=bo4,r=8,lw=2 if ssel else 1)
        if ssel: d.rectangle([8,sy,12,sy+60],fill=LIME)
        # Mini preview proportional
        dw7=int(728*0.06 if '728' in slbl else (300*0.1 if '300' in slbl else (160*0.05 if '160' in slbl else 60)))
        dh7=int(90*0.06*dw7/(728*0.06) if '728' in slbl else max(14,min(50,int(250*0.1))))
        dw7=max(20,min(60,dw7)); dh7=max(6,min(44,dh7))
        rr(d,20,sy+10,dw7,dh7,fill=(210,215,240),r=2)
        t(d,slbl,92,sy+12,13,col=LIME_D if ssel else TEXT,bold=ssel)
        t(d,ssub,92,sy+34,11,col=TEXT3)
    # CENTER: canvas
    CP_X=LP_W
    d.rectangle([CP_X,BODY_Y,CP_X+CP_W,H],fill=(240,242,252))
    t(d,'728 × 90 — 편집 캔버스',CP_X+20,BODY_Y+14,13,col=TEXT2,bold=True)
    d.line([(CP_X,BODY_Y+40),(CP_X+CP_W,BODY_Y+40)],fill=BORDER,width=1)
    CV_W=CP_W-80; CV_H=int(CV_W*90/728); CV_X=CP_X+40; CV_Y=BODY_Y+80
    rr(d,CV_X,CV_Y,CV_W,CV_H,fill=(215,220,240),ol=BORDER2,r=3)
    rr(d,CV_X+4,CV_Y+4,CV_W//4,CV_H-8,fill=BLUE_L,r=2)
    tc(d,'로고',CV_X+CV_W//8,CV_Y+CV_H//2-8,10,col=BLUE_M)
    t(d,'여름 특가! 아기사랑 분유 10% 할인 — 지금!',CV_X+CV_W//4+12,CV_Y+CV_H//2-8,min(13,int(CV_H*0.4)),col=(30,35,100),bold=True)
    rr(d,CV_X+CV_W-84,CV_Y+4,72,CV_H-8,fill=LIME,r=3)
    tc(d,'구매하기',CV_X+CV_W-48,CV_Y+CV_H//2-8,11,col=BLUE3,bold=True)
    for gx8,gy8 in [(CV_X,CV_Y),(CV_X+CV_W,CV_Y),(CV_X,CV_Y+CV_H),(CV_X+CV_W,CV_Y+CV_H)]:
        d.line([(gx8-10,gy8),(gx8+10,gy8)],fill=LIME,width=2)
        d.line([(gx8,gy8-10),(gx8,gy8+10)],fill=LIME,width=2)
    # Guide lines
    d.line([(CV_X+CV_W//4,CV_Y),(CV_X+CV_W//4,CV_Y+CV_H)],fill=(200,207,235),width=1)
    d.line([(CV_X+CV_W*3//4,CV_Y),(CV_X+CV_W*3//4,CV_Y+CV_H)],fill=(200,207,235),width=1)
    # Crop handles
    for hx,hy in [(CV_X+CV_W//4-6,CV_Y+CV_H//2-6),(CV_X+CV_W*3//4-6,CV_Y+CV_H//2-6)]:
        rr(d,hx,hy,12,12,fill=WHITE,ol=BLUE,r=3,lw=2)
    # Toolbar
    tool_y=CV_Y+CV_H+20
    tools=[('이동',True),('크롭',False),('텍스트',False),('배경',False)]
    tx8=CP_X+40
    for tn,tsel in tools:
        tw8=tw(d,tn,12)+24
        rr(d,tx8,tool_y,tw8,30,fill=BLUE if tsel else CARD,ol=BLUE if tsel else BORDER,r=15)
        tc(d,tn,tx8+tw8//2,tool_y+7,12,col=WHITE if tsel else TEXT2,bold=tsel)
        tx8+=tw8+10
    # Background options
    t(d,'배경 스타일',CP_X+40,tool_y+50,12,col=TEXT2,bold=True)
    for bi,(blbl,bsel) in enumerate([('원본 유지',True),('블러',False),('단색',False),('제거',False)]):
        bx=CP_X+40+bi*140
        rr(d,bx,tool_y+68,128,30,fill=BLUE if bsel else CARD,ol=BLUE if bsel else BORDER,r=15)
        tc(d,blbl,bx+64,tool_y+75,12,col=WHITE if bsel else TEXT2,bold=bsel)
    # RIGHT: properties
    RP_X=CP_X+CP_W
    d.rectangle([RP_X,BODY_Y,RP_X+RP_W,H],fill=WHITE)
    d.line([(RP_X,BODY_Y),(RP_X,H)],fill=BORDER,width=1)
    t(d,'속성 편집',RP_X+16,BODY_Y+14,14,col=TEXT,bold=True)
    d.line([(RP_X,BODY_Y+40),(RP_X+RP_W,BODY_Y+40)],fill=BORDER,width=1)
    py5=BODY_Y+54
    for ln,lv in [('X 위치','0 px'),('Y 위치','0 px'),('너비','728 px'),('높이','90 px')]:
        t(d,ln,RP_X+16,py5,10,col=TEXT3)
        rr(d,RP_X+16,py5+16,RP_W-32,28,fill=BG,ol=BORDER,r=5)
        t(d,lv,RP_X+26,py5+21,12,col=TEXT); py5+=52
    t(d,'스케일',RP_X+16,py5,10,col=TEXT3)
    rr(d,RP_X+16,py5+16,RP_W-32,8,fill=(228,232,252),r=4)
    rr(d,RP_X+16,py5+16,int((RP_W-32)*0.78),8,fill=LIME,r=4)
    d.ellipse([RP_X+16+int((RP_W-32)*0.78)-7,py5+12,RP_X+16+int((RP_W-32)*0.78)+7,py5+28],fill=LIME)
    py5+=46
    t(d,'텍스트 오버레이',RP_X+16,py5,10,col=TEXT3)
    tg=RP_X+RP_W-46
    rr(d,tg,py5+14,38,20,fill=LIME,r=10)
    d.ellipse([tg+18,py5+16,tg+34,py5+32],fill=WHITE)
    py5+=50
    t(d,'폰트 크기',RP_X+16,py5,10,col=TEXT3)
    rr(d,RP_X+16,py5+16,RP_W-32,28,fill=BG,ol=BORDER,r=5)
    t(d,'18 pt',RP_X+26,py5+22,12,col=TEXT)
    btn(d,RP_X+12,H-56,RP_W-24,38,'다음: 예산 설정 →',sz=13,r=19)
    fp=str(OUT/'07_campaign_step3_size.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 07_campaign_step3_size.png')


# ══════════════════════════════════════════════════════════════
# 08 — 캠페인 Step4: 예산 & 스케줄
# ══════════════════════════════════════════════════════════════
def s08():
    img, d = ni()
    nav(img, d, '캠페인')
    d = ImageDraw.Draw(img)
    STEPS=['매체 선택 ✓','소재 업로드 ✓','사이즈 조정 ✓','예산 & 일정']
    stepbar(img,d,STEPS,3); d=ImageDraw.Draw(img)
    MX=200; BODY_Y=132; FORM_W=800
    t(d,'예산과 집행 일정을 설정하세요',MX,BODY_Y,20,col=TEXT,bold=True)
    t(d,'집행 예산과 기간을 설정하면 일일 예산이 자동 계산됩니다',MX,BODY_Y+30,13,col=TEXT3)
    FY=BODY_Y+72
    rr(d,MX,FY,FORM_W,490,fill=CARD,ol=BORDER,r=12)
    def field2(lbl,x,y,w,ph='',val='',req=True):
        marker=' *' if req else ''
        t(d,lbl+marker,x,y,12,col=TEXT2,bold=True)
        rr(d,x,y+20,w,36,fill=BG,ol=BORDER,r=6)
        t(d,val if val else ph,x+12,y+28,13,col=TEXT if val else TEXT3)
    FM=MX+32; FW=FORM_W-64; half=(FW-20)//2
    field2('캠페인 이름',FM,FY+20,FW,val='여름 신제품 맘카페 광고')
    field2('총 예산 (원)',FM,FY+92,half,val='8,400,000')
    t(d,'원',FM+half-30,FY+128,12,col=TEXT3)
    field2('일일 예산 한도',FM+half+20,FY+92,half,ph='자동 계산')
    t(d,'₩271,000/일 (자동)',FM+half+32,FY+130,12,col=TEXT3)
    # Date pickers
    t(d,'집행 기간 *',FM,FY+164,12,col=TEXT2,bold=True)
    half2=(half-12)//2
    rr(d,FM,FY+184,half2,36,fill=BG,ol=BORDER,r=6)
    t(d,'2024-05-01  📅',FM+12,FY+194,12,col=TEXT)
    t(d,'~',FM+half2+4,FY+195,14,col=TEXT3)
    rr(d,FM+half2+18,FY+184,half2,36,fill=BG,ol=BORDER,r=6)
    t(d,'2024-05-31  📅',FM+half2+30,FY+194,12,col=TEXT)
    t(d,'집행 기간: 31일',FM+half+20,FY+192,13,col=LIME_D,bold=True)
    # Bidding details
    t(d,'입찰 방식 *',FM,FY+244,12,col=TEXT2,bold=True)
    for bi,(blbl,bval,bsel) in enumerate([('CPM 고정','₩3,200/1,000노출',True),('CPC 자동','AI 최적화 입찰',False),('일 예산 소진형','일일 예산 내 최대 노출',False)]):
        bx=FM+bi*(FW//3+8)
        rr(d,bx,FY+264,FW//3,64,fill=LIME_L if bsel else BG,ol=LIME if bsel else BORDER,r=8,lw=2 if bsel else 1)
        t(d,blbl,bx+14,FY+276,13,col=LIME_D if bsel else TEXT,bold=bsel)
        t(d,bval,bx+14,FY+296,11,col=TEXT3)
    # Daily budget breakdown
    t(d,'예산 배분',FM,FY+348,12,col=TEXT2,bold=True)
    for mi,(mn,mpct) in enumerate([('맘카페',70),('클리앙',30)]):
        my4=FY+368+mi*44
        t(d,mn,FM,my4+4,12,col=TEXT2)
        t(d,f'{mpct}%',FM+80,my4+4,12,col=TEXT3)
        SB_W=FW-160; amt3=int(8400000*mpct/100)
        rr(d,FM+120,my4+8,SB_W,8,fill=(228,232,252),r=4)
        rr(d,FM+120,my4+8,int(SB_W*mpct/100),8,fill=LIME,r=4)
        t(d,f'₩{amt3:,}',FM+120+SB_W+8,my4+2,12,col=TEXT2,bold=True)
    # Summary box
    rr(d,FM,FY+462,FW,60,fill=BLUE_L,ol=BLUE_L,r=8)
    t(d,'총 예산 ₩8,400,000  ·  집행 기간 31일  ·  일일 평균 ₩271,000',FM+16,FY+476,13,col=BLUE,bold=True)
    t(d,'예상 노출: 약 2,625,000회  ·  예상 클릭: 약 52,500회',FM+16,FY+498,12,col=BLUE_M)
    # Buttons
    d.line([(MX,FY+500),(MX+FORM_W+240,FY+500)],fill=BORDER,width=1)
    rr(d,MX,FY+510,120,36,ol=BORDER,r=18)
    tc(d,'← 이전',MX+60,FY+518,13,col=TEXT2)
    btn(d,MX+FORM_W-148,FY+510,152,36,'🚀 캠페인 시작하기',sz=14,r=18)
    # Right summary card
    SX=MX+FORM_W+32; SW=W-SX-40
    rr(d,SX,FY,SW,H-FY-20,fill=CARD,ol=BORDER,r=12)
    rr(d,SX,FY,SW,50,fill=BLUE,r=12)
    d.rectangle([SX,FY+28,SX+SW,FY+50],fill=BLUE)
    tc(d,'캠페인 요약',SX+SW//2,FY+15,13,col=WHITE,bold=True)
    sy6=FY+62
    for k,v in [('캠페인명','여름 신제품...'),('선택 매체','맘카페, 클리앙'),('소재 사이즈','5개'),('집행 기간','05/01~05/31')]:
        t(d,k,SX+16,sy6,11,col=TEXT3)
        t(d,v,SX+16,sy6+18,13,col=TEXT); sy6+=46
    fp=str(OUT/'08_campaign_step4_budget.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 08_campaign_step4_budget.png')


# ══════════════════════════════════════════════════════════════
# 09 — 캠페인 목록
# ══════════════════════════════════════════════════════════════
def s09():
    img, d = ni()
    nav(img, d, '캠페인')
    d = ImageDraw.Draw(img)
    sidebar(img, d, '캠페인 관리')
    MX=240; MY=76
    t(d,'캠페인 관리',MX,MY,22,col=TEXT,bold=True)
    t(d,'총 12개 캠페인 · 집행중 3개',MX,MY+32,13,col=TEXT3)
    btn(d,W-220,MY-2,172,34,'+ 캠페인 만들기',sz=13,r=17)
    # Filters
    FILTER_Y=MY+68
    rr(d,MX,FILTER_Y,320,36,fill=CARD,ol=BORDER,r=18)
    t(d,'🔍  캠페인 검색...',MX+16,FILTER_Y+10,13,col=TEXT3)
    tabs=[('전체',True),('집행중',False),('일시정지',False),('완료',False),('검토중',False)]
    tx9=MX+338
    for tlbl,tsel in tabs:
        tw9=tw(d,tlbl,12)+22
        rr(d,tx9,FILTER_Y+4,tw9,28,fill=BLUE if tsel else CARD,ol=BLUE if tsel else BORDER,r=14)
        tc(d,tlbl,tx9+tw9//2,FILTER_Y+9,12,col=WHITE if tsel else TEXT2,bold=tsel)
        tx9+=tw9+10
    # Table
    TABLE_Y=FILTER_Y+52
    d.rectangle([MX,TABLE_Y,W-40,TABLE_Y+36],fill=BLUE_L)
    cols9=[('캠페인명',220),('상태',90),('매체',130),('예산',110),('소진율',110),('노출',100),('클릭',90),('전환율',80),('기간',120),('관리',80)]
    hx9=MX+14
    for cn,cw9 in cols9:
        t(d,cn,hx9,TABLE_Y+10,11,col=BLUE_M,bold=True); hx9+=cw9
    d.line([(MX,TABLE_Y+36),(W-40,TABLE_Y+36)],fill=BORDER,width=1)
    rows9=[
        ('맘카페 유아식품 캠페인','집행중','맘카페·베이비','₩8.4M',72,1240000,18300,'3.8%','04/01-04/30'),
        ('인벤 게이밍 디바이스','집행중','인벤·루리웹','₩5.2M',53,820000,12100,'2.9%','04/10-05/09'),
        ('뽐뿌 생활가전 프로모션','대기','뽐뿌','₩3.6M',0,0,0,'—','05/01-05/31'),
        ('클리앙 테크 제품 리뷰','완료','클리앙','₩2.8M',100,460000,6800,'4.2%','03/01-03/31'),
        ('맘카페 육아용품 시즌','검토중','맘카페','₩6.1M',0,0,0,'—','05/15-06/14'),
        ('인벤 신규 게임 론칭','집행중','인벤','₩4.2M',38,380000,5400,'2.1%','04/15-05/14'),
        ('82cook 주방가전','일시정지','82cook','₩1.8M',45,190000,2800,'1.8%','04/05-04/25'),
    ]
    for ri,(rname,rstat,rmedia,rbudget,rpct,rimp,rclk,rctr,rperiod) in enumerate(rows9):
        ry9=TABLE_Y+36+ri*52
        bg9=CARD if ri%2==0 else (249,250,255)
        d.rectangle([MX,ry9,W-40,ry9+52],fill=bg9)
        d.line([(MX,ry9+52),(W-40,ry9+52)],fill=BORDER,width=1)
        rx9=MX+14
        t(d,rname,rx9,ry9+12,13,col=TEXT,bold=True)
        t(d,rmedia,rx9,ry9+32,10,col=TEXT3); rx9+=220
        sbadge(d,rx9,ry9+17,rstat); rx9+=90
        t(d,rmedia[:8],rx9,ry9+20,11,col=TEXT2); rx9+=130
        t(d,rbudget,rx9,ry9+20,12,col=TEXT); rx9+=110
        bw9=70
        rr(d,rx9,ry9+22,bw9,8,fill=(228,232,252),r=4)
        if rpct: rr(d,rx9,ry9+22,int(bw9*rpct/100),8,fill=LIME,r=4)
        t(d,f'{rpct}%',rx9,ry9+34,9,col=TEXT3); rx9+=110
        t(d,f'{rimp:,}' if rimp else '—',rx9,ry9+20,12,col=TEXT); rx9+=100
        t(d,f'{rclk:,}' if rclk else '—',rx9,ry9+20,12,col=TEXT); rx9+=90
        t(d,rctr,rx9,ry9+20,12,col=TEXT); rx9+=80
        t(d,rperiod,rx9,ry9+20,11,col=TEXT3); rx9+=120
        rr(d,rx9,ry9+14,60,24,ol=BORDER,r=5)
        tc(d,'관리',rx9+30,ry9+20,11,col=TEXT2)
    t(d,'총 12개 · 1/2 페이지',MX,H-28,11,col=TEXT3)
    fp=str(OUT/'09_campaign_list.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 09_campaign_list.png')


# ══════════════════════════════════════════════════════════════
# 10 — 캠페인 상세 (매체별 성과 비교)
# ══════════════════════════════════════════════════════════════
def s10():
    img, d = ni()
    nav(img, d, '캠페인')
    d = ImageDraw.Draw(img)
    sidebar(img, d, '캠페인 관리')
    MX=240; MY=76
    t(d,'맘카페 유아식품 캠페인',MX,MY,20,col=TEXT,bold=True)
    sbadge(d,MX,MY+34,'집행중')
    t(d,'2024-04-01 ~ 2024-04-30  ·  예산 ₩8,400,000',MX+100,MY+38,12,col=TEXT3)
    btn(d,W-220,MY-2,172,34,'캠페인 수정',sz=13,r=17)
    KY=MY+76; KW=(W-MX-40-3*14)//4
    kpi_d=[('총 노출수','1,240,000','18.4%',True,LIME),('총 클릭수','18,300','12.1%',True,BLUE_M),
           ('전환율','3.8%','0.6%p',True,SUCCESS),('소진율','72%','—',True,WARN)]
    for i,(lbl,val,chg,up,acc) in enumerate(kpi_d):
        kpi(d,MX+i*(KW+14),KY,KW,100,lbl,val,chg,up,acc)
    CY=KY+116; CH=210; CW_L=int((W-MX-40)*0.60); CW_R=W-MX-40-CW_L-16
    linechart(d,MX,CY,CW_L,CH,[8200,9100,10400,12100,14200,15800,18300],
              col=LIME,title='일별 클릭수 — 맘카페 vs 베이비뉴스',
              data2=[1200,1400,1600,1900,2100,2400,2800],col2=BLUE_M)
    barchart_v(d,MX+CW_L+16,CY,CW_R,CH,
               [('맘카페',16200),('베이비뉴스',2100)],
               col=LIME,title='매체별 클릭수')
    # Media comparison table
    MCY=CY+CH+16
    t(d,'매체별 성과 비교',MX,MCY,15,col=TEXT,bold=True)
    rr(d,MX,MCY+28,W-MX-40,36,fill=BLUE_L,r=6)
    mcols=[('매체',140),('노출수',120),('클릭수',110),('CTR',90),('전환',90),('CPA',110),('소진 예산',120)]
    hxm=MX+14
    for cn,cw in mcols:
        t(d,cn,hxm,MCY+38,11,col=BLUE_M,bold=True); hxm+=cw
    mrows=[('맘카페',1,112000,16800,'2.9%',320,'₩23,040','₩6,220,000'),
           ('베이비뉴스',1,128000,1500,'1.2%',22,'₩99,000','₩2,180,000')]
    for ri,(mn,_,mimp,mclk,mctr,mcv,mcpa,mbudget) in enumerate(mrows):
        ry=MCY+64+ri*48
        d.rectangle([MX,ry,MX+sum(c[1] for c in mcols),ry+48],fill=CARD if ri%2==0 else (249,250,255))
        d.line([(MX,ry+48),(MX+sum(c[1] for c in mcols),ry+48)],fill=BORDER,width=1)
        vals=[mn,f'{mimp:,}',f'{mclk:,}',mctr,str(mcv),mcpa,mbudget]
        rxm=MX+14
        for v,(cn,cw) in zip(vals,mcols):
            t(d,v,rxm,ry+14,12,col=TEXT); rxm+=cw
    fp=str(OUT/'10_campaign_detail.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 10_campaign_detail.png')


# ══════════════════════════════════════════════════════════════
# 11 — 소재 라이브러리
# ══════════════════════════════════════════════════════════════
def s11():
    img, d = ni()
    nav(img, d, '소재')
    d = ImageDraw.Draw(img)
    sidebar(img, d, '소재 라이브러리')
    MX=240; MY=76
    t(d,'소재 라이브러리',MX,MY,22,col=TEXT,bold=True)
    t(d,'업로드 소재 및 AI 생성 변형본 관리',MX,MY+32,13,col=TEXT3)
    rr(d,W-220,MY-2,172,34,fill=LIME,r=17)
    tc(d,'+ 소재 업로드',W-220+86,MY+5,13,col=BLUE3,bold=True)
    FILTER_Y=MY+68
    tabs2=[('전체',True),('원본',False),('AI 변형본',False),('배너',False),('모바일',False)]
    tx=MX
    for tlbl,tsel in tabs2:
        tw2=tw(d,tlbl,12)+22
        rr(d,tx,FILTER_Y,tw2,30,fill=BLUE if tsel else CARD,ol=BLUE if tsel else BORDER,r=15)
        tc(d,tlbl,tx+tw2//2,FILTER_Y+7,12,col=WHITE if tsel else TEXT2,bold=tsel)
        tx+=tw2+10
    # Grid
    GY=FILTER_Y+48; GCW=4; GAP=16
    CARD_W=(W-MX-40-GAP*(GCW-1))//GCW; CARD_H=220
    assets=[('분유_메인이미지.jpg','원본','1920×1080',LIME),('배너_728x90.png','AI 변형','728×90',BLUE_M),
            ('배너_300x250.png','AI 변형','300×250',BLUE_M),('배너_320x480.png','AI 변형','320×480',BLUE_M),
            ('제품_화이트.png','원본','1920×1080',LIME),('배너_160x600.png','AI 변형','160×600',BLUE_M),
            ('배너_320x100.png','AI 변형','320×100',BLUE_M),('+ AI 변형 생성',None,None,None)]
    for ai,(aname,atype,asize,acc) in enumerate(assets):
        col_i=ai%GCW; row_i=ai//GCW
        ax=MX+col_i*(CARD_W+GAP); ay=GY+row_i*(CARD_H+14)
        if acc is None:
            rr(d,ax,ay,CARD_W,CARD_H,ol=BORDER,r=10)
            d.rounded_rectangle([ax,ay,ax+CARD_W,ay+CARD_H],radius=10,outline=BORDER,width=2)
            tc(d,'✨',ax+CARD_W//2,ay+60,28,col=BORDER2)
            tc(d,'AI 변형 생성',ax+CARD_W//2,ay+110,13,col=TEXT3)
            continue
        rr(d,ax,ay,CARD_W,CARD_H,fill=CARD,ol=BORDER,r=10)
        rr(d,ax,ay,CARD_W,130,fill=(215,220,242),r=8)
        d.rectangle([ax,ay+108,ax+CARD_W,ay+130],fill=(215,220,242))
        tc(d,aname[:12],ax+CARD_W//2,ay+52,11,col=BLUE_M)
        rr(d,ax+10,ay+10,tw(d,atype,10)+14,20,fill=LIME_L if acc==LIME else BLUE_L,r=10)
        t(d,atype,ax+17,ay+14,10,col=acc)
        t(d,aname[:18],ax+12,ay+140,12,col=TEXT,bold=True)
        t(d,asize,ax+12,ay+160,11,col=TEXT3)
        rr(d,ax+12,ay+180,CARD_W-24,28,ol=BORDER,r=14)
        tc(d,'캠페인에 사용',ax+12+(CARD_W-24)//2,ay+187,11,col=TEXT2)
    fp=str(OUT/'11_creative_library.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 11_creative_library.png')


# ══════════════════════════════════════════════════════════════
# 12 — 리포트
# ══════════════════════════════════════════════════════════════
def s12():
    img, d = ni()
    nav(img, d, '리포트')
    d = ImageDraw.Draw(img)
    sidebar(img, d, '리포트')
    MX=240; MY=76
    t(d,'성과 리포트',MX,MY,22,col=TEXT,bold=True)
    # Date range
    rr(d,MX,MY+36,220,34,fill=CARD,ol=BORDER,r=17)
    t(d,'2024-04-01 ~ 2024-04-30  📅',MX+16,MY+46,12,col=TEXT)
    tabs3=[('일별',True),('주별',False),('월별',False)]
    tx2=MX+240
    for tlbl,tsel in tabs3:
        rr(d,tx2,MY+40,64,26,fill=BLUE if tsel else CARD,ol=BLUE if tsel else BORDER,r=13)
        tc(d,tlbl,tx2+32,MY+46,12,col=WHITE if tsel else TEXT2,bold=tsel)
        tx2+=72
    btn(d,W-200,MY-2,158,34,'리포트 다운로드',sz=12,r=17)
    # KPIs
    KY=MY+84; KW=(W-MX-40-3*14)//4
    kpi(d,MX,KY,KW,90,'총 노출수','4,820,000','22.1%',True,LIME)
    kpi(d,MX+KW+14,KY,KW,90,'총 클릭수','94,500','15.3%',True,BLUE_M)
    kpi(d,MX+2*(KW+14),KY,KW,90,'평균 CTR','1.96%','0.3%p',True,SUCCESS)
    kpi(d,MX+3*(KW+14),KY,KW,90,'집행 예산','₩38.2M','8.2%',False,WARN)
    # Main chart
    CH_Y=KY+106; CH_H=220; CW=W-MX-40
    linechart(d,MX,CH_Y,CW,CH_H,
              [2800,3100,3400,3800,4200,4500,4820]*1,  # simplified 7pt
              col=LIME,title='일별 노출수 추이 (단위: 천)',
              data2=[1800,2000,2200,2500,2700,2900,3100],col2=BLUE_M)
    d = ImageDraw.Draw(img)
    # 2-col charts below
    CHART2_Y=CH_Y+CH_H+16; CHART2_H=200
    CW2_L=int((W-MX-40)*0.5); CW2_R=W-MX-40-CW2_L-16
    barchart_v(d,MX,CHART2_Y,CW2_L,CHART2_H,
               [('맘카페',38200),('인벤',21400),('클리앙',14800),('뽐뿌',8700),('베이비뉴스',6400),('루리웹',4900)],
               col=LIME,title='매체별 클릭수')
    barchart_v(d,MX+CW2_L+16,CHART2_Y,CW2_R,CHART2_H,
               [('CTR 3.8%',3800),('CTR 2.9%',2900),('CTR 2.1%',2100)],
               col=BLUE_M,title='CTR 상위 캠페인')
    fp=str(OUT/'12_report.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 12_report.png')


# ══════════════════════════════════════════════════════════════
# 13 — 매체사 가입/온보딩
# ══════════════════════════════════════════════════════════════
def s13():
    img, d = ni()
    img.paste(gv(W, H, BLUE3, BLUE2), (0,0))
    d = ImageDraw.Draw(img)
    t(d,'Ad',30,18,22,col=LIME,bold=True); t(d,'Mix',62,18,22,col=WHITE,bold=True)
    t(d,'매체사 파트너 포털',100,22,13,col=(140,165,220))
    rr(d,W//2-300,80,600,720,fill=WHITE,ol=BORDER,r=16)
    tc(d,'매체사 파트너 등록',W//2,108,22,col=TEXT,bold=True)
    tc(d,'AdMix 파트너가 되어 광고 수익을 창출하세요',W//2,142,13,col=TEXT3)
    # Steps
    for i,(snum,slbl) in enumerate([('01','매체 정보'),('02','인벤토리'),('03','정산 설정'),('04','검토 완료')]):
        sx=W//2-220+i*148; sy=176
        fc=LIME if i==0 else (220,224,248)
        d.ellipse([sx-16,sy-16,sx+16,sy+16],fill=fc)
        tc(d,snum,sx,sy-8,13,col=BLUE3 if i==0 else TEXT3,bold=True)
        tc(d,slbl,sx,sy+22,11,col=BLUE if i==0 else TEXT3,bold=(i==0))
        if i<3: d.line([(sx+16,sy),(sx+132,sy)],fill=(215,220,248),width=2)
    # Form
    FMX=W//2-260; FMY=236
    def field3(lbl,x,y,w,ph='',val=''):
        t(d,lbl,x,y,12,col=TEXT2,bold=True)
        rr(d,x,y+20,w,36,fill=BG,ol=BORDER,r=6)
        t(d,val if val else ph,x+12,y+28,13,col=TEXT if val else TEXT3)
    field3('매체(사이트) 이름',FMX,FMY,520,val='인벤 (inven.co.kr)')
    field3('URL',FMX,FMY+68,520,val='https://www.inven.co.kr')
    field3('카테고리',FMX,FMY+136,248,ph='카테고리 선택 ▾')
    field3('월 평균 UV',FMX+270,FMY+136,248,val='1,820,000')
    field3('담당자 이름',FMX,FMY+204,248,val='홍길동')
    field3('이메일',FMX+270,FMY+204,248,val='gildong@inven.co.kr')
    # Inventory types
    t(d,'지원 광고 유형 *',FMX,FMY+272,12,col=TEXT2,bold=True)
    for ci,(clbl,csel) in enumerate([('배너',True),('네이티브',True),('동영상',False),('팝업',False)]):
        cw=tw(d,clbl,12)+24
        rr(d,FMX+ci*132,FMY+292,cw,28,fill=BLUE if csel else CARD,ol=BLUE if csel else BORDER,r=14)
        tc(d,clbl,FMX+ci*132+cw//2,FMY+298,12,col=WHITE if csel else TEXT2,bold=csel)
    # Terms
    rr(d,FMX,FMY+340,20,20,fill=LIME,r=4)
    tc(d,'✓',FMX+10,FMY+342,12,col=WHITE,bold=True)
    t(d,'AdMix 매체사 파트너 계약 조건에 동의합니다',FMX+30,FMY+344,12,col=TEXT2)
    btn(d,FMX,FMY+378,520,46,'다음 단계: 광고 인벤토리 설정 →',sz=14,r=23)
    fp=str(OUT/'13_media_onboarding.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 13_media_onboarding.png')


# ══════════════════════════════════════════════════════════════
# 14 — 매체사 광고 인벤토리 관리
# ══════════════════════════════════════════════════════════════
def s14():
    img, d = ni()
    nav(img, d)
    d = ImageDraw.Draw(img)
    media_sidebar(d, '인벤토리 관리')
    MX=240; MY=76
    t(d,'광고 인벤토리 관리',MX,MY,20,col=TEXT,bold=True)
    t(d,'인벤 (inven.co.kr) · 파트너 매체',MX,MY+30,12,col=TEXT3)
    # Stats
    KY=MY+66; KW=(W-MX-40-3*14)//4
    kpi(d,MX,KY,KW,90,'이번 달 수익','₩3,840,000','12.4%',True,LIME)
    kpi(d,MX+KW+14,KY,KW,90,'게재 요청','48건','8건 증가',True,BLUE_M)
    kpi(d,MX+2*(KW+14),KY,KW,90,'평균 CPM','₩2,800','—',True,SUCCESS)
    kpi(d,MX+3*(KW+14),KY,KW,90,'광고 점유율','72%','5%p',True,WARN)
    # Inventory slots
    INV_Y=KY+106
    t(d,'광고 슬롯 목록',MX,INV_Y,15,col=TEXT,bold=True)
    btn(d,W-200,INV_Y-4,156,32,'+ 슬롯 추가',sz=12,r=16)
    rr(d,MX,INV_Y+34,W-MX-40,36,fill=BLUE_L,r=6)
    scols=[('슬롯 이름',180),('사이즈',100),('위치',140),('상태',90),('현재 광고주',160),('CPM',90),('노출/일',100),('수익/일',100)]
    shx=MX+14
    for cn,cw in scols:
        t(d,cn,shx,INV_Y+44,11,col=BLUE_M,bold=True); shx+=cw
    srows=[('헤더 배너 1','728×90','상단 고정','집행중','맘카페 캠페인','₩3,200','42,000','₩134,400'),
           ('사이드바 스카이','160×600','우측 고정','집행중','인벤 게임 광고','₩3,500','18,200','₩63,700'),
           ('본문 중간 배너','300×250','스크롤 중간','대기','—','₩2,800','—','—'),
           ('모바일 배너','320×100','하단 고정','집행중','맘카페 캠페인','₩2,100','35,800','₩75,180'),
           ('팝업 광고','640×480','전면 팝업','일시정지','—','₩8,500','—','—')]
    for ri,srow in enumerate(srows):
        ry=INV_Y+70+ri*52
        bg5=CARD if ri%2==0 else (249,250,255)
        d.rectangle([MX,ry,W-40,ry+52],fill=bg5)
        d.line([(MX,ry+52),(W-40,ry+52)],fill=BORDER,width=1)
        rxs=MX+14
        for v,(cn,cw) in zip(srow,scols):
            if cn=='상태': sbadge(d,rxs,ry+17,v)
            else: t(d,v,rxs,ry+18,12,col=TEXT)
            rxs+=cw
    # Revenue chart
    RCHART_Y=INV_Y+340
    linechart(d,MX,RCHART_Y,W-MX-40,200,
              [2800000,3100000,3400000,3600000,3840000,3650000,3900000],
              col=LIME,title='일별 광고 수익 추이 (원)')
    fp=str(OUT/'14_media_inventory.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 14_media_inventory.png')


# ══════════════════════════════════════════════════════════════
# 15 — 모바일 대시보드 (390×844)
# ══════════════════════════════════════════════════════════════
def s15():
    img = Image.new('RGB', (MW, MH), BG)
    d = ImageDraw.Draw(img)
    # Nav
    img.paste(gv(MW, 56, BLUE3, BLUE), (0,0))
    d = ImageDraw.Draw(img)
    t(d,'Ad',16,16,18,col=LIME,bold=True); t(d,'Mix',44,16,18,col=WHITE,bold=True)
    d.ellipse([MW-42,14,MW-12,44],fill=BLUE2)
    tc(d,'재',MW-27,22,13,col=WHITE,bold=True)
    # Body
    MX=16; MY=68
    t(d,'안녕하세요, 재우님 👋',MX,MY,16,col=TEXT,bold=True)
    t(d,'오늘의 성과 요약',MX,MY+24,12,col=TEXT3)
    # 2x2 KPI grid
    KW=(MW-MX*2-12)//2; KH=88; KY=MY+52
    kpi(d,MX,KY,KW,KH,'총 노출수','2,481K','▲12%',True,LIME)
    kpi(d,MX+KW+12,KY,KW,KH,'클릭수','48.2K','▲8%',True,BLUE_M)
    kpi(d,MX,KY+KH+10,KW,KH,'전환율','3.8%','▲0.5',True,SUCCESS)
    kpi(d,MX+KW+12,KY+KH+10,KW,KH,'집행 예산','₩32.9M','▼4%',False,WARN)
    # Chart
    CHART_Y=KY+KH*2+30
    linechart(d,MX,CHART_Y,MW-MX*2,160,[280,320,360,410,445,460,482],
              col=LIME,title='이번 주 클릭수')
    d = ImageDraw.Draw(img)
    # Campaign cards
    CAM_Y=CHART_Y+176
    t(d,'진행 중인 캠페인',MX,CAM_Y,14,col=TEXT,bold=True)
    for ci,(cname,cstat,cpct,cacc) in enumerate([
        ('맘카페 유아식품','집행중',72,LIME),
        ('인벤 게이밍','집행중',53,BLUE_M)]):
        CY2=CAM_Y+28+ci*90
        rr(d,MX,CY2,MW-MX*2,80,fill=CARD,ol=BORDER,r=10)
        rr(d,MX,CY2,MW-MX*2,4,fill=cacc,r=2)
        sbadge(d,MX+12,CY2+16,cstat)
        t(d,cname,MX+12,CY2+46,14,col=TEXT,bold=True)
        bw3=MW-MX*2-24
        rr(d,MX+12,CY2+68,bw3,6,fill=(228,232,252),r=3)
        rr(d,MX+12,CY2+68,int(bw3*cpct/100),6,fill=cacc,r=3)
        t(d,f'{cpct}%',MW-MX-28,CY2+62,10,col=TEXT3)
    # Bottom nav
    d.rectangle([0,MH-64,MW,MH],fill=WHITE)
    d.line([(0,MH-64),(MW,MH-64)],fill=BORDER,width=1)
    for i,(icon,lbl,isel) in enumerate([('🏠','홈',True),('📋','캠페인',False),('🖼','소재',False),('📊','리포트',False)]):
        bx=MW//4*i+MW//8
        t(d,icon,bx-12,MH-54,18)
        tc(d,lbl,bx,MH-28,10,col=LIME_D if isel else TEXT3,bold=isel)
    fp=str(OUT/'15_mobile_dashboard.png'); img.save(fp)
    assert os.path.exists(fp); print('OK 15_mobile_dashboard.png')


# ══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('AdMix Full Wireframe Suite 생성 시작 (15장)')
    s01(); s02(); s03(); s04(); s05()
    s06(); s07(); s08(); s09(); s10()
    s11(); s12(); s13(); s14(); s15()
    print()
    files_expected = [
        '01_landing_hero.png','02_service_intro.png','03_pricing.png',
        '04_dashboard_home.png','05_campaign_step1_media.png',
        '06_campaign_step2_creative.png','07_campaign_step3_size.png',
        '08_campaign_step4_budget.png','09_campaign_list.png',
        '10_campaign_detail.png','11_creative_library.png',
        '12_report.png','13_media_onboarding.png',
        '14_media_inventory.png','15_mobile_dashboard.png',
    ]
    ok = 0
    for fname in files_expected:
        fp = OUT / fname
        if os.path.exists(str(fp)):
            kb = fp.stat().st_size // 1024
            print(f'  {fname}: {kb} KB — {fp}')
            ok += 1
        else:
            print(f'  MISSING: {fname}')
    print(f'\n{ok}/15 파일 생성 완료')
    print(f'저장 경로: {OUT}')
