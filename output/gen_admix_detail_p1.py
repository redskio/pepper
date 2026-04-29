# -*- coding: utf-8 -*-
"""AdMix Detail Wireframes — Part 1: screens 00~35"""
import sys, io, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from pathlib import Path

OUT = Path('C:/Agent/pepper/admix_wireframes')
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1440, 900

# ── Colors ──────────────────────────────────────────────────────
INDIGO  = (99, 102, 241)
INDIGO2 = (79,  70, 229)
INDIGO3 = (49,  46, 129)
AMBER   = (245, 158, 11)
AMBER_L = (254, 243, 199)
BG      = (248, 249, 250)
WHITE   = (255, 255, 255)
GRAY1   = (249, 250, 251)
GRAY2   = (243, 244, 246)
GRAY3   = (229, 231, 235)
GRAY4   = (156, 163, 175)
GRAY5   = (107, 114, 128)
GRAY6   = (75,  85,  99)
DARK    = (17,  24,  39)
GREEN   = (16, 185, 129)
GREEN_L = (209, 250, 229)
RED     = (239, 68,  68)
RED_L   = (254, 226, 226)
BLUE    = (59, 130, 246)
BLUE_L  = (219, 234, 254)
PURPLE  = (139, 92, 246)
PURPLE_L= (237, 233, 254)
NAV_BG  = (17,  24,  39)
SIDEBAR = (30,  41,  59)

# ── Font cache ───────────────────────────────────────────────────
_fc = {}
def fnt(sz, bold=False):
    key = (sz, bold)
    if key not in _fc:
        fp = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
        try:   _fc[key] = ImageFont.truetype(fp, sz)
        except:_fc[key] = ImageFont.load_default()
    return _fc[key]

# ── Primitives ───────────────────────────────────────────────────
def rr(d, x, y, w, h, fill=None, ol=None, lw=1, r=8):
    if w > 0 and h > 0:
        d.rounded_rectangle([x, y, x+w, y+h], radius=min(r, w//2, h//2),
                             fill=fill, outline=ol, width=lw)

def t(d, x, y, txt, f, fill=DARK, anchor='la'):
    d.text((x, y), str(txt), font=f, fill=fill, anchor=anchor)

def tc(d, x, y, txt, f, fill=DARK):
    d.text((x, y), str(txt), font=f, fill=fill, anchor='mm')

def tw(d, x, y, w, txt, f, fill=DARK):
    d.text((x + w//2, y), str(txt), font=f, fill=fill, anchor='mt')

def btn(d, x, y, w, h, txt, bg=INDIGO, fg=WHITE, r=8, sz=15):
    rr(d, x, y, w, h, fill=bg, r=r)
    tc(d, x+w//2, y+h//2, txt, fnt(sz, True), fill=fg)

def btn_outline(d, x, y, w, h, txt, col=INDIGO, sz=15):
    rr(d, x, y, w, h, ol=col, lw=2, r=8)
    tc(d, x+w//2, y+h//2, txt, fnt(sz, True), fill=col)

def pill(d, x, y, txt, bg=INDIGO, fg=WHITE, sz=12, px=10, py=4):
    tw2 = d.textlength(txt, font=fnt(sz, True))
    rr(d, x, y, int(tw2)+px*2, sz+py*2+2, fill=bg, r=999)
    t(d, x+px, y+py+1, txt, fnt(sz, True), fill=fg)
    return int(tw2)+px*2

def input_box(d, x, y, w, h, placeholder='', value='', r=8):
    rr(d, x, y, w, h, fill=WHITE, ol=GRAY3, lw=1, r=r)
    tx = x + 12
    ty = y + h//2
    if value:
        t(d, tx, ty, value, fnt(14), fill=DARK, anchor='lm')
    else:
        t(d, tx, ty, placeholder, fnt(14), fill=GRAY4, anchor='lm')

def label_input(d, x, y, w, lbl, placeholder='', value='', gap=28):
    t(d, x, y, lbl, fnt(13, True), fill=GRAY6)
    input_box(d, x, y+gap, w, 40, placeholder, value)
    return y + gap + 40

def card(img, d, x, y, w, h, shadow=True, r=12):
    if shadow:
        sh = img.copy().convert('RGBA')
        shd = Image.new('RGBA', img.size, (0,0,0,0))
        sd = ImageDraw.Draw(shd)
        sd.rounded_rectangle([x+2, y+4, x+w+2, y+h+4], radius=r,
                              fill=(0,0,0,30))
        blurred = shd.filter(ImageFilter.GaussianBlur(6))
        img.paste(Image.alpha_composite(Image.new('RGBA',img.size,(0,0,0,0)), blurred).convert('RGB'),
                  mask=blurred.split()[3])
    rr(d, x, y, w, h, fill=WHITE, ol=GRAY3, lw=1, r=r)

def kpi(d, x, y, w, h, label, val, chg='', up=True, acc=INDIGO):
    rr(d, x, y, w, h, fill=WHITE, ol=GRAY3, lw=1, r=12)
    t(d, x+16, y+14, label, fnt(12), fill=GRAY5)
    t(d, x+16, y+40, val, fnt(24, True), fill=DARK)
    if chg:
        col = GREEN if up else RED
        arrow = '+' if up else ''
        t(d, x+16, y+76, f'{arrow}{chg}', fnt(12, True), fill=col)

def gv(w, h, c1, c2):
    a = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        t2 = y / max(h-1, 1)
        for c in range(3): a[y,:,c] = int(c1[c]*(1-t2)+c2[c]*t2)
    return Image.fromarray(a)

def linechart(d, x, y, w, h, data, col=INDIGO, bg=INDIGO, label=''):
    # background
    rr(d, x, y, w, h, fill=GRAY1, r=0)
    if not data: return
    mn, mx = min(data), max(data)
    if mx == mn: mx = mn + 1
    pts = []
    for i, v in enumerate(data):
        px2 = x + int(i/(len(data)-1)*w) if len(data)>1 else x+w//2
        py2 = y + h - int((v-mn)/(mx-mn)*(h-20)) - 10
        pts.append((px2, py2))
    # area fill
    poly = [(x, y+h)] + pts + [(x+w, y+h)]
    fill_col = col + (40,) if len(col)==3 else col
    tmp = Image.new('RGBA', (w, h), (0,0,0,0))
    td = ImageDraw.Draw(tmp)
    local_poly = [(px2-x, py2-y) for px2,py2 in poly]
    td.polygon(local_poly, fill=(*col, 50))
    # line
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=col, width=2)
    for px2,py2 in pts:
        d.ellipse([px2-3, py2-3, px2+3, py2+3], fill=col)

def barchart_v(d, x, y, w, h, data, labels=None, col=INDIGO):
    if not data: return
    mx = max(data) if data else 1
    bw = max(8, (w - (len(data)+1)*8) // len(data))
    for i, v in enumerate(data):
        bx = x + 8 + i*(bw+8)
        bh = int((v/mx)*(h-30)) if mx else 0
        by = y + h - 30 - bh
        rr(d, bx, by, bw, bh, fill=col, r=4)
        if labels:
            tc(d, bx+bw//2, y+h-14, labels[i], fnt(10), fill=GRAY5)

def barchart_h(d, x, y, w, h, data, labels=None, cols=None):
    if not data: return
    mx = max(data) if data else 1
    bh = max(8, (h - (len(data)+1)*6) // len(data))
    default_cols = [INDIGO, AMBER, GREEN, PURPLE, BLUE]
    for i, v in enumerate(data):
        by = y + 6 + i*(bh+6)
        bw2 = int((v/mx)*(w-80)) if mx else 0
        col = cols[i] if cols else default_cols[i % len(default_cols)]
        rr(d, x+80, by, bw2, bh, fill=col, r=4)
        if labels:
            t(d, x, by+bh//2, labels[i], fnt(11), fill=GRAY6, anchor='lm')
        t(d, x+80+bw2+6, by+bh//2, str(v), fnt(11, True), fill=DARK, anchor='lm')

# ── Layout ───────────────────────────────────────────────────────
def nav_top(img, d, active=''):
    """Top navigation bar (landing/public pages)"""
    rr(d, 0, 0, W, 60, fill=WHITE, r=0)
    d.line([(0,60),(W,60)], fill=GRAY3, width=1)
    # Logo
    t(d, 40, 18, 'AdMix', fnt(22, True), fill=INDIGO)
    # Nav items
    items = ['서비스 소개', '요금제', '사례', '블로그']
    for i, it in enumerate(items):
        tx = 200 + i*100
        col = INDIGO if it == active else GRAY6
        t(d, tx, 20, it, fnt(14, it==active), fill=col)
    # CTA
    btn(d, W-180, 14, 80, 32, '로그인', bg=WHITE, fg=INDIGO)
    btn(d, W-90, 14, 80, 32, '시작하기', bg=INDIGO)

def app_nav(img, d, user='김재우'):
    """App top nav"""
    rr(d, 0, 0, W, 56, fill=DARK, r=0)
    t(d, 24, 16, 'AdMix', fnt(20, True), fill=WHITE)
    # right side
    t(d, W-200, 18, user, fnt(14), fill=GRAY3)
    rr(d, W-50, 16, 30, 24, fill=GRAY6, r=12)
    tc(d, W-35, 28, user[0], fnt(13, True), fill=WHITE)

def sidebar(img, d, active='dashboard'):
    """Left sidebar"""
    rr(d, 0, 56, 220, H-56, fill=SIDEBAR, r=0)
    items = [
        ('dashboard', '대시보드', '10'),
        ('campaign', '캠페인', '20'),
        ('material', '소재 관리', '30'),
        ('report', '리포트', '60'),
        ('credit', '크레딧', '11'),
        ('settings', '설정', ''),
    ]
    for i, (key, label, _) in enumerate(items):
        y0 = 80 + i*52
        is_active = key == active
        if is_active:
            rr(d, 8, y0-6, 204, 40, fill=INDIGO, r=8)
        col = WHITE if is_active else GRAY4
        t(d, 36, y0+4, label, fnt(14, is_active), fill=col)

def base_app(active_sidebar='dashboard'):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    app_nav(img, d)
    sidebar(img, d, active_sidebar)
    return img, d

def content_area():
    """Returns (img, d) ready for content in 220..1440, 56..900"""
    return 220, 56, W-220, H-56  # x,y,w,h of content area

# ── Section header ───────────────────────────────────────────────
def section_title(d, x, y, title, subtitle=''):
    t(d, x, y, title, fnt(22, True), fill=DARK)
    if subtitle:
        t(d, x, y+32, subtitle, fnt(14), fill=GRAY5)

# ================================================================
# SCREEN FUNCTIONS
# ================================================================

def s00_landing():
    img = Image.new('RGB', (W, H), WHITE)
    d = ImageDraw.Draw(img)
    nav_top(img, d)

    # Hero section — indigo gradient
    hero = gv(W, 500, INDIGO2, INDIGO3)
    img.paste(hero, (0, 60))
    d2 = ImageDraw.Draw(img)

    # Hero text
    tc(d2, W//2, 200, 'AI가 만드는 완벽한 광고', fnt(52, True), fill=WHITE)
    tc(d2, W//2, 270, '제품 이미지만 올리면 AI가 소재 편집부터 후킹 문구까지 자동으로', fnt(20), fill=(200,200,255))
    tc(d2, W//2, 320, '인스타그램 · 카카오 · 네이버 · 유튜브 매체별 자동 최적화', fnt(16), fill=(180,180,240))

    # CTA buttons
    btn(d2, W//2-180, 370, 160, 52, '무료로 시작하기', bg=AMBER, fg=DARK, sz=17)
    btn_outline(d2, W//2+20, 370, 160, 52, '데모 보기', col=WHITE, sz=17)

    # Stats
    stats = [('1,240+', '광고주'), ('3.2M', '월 노출'), ('4.8배', '평균 ROAS')]
    for i, (val, lbl) in enumerate(stats):
        sx = W//2 - 240 + i*240
        tc(d2, sx, 465, val, fnt(32, True), fill=WHITE)
        tc(d2, sx, 505, lbl, fnt(14), fill=(180,180,240))

    # Value prop cards
    y0 = 580
    cards = [
        ('소재 자동 편집', 'AI가 제품 이미지를 매체별\n최적 사이즈로 자동 크롭·편집'),
        ('후킹 문구 생성', '클릭률 높은 광고 카피를\nAI가 3가지 버전으로 제안'),
        ('멀티 매체 집행', '인스타·카카오·네이버·유튜브\n한 번에 동시 집행'),
        ('성과 자동 최적화', '실시간 데이터로 예산 배분을\nAI가 자동으로 조정'),
    ]
    for i, (title, desc) in enumerate(cards):
        cx = 60 + i*340
        rr(d2, cx, y0, 300, 130, fill=WHITE, ol=GRAY3, r=16)
        # icon circle
        d2.ellipse([cx+20, y0+20, cx+60, y0+60], fill=INDIGO)
        tc(d2, cx+40, y0+40, '★', fnt(20, True), fill=WHITE)
        t(d2, cx+20, y0+72, title, fnt(15, True), fill=DARK)
        t(d2, cx+20, y0+96, desc.split('\n')[0], fnt(12), fill=GRAY5)
        t(d2, cx+20, y0+112, desc.split('\n')[1] if '\n' in desc else '', fnt(12), fill=GRAY5)

    fp = OUT / '00_landing.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s01_service_intro():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    nav_top(img, d, '서비스 소개')

    # Page title
    tc(d, W//2, 120, '3단계로 끝나는 광고 집행', fnt(38, True), fill=DARK)
    tc(d, W//2, 168, '복잡한 광고 설정은 AI에게 맡기고, 결과만 확인하세요', fnt(16), fill=GRAY5)

    # 3-step flow
    steps = [
        ('01', '소재 업로드', '제품 이미지나 영상을\n플랫폼에 업로드', INDIGO),
        ('02', 'AI 자동 최적화', 'AI가 매체별 사이즈 크롭,\n후킹 문구 자동 생성', AMBER),
        ('03', '캠페인 집행', '원하는 매체 선택 후\n예산 설정으로 바로 집행', GREEN),
    ]

    for i, (num, title, desc, col) in enumerate(steps):
        cx = 160 + i*400
        # Arrow between steps
        if i < 2:
            d.line([(cx+280, 330), (cx+400-20, 330)], fill=GRAY3, width=2)
            tc(d, cx+340, 322, '→', fnt(20), fill=GRAY4)

        # Step card
        rr(d, cx, 220, 260, 280, fill=WHITE, ol=GRAY3, r=16)
        # Icon circle
        d.ellipse([cx+90, 240, cx+170, 320], fill=col)
        tc(d, cx+130, 280, num, fnt(28, True), fill=WHITE)
        tc(d, cx+130, 370, title, fnt(18, True), fill=DARK)
        for j, line in enumerate(desc.split('\n')):
            tc(d, cx+130, 400+j*22, line, fnt(13), fill=GRAY5)

    # Feature list
    y0 = 560
    rr(d, 80, y0, W-160, 260, fill=WHITE, ol=GRAY3, r=16)
    t(d, 120, y0+24, 'AdMix가 자동으로 해주는 것들', fnt(18, True), fill=DARK)

    features = [
        '매체별 최적 사이즈 자동 크롭 (16:9, 1:1, 9:16, 4:5 등 12가지)',
        'AI 후킹 문구 3가지 버전 자동 생성 및 A/B 테스트',
        '인스타그램 · 카카오 · 네이버 · 유튜브 동시 집행',
        '실시간 성과 모니터링 및 예산 자동 최적화',
        '소재 승인 상태 실시간 알림',
    ]
    for i, feat in enumerate(features):
        fy = y0 + 60 + i*36
        d.ellipse([120, fy+4, 130, fy+14], fill=GREEN)
        t(d, 142, fy, feat, fnt(14), fill=GRAY6)

    fp = OUT / '01_service_intro.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s02_login():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    # Left panel
    left = gv(W//2, H, INDIGO2, INDIGO3)
    img.paste(left, (0, 0))
    d2 = ImageDraw.Draw(img)
    tc(d2, W//4, H//2-60, 'AdMix', fnt(48, True), fill=WHITE)
    tc(d2, W//4, H//2, 'AI 광고 자동화 플랫폼', fnt(18), fill=(200,200,255))
    tc(d2, W//4, H//2+40, '소재 업로드 → AI 최적화 → 집행', fnt(14), fill=(180,180,240))

    # Right panel — login form
    x0, y0 = W//2 + 100, H//2 - 160
    t(d2, x0, y0, '로그인', fnt(28, True), fill=DARK)
    t(d2, x0, y0+40, 'AdMix 계정으로 로그인하세요', fnt(14), fill=GRAY5)

    y = y0 + 90
    y = label_input(d2, x0, y, 360, '이메일', 'example@company.com')
    y += 16
    y = label_input(d2, x0, y, 360, '비밀번호', '••••••••••')
    y += 16

    # Remember + forgot
    rr(d2, x0, y, 16, 16, ol=GRAY3, r=3)
    t(d2, x0+24, y, '로그인 상태 유지', fnt(13), fill=GRAY5)
    t(d2, x0+260, y, '비밀번호 찾기', fnt(13), fill=INDIGO)
    y += 32

    btn(d2, x0, y, 360, 48, '로그인', bg=INDIGO, sz=16)
    y += 64

    # Divider
    d2.line([(x0, y+8), (x0+160, y+8)], fill=GRAY3, width=1)
    tc(d2, x0+180, y+8, 'OR', fnt(12), fill=GRAY4)
    d2.line([(x0+200, y+8), (x0+360, y+8)], fill=GRAY3, width=1)
    y += 24

    btn_outline(d2, x0, y, 360, 44, 'Google로 로그인', col=GRAY6)
    y += 60

    tc(d2, x0+180, y, '계정이 없으신가요?', fnt(13), fill=GRAY5)
    tc(d2, x0+290, y, '무료 가입', fnt(13, True), fill=INDIGO)

    fp = OUT / '02_login.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s03_signup():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    left = gv(W//2, H, INDIGO2, INDIGO3)
    img.paste(left, (0, 0))
    d2 = ImageDraw.Draw(img)
    tc(d2, W//4, H//2-60, 'AdMix', fnt(48, True), fill=WHITE)
    tc(d2, W//4, H//2, '14일 무료 체험', fnt(20, True), fill=AMBER)
    tc(d2, W//4, H//2+40, '신용카드 없이 시작하세요', fnt(14), fill=(200,200,255))

    x0, y0 = W//2 + 80, 80
    t(d2, x0, y0, '무료로 시작하기', fnt(28, True), fill=DARK)
    t(d2, x0, y0+38, '14일 무료 체험, 이후 요금제 선택', fnt(13), fill=GRAY5)

    y = y0 + 88
    # Two columns
    y = label_input(d2, x0, y, 176, '이름', '홍길동')
    # second column
    label_input(d2, x0+192, y-68, 176, '회사명', 'Stark Industries')
    y += 16
    y = label_input(d2, x0, y, 368, '이메일', 'work@company.com')
    y += 16
    y = label_input(d2, x0, y, 368, '비밀번호', '8자 이상, 영문+숫자 조합')
    y += 16

    # Role select
    t(d2, x0, y, '광고주 유형', fnt(13, True), fill=GRAY6)
    rr(d2, x0, y+28, 368, 40, fill=WHITE, ol=GRAY3, r=8)
    t(d2, x0+12, y+44, '광고주 (직접 광고 집행)', fnt(14), fill=DARK)
    t(d2, x0+340, y+44, '▾', fnt(12), fill=GRAY4)
    y += 84

    # Agreement
    rr(d2, x0, y, 16, 16, ol=GRAY3, r=3)
    t(d2, x0+24, y, '이용약관 및 개인정보 처리방침에 동의합니다', fnt(12), fill=GRAY6)
    y += 28
    rr(d2, x0, y, 16, 16, fill=INDIGO, ol=INDIGO, r=3)
    t(d2, x0+24, y, '마케팅 정보 수신에 동의합니다 (선택)', fnt(12), fill=GRAY6)
    y += 36

    btn(d2, x0, y, 368, 48, '가입하고 무료 체험 시작', bg=INDIGO, sz=15)
    y += 64
    tc(d2, x0+184, y, '이미 계정이 있으신가요?   로그인', fnt(13), fill=GRAY5)

    fp = OUT / '03_signup.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s10_dashboard():
    img, d = base_app('dashboard')
    cx, cy, cw, ch = 240, 76, W-260, H-96

    section_title(d, cx, cy, '대시보드', '안녕하세요, 김재우님 👋')

    # KPI row
    kpis = [
        ('활성 캠페인', '12개', '+3 이번주', True),
        ('총 노출수', '3,240,500', '+18.2%', True),
        ('총 클릭수', '48,320', '+12.4%', True),
        ('예산 소진율', '68%', '-5%', False),
    ]
    kpi_w = (cw-40) // 4 - 8
    for i, (lbl, val, chg, up) in enumerate(kpis):
        kpi(d, cx + i*(kpi_w+8), cy+70, kpi_w, 100, lbl, val, chg, up)

    # Line chart
    rr(d, cx, cy+190, cw*6//10-8, 260, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+206, '일별 노출 추이', fnt(15, True), fill=DARK)
    t(d, cx+16, cy+226, '최근 14일', fnt(11), fill=GRAY4)
    data = [120,145,132,178,195,210,188,225,240,218,265,280,295,310]
    linechart(d, cx+16, cy+248, cw*6//10-40, 180, data, col=INDIGO)
    # X labels
    xlabels = ['4/16','4/17','4/18','4/19','4/20','4/21','4/22','4/23','4/24','4/25','4/26','4/27','4/28','4/29']
    step = (cw*6//10-40)//(len(xlabels)-1)
    for j, xl in enumerate(xlabels[::2]):
        t(d, cx+16+j*step*2, cy+436, xl, fnt(9), fill=GRAY4)

    # Pie/bar chart — media breakdown
    rr(d, cx+cw*6//10+8, cy+190, cw*4//10-16, 260, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+cw*6//10+24, cy+206, '매체별 예산 비중', fnt(15, True), fill=DARK)
    media = [('인스타그램', 42, INDIGO), ('카카오', 28, AMBER), ('네이버', 18, GREEN), ('유튜브', 12, PURPLE)]
    for i, (nm, pct, col) in enumerate(media):
        by = cy+248+i*44
        rr(d, cx+cw*6//10+24, by, int((cw*4//10-80)*pct/100), 28, fill=col, r=4)
        t(d, cx+cw*6//10+24, by+32, f'{nm}  {pct}%', fnt(11), fill=GRAY6)

    # Campaign list
    rr(d, cx, cy+470, cw, 260, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+486, '진행 중인 캠페인', fnt(15, True), fill=DARK)
    btn(d, cx+cw-120, cy+482, 100, 28, '전체 보기', bg=GRAY2, fg=GRAY6, sz=12)

    headers = ['캠페인명', '매체', '노출수', '클릭수', 'CTR', '예산 소진', '상태']
    col_x = [cx+16, cx+250, cx+420, cx+540, cx+640, cx+730, cx+860]
    for j, (hdr, hx) in enumerate(zip(headers, col_x)):
        t(d, hx, cy+516, hdr, fnt(12, True), fill=GRAY5)
    d.line([(cx+16, cy+534), (cx+cw-16, cy+534)], fill=GRAY3, width=1)

    rows = [
        ['봄 시즌 신상품 캠페인', '인스타그램', '245,800', '3,240', '1.32%', '74%', '집행중'],
        ['브랜드 인지도 캠페인', '카카오+네이버', '189,200', '2,180', '1.15%', '52%', '집행중'],
        ['신규 회원 유치 이벤트', '인스타그램', '98,400', '1,640', '1.67%', '88%', '검수중'],
    ]
    for ri, row in enumerate(rows):
        ry = cy+544+ri*44
        if ri%2==0: rr(d, cx+8, ry-6, cw-16, 36, fill=GRAY1, r=4)
        for j, (cell, hx) in enumerate(zip(row, col_x)):
            if j == 6:
                col = GREEN if cell=='집행중' else AMBER
                pill(d, hx, ry, cell, bg=GREEN_L if cell=='집행중' else AMBER_L,
                     fg=GREEN if cell=='집행중' else AMBER, sz=11)
            else:
                t(d, hx, ry, cell, fnt(12), fill=GRAY6)

    fp = OUT / '10_dashboard.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s11_credit_charge():
    img, d = base_app('credit')
    cx, cy = 240, 76

    section_title(d, cx, cy, '크레딧 충전', '충전된 크레딧으로 캠페인을 집행합니다')

    # Current balance
    rr(d, cx, cy+60, 340, 100, fill=INDIGO, r=16)
    t(d, cx+24, cy+76, '보유 크레딧', fnt(13), fill=(200,200,255))
    t(d, cx+24, cy+104, '₩ 128,500', fnt(32, True), fill=WHITE)
    t(d, cx+24, cy+146, '약 6일치 예산', fnt(12), fill=(180,180,240))

    # Amount select
    t(d, cx, cy+188, '충전 금액 선택', fnt(16, True), fill=DARK)
    amounts = ['₩ 50,000', '₩ 100,000', '₩ 200,000', '₩ 500,000']
    for i, amt in enumerate(amounts):
        ax = cx + i*200
        is_sel = i == 1
        rr(d, ax, cy+222, 180, 64, fill=INDIGO if is_sel else WHITE,
           ol=INDIGO if is_sel else GRAY3, lw=2, r=12)
        tc(d, ax+90, cy+254, amt, fnt(18, True), fill=WHITE if is_sel else DARK)

    # Custom amount
    t(d, cx, cy+316, '직접 입력', fnt(14, True), fill=DARK)
    rr(d, cx, cy+346, 380, 48, fill=WHITE, ol=GRAY3, r=8)
    t(d, cx+16, cy+362, '₩', fnt(16), fill=GRAY5)
    t(d, cx+40, cy+362, '100,000', fnt(16), fill=DARK)
    t(d, cx+196, cy+362, '원', fnt(16), fill=GRAY5)

    # Payment method
    t(d, cx, cy+428, '결제 방법', fnt(16, True), fill=DARK)
    methods = [('신용카드', True), ('계좌이체', False), ('카카오페이', False)]
    for i, (m, sel) in enumerate(methods):
        mx = cx + i*200
        rr(d, mx, cy+462, 180, 52, fill=WHITE,
           ol=INDIGO if sel else GRAY3, lw=2 if sel else 1, r=8)
        if sel:
            d.ellipse([mx+16, cy+478, mx+26, cy+488], fill=INDIGO)
        else:
            d.ellipse([mx+16, cy+478, mx+26, cy+488], outline=GRAY3, width=2)
        t(d, mx+38, cy+474, m, fnt(14, sel), fill=INDIGO if sel else GRAY6)

    # Card info
    rr(d, cx, cy+542, 780, 160, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+20, cy+562, '카드 정보', fnt(14, True), fill=DARK)
    input_box(d, cx+20, cy+590, 740, 40, '카드번호 (16자리)', '1234  5678  9012  3456')
    input_box(d, cx+20, cy+642, 360, 40, '유효기간 (MM/YY)', '12/27')
    input_box(d, cx+392, cy+642, 368, 40, 'CVC', '***')

    btn(d, cx, cy+730, 380, 52, '₩ 100,000 충전하기', bg=INDIGO, sz=16)
    t(d, cx, cy+796, '* 충전된 크레딧은 환불되지 않습니다. 캠페인 집행에만 사용 가능합니다.', fnt(11), fill=GRAY4)

    fp = OUT / '11_credit_charge.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s12_credit_history():
    img, d = base_app('credit')
    cx, cy = 240, 76

    section_title(d, cx, cy, '크레딧 내역', '충전 및 사용 내역을 확인합니다')

    # Summary cards
    for i, (lbl, val, col) in enumerate([
        ('총 충전', '₩ 1,200,000', INDIGO),
        ('총 사용', '₩ 1,071,500', AMBER),
        ('잔여 크레딧', '₩ 128,500', GREEN),
    ]):
        rr(d, cx+i*340, cy+60, 320, 80, fill=WHITE, ol=GRAY3, r=12)
        t(d, cx+i*340+16, cy+76, lbl, fnt(12), fill=GRAY5)
        t(d, cx+i*340+16, cy+102, val, fnt(24, True), fill=col)

    # Filter row
    t(d, cx, cy+172, '기간:', fnt(13), fill=GRAY6)
    for i, period in enumerate(['전체', '이번달', '지난달', '3개월']):
        is_sel = i == 0
        btn(d, cx+56+i*88, cy+164, 80, 28,
            period, bg=INDIGO if is_sel else GRAY2, fg=WHITE if is_sel else GRAY6, sz=12)

    # Table
    rr(d, cx, cy+212, W-280, 560, fill=WHITE, ol=GRAY3, r=12)
    headers = ['날짜', '구분', '금액', '잔여 크레딧', '비고']
    col_x = [cx+16, cx+160, cx+320, cx+480, cx+640]
    for hdr, hx in zip(headers, col_x):
        t(d, hx, cy+228, hdr, fnt(12, True), fill=GRAY5)
    d.line([(cx+8, cy+248), (W-168, cy+248)], fill=GRAY3, width=1)

    rows = [
        ('2026.04.29', '충전', '+₩ 100,000', '₩ 228,500', '신용카드'),
        ('2026.04.28', '사용', '-₩ 32,400', '₩ 128,500', '봄 시즌 캠페인'),
        ('2026.04.27', '사용', '-₩ 28,100', '₩ 160,900', '브랜드 인지도 캠페인'),
        ('2026.04.26', '사용', '-₩ 19,800', '₩ 189,000', '신규 회원 유치'),
        ('2026.04.25', '충전', '+₩ 200,000', '₩ 208,800', '계좌이체'),
        ('2026.04.24', '사용', '-₩ 41,200', '₩ 8,800', '유튜브 광고 캠페인'),
        ('2026.04.23', '사용', '-₩ 15,600', '₩ 50,000', '카카오 광고'),
        ('2026.04.22', '충전', '+₩ 50,000', '₩ 65,600', '신용카드'),
    ]
    for ri, row in enumerate(rows):
        ry = cy+258+ri*48
        if ri%2==0: rr(d, cx+8, ry-4, W-296, 40, fill=GRAY1, r=4)
        for j, (cell, hx) in enumerate(zip(row, col_x)):
            if j == 1:
                col = GREEN if '충전' in cell else AMBER
                bg = GREEN_L if '충전' in cell else AMBER_L
                pill(d, hx, ry+4, cell, bg=bg, fg=col, sz=11)
            elif j == 2:
                col = GREEN if '+' in cell else RED
                t(d, hx, ry+8, cell, fnt(13, True), fill=col)
            else:
                t(d, hx, ry+8, cell, fnt(12), fill=GRAY6)

    fp = OUT / '12_credit_history.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s20_campaign_type_select():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '새 캠페인 만들기', '광고 집행 방식을 선택하세요')

    # Step bar
    steps = ['광고 유형 선택', '기본 정보', '타겟 설정', '예산 설정', '매체 선택', '완료']
    bar_w = (W-280)
    step_w = bar_w // len(steps)
    for i, s in enumerate(steps):
        sx = cx + i*step_w
        col = INDIGO if i == 0 else GRAY3
        d.ellipse([sx+step_w//2-12, cy+60, sx+step_w//2+12, cy+84], fill=col)
        tc(d, sx+step_w//2, cy+72, str(i+1), fnt(12, True), fill=WHITE if i==0 else GRAY4)
        tc(d, sx+step_w//2, cy+98, s, fnt(11, i==0), fill=INDIGO if i==0 else GRAY4)
        if i < len(steps)-1:
            d.line([(sx+step_w//2+12, cy+72), (sx+step_w-12+step_w//2, cy+72)], fill=GRAY3, width=2)

    # Type cards
    t(d, cx, cy+138, '광고 유형을 선택해주세요', fnt(16, True), fill=DARK)

    types = [
        ('버티컬 광고', '특정 매체·타겟에 집중 집행',
         ['매체별 상세 타겟 설정', '소재별 성과 분석', 'CPC/CPM 입찰 방식', 'AI 소재 최적화 포함'],
         INDIGO, True),
        ('예산 소진 방식', '예산을 자동으로 최적 분배',
         ['AI가 자동으로 매체 배분', '성과 기반 실시간 조정', '최소 설정으로 빠른 시작', '보장형 노출'],
         AMBER, False),
    ]

    for i, (title, sub, feats, col, selected) in enumerate(types):
        tx = cx + i*540
        rr(d, tx, cy+168, 500, 420, fill=WHITE,
           ol=col, lw=3 if selected else 1, r=16)
        if selected:
            t(d, tx+380, cy+178, '추천', fnt(11, True), fill=WHITE)
            rr(d, tx+372, cy+174, 52, 24, fill=col, r=12)
            t(d, tx+374, cy+178, '추천', fnt(11, True), fill=WHITE)

        # Icon
        d.ellipse([tx+200, cy+210, tx+300, cy+310], fill=col)
        tc(d, tx+250, cy+260, '▶' if i==0 else '⚡', fnt(32, True), fill=WHITE)

        tc(d, tx+250, cy+332, title, fnt(22, True), fill=DARK)
        tc(d, tx+250, cy+362, sub, fnt(13), fill=GRAY5)

        for j, feat in enumerate(feats):
            fy = cy+396+j*38
            d.ellipse([tx+48, fy+7, tx+58, fy+17], fill=col)
            t(d, tx+70, fy+4, feat, fnt(13), fill=GRAY6)

        if selected:
            btn(d, tx+100, cy+558, 300, 44, '버티컬 광고 선택', bg=col, sz=15)
        else:
            btn_outline(d, tx+100, cy+558, 300, 44, '예산 소진 방식 선택', col=col)

    fp = OUT / '20_campaign_type_select.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s21_vertical_campaign_info():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '캠페인 기본 정보', '버티컬 광고 캠페인 설정')

    # Step bar (step 2 active)
    steps = ['유형 선택', '기본 정보', '타겟 설정', '예산 설정', '매체 선택', '완료']
    step_w = (W-280)//len(steps)
    for i, s in enumerate(steps):
        sx = cx+i*step_w
        col = INDIGO if i<=1 else GRAY3
        d.ellipse([sx+step_w//2-12, cy+56, sx+step_w//2+12, cy+80], fill=col)
        tc(d, sx+step_w//2, cy+68, str(i+1), fnt(12, True), fill=WHITE if i<=1 else GRAY4)
        tc(d, sx+step_w//2, cy+94, s, fnt(10, i==1), fill=INDIGO if i<=1 else GRAY4)
        if i < len(steps)-1:
            lcolor = INDIGO if i < 1 else GRAY3
            d.line([(sx+step_w//2+12, cy+68), (sx+step_w-12+step_w//2, cy+68)], fill=lcolor, width=2)

    # Form
    rr(d, cx, cy+118, W-280, 680, fill=WHITE, ol=GRAY3, r=16)

    y = cy+142
    # Campaign name
    t(d, cx+24, y, '캠페인명 *', fnt(13, True), fill=GRAY6)
    input_box(d, cx+24, y+28, W-344, 44, '', '2026 봄 시즌 신상품 프로모션')
    y += 96

    # Campaign objective
    t(d, cx+24, y, '캠페인 목표 *', fnt(13, True), fill=GRAY6)
    objectives = [('브랜드 인지도', '노출 최대화'), ('트래픽', '클릭 유도'), ('전환', '구매/가입 유도'), ('동영상 조회', '영상 시청')]
    for j, (obj, desc) in enumerate(objectives):
        ox = cx+24+j*260
        is_sel = j == 2
        rr(d, ox, y+28, 240, 72, fill=INDIGO if is_sel else WHITE,
           ol=INDIGO if is_sel else GRAY3, lw=2 if is_sel else 1, r=8)
        t(d, ox+16, y+42, obj, fnt(13, True), fill=WHITE if is_sel else DARK)
        t(d, ox+16, y+62, desc, fnt(11), fill=(200,200,255) if is_sel else GRAY4)
    y += 124

    # Period
    t(d, cx+24, y, '캠페인 기간 *', fnt(13, True), fill=GRAY6)
    input_box(d, cx+24, y+28, 260, 44, '시작일', '2026.05.01')
    t(d, cx+300, y+46, '~', fnt(18), fill=GRAY4)
    input_box(d, cx+320, y+28, 260, 44, '종료일', '2026.05.31')
    rr(d, cx+600, y+28, 200, 44, fill=GRAY2, r=8)
    tc(d, cx+700, y+50, '30일간 집행', fnt(13, True), fill=GRAY6)
    y += 96

    # Daily budget preview
    t(d, cx+24, y, '캠페인 설명 (선택)', fnt(13, True), fill=GRAY6)
    rr(d, cx+24, y+28, W-344, 80, fill=WHITE, ol=GRAY3, r=8)
    t(d, cx+40, y+44, '봄 시즌 신상품 론칭을 위한 브랜드 인지도 및 전환 캠페인. 20-35세 여성 타겟.', fnt(13), fill=GRAY6)
    y += 132

    # Bottom buttons
    btn(d, cx+24, y+20, 160, 44, '← 이전', bg=GRAY2, fg=GRAY6)
    btn(d, W-304, y+20, 160, 44, '다음 단계 →', bg=INDIGO)

    fp = OUT / '21_vertical_campaign_info.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s22_vertical_target():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '타겟 설정', '광고를 보여줄 대상을 설정합니다')

    # Step bar
    steps = ['유형', '기본 정보', '타겟', '예산', '매체', '완료']
    step_w = (W-280)//len(steps)
    for i, s in enumerate(steps):
        sx = cx+i*step_w
        col = INDIGO if i<=2 else GRAY3
        d.ellipse([sx+step_w//2-12, cy+56, sx+step_w//2+12, cy+80], fill=col)
        tc(d, sx+step_w//2, cy+68, str(i+1), fnt(12, True), fill=WHITE if i<=2 else GRAY4)
        tc(d, sx+step_w//2, cy+94, s, fnt(10, i==2), fill=INDIGO if i<=2 else GRAY4)
        if i < len(steps)-1:
            lcolor = INDIGO if i < 2 else GRAY3
            d.line([(sx+step_w//2+12, cy+68), (sx+step_w-12+step_w//2, cy+68)], fill=lcolor, width=2)

    rr(d, cx, cy+118, W-280, 680, fill=WHITE, ol=GRAY3, r=16)
    y = cy+142

    # Age
    t(d, cx+24, y, '연령대', fnt(14, True), fill=DARK)
    ages = ['18-24', '25-34', '35-44', '45-54', '55+']
    for j, age in enumerate(ages):
        is_sel = j in [1, 2]
        ax = cx+24+j*156
        rr(d, ax, y+32, 136, 40, fill=INDIGO if is_sel else WHITE,
           ol=INDIGO if is_sel else GRAY3, lw=2 if is_sel else 1, r=8)
        tc(d, ax+68, y+52, age, fnt(14, True), fill=WHITE if is_sel else GRAY6)
    y += 96

    # Gender
    t(d, cx+24, y, '성별', fnt(14, True), fill=DARK)
    for j, (gen, sel) in enumerate([('전체', False), ('남성', False), ('여성', True)]):
        gx = cx+24+j*160
        rr(d, gx, y+32, 140, 40, fill=INDIGO if sel else WHITE,
           ol=INDIGO if sel else GRAY3, lw=2 if sel else 1, r=8)
        tc(d, gx+70, y+52, gen, fnt(14, sel), fill=WHITE if sel else GRAY6)
    y += 96

    # Location
    t(d, cx+24, y, '지역', fnt(14, True), fill=DARK)
    locs = [('서울', True), ('경기', True), ('인천', False), ('부산', False), ('대구', False), ('전국', False)]
    for j, (loc, sel) in enumerate(locs):
        lx = cx+24+j*140
        rr(d, lx, y+32, 120, 40, fill=INDIGO if sel else WHITE,
           ol=INDIGO if sel else GRAY3, r=8)
        tc(d, lx+60, y+52, loc, fnt(13, sel), fill=WHITE if sel else GRAY6)
    y += 96

    # Interest
    t(d, cx+24, y, '관심사', fnt(14, True), fill=DARK)
    interests = ['패션/뷰티', '쇼핑', '라이프스타일', '건강/운동', '음식', '여행', '테크', 'K-POP']
    xpos = cx+24
    for interest in interests:
        tw2 = d.textlength(interest, font=fnt(12, True))
        is_sel = interest in ['패션/뷰티', '쇼핑', '라이프스타일']
        pw = int(tw2)+24
        rr(d, xpos, y+32, pw, 36, fill=INDIGO if is_sel else WHITE,
           ol=INDIGO if is_sel else GRAY3, r=18)
        tc(d, xpos+pw//2, y+50, interest, fnt(12, True), fill=WHITE if is_sel else GRAY6)
        xpos += pw + 10
    y += 88

    # Preview
    rr(d, cx+24, y, W-328, 120, fill=INDIGO, r=12)
    t(d, cx+48, y+16, '예상 도달 범위', fnt(14, True), fill=WHITE)
    t(d, cx+48, y+44, '240만 ~ 380만명', fnt(28, True), fill=WHITE)
    t(d, cx+48, y+84, '서울/경기 거주 25-44세 여성 | 패션/쇼핑/라이프스타일 관심', fnt(12), fill=(200,200,255))

    btn(d, cx+24, y+140, 160, 44, '← 이전', bg=GRAY2, fg=GRAY6)
    btn(d, W-304, y+140, 160, 44, '다음 단계 →', bg=INDIGO)

    fp = OUT / '22_vertical_target.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s23_vertical_budget():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '예산 설정', '캠페인 예산과 입찰 방식을 설정합니다')

    steps = ['유형', '기본 정보', '타겟', '예산', '매체', '완료']
    step_w = (W-280)//len(steps)
    for i, s in enumerate(steps):
        sx = cx+i*step_w
        col = INDIGO if i<=3 else GRAY3
        d.ellipse([sx+step_w//2-12, cy+56, sx+step_w//2+12, cy+80], fill=col)
        tc(d, sx+step_w//2, cy+68, str(i+1), fnt(12, True), fill=WHITE if i<=3 else GRAY4)
        tc(d, sx+step_w//2, cy+94, s, fnt(10, i==3), fill=INDIGO if i<=3 else GRAY4)
        if i < len(steps)-1:
            lcolor = INDIGO if i < 3 else GRAY3
            d.line([(sx+step_w//2+12, cy+68), (sx+step_w-12+step_w//2, cy+68)], fill=lcolor, width=2)

    rr(d, cx, cy+118, W-280, 680, fill=WHITE, ol=GRAY3, r=16)
    y = cy+142

    # Budget type
    t(d, cx+24, y, '예산 유형', fnt(14, True), fill=DARK)
    for j, (bt, desc, sel) in enumerate([
        ('일일 예산', '매일 지출 한도 설정', True),
        ('총 예산', '전체 기간 지출 한도', False),
    ]):
        bx = cx+24+j*400
        rr(d, bx, y+32, 360, 60, fill=WHITE, ol=INDIGO if sel else GRAY3, lw=2 if sel else 1, r=8)
        d.ellipse([bx+16, y+52, bx+26, y+62], fill=INDIGO if sel else GRAY3)
        t(d, bx+40, y+44, bt, fnt(14, True), fill=DARK)
        t(d, bx+40, y+64, desc, fnt(12), fill=GRAY5)
    y += 116

    # Daily budget input
    t(d, cx+24, y, '일일 예산 *', fnt(14, True), fill=DARK)
    rr(d, cx+24, y+32, 300, 52, fill=WHITE, ol=INDIGO, lw=2, r=8)
    t(d, cx+40, y+52, '₩', fnt(18), fill=GRAY5)
    t(d, cx+68, y+50, '50,000', fnt(22, True), fill=DARK)
    t(d, cx+200, y+52, '원 / 일', fnt(14), fill=GRAY5)
    rr(d, cx+340, y+38, 90, 40, fill=INDIGO, r=8)
    tc(d, cx+385, y+58, '직접 입력', fnt(11, True), fill=WHITE)
    t(d, cx+24, y+94, '예상 월 지출: ₩ 1,550,000 (31일)', fnt(12), fill=GRAY4)
    y += 120

    # Bid method
    t(d, cx+24, y, '입찰 방식', fnt(14, True), fill=DARK)
    bids = [
        ('CPC', '클릭당 과금', '클릭을 유도할 때 적합', True),
        ('CPM', '1,000 노출당 과금', '브랜드 인지도에 적합', False),
        ('최적화 자동입찰', 'AI가 자동 최적화', '성과 극대화', False),
    ]
    for j, (bm, sub, desc, sel) in enumerate(bids):
        bx = cx+24+j*340
        rr(d, bx, y+32, 316, 80, fill=INDIGO if sel else WHITE,
           ol=INDIGO if sel else GRAY3, lw=2 if sel else 1, r=8)
        t(d, bx+16, y+48, bm, fnt(16, True), fill=WHITE if sel else DARK)
        t(d, bx+16, y+72, sub, fnt(11), fill=(200,200,255) if sel else GRAY5)
        t(d, bx+16, y+90, desc, fnt(11), fill=(180,180,240) if sel else GRAY4)
    y += 132

    # Max CPC
    t(d, cx+24, y, '최대 CPC 입찰가', fnt(14, True), fill=DARK)
    rr(d, cx+24, y+32, 260, 48, fill=WHITE, ol=GRAY3, r=8)
    t(d, cx+40, y+52, '₩ 320', fnt(16), fill=DARK)
    t(d, cx+24, y+90, '권장 입찰가: ₩ 280 ~ ₩ 380', fnt(12), fill=GRAY4)
    y += 120

    # Budget summary
    rr(d, cx+24, y, W-328, 100, fill=INDIGO, r=12)
    t(d, cx+48, y+16, '예산 요약', fnt(14, True), fill=WHITE)
    items = [('일일 예산', '₩ 50,000'), ('입찰 방식', 'CPC / 최대 ₩320'), ('예상 일 클릭', '약 156회'), ('예상 월 총 지출', '₩ 1,550,000')]
    for j, (k, v) in enumerate(items):
        jx = cx+48+j*240
        t(d, jx, y+44, k, fnt(11), fill=(180,180,240))
        t(d, jx, y+64, v, fnt(13, True), fill=WHITE)

    btn(d, cx+24, y+116, 160, 44, '← 이전', bg=GRAY2, fg=GRAY6)
    btn(d, W-304, y+116, 160, 44, '다음 단계 →', bg=INDIGO)

    fp = OUT / '23_vertical_budget.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s24_vertical_media_select():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '매체 선택', '광고를 집행할 매체를 선택하세요')

    steps = ['유형', '기본 정보', '타겟', '예산', '매체', '완료']
    step_w = (W-280)//len(steps)
    for i, s in enumerate(steps):
        sx = cx+i*step_w
        col = INDIGO if i<=4 else GRAY3
        d.ellipse([sx+step_w//2-12, cy+56, sx+step_w//2+12, cy+80], fill=col)
        tc(d, sx+step_w//2, cy+68, str(i+1), fnt(12, True), fill=WHITE if i<=4 else GRAY4)
        tc(d, sx+step_w//2, cy+94, s, fnt(10, i==4), fill=INDIGO if i<=4 else GRAY4)
        if i < len(steps)-1:
            lcolor = INDIGO
            d.line([(sx+step_w//2+12, cy+68), (sx+step_w-12+step_w//2, cy+68)], fill=lcolor, width=2)

    rr(d, cx, cy+118, W-280, 680, fill=WHITE, ol=GRAY3, r=16)
    y = cy+142

    t(d, cx+24, y, '집행 매체 선택 (복수 선택 가능)', fnt(16, True), fill=DARK)
    t(d, cx+24, y+28, '선택한 매체에 맞는 소재 사이즈를 다음 단계에서 설정합니다', fnt(13), fill=GRAY5)

    media = [
        ('인스타그램', '피드·스토리·릴스', '최소 ₩5,000/일', True, (225,48,108)),
        ('카카오', '카카오톡·카카오스토리', '최소 ₩10,000/일', True, (254,229,0)),
        ('네이버', 'GFA·밴드·네이버뉴스', '최소 ₩5,000/일', False, (3,199,90)),
        ('유튜브', '인스트림·범퍼·디스커버리', '최소 ₩10,000/일', False, (255,0,0)),
        ('메타(페이스북)', '피드·마켓플레이스·릴스', '최소 ₩5,000/일', False, (24,119,242)),
        ('틱톡', '인피드·탑뷰', '최소 ₩30,000/일', False, (0,0,0)),
    ]
    for i, (nm, sub, min_budget, sel, col) in enumerate(media):
        mx = cx+24+(i%3)*360
        my = y+60+(i//3)*190
        rr(d, mx, my, 340, 160, fill=WHITE, ol=col if sel else GRAY3, lw=3 if sel else 1, r=12)
        if sel:
            rr(d, mx+296, my+8, 36, 36, fill=col, r=18)
            tc(d, mx+314, my+26, '✓', fnt(16, True), fill=WHITE)
        # Color circle
        d.ellipse([mx+24, my+24, mx+64, my+64], fill=col)
        tc(d, mx+44, my+44, nm[0], fnt(20, True), fill=WHITE)
        t(d, mx+84, my+28, nm, fnt(16, True), fill=DARK)
        t(d, mx+84, my+52, sub, fnt(11), fill=GRAY5)
        rr(d, mx+24, my+82, 290, 1, fill=GRAY3)
        t(d, mx+24, my+96, '지원 포맷:', fnt(11), fill=GRAY5)
        t(d, mx+100, my+96, '이미지·영상·카루셀', fnt(11, True), fill=GRAY6)
        t(d, mx+24, my+118, '최소 예산:', fnt(11), fill=GRAY5)
        t(d, mx+100, my+118, min_budget, fnt(11, True), fill=col)
        rr(d, mx+24, my+138, 290, 1, fill=GRAY3)

    y = cy+142+60+2*190+20
    rr(d, cx+24, y, W-328, 60, fill=INDIGO, r=10)
    t(d, cx+48, y+16, '선택된 매체: 인스타그램, 카카오   |   예상 일일 예산 배분: 인스타그램 60% · 카카오 40%', fnt(13), fill=WHITE)

    btn(d, cx+24, y+76, 160, 44, '← 이전', bg=GRAY2, fg=GRAY6)
    btn(d, W-304, y+76, 200, 44, '소재 업로드 →', bg=INDIGO)

    fp = OUT / '24_vertical_media_select.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s30_material_upload():
    img, d = base_app('material')
    cx, cy = 240, 76

    section_title(d, cx, cy, '소재 업로드', '광고에 사용할 이미지/영상을 업로드하세요')

    # Drop zone
    rr(d, cx, cy+60, W-280, 320, fill=WHITE, ol=INDIGO, lw=2, r=16)
    # Dashed border effect
    for i in range(0, W-280, 24):
        if i % 48 < 24:
            d.line([(cx+i, cy+60), (min(cx+i+16, cx+W-280), cy+60)], fill=INDIGO, width=2)
            d.line([(cx+i, cy+380), (min(cx+i+16, cx+W-280), cy+380)], fill=INDIGO, width=2)
    for j in range(0, 320, 24):
        if j % 48 < 24:
            d.line([(cx, cy+60+j), (cx, min(cy+60+j+16, cy+380))], fill=INDIGO, width=2)
            d.line([(cx+W-280, cy+60+j), (cx+W-280, min(cy+60+j+16, cy+380))], fill=INDIGO, width=2)

    # Upload icon + text
    d.ellipse([W//2-48, cy+120, W//2+48, cy+216], fill=BLUE_L)
    tc(d, W//2, cy+168, '↑', fnt(48, True), fill=INDIGO)
    tc(d, W//2, cy+236, '이미지 또는 영상을 드래그하거나 클릭하세요', fnt(16), fill=GRAY6)
    tc(d, W//2, cy+264, 'PNG, JPG, MP4 지원 / 최대 50MB / 최대 10개', fnt(13), fill=GRAY4)
    btn(d, W//2-80, cy+296, 160, 44, '파일 선택', bg=INDIGO, sz=15)

    # Uploaded files
    t(d, cx, cy+404, '업로드된 소재 (3개)', fnt(15, True), fill=DARK)

    files = [
        ('product_main.jpg', '2.4 MB', '1080x1080', 'JPG'),
        ('product_lifestyle.jpg', '3.1 MB', '1440x960', 'JPG'),
        ('brand_video.mp4', '18.2 MB', '1920x1080', 'MP4'),
    ]
    for i, (fname, size, dim, fmt) in enumerate(files):
        fx = cx + i*400
        rr(d, fx, cy+434, 380, 180, fill=WHITE, ol=GRAY3, r=12)
        # Thumbnail
        rr(d, fx+12, cy+448, 120, 90, fill=GRAY2, r=8)
        tc(d, fx+72, cy+493, fmt, fnt(14, True), fill=GRAY5)
        t(d, fx+144, cy+454, fname, fnt(13, True), fill=DARK)
        t(d, fx+144, cy+476, f'크기: {size}  해상도: {dim}', fnt(12), fill=GRAY5)
        rr(d, fx+144, cy+498, 60, 24, fill=GREEN_L, r=12)
        tc(d, fx+174, cy+510, '정상', fnt(11, True), fill=GREEN)
        # Delete button
        rr(d, fx+340, cy+448, 28, 28, fill=GRAY2, r=14)
        tc(d, fx+354, cy+462, '×', fnt(16, True), fill=GRAY5)
        # Usage bar
        t(d, fx+144, cy+534, '사용 예정 매체:', fnt(11), fill=GRAY4)
        pill(d, fx+248, cy+530, '인스타', bg=INDIGO, sz=10, px=8, py=2)

    btn(d, cx, cy+650, W-280, 52, '다음: 사이즈 선택 →', bg=INDIGO, sz=16)

    fp = OUT / '30_material_upload.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s31_material_size_select():
    img, d = base_app('material')
    cx, cy = 240, 76

    section_title(d, cx, cy, '사이즈 선택', '매체별 광고 사이즈를 선택하세요 (복수 선택 가능)')

    # Left: size list
    rr(d, cx, cy+60, 660, 740, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+76, '매체별 권장 사이즈', fnt(15, True), fill=DARK)
    btn(d, cx+520, cy+72, 128, 28, '전체 선택', bg=GRAY2, fg=GRAY6, sz=12)

    size_groups = [
        ('인스타그램', (225,48,108), [
            ('정사각형', '1:1', '1080x1080', True),
            ('세로형', '4:5', '1080x1350', True),
            ('스토리/릴스', '9:16', '1080x1920', True),
            ('가로형', '16:9', '1080x608', False),
        ]),
        ('카카오', (254,229,0), [
            ('카카오 배너', '4:1', '1029x258', True),
            ('비즈보드', '2:1', '1029x514', False),
        ]),
        ('네이버 GFA', (3,199,90), [
            ('정사각형', '1:1', '800x800', False),
            ('가로형', '16:9', '800x450', False),
        ]),
        ('유튜브', (255,0,0), [
            ('인스트림', '16:9', '1920x1080', False),
        ]),
    ]

    gy = cy+108
    for group_name, gcol, sizes in size_groups:
        # Group header
        rr(d, cx+12, gy, 640, 32, fill=GRAY1, r=4)
        d.ellipse([cx+20, gy+8, cx+36, gy+24], fill=gcol if gcol != (254,229,0) else (200,180,0))
        t(d, cx+44, gy+8, group_name, fnt(13, True), fill=DARK)
        gy += 38

        for sname, ratio, res, sel in sizes:
            if sel:
                rr(d, cx+12, gy, 640, 36, fill=INDIGO, r=6)
                rr(d, cx+20, gy+10, 16, 16, fill=WHITE, r=2)
                tc(d, cx+28, gy+18, '✓', fnt(10, True), fill=INDIGO)
                t(d, cx+48, gy+10, sname, fnt(13, True), fill=WHITE)
                t(d, cx+280, gy+10, ratio, fnt(12), fill=(200,200,255))
                t(d, cx+400, gy+10, res, fnt(12), fill=(200,200,255))
            else:
                rr(d, cx+20, gy+10, 16, 16, ol=GRAY3, r=2)
                t(d, cx+48, gy+10, sname, fnt(13), fill=GRAY6)
                t(d, cx+280, gy+10, ratio, fnt(12), fill=GRAY4)
                t(d, cx+400, gy+10, res, fnt(12), fill=GRAY4)
            gy += 40
        gy += 8

    # Right: preview
    rr(d, cx+676, cy+60, W-280-676, 740, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+692, cy+76, '선택된 사이즈 (5개)', fnt(14, True), fill=DARK)

    previews = [
        ('인스타 1:1', 80, 80),
        ('인스타 4:5', 64, 80),
        ('인스타 9:16', 45, 80),
        ('카카오 배너', 80, 20),
        ('인스타 가로', 80, 45),
    ]
    for i, (lbl, pw, ph) in enumerate(previews):
        px2 = cx+692+(i%3)*140
        py2 = cy+110+(i//3)*160
        # Ratio box
        rr(d, px2+20, py2, pw, ph, fill=GRAY2, ol=INDIGO, lw=2, r=4)
        tc(d, px2+20+pw//2, py2+ph//2, '', fnt(10), fill=GRAY4)
        t(d, px2+20, py2+ph+6, lbl, fnt(10), fill=GRAY6)

    btn(d, cx, cy+826, 660, 44, '← 이전', bg=GRAY2, fg=GRAY6)
    btn(d, cx+676, cy+826, W-280-676, 44, 'AI 크롭 시작 →', bg=INDIGO)

    fp = OUT / '31_material_size_select.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s32_ai_crop_adjust():
    img, d = base_app('material')
    cx, cy = 240, 76

    section_title(d, cx, cy, 'AI 자동 크롭 & 조정', 'AI가 각 사이즈에 맞게 자동으로 크롭했습니다. 수동으로 조정할 수 있습니다.')

    # Left: source image
    rr(d, cx, cy+60, 360, 480, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+76, '원본 소재', fnt(14, True), fill=DARK)
    rr(d, cx+16, cy+104, 330, 280, fill=GRAY2, r=8)
    tc(d, cx+181, cy+244, '제품 이미지', fnt(16), fill=GRAY4)
    tc(d, cx+181, cy+268, '1440 × 960', fnt(12), fill=GRAY4)
    t(d, cx+16, cy+398, 'product_main.jpg', fnt(12, True), fill=GRAY6)
    t(d, cx+16, cy+418, '크기: 2.4MB  해상도: 1440×960', fnt(11), fill=GRAY4)
    btn(d, cx+16, cy+448, 160, 36, '소재 교체', bg=GRAY2, fg=GRAY6, sz=13)

    # Right: cropped previews grid
    rr(d, cx+376, cy+60, W-280-376, 740, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+392, cy+76, 'AI 크롭 결과 (5개 사이즈)', fnt(14, True), fill=DARK)
    t(d, cx+392, cy+96, '각 이미지를 클릭하면 수동 조정 가능', fnt(11), fill=GRAY4)

    crops = [
        ('인스타 1:1', 160, 160, True),
        ('인스타 4:5', 128, 160, True),
        ('인스타 스토리 9:16', 90, 160, False),
        ('카카오 배너 4:1', 200, 50, True),
        ('인스타 가로 16:9', 200, 112, False),
    ]

    for i, (lbl, cw2, ch2, ok) in enumerate(crops):
        cpx = cx+392+(i%3)*240
        cpy = cy+120+(i//3)*220
        # Crop box with border
        border_col = GREEN if ok else AMBER
        rr(d, cpx, cpy, cw2+4, ch2+4, fill=border_col, r=6)
        rr(d, cpx+2, cpy+2, cw2, ch2, fill=GRAY2, r=5)
        tc(d, cpx+cw2//2+2, cpy+ch2//2+2, '📷', fnt(20), fill=GRAY4)
        t(d, cpx, cpy+ch2+12, lbl, fnt(10, True), fill=DARK)
        status = '자동 완료' if ok else '수동 조정 필요'
        t(d, cpx, cpy+ch2+26, status, fnt(9), fill=GREEN if ok else AMBER)
        # Edit button
        rr(d, cpx+cw2-30, cpy+4, 26, 22, fill=(0,0,0,120), r=4)
        tc(d, cpx+cw2-17, cpy+15, '✎', fnt(11), fill=WHITE)

    # Adjustment handles example (for selected crop)
    apy = cy+120
    apx = cx+392+(2%3)*240
    # Handle circles at corners
    for hx, hy in [(apx, apy), (apx+90+4, apy), (apx, apy+160+4), (apx+90+4, apy+160+4)]:
        d.ellipse([hx-6, hy-6, hx+6, hy+6], fill=INDIGO, outline=WHITE, width=2)

    btn(d, cx+376, cy+820, W-280-376, 44, '후킹 문구 생성 →', bg=INDIGO)

    fp = OUT / '32_ai_crop_adjust.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s33_ai_hook_generate():
    img, d = base_app('material')
    cx, cy = 240, 76

    section_title(d, cx, cy, 'AI 후킹 문구 생성', 'AI가 클릭률 높은 광고 카피를 자동으로 생성합니다')

    # Left input
    rr(d, cx, cy+60, 460, 740, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+76, '제품 정보 입력', fnt(15, True), fill=DARK)

    y = cy+110
    t(d, cx+16, y, '제품/서비스 카테고리', fnt(13, True), fill=GRAY6)
    rr(d, cx+16, y+26, 428, 40, fill=WHITE, ol=GRAY3, r=8)
    t(d, cx+32, y+42, '패션 / 의류 (봄 시즌 아이템)', fnt(13), fill=DARK)
    t(d, cx+432, y+42, '▾', fnt(12), fill=GRAY4)
    y += 82

    t(d, cx+16, y, '주요 특징 (3가지)', fnt(13, True), fill=GRAY6)
    features_input = ['봄 신상 20% 할인', '무료 배송', '친환경 소재']
    for j, feat in enumerate(features_input):
        input_box(d, cx+16, y+26+j*52, 428, 40, f'특징 {j+1}', feat)
    y += 200

    t(d, cx+16, y, '타겟 고객', fnt(13, True), fill=GRAY6)
    input_box(d, cx+16, y+26, 428, 40, '예: 20-30대 여성', '20-35세 패션 관심 여성')
    y += 82

    t(d, cx+16, y, '광고 목표', fnt(13, True), fill=GRAY6)
    for j, (goal, sel) in enumerate([('클릭 유도', True), ('구매 전환', False), ('인지도', False)]):
        gx = cx+16+j*148
        rr(d, gx, y+26, 136, 36, fill=INDIGO if sel else WHITE, ol=INDIGO if sel else GRAY3, r=8)
        tc(d, gx+68, y+44, goal, fnt(12, sel), fill=WHITE if sel else GRAY6)
    y += 82

    t(d, cx+16, y, '광고 톤', fnt(13, True), fill=GRAY6)
    for j, (tone, sel) in enumerate([('친근한', False), ('세련된', True), ('긴박한', False), ('유머러스', False)]):
        tx2 = cx+16+j*112
        rr(d, tx2, y+26, 100, 36, fill=INDIGO if sel else WHITE, ol=INDIGO if sel else GRAY3, r=8)
        tc(d, tx2+50, y+44, tone, fnt(12, sel), fill=WHITE if sel else GRAY6)

    btn(d, cx+16, cy+770, 428, 44, '✨ AI 문구 생성', bg=INDIGO, sz=15)

    # Right: Generated hooks
    rr(d, cx+476, cy+60, W-280-476, 740, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+492, cy+76, 'AI 생성 후킹 문구 (3가지)', fnt(15, True), fill=DARK)
    t(d, cx+492, cy+96, '마음에 드는 문구를 선택하거나 직접 수정하세요', fnt(11), fill=GRAY4)

    hooks = [
        ('A안 — 감성 어필',
         '이 봄, 당신의 스타일을\n새롭게 정의하세요',
         '신상 컬렉션 20% 할인 + 무료배송',
         '지금 쇼핑하기', 8.4, True),
        ('B안 — 혜택 강조',
         '봄 신상 최대 20% 세일\n오늘만 무료배송',
         '친환경 소재로 만든 봄 시즌 컬렉션',
         '할인 받기', 7.2, False),
        ('C안 — 긴박감 자극',
         '한정 수량! 봄 신상\n놓치면 아쉬운 그 아이템',
         '지금 바로 확인하세요',
         '빠른 주문', 6.8, False),
    ]

    for i, (label, headline, sub, cta, score, selected) in enumerate(hooks):
        hx = cx+492
        hy = cy+120+i*192
        border_col = INDIGO if selected else GRAY3
        rr(d, hx, hy, W-280-492, 172, fill=INDIGO if selected else WHITE,
           ol=border_col, lw=3 if selected else 1, r=12)
        col = WHITE if selected else DARK
        sub_col = (200,200,255) if selected else GRAY5
        t(d, hx+16, hy+12, label, fnt(12), fill=sub_col)
        t(d, hx+16, hy+34, headline.split('\n')[0], fnt(17, True), fill=col)
        t(d, hx+16, hy+58, headline.split('\n')[1] if '\n' in headline else '', fnt(17, True), fill=col)
        t(d, hx+16, hy+88, sub, fnt(12), fill=sub_col)
        # CTA badge
        rr(d, hx+16, hy+112, 100, 32, fill=AMBER if selected else AMBER_L, r=8)
        tc(d, hx+66, hy+128, cta, fnt(12, True), fill=DARK)
        # Score
        t(d, hx+W-280-492-80, hy+12, f'예상 CTR', fnt(10), fill=sub_col)
        t(d, hx+W-280-492-80, hy+30, f'{score}%', fnt(18, True), fill=AMBER if selected else AMBER)
        # Edit
        btn_outline(d, hx+W-280-492-90, hy+112, 74, 32, '수정', col=WHITE if selected else INDIGO)
        if selected:
            rr(d, hx+W-280-492-170, hy+8, 70, 24, fill=AMBER, r=12)
            tc(d, hx+W-280-492-135, hy+20, '선택됨', fnt(11, True), fill=DARK)

    btn(d, cx+476, cy+820, W-280-476, 44, '매체별 미리보기 →', bg=INDIGO)

    fp = OUT / '33_ai_hook_generate.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s34_media_preview():
    img, d = base_app('material')
    cx, cy = 240, 76

    section_title(d, cx, cy, '매체별 미리보기', '실제 광고가 어떻게 보이는지 확인하세요')

    # Tab bar
    tabs = ['인스타그램', '카카오', '네이버', '유튜브']
    for i, tab in enumerate(tabs):
        is_sel = i == 0
        tx2 = cx + i*200
        if is_sel:
            rr(d, tx2, cy+60, 180, 38, fill=INDIGO, r=8)
        t(d, tx2+90, cy+79, tab, fnt(14, is_sel), fill=WHITE if is_sel else GRAY5, anchor='mm')
        if is_sel:
            d.line([(tx2, cy+98), (tx2+180, cy+98)], fill=INDIGO, width=3)

    # Instagram phone mockup
    phone_x, phone_y = cx+40, cy+112
    phone_w, phone_h = 320, 600
    rr(d, phone_x, phone_y, phone_w, phone_h, fill=DARK, r=40)
    rr(d, phone_x+8, phone_y+20, phone_w-16, phone_h-40, fill=WHITE, r=32)

    # Instagram UI inside phone
    # Header
    rr(d, phone_x+8, phone_y+20, phone_w-16, 48, fill=WHITE, r=0)
    t(d, phone_x+20, phone_y+36, '인스타그램', fnt(14, True), fill=DARK)

    # Ad post
    rr(d, phone_x+8, phone_y+68, phone_w-16, 48, fill=WHITE, r=0)
    d.ellipse([phone_x+18, phone_y+78, phone_x+50, phone_y+110], fill=INDIGO)
    tc(d, phone_x+34, phone_y+94, 'A', fnt(13, True), fill=WHITE)
    t(d, phone_x+58, phone_y+82, '내 브랜드', fnt(12, True), fill=DARK)
    t(d, phone_x+58, phone_y+98, '광고', fnt(10), fill=GRAY5)
    t(d, phone_x+phone_w-50, phone_y+88, '···', fnt(14), fill=GRAY4)

    # Ad image
    rr(d, phone_x+8, phone_y+116, phone_w-16, phone_w-16, fill=GRAY2, r=0)
    tc(d, phone_x+phone_w//2, phone_y+116+(phone_w-16)//2, '제품 이미지', fnt(14), fill=GRAY5)

    # Action bar + caption
    action_y = phone_y+116+phone_w-16+8
    t(d, phone_x+20, action_y, '♡ 저장 공유', fnt(12), fill=DARK)
    t(d, phone_x+20, action_y+24, '이 봄, 당신의 스타일을 새롭게 정의하세요', fnt(11, True), fill=DARK)
    t(d, phone_x+20, action_y+40, '신상 컬렉션 20% 할인 + 무료배송', fnt(10), fill=GRAY6)
    rr(d, phone_x+20, action_y+60, phone_w-48, 36, fill=INDIGO, r=8)
    tc(d, phone_x+phone_w//2, action_y+78, '지금 쇼핑하기', fnt(12, True), fill=WHITE)

    # Right: specs and options
    rx = cx+420
    rr(d, rx, cy+112, W-280-420, 600, fill=WHITE, ol=GRAY3, r=12)
    t(d, rx+16, cy+128, '인스타그램 광고 상세', fnt(15, True), fill=DARK)

    t(d, rx+16, cy+164, '선택된 포맷', fnt(13, True), fill=GRAY6)
    for i, (fmt, sel) in enumerate([('피드 (1:1)', True), ('스토리 (9:16)', False), ('릴스 (9:16)', False)]):
        fx2 = rx+16+i*220
        rr(d, fx2, cy+186, 200, 36, fill=INDIGO if sel else WHITE,
           ol=INDIGO if sel else GRAY3, r=8)
        tc(d, fx2+100, cy+204, fmt, fnt(12, sel), fill=WHITE if sel else GRAY6)

    t(d, rx+16, cy+244, '광고 소재', fnt(13, True), fill=GRAY6)
    rr(d, rx+16, cy+266, 200, 120, fill=GRAY2, r=8)
    tc(d, rx+116, cy+326, '1:1 크롭', fnt(12), fill=GRAY4)

    t(d, rx+232, cy+266, '광고 문구', fnt(12, True), fill=GRAY6)
    rr(d, rx+232, cy+286, W-280-460, 100, fill=GRAY1, r=8)
    t(d, rx+248, cy+298, '이 봄, 당신의 스타일을', fnt(11, True), fill=DARK)
    t(d, rx+248, cy+316, '새롭게 정의하세요', fnt(11, True), fill=DARK)
    t(d, rx+248, cy+338, '신상 컬렉션 20% 할인 + 무료배송', fnt(10), fill=GRAY6)

    t(d, rx+16, cy+408, '예상 성과', fnt(13, True), fill=GRAY6)
    for i, (metric, val) in enumerate([('예상 노출', '45,000~80,000'), ('예상 클릭', '600~1,200'), ('예상 CTR', '1.2%~1.8%')]):
        my = cy+430+i*52
        rr(d, rx+16, my, W-280-460, 44, fill=GRAY1, r=8)
        t(d, rx+32, my+10, metric, fnt(12), fill=GRAY5)
        t(d, rx+32, my+28, val, fnt(13, True), fill=DARK)

    btn(d, cx+420, cy+742, W-280-420, 44, '소재 최종 확인 →', bg=INDIGO)

    fp = OUT / '34_media_preview.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s35_material_confirm():
    img, d = base_app('material')
    cx, cy = 240, 76

    section_title(d, cx, cy, '소재 최종 확인', '캠페인 제출 전 소재를 최종 확인하세요')

    # Summary bar
    rr(d, cx, cy+60, W-280, 64, fill=INDIGO, r=12)
    items = [('캠페인', '봄 시즌 신상품 프로모션'), ('매체', '인스타그램 · 카카오'),
             ('소재', '3개'), ('사이즈', '5가지'), ('집행 기간', '2026.05.01~05.31')]
    for i, (k, v) in enumerate(items):
        sx = cx+24+i*220
        t(d, sx, cy+72, k, fnt(11), fill=(180,180,240))
        t(d, sx, cy+90, v, fnt(13, True), fill=WHITE)

    # Material grid
    t(d, cx, cy+144, '소재별 크롭 현황', fnt(15, True), fill=DARK)

    source_files = ['product_main.jpg', 'product_lifestyle.jpg', 'brand_video.mp4']
    size_cols = ['1:1\n1080×1080', '4:5\n1080×1350', '9:16\n1080×1920', '카카오\n1029×258', '인스타가로\n1080×608']

    # Header
    col_x2 = [cx, cx+200] + [cx+200+j*220 for j in range(5)]
    t(d, col_x2[0], cy+170, '원본 소재', fnt(12, True), fill=GRAY5)
    for j, sc in enumerate(size_cols):
        tc(d, col_x2[j+2]+80, cy+170, sc.replace('\n', ' '), fnt(10, True), fill=GRAY5)

    d.line([(cx, cy+188), (W-160, cy+188)], fill=GRAY3, width=1)

    for ri, fname in enumerate(source_files):
        ry = cy+196+ri*160
        # Source thumbnail
        rr(d, col_x2[0], ry+8, 150, 110, fill=GRAY2, r=6)
        tc(d, col_x2[0]+75, ry+63, fname[:16], fnt(9), fill=GRAY4)
        # Status pills
        statuses = [True, True, True, True, False] if ri < 2 else [False, False, False, False, False]
        for j, ok in enumerate(statuses):
            tx2 = col_x2[j+2]
            if ri == 2 and j == 0:
                rr(d, tx2+10, ry+20, 120, 80, fill=AMBER_L, r=6)
                tc(d, tx2+70, ry+45, '동영상\n지원불가', fnt(9), fill=AMBER)
            elif ok:
                rr(d, tx2+10, ry+20, 120, 80, fill=GREEN_L, r=6)
                tc(d, tx2+70, ry+55, '✓ 준비', fnt(11, True), fill=GREEN)
            else:
                rr(d, tx2+10, ry+20, 120, 80, fill=GRAY2, r=6)
                tc(d, tx2+70, ry+55, '미선택', fnt(10), fill=GRAY4)

    # Checklist
    rr(d, cx, cy+688, W-280, 120, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+704, '제출 전 확인 체크리스트', fnt(14, True), fill=DARK)
    checks = [
        ('소재 크롭 검토 완료', True),
        ('AI 후킹 문구 선택 완료', True),
        ('매체별 미리보기 확인', True),
        ('크레딧 잔액 충분 (잔여 ₩128,500 / 필요 ₩50,000/일)', True),
    ]
    for i, (check, ok) in enumerate(checks):
        cy2 = cy+726+i*18
        ix = cx+16+(i%2)*580
        d.ellipse([ix, cy2+2, ix+12, cy2+14], fill=GREEN if ok else GRAY3)
        t(d, ix+20, cy2, check, fnt(12), fill=DARK if ok else GRAY4)

    btn(d, cx, cy+828, W-280, 52, '캠페인 검수 신청 →', bg=INDIGO, sz=17)

    fp = OUT / '35_material_confirm.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

# ── Run all ──────────────────────────────────────────────────────
if __name__ == '__main__':
    funcs = [
        s00_landing, s01_service_intro, s02_login, s03_signup,
        s10_dashboard, s11_credit_charge, s12_credit_history,
        s20_campaign_type_select, s21_vertical_campaign_info,
        s22_vertical_target, s23_vertical_budget, s24_vertical_media_select,
        s30_material_upload, s31_material_size_select, s32_ai_crop_adjust,
        s33_ai_hook_generate, s34_media_preview, s35_material_confirm,
    ]
    for fn in funcs:
        try:
            fn()
        except Exception as e:
            print(f'FAIL {fn.__name__}: {e}')
            import traceback; traceback.print_exc()

    print(f'\nPart 1 done: {len(funcs)} screens')
