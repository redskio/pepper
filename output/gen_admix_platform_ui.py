# -*- coding: utf-8 -*-
"""AdMix Platform UI — 5 screens 1440x900
Navy #1A2B4B + Orange #FF6B35  · SaaS / Marketplace feel
"""
import sys, io, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path('C:/Agent/pepper/admix_ui')
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1440, 900

# ── Palette ──────────────────────────────────────────────────
NAVY     = (26,  43,  75)
NAVY2    = (36,  58, 100)
NAVY3    = (15,  25,  50)
NAVY_L   = (230, 235, 248)
NAVY_MID = (55,  85, 140)
ORANGE   = (255, 107,  53)
ORANGE2  = (230,  80,  25)
ORANGE_L = (255, 237, 228)
WHITE    = (255, 255, 255)
BG       = (247, 248, 252)
CARD     = (255, 255, 255)
BORDER   = (222, 227, 242)
BORDER2  = (205, 213, 232)
TEXT     = (15,  23,  42)
TEXT2    = (65,  82, 110)
TEXT3    = (145, 160, 185)
SUCCESS  = (16,  185, 129)
SUCCL    = (207, 250, 229)
WARN     = (245, 158,  11)
WARNL    = (253, 242, 196)
PURPLE   = (124,  58, 237)
PURPL    = (236, 228, 253)

_fc = {}
def fnt(sz, bold=False):
    key = (sz, bold)
    if key not in _fc:
        fp = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
        try:   _fc[key] = ImageFont.truetype(fp, sz)
        except: _fc[key] = ImageFont.load_default()
    return _fc[key]

# ── Primitives ────────────────────────────────────────────────
def rr(d, x, y, w, h, fill=None, ol=None, lw=1, r=10):
    if w > 0 and h > 0:
        d.rounded_rectangle([x, y, x+w, y+h], radius=min(r, w//2, h//2),
                             fill=fill, outline=ol, width=lw)

def t(d, s, x, y, sz, col=None, bold=False):
    d.text((x, y), str(s), font=fnt(sz, bold), fill=col or TEXT)

def tc(d, s, cx, y, sz, col=None, bold=False):
    bb = d.textbbox((0, 0), str(s), font=fnt(sz, bold))
    d.text((cx-(bb[2]-bb[0])//2, y), str(s), font=fnt(sz, bold), fill=col or TEXT)

def tw(d, s, sz, bold=False):
    bb = d.textbbox((0, 0), str(s), font=fnt(sz, bold))
    return bb[2]-bb[0]

def th_px(d, s, sz, bold=False):
    bb = d.textbbox((0, 0), str(s), font=fnt(sz, bold))
    return bb[3]-bb[1]

def btn(d, x, y, w, h, lbl, sz=15, fill=ORANGE, col=WHITE, r=24, bold=True):
    rr(d, x, y, w, h, fill=fill, r=r)
    tc(d, lbl, x+w//2, y+(h-th_px(d,lbl,sz,bold))//2, sz, col=col, bold=bold)

def btn_ghost(d, x, y, w, h, lbl, sz=14, ol=None, col=None, r=24):
    ol = ol or (130, 155, 200)
    col = col or (180, 205, 240)
    rr(d, x, y, w, h, ol=ol, lw=2, r=r)
    tc(d, lbl, x+w//2, y+(h-th_px(d,lbl,sz))//2, sz, col=col)

def grad_v(w, h, c1, c2):
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        t2 = y/max(h-1, 1)
        for c in range(3):
            arr[y, :, c] = int(c1[c]*(1-t2) + c2[c]*t2)
    return Image.fromarray(arr)

def grad_h(w, h, c1, c2):
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for x in range(w):
        t2 = x/max(w-1, 1)
        for c in range(3):
            arr[:, x, c] = int(c1[c]*(1-t2) + c2[c]*t2)
    return Image.fromarray(arr)

def shadow_card(img, d, x, y, w, h, r=12):
    """Draw card with subtle shadow via blur"""
    shadow = Image.new('RGBA', (w+20, h+20), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([8, 8, w+12, h+12], radius=r, fill=(0, 0, 0, 40))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img_rgba = img.convert('RGBA')
    img_rgba.paste(shadow, (x-10, y-10), shadow)
    base = img_rgba.convert('RGB')
    img.paste(base)

# ── Shared Nav ────────────────────────────────────────────────
def nav_bar(img, d, active=''):
    g = grad_h(W, 64, NAVY3, NAVY)
    img.paste(g, (0, 0))
    # Logo
    t(d, 'Ad', 30, 18, 24, col=ORANGE, bold=True)
    t(d, 'Mix', 64, 18, 24, col=WHITE,  bold=True)
    d.ellipse([96, 29, 104, 37], fill=(80, 105, 150))
    t(d, '버티컬 광고 플랫폼', 114, 24, 12, col=(150, 175, 215))
    items = ['대시보드', '캠페인', '매체', '소재', '분석']
    nx = 320
    for item in items:
        is_a = item == active
        t(d, item, nx, 22, 14, col=WHITE if is_a else (175, 200, 235))
        if is_a:
            bb = d.textbbox((nx, 22), item, font=fnt(14))
            d.rectangle([nx, 60, bb[2]+2, 64], fill=ORANGE)
        nx += 108
    rr(d, W-224, 15, 152, 34, fill=ORANGE, r=17)
    tc(d, '+ 새 캠페인', W-224+76, 22, 13, col=WHITE, bold=True)
    d.ellipse([W-56, 15, W-18, 49], fill=NAVY_MID)
    tc(d, '재', W-37, 24, 14, col=WHITE, bold=True)

# ── KPI Card ─────────────────────────────────────────────────
def kpi_card(d, x, y, w, h, label, val, change, up=True, accent=ORANGE):
    rr(d, x, y, w, h, fill=CARD, ol=BORDER, r=12)
    rr(d, x, y, 4, h, fill=accent, r=2)
    t(d, label, x+20, y+18, 12, col=TEXT3)
    t(d, val,   x+20, y+38, 28, col=TEXT, bold=True)
    # Change badge
    chg_col = SUCCESS if up else (239, 68, 68)
    chg_bg  = SUCCL if up else (254, 226, 226)
    chg_lbl = f'▲ {change}' if up else f'▼ {change}'
    rr(d, x+20, y+h-36, tw(d, chg_lbl, 12)+14, 22, fill=chg_bg, r=11)
    t(d, chg_lbl, x+27, y+h-32, 12, col=chg_col, bold=True)
    t(d, '전월比', x+tw(d,chg_lbl,12)+20+20, y+h-32, 11, col=TEXT3)

# ── Line/Area Chart ───────────────────────────────────────────
def area_chart(img, d, x, y, w, h, data, col=ORANGE, bg=CARD, title=''):
    rr(d, x, y, w, h, fill=bg, ol=BORDER, r=12)
    if title:
        t(d, title, x+20, y+16, 13, col=TEXT2, bold=True)
    PAD_L, PAD_R, PAD_T, PAD_B = 52, 24, 48, 36
    CX = x + PAD_L;  CY = y + PAD_T
    CW = w - PAD_L - PAD_R;  CH = h - PAD_T - PAD_B
    labels = ['4/21', '4/22', '4/23', '4/24', '4/25', '4/26', '4/27']
    n = len(labels)
    for i, lbl in enumerate(labels):
        px = CX + i*CW//(n-1)
        t(d, lbl, px - tw(d,lbl,10)//2, y+h-PAD_B+6, 10, col=TEXT3)
        d.line([(px, CY), (px, CY+CH)], fill=(230, 233, 245), width=1)
    for i in range(5):
        gy = CY + i*CH//4
        d.line([(CX, gy), (CX+CW, gy)], fill=(230, 233, 245), width=1)
    if not data or len(data) < 2:
        return
    mn, mx = min(data), max(data)
    rng = max(mx-mn, 1)
    pts = []
    for i, v in enumerate(data):
        px = CX + i*CW//(n-1)
        py = CY + CH - int((v-mn)/rng * CH * 0.85) - 8
        pts.append((px, py))
    # Fill
    fill_poly = [(pts[0][0], CY+CH)] + pts + [(pts[-1][0], CY+CH)]
    fc = tuple(int(0.88*255 + 0.12*col[c]) for c in range(3))
    d.polygon(fill_poly, fill=fc)
    # Line
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=col, width=3)
    for px, py in pts:
        d.ellipse([px-5, py-5, px+5, py+5], fill=CARD, outline=col, width=2)

def bar_chart_h(d, x, y, w, h, items, col=ORANGE, bg=CARD, title=''):
    """Horizontal bar chart"""
    rr(d, x, y, w, h, fill=bg, ol=BORDER, r=12)
    if title:
        t(d, title, x+20, y+16, 13, col=TEXT2, bold=True)
    PAD_L = 120; PAD_T = 44; ITEM_H = 36; GAP = 10
    total_h_needed = len(items)*(ITEM_H+GAP)
    start_y = y + PAD_T + max(0, (h - PAD_T - 20 - total_h_needed) // 2)
    max_val = max(v for _, v in items) if items else 1
    bar_w = w - PAD_L - 80
    for i, (lbl, val) in enumerate(items):
        by = start_y + i*(ITEM_H+GAP)
        t(d, lbl, x+16, by+8, 12, col=TEXT2)
        bw = int(bar_w * val / max_val)
        rr(d, x+PAD_L, by, bw, ITEM_H, fill=col, r=6)
        pct_lbl = f'{val:,}'
        t(d, pct_lbl, x+PAD_L+bw+8, by+9, 12, col=TEXT2, bold=True)


# ═══════════════════════════════════════════════════════════════
# SCREEN 01 — 랜딩 / 온보딩
# ═══════════════════════════════════════════════════════════════
def screen_01():
    img = Image.new('RGB', (W, H), BG)
    d   = ImageDraw.Draw(img)

    # ── Hero gradient (top 570px) ──────────────────────────────
    hero_h = 572
    hero = grad_v(W, hero_h, NAVY3, NAVY2)
    img.paste(hero, (0, 0))
    d = ImageDraw.Draw(img)  # redraw after paste

    # Decorative circles (background depth)
    import random; random.seed(7)
    for _ in range(80):
        rx = random.randint(0, W); ry = random.randint(0, hero_h)
        rs = random.randint(1, 3)
        gc = random.randint(35, 65)
        d.ellipse([rx-rs, ry-rs, rx+rs, ry+rs], fill=(gc, gc+15, gc+35))
    # Large soft glow circles
    for cx2, cy2, cr, cl in [(W-180, 80, 260, (45,70,115)),
                              (200,   480, 200, (22,38,68)),
                              (W//2,  300, 400, (30,52,90))]:
        d.ellipse([cx2-cr, cy2-cr, cx2+cr, cy2+cr], fill=cl)

    nav_bar(img, d)

    # ── Tagline pill ──────────────────────────────────────────
    pill_w = 320
    rr(d, W//2-pill_w//2, 86, pill_w, 34, fill=(45, 68, 110), r=17)
    tc(d, '🚀  AI 기반 버티컬 광고 자동화 플랫폼', W//2, 94, 13, col=ORANGE)

    # ── Main headline ─────────────────────────────────────────
    tc(d, '버티컬 매체 광고,', W//2, 140, 58, col=WHITE, bold=True)
    tc(d, '이제 직접 집행하세요', W//2, 207, 58, col=ORANGE, bold=True)

    # ── Subtitle ──────────────────────────────────────────────
    tc(d, '맘카페, 인벤 등 틈새 매체에 AI 기반으로 광고를 집행하는 올인원 셀프서브 플랫폼', W//2, 286, 16, col=(175, 200, 238))
    tc(d, '소재 업로드 → 매체 선택 → 자동 집행. 대행사 없이 직접, 더 빠르게.', W//2, 314, 16, col=(145, 172, 215))

    # ── CTA buttons ───────────────────────────────────────────
    btn(d, W//2-212, 362, 210, 54, '지금 시작하기  →', sz=17, r=27)
    btn_ghost(d, W//2+16, 362, 176, 54, '플랫폼 둘러보기', sz=15, r=27)

    # ── Stats row ─────────────────────────────────────────────
    stats = [('500+', '파트너 매체'), ('2.4M+', '월 도달 UV'), ('380 %', '평균 ROAS')]
    sx = W//2 - 320
    for val, lbl in stats:
        tc(d, val, sx, 442, 26, col=ORANGE, bold=True)
        tc(d, lbl, sx, 476, 13, col=(160, 185, 225))
        if sx < W//2 + 200:
            d.line([(sx+120, 450), (sx+120, 490)], fill=(55, 80, 120), width=1)
        sx += 320

    # ── Partner badges ────────────────────────────────────────
    tc(d, '국내 대표 버티컬 매체와 함께합니다', W//2, hero_h+20, 15, col=TEXT2)
    partners = [('맘카페', ORANGE_L, ORANGE), ('인벤', NAVY_L, NAVY_MID),
                ('뽐뿌', NAVY_L, NAVY_MID), ('클리앙', NAVY_L, NAVY_MID),
                ('베이비뉴스', ORANGE_L, ORANGE), ('82cook', NAVY_L, NAVY_MID),
                ('루리웹', NAVY_L, NAVY_MID)]
    bx = W//2 - 520
    by = hero_h + 50
    for pname, pbg, ptc in partners:
        pw2 = tw(d, pname, 13, bold=True) + 34
        rr(d, bx, by, pw2, 38, fill=pbg, ol=BORDER, r=19)
        tc(d, pname, bx+pw2//2, by+9, 13, col=ptc, bold=True)
        bx += pw2 + 14

    # ── How it works ──────────────────────────────────────────
    FLOW_Y = hero_h + 112
    rr(d, 40, FLOW_Y, W-80, 228, fill=CARD, ol=BORDER, r=16)
    tc(d, '3단계로 광고를 시작하세요', W//2, FLOW_Y+18, 18, col=TEXT, bold=True)

    flow_steps = [
        ('01', '매체 선택',    '맘카페·인벤 등 원하는\n버티컬 매체를 고르세요',       ORANGE),
        ('02', '소재 업로드',  'AI가 매체 사이즈에 맞게\n자동 최적화해드립니다',       NAVY),
        ('03', '캠페인 집행',  '실시간 성과 추이를\n모니터링하며 최적화',              SUCCESS),
    ]
    fx = W//2 - 400
    for i, (num, title, desc, col_s) in enumerate(flow_steps):
        d.ellipse([fx-36, FLOW_Y+60, fx+36, FLOW_Y+132], fill=col_s)
        tc(d, num, fx, FLOW_Y+86, 20, col=WHITE, bold=True)
        tc(d, title, fx, FLOW_Y+146, 16, col=TEXT, bold=True)
        for li, line in enumerate(desc.split('\n')):
            tc(d, line, fx, FLOW_Y+170+li*22, 13, col=TEXT2)
        if i < 2:
            ax = fx + 80
            d.line([(ax, FLOW_Y+96), (ax+160, FLOW_Y+96)], fill=BORDER2, width=2)
            d.polygon([(ax+158, FLOW_Y+89),(ax+172, FLOW_Y+96),(ax+158, FLOW_Y+103)],
                      fill=BORDER2)
        fx += 400

    path = str(OUT / 'admix_01_onboarding.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: admix_01_onboarding.png')


# ═══════════════════════════════════════════════════════════════
# SCREEN 02 — 광고주 대시보드
# ═══════════════════════════════════════════════════════════════
def screen_02():
    img = Image.new('RGB', (W, H), BG)
    d   = ImageDraw.Draw(img)

    # Nav
    nav_bar(img, d, '대시보드')
    d = ImageDraw.Draw(img)

    # ── Page header ───────────────────────────────────────────
    MX = 48; MY = 80
    t(d, '안녕하세요, 재우님 👋', MX, MY, 22, col=TEXT, bold=True)
    t(d, '오늘 캠페인 현황을 확인하세요', MX, MY+34, 14, col=TEXT2)

    # ── KPI Cards (4개) ───────────────────────────────────────
    KW  = (W - MX*2 - 36) // 4
    KH  = 108
    KY  = MY + 78
    kpis = [
        ('총 노출수',    '2,481,300',  '12.4 %', True,  ORANGE),
        ('총 클릭수',    '48,204',     '8.1 %',  True,  NAVY_MID),
        ('전환율',       '3.82 %',     '0.5 %p', True,  SUCCESS),
        ('집행 예산',    '₩32.9M',     '4.2 %',  False, PURPLE),
    ]
    for i, (lbl, val, chg, up, acc) in enumerate(kpis):
        kpi_card(d, MX + i*(KW+12), KY, KW, KH, lbl, val, chg, up, acc)

    # ── Chart row ─────────────────────────────────────────────
    CH_Y = KY + KH + 20
    CH_H = 220
    CW_L = int((W - MX*2 - 20) * 0.62)
    CW_R = W - MX*2 - 20 - CW_L

    data_clicks = [28400, 32100, 35800, 41200, 44800, 46100, 48204]
    area_chart(img, d, MX, CH_Y, CW_L, CH_H, data_clicks,
               col=ORANGE, title='일별 클릭수 추이 (최근 7일)')
    d = ImageDraw.Draw(img)

    # Spend bar chart
    bar_data = [('맘카페', 18600000), ('인벤', 8300000), ('클리앙', 4200000), ('뽐뿌', 1800000)]
    bar_chart_h(d, MX+CW_L+20, CH_Y, CW_R, CH_H, bar_data, col=ORANGE, title='매체별 예산 집행')

    # ── Campaign Cards ────────────────────────────────────────
    CAM_Y = CH_Y + CH_H + 20
    t(d, '진행 중인 캠페인', MX, CAM_Y, 17, col=TEXT, bold=True)
    btn(d, W-MX-150, CAM_Y-4, 146, 36, '+ 새 캠페인', sz=13, r=18)

    campaigns = [
        ('맘카페 유아식품 캠페인',    '집행중',  '₩8.4M / ₩12M',  '노출 1.24M  클릭 18.3K',  72, ORANGE),
        ('인벤 게이밍 디바이스 광고', '집행중',  '₩5.2M / ₩8M',   '노출 820K   클릭 12.1K',  53, SUCCESS),
        ('클리앙 테크 제품',          '일시정지', '₩2.8M / ₩5M',   '노출 460K   클릭 6.8K',   56, WARN),
        ('+ 새 캠페인 만들기',        '',        '',               '',                          0,  None),
    ]
    CARD_W = (W - MX*2 - 36) // 4
    CARD_H = int(H - CAM_Y - 56)
    for ci, (name, status, budget, metrics, pct, acc) in enumerate(campaigns):
        cx3 = MX + ci*(CARD_W+12)
        cy3 = CAM_Y + 36

        if ci == 3:  # "New campaign" card
            rr(d, cx3, cy3, CARD_W, CARD_H, ol=BORDER, r=12, lw=2)
            d.rounded_rectangle([cx3, cy3, cx3+CARD_W, cy3+CARD_H],
                                 radius=12, outline=BORDER, width=2)
            tc(d, '+', cx3+CARD_W//2, cy3+CARD_H//2-36, 40, col=BORDER2, bold=True)
            tc(d, '새 캠페인 시작', cx3+CARD_W//2, cy3+CARD_H//2+12, 14, col=TEXT3)
            continue

        rr(d, cx3, cy3, CARD_W, CARD_H, fill=CARD, ol=BORDER, r=12)
        # Color header strip
        rr(d, cx3, cy3, CARD_W, 6, fill=acc, r=3)
        # Status badge
        stat_cfg = {
            '집행중':  (SUCCL,  SUCCESS),
            '일시정지':(WARNL,  WARN),
            '완료':    (NAVY_L, NAVY_MID),
        }
        sbg, stc2 = stat_cfg.get(status, (NAVY_L, NAVY_MID))
        rr(d, cx3+14, cy3+20, tw(d,status,11)+16, 22, fill=sbg, r=11)
        t(d, status, cx3+22, cy3+24, 11, col=stc2, bold=True)

        t(d, name, cx3+14, cy3+54, 14, col=TEXT, bold=True)
        t(d, metrics, cx3+14, cy3+78, 12, col=TEXT2)
        t(d, '예산', cx3+14, cy3+CARD_H-84, 11, col=TEXT3)
        t(d, budget, cx3+14, cy3+CARD_H-66, 13, col=TEXT, bold=True)

        # Progress bar
        rr(d, cx3+14, cy3+CARD_H-38, CARD_W-28, 8, fill=(235,238,248), r=4)
        if pct > 0:
            rr(d, cx3+14, cy3+CARD_H-38, int((CARD_W-28)*pct/100), 8, fill=acc, r=4)
        t(d, f'{pct}%', cx3+CARD_W-42, cy3+CARD_H-42, 11, col=TEXT3)

    path = str(OUT / 'admix_02_dashboard.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: admix_02_dashboard.png')


# ═══════════════════════════════════════════════════════════════
# SCREEN 03 — 캠페인 생성 마법사 Step1: 매체 선택
# ═══════════════════════════════════════════════════════════════
def screen_03():
    img = Image.new('RGB', (W, H), BG)
    d   = ImageDraw.Draw(img)
    nav_bar(img, d, '캠페인')
    d = ImageDraw.Draw(img)

    MX = 48

    # ── Wizard header (navy band) ─────────────────────────────
    WIZ_H = 100
    wiz_bg = grad_v(W, WIZ_H+64, NAVY, NAVY2)
    img.paste(wiz_bg, (0, 64))
    d = ImageDraw.Draw(img)

    tc(d, '캠페인 만들기', W//2, 76, 18, col=WHITE, bold=True)

    # Step bar inside wizard header
    steps_lbl = ['매체 선택', '소재 업로드', '리뷰 & 집행']
    S_Y = 104; SW = 500
    for i, slbl in enumerate(steps_lbl):
        sx = W//2 - SW//2 + i*(SW//2)
        done = i == 0; cur = i == 0
        fill_s = SUCCESS if done else (ORANGE if cur else (80, 100, 145))
        d.ellipse([sx-18, S_Y-18, sx+18, S_Y+18], fill=fill_s)
        mark = '1' if done else str(i+1)
        tc(d, mark, sx, S_Y-8, 14, col=WHITE, bold=True)
        tc(d, slbl, sx, S_Y+24, 12, col=WHITE if cur else (160,185,225), bold=cur)
        if i < 2:
            lc = SUCCESS if done else (80, 105, 150)
            d.line([(sx+18, S_Y), (sx+SW//2-18, S_Y)], fill=lc, width=2)

    # Body starts below wizard header
    BODY_Y = 64 + WIZ_H + 10

    # ── Filter chips + search ─────────────────────────────────
    rr(d, MX, BODY_Y, W-MX*2, 52, fill=CARD, ol=BORDER, r=10)
    # Search
    rr(d, MX+16, BODY_Y+10, 260, 32, fill=BG, ol=BORDER, r=16)
    t(d, '🔍  매체 검색...', MX+32, BODY_Y+17, 13, col=TEXT3)
    # Chips
    cats2 = [('전체', True), ('육아/맘', False), ('게임', False),
             ('IT/테크', False), ('생활정보', False), ('뷰티', False), ('금융', False)]
    chip_x = MX + 300
    for clbl, csel in cats2:
        cw2 = tw(d, clbl, 12) + 24
        fill_c = ORANGE if csel else (BG)
        ol_c   = ORANGE if csel else BORDER
        rr(d, chip_x, BODY_Y+11, cw2, 30, fill=fill_c, ol=ol_c, r=15)
        tc(d, clbl, chip_x+cw2//2, BODY_Y+17, 12,
           col=WHITE if csel else TEXT2, bold=csel)
        chip_x += cw2 + 10

    # ── Media cards grid (LEFT 2/3) ───────────────────────────
    GRID_Y = BODY_Y + 64
    GRID_W = int((W - MX*2) * 0.64)
    GRID_H = H - GRID_Y - 20
    COLS   = 3
    GAP    = 14
    MCW    = (GRID_W - GAP*(COLS-1)) // COLS
    MCH    = (GRID_H - GAP) // 2

    medias_cards = [
        ('맘카페',    '육아 · 맘',   '2,400만',  '₩3,200', True,  True,  ORANGE_L, ORANGE),
        ('인벤',      '게임',        '1,820만',  '₩2,800', True,  False, NAVY_L,   NAVY_MID),
        ('뽐뿌',      '생활정보',    '952만',    '₩2,100', False, False, NAVY_L,   NAVY_MID),
        ('클리앙',    'IT / 테크',   '678만',    '₩3,800', False, True,  NAVY_L,   NAVY_MID),
        ('베이비뉴스','육아 · 맘',   '428만',    '₩4,200', True,  True,  ORANGE_L, ORANGE),
        ('루리웹',    '게임',        '542만',    '₩2,600', False, False, NAVY_L,   NAVY_MID),
    ]
    for mi, (mname, mcat, muv, mcpm, msel, mrec, mbg, mtc2) in enumerate(medias_cards):
        col_i = mi % COLS; row_i = mi // COLS
        mx2 = MX + col_i*(MCW+GAP)
        my2 = GRID_Y + row_i*(MCH+GAP)
        border_c = ORANGE if msel else BORDER
        lw2      = 2 if msel else 1
        fill2    = ORANGE_L if msel else CARD
        rr(d, mx2, my2, MCW, MCH, fill=fill2, ol=border_c, lw=lw2, r=12)
        # Logo placeholder circle
        d.ellipse([mx2+20, my2+16, mx2+64, my2+60], fill=mbg)
        tc(d, mname[0], mx2+42, my2+26, 18, col=mtc2, bold=True)
        # Recommended
        if mrec:
            rr(d, mx2+MCW-76, my2+14, 62, 22, fill=WARNL, r=11)
            tc(d, '⭐ 추천', mx2+MCW-45, my2+18, 10, col=WARN)
        # Checkbox
        cb_fill = ORANGE if msel else (235, 238, 248)
        rr(d, mx2+MCW-36, my2+MCH-40, 22, 22, fill=cb_fill, r=5)
        if msel:
            tc(d, '✓', mx2+MCW-25, my2+MCH-38, 12, col=WHITE, bold=True)
        t(d, mname, mx2+76, my2+20, 17, col=TEXT, bold=True)
        t(d, mcat,  mx2+76, my2+46, 12, col=TEXT3)
        t(d, '월 UV',       mx2+20, my2+MCH-62, 11, col=TEXT3)
        t(d, muv,           mx2+20, my2+MCH-44, 14, col=TEXT, bold=True)
        t(d, 'CPM',         mx2+MCW//2, my2+MCH-62, 11, col=TEXT3)
        t(d, mcpm,          mx2+MCW//2, my2+MCH-44, 14, col=TEXT, bold=True)

    # ── Right panel: 예산 배분 ─────────────────────────────────
    RX = MX + GRID_W + 16
    RW = W - RX - MX
    rr(d, RX, GRID_Y, RW, GRID_H, fill=CARD, ol=BORDER, r=12)

    # Header
    rr(d, RX, GRID_Y, RW, 52, fill=NAVY, r=12)
    d.rectangle([RX, GRID_Y+30, RX+RW, GRID_Y+52], fill=NAVY)
    tc(d, '선택 매체 & 예산', RX+RW//2, GRID_Y+15, 14, col=WHITE, bold=True)

    # Selected media
    t(d, '선택 매체 2개', RX+16, GRID_Y+62, 12, col=TEXT3)
    sels = [('맘카페', ORANGE, 70), ('베이비뉴스', SUCCESS, 30)]
    sy3 = GRID_Y+84
    SBAR_W = RW - 32
    for sname, sc, spct in sels:
        rr(d, RX+16, sy3, tw(d,sname,12,True)+20, 24, fill=sc, r=12)
        tc(d, sname, RX+16+(tw(d,sname,12,True)+20)//2, sy3+5, 12, col=WHITE, bold=True)
        sy3 += 34

    d.line([(RX+16, sy3+8), (RX+RW-16, sy3+8)], fill=BORDER, width=1)
    sy3 += 22

    # Budget sliders
    t(d, '총 예산', RX+16, sy3, 12, col=TEXT3)
    t(d, '₩8,400,000', RX+16, sy3+18, 18, col=TEXT, bold=True)
    sy3 += 50

    for sname, sc, spct in sels:
        t(d, sname, RX+16, sy3, 12, col=TEXT)
        tc(d, f'{spct}%', RX+RW-16, sy3, 12, col=TEXT3)
        sy3 += 20
        rr(d, RX+16, sy3, SBAR_W, 8, fill=(235,238,248), r=4)
        rr(d, RX+16, sy3, int(SBAR_W*spct/100), 8, fill=sc, r=4)
        tx5 = RX+16 + int(SBAR_W*spct/100)
        d.ellipse([tx5-7, sy3-5, tx5+7, sy3+13], fill=sc)
        amt2 = int(8400000*spct/100)
        t(d, f'₩{amt2:,}', RX+16, sy3+14, 11, col=TEXT3)
        sy3 += 44

    d.line([(RX+16, sy3+6), (RX+RW-16, sy3+6)], fill=BORDER, width=1)
    t(d, '예상 도달',   RX+16,     sy3+18, 11, col=TEXT3)
    t(d, '1,280만',     RX+16,     sy3+34, 16, col=TEXT, bold=True)
    t(d, '예상 CPM',    RX+RW//2,  sy3+18, 11, col=TEXT3)
    t(d, '₩3,100',      RX+RW//2,  sy3+34, 16, col=TEXT, bold=True)

    # CTA
    btn_y4 = GRID_Y + GRID_H - 56
    btn(d, RX+12, btn_y4, RW-24, 44, '다음: 소재 업로드  →', sz=14, r=22)

    path = str(OUT / 'admix_03_media_select.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: admix_03_media_select.png')


# ═══════════════════════════════════════════════════════════════
# SCREEN 04 — 소재 업로드 & 사이즈 편집
# ═══════════════════════════════════════════════════════════════
def screen_04():
    img = Image.new('RGB', (W, H), BG)
    d   = ImageDraw.Draw(img)
    nav_bar(img, d, '소재')
    d = ImageDraw.Draw(img)

    MX = 0; BODY_Y = 64

    # ── AI Banner (orange gradient) ────────────────────────────
    ai_h = 52
    ai_g = grad_h(W, ai_h, ORANGE2, ORANGE)
    img.paste(ai_g, (0, BODY_Y))
    d = ImageDraw.Draw(img)
    t(d, '✨  AI 후킹 문구 추천', 32, BODY_Y+15, 14, col=WHITE, bold=True)
    ai_suggestions = ['"여름 특가! 아기사랑 분유 10% 할인"', '"지금 바로 시작하는 건강한 육아"']
    t(d, f'  {ai_suggestions[0]}', 250, BODY_Y+16, 13, col=(255,235,220))
    rr(d, W-200, BODY_Y+11, 160, 30, fill=(230,80,20), r=15)
    tc(d, '✨ 문구 바꾸기', W-200+80, BODY_Y+17, 12, col=WHITE, bold=True)

    # ── 3-panel layout ────────────────────────────────────────
    PY   = BODY_Y + ai_h + 8
    PH   = H - PY - 12
    LP_W = 300           # Left: source
    RP_W = 320           # Right: controls
    CP_W = W - LP_W - RP_W  # Center: previews

    # ── LEFT panel: 원본 소재 ─────────────────────────────────
    rr(d, 0, PY, LP_W, PH, fill=NAVY3, r=0)
    d.rectangle([0, PY, LP_W, PY+PH], fill=NAVY3)
    t(d, '원본 소재', 20, PY+14, 13, col=(160,185,225), bold=True)
    d.line([(0, PY+40), (LP_W, PY+40)], fill=(35,55,90), width=1)

    # Simulated uploaded image (dark placeholder with orange label strip)
    IMG_Y = PY + 50; IMG_H = 200
    rr(d, 16, IMG_Y, LP_W-32, IMG_H, fill=(35, 55, 90), r=8)
    tc(d, '🖼', LP_W//2, IMG_Y+60, 40, col=(60,90,140))
    tc(d, '분유_메인이미지.jpg', LP_W//2, IMG_Y+130, 12, col=(130,160,200))
    tc(d, '1920 × 1080  ·  2.4 MB',    LP_W//2, IMG_Y+152, 11, col=(90,120,165))
    # Mini controls
    rr(d, 16, IMG_Y+IMG_H+12, 130, 30, fill=(50,78,125), r=15)
    tc(d, '이미지 교체', 81, IMG_Y+IMG_H+19, 12, col=(180,205,240))
    rr(d, 154, IMG_Y+IMG_H+12, 130, 30, ol=(80,110,160), lw=1, r=15)
    tc(d, '삭제', 219, IMG_Y+IMG_H+19, 12, col=(160,185,225))

    # Crop options
    t(d, '크롭 방식', 20, IMG_Y+IMG_H+54, 12, col=(140,168,210))
    for ci2, (clbl2, csel2) in enumerate([('스마트 크롭', True), ('중앙', False), ('상단', False)]):
        cw3 = tw(d, clbl2, 11) + 16
        rr(d, 20+ci2*90, IMG_Y+IMG_H+70, cw3, 26, fill=ORANGE if csel2 else (35,55,90), r=13)
        tc(d, clbl2, 20+ci2*90+cw3//2, IMG_Y+IMG_H+76, 11, col=WHITE if csel2 else (130,160,200))

    # File list
    t(d, '업로드 파일', 20, PY+PH-160, 12, col=(140,168,210), bold=True)
    for fi, (fname2, fsize) in enumerate([('분유_메인.jpg','2.4 MB'), ('제품_화이트.png','1.1 MB')]):
        fy2 = PY+PH-138+fi*52
        rr(d, 16, fy2, LP_W-32, 44, fill=(35,55,90), r=6)
        d.ellipse([24, fy2+10, 46, fy2+34], fill=(50,80,130))
        t(d, '🖼', 27, fy2+10, 14, col=(140,168,210))
        t(d, fname2, 56, fy2+10, 12, col=(200,215,240))
        t(d, fsize,  56, fy2+26, 11, col=(100,130,175))

    # ── CENTER: size preview cards ─────────────────────────────
    CP_X = LP_W
    d.rectangle([CP_X, PY, CP_X+CP_W, PY+PH], fill=BG)
    t(d, '매체별 사이즈 미리보기', CP_X+20, PY+14, 13, col=TEXT2, bold=True)
    rr(d, CP_X+CP_W-164, PY+10, 144, 28, fill=ORANGE_L, ol=ORANGE, r=14, lw=1)
    tc(d, '선택: 300×250  ✓', CP_X+CP_W-164+72, PY+16, 11, col=ORANGE, bold=True)
    d.line([(CP_X, PY+44), (CP_X+CP_W, PY+44)], fill=BORDER, width=1)

    size_previews = [
        ('728 × 90',   728, 90,  'leaderboard',  False),
        ('300 × 250',  300, 250, 'medium rect',  True),
        ('320 × 480',  320, 480, 'half page',    False),
        ('160 × 600',  160, 600, 'skyscraper',   False),
        ('320 × 100',  320, 100, 'mobile banner',False),
    ]
    PREV_Y = PY + 54; COL_GAP2 = 16
    PC1_W  = CP_W//2 - COL_GAP2
    px_col = [CP_X + 16, CP_X + CP_W//2 + 8]
    py_row = [PREV_Y, PREV_Y, PREV_Y]
    cur_row = [PREV_Y, PREV_Y]

    for si, (slbl, sw2, sh2, ssub, ssel) in enumerate(size_previews):
        col_i2  = si % 2
        card_x2 = px_col[col_i2]
        card_y2 = cur_row[col_i2]
        # Proportional preview (max 120px tall, 200px wide)
        max_pw = PC1_W - 32; max_ph = 110
        ratio  = min(max_pw/sw2, max_ph/sh2)
        disp_w = max(int(sw2*ratio), 20)
        disp_h = max(int(sh2*ratio), 10)
        card_h2 = disp_h + 64

        border_s = ORANGE if ssel else BORDER
        bg_s     = ORANGE_L if ssel else CARD
        rr(d, card_x2, card_y2, PC1_W, card_h2, fill=bg_s, ol=border_s,
           lw=2 if ssel else 1, r=10)
        # Preview box
        preview_x = card_x2 + (PC1_W - disp_w) // 2
        preview_y = card_y2 + 8
        rr(d, preview_x, preview_y, disp_w, disp_h, fill=(220,225,238), ol=BORDER2, r=4)
        # Mini banner content
        rr(d, preview_x+4, preview_y+4, disp_w//3, disp_h-8, fill=NAVY_L, r=2)
        t(d, '광고', preview_x+8, preview_y+disp_h//2-8, max(8, int(12*ratio)), col=NAVY_MID)
        rr(d, preview_x+disp_w-int(40*ratio), preview_y+4,
           int(36*ratio), disp_h-8, fill=ORANGE, r=2)

        # Labels
        tc(d, slbl, card_x2+PC1_W//2, card_y2+card_h2-42, 12, col=TEXT, bold=ssel)
        tc(d, ssub, card_x2+PC1_W//2, card_y2+card_h2-22, 10, col=TEXT3)
        cur_row[col_i2] += card_h2 + 10

    # ── RIGHT panel: 편집 컨트롤 ─────────────────────────────
    RP_X = CP_X + CP_W
    rr(d, RP_X, PY, RP_W, PH, fill=CARD, ol=BORDER, r=0)
    d.rectangle([RP_X, PY, RP_X+RP_W, PY+PH], fill=CARD)
    d.line([(RP_X, PY), (RP_X, PY+PH)], fill=BORDER, width=1)
    t(d, '편집 옵션', RP_X+18, PY+14, 14, col=TEXT, bold=True)
    d.line([(RP_X, PY+44), (RP_X+RP_W, PY+44)], fill=BORDER, width=1)

    ry2 = PY + 58
    for lbl3, val3 in [('선택 사이즈','300 × 250 px'),('파일 형식','PNG'),('용량 제한','150 KB')]:
        t(d, lbl3, RP_X+18, ry2, 11, col=TEXT3)
        rr(d, RP_X+18, ry2+18, RP_W-36, 32, fill=BG, ol=BORDER, r=6)
        t(d, val3, RP_X+30, ry2+25, 13, col=TEXT)
        ry2 += 62

    # Position sliders
    t(d, '위치 조정', RP_X+18, ry2, 12, col=TEXT, bold=True)
    ry2 += 20
    SLIDER_W = RP_W - 36
    for sname2, sval in [('X 오프셋', 60), ('Y 오프셋', 35), ('스케일', 78)]:
        t(d, sname2, RP_X+18, ry2+4, 11, col=TEXT3)
        rr(d, RP_X+18, ry2+20, SLIDER_W, 8, fill=(235,238,248), r=4)
        rr(d, RP_X+18, ry2+20, int(SLIDER_W*sval/100), 8, fill=ORANGE, r=4)
        tx6 = RP_X+18 + int(SLIDER_W*sval/100)
        d.ellipse([tx6-7, ry2+16, tx6+7, ry2+28], fill=ORANGE)
        tc(d, f'{sval}', RP_X+RW_right-20 if False else RP_X+RP_W-26, ry2+2, 11, col=TEXT3)
        ry2 += 44

    # Text overlay
    d.line([(RP_X+18, ry2+4), (RP_X+RP_W-18, ry2+4)], fill=BORDER, width=1)
    ry2 += 16
    t(d, '텍스트 오버레이', RP_X+18, ry2, 12, col=TEXT, bold=True)
    tg_x = RP_X+RP_W-48
    rr(d, tg_x, ry2-2, 38, 20, fill=ORANGE, r=10)
    d.ellipse([tg_x+18, ry2, tg_x+34, ry2+16], fill=WHITE)
    ry2 += 30
    t(d, '"여름 특가! 아기사랑 분유 10% 할인"', RP_X+18, ry2, 11, col=TEXT2)
    rr(d, RP_X+18, ry2+22, SLIDER_W, 28, fill=BG, ol=BORDER, r=6)
    t(d, '텍스트 직접 입력...', RP_X+28, ry2+28, 11, col=TEXT3)

    ry2 += 66
    t(d, 'AI 추천 문구', RP_X+18, ry2, 12, col=TEXT, bold=True)
    ry2 += 20
    ai_phrses = ['"여름 특가! 아기사랑 분유 10% 할인"', '"지금 바로 시작하는 건강한 육아"']
    for ai_p in ai_phrses:
        rr(d, RP_X+18, ry2, SLIDER_W, 36, fill=ORANGE_L if '10%' in ai_p else BG,
           ol=ORANGE if '10%' in ai_p else BORDER, r=6)
        t(d, ai_p, RP_X+26, ry2+9, 10, col=ORANGE if '10%' in ai_p else TEXT2)
        ry2 += 44

    # Bottom CTA
    btn_bot = PY + PH - 56
    d.line([(RP_X, btn_bot), (RP_X+RP_W, btn_bot)], fill=BORDER, width=1)
    btn(d, RP_X+12, btn_bot+10, RP_W-24, 38, '리뷰로 이동  →', sz=14, r=19)

    path = str(OUT / 'admix_04_creative_editor.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: admix_04_creative_editor.png')


# ═══════════════════════════════════════════════════════════════
# SCREEN 05 — 캠페인 집행 확인 & 리뷰
# ═══════════════════════════════════════════════════════════════
def screen_05():
    img = Image.new('RGB', (W, H), BG)
    d   = ImageDraw.Draw(img)
    nav_bar(img, d, '캠페인')
    d = ImageDraw.Draw(img)

    # Wizard nav band (dark navy)
    wiz_g = grad_v(W, 60, NAVY, NAVY2)
    img.paste(wiz_g, (0, 64))
    d = ImageDraw.Draw(img)
    tc(d, '캠페인 만들기', W//2, 76, 16, col=WHITE, bold=True)
    steps_l2 = ['매체 선택', '소재 업로드', '리뷰 & 집행']
    for i, slbl2 in enumerate(steps_l2):
        sx2 = W//2 - 240 + i*240
        done2 = i < 2; cur2 = i == 2
        fc2 = SUCCESS if done2 else ORANGE
        d.ellipse([sx2-16, 100, sx2+16, 132], fill=fc2)
        tc(d, '✓' if done2 else '3', sx2, 108, 14, col=WHITE, bold=True)
        tc(d, slbl2, sx2, 136, 11, col=WHITE if cur2 else (170,195,230), bold=cur2)
        if i < 2:
            lc3 = SUCCESS
            d.line([(sx2+16, 116), (sx2+224, 116)], fill=lc3, width=2)

    MX = 48; BODY_Y = 140

    # ── Alert banner ─────────────────────────────────────────
    rr(d, MX, BODY_Y, W-MX*2, 48, fill=SUCCL, ol=SUCCESS, r=8)
    t(d, '소재 준비 완료  —  아래에서 최종 확인 후 캠페인을 시작하세요 🎉', MX+20, BODY_Y+14, 14, col=SUCCESS, bold=True)

    # ── 2-column layout ────────────────────────────────────────
    SPLIT_Y = BODY_Y + 64
    SPLIT_H = H - SPLIT_Y - 72
    LCW2 = int((W - MX*2) * 0.58)
    RCX2 = MX + LCW2 + 20
    RCW2 = W - RCX2 - MX

    # ── LEFT: summary ─────────────────────────────────────────
    rr(d, MX, SPLIT_Y, LCW2, SPLIT_H, fill=CARD, ol=BORDER, r=12)

    # Campaign name header
    rr(d, MX, SPLIT_Y, LCW2, 52, fill=NAVY, r=12)
    d.rectangle([MX, SPLIT_Y+30, MX+LCW2, SPLIT_Y+52], fill=NAVY)
    t(d, '여름 신제품 맘카페 광고', MX+20, SPLIT_Y+15, 16, col=WHITE, bold=True)

    SEC_Y = SPLIT_Y + 62; SEC_PAD = 20

    def summary_section(title, rows_data, sy):
        t(d, title, MX+SEC_PAD, sy, 13, col=TEXT3, bold=True)
        d.line([(MX+SEC_PAD, sy+20), (MX+LCW2-SEC_PAD, sy+20)], fill=BORDER, width=1)
        iy = sy + 28
        for k, v, extra in rows_data:
            t(d, k, MX+SEC_PAD, iy, 12, col=TEXT3)
            t(d, v, MX+LCW2//2, iy, 14, col=TEXT, bold=True)
            if extra:
                t(d, extra, MX+LCW2*3//4, iy, 11, col=SUCCESS)
            iy += 34
        return iy + 8

    # Media section
    SEC_Y = summary_section('선택 매체', [
        ('매체 1', '맘카페', '육아/맘  · 월 UV 2,400만'),
        ('매체 2', '베이비뉴스', '육아/맘  · 월 UV 428만'),
    ], SEC_Y)

    # Creative section
    t(d, '소재 (3개 사이즈)', MX+SEC_PAD, SEC_Y, 13, col=TEXT3, bold=True)
    d.line([(MX+SEC_PAD, SEC_Y+20), (MX+LCW2-SEC_PAD, SEC_Y+20)], fill=BORDER, width=1)
    thumb_sizes2 = [('728×90', 728, 90), ('300×250', 300, 250), ('320×100', 320, 100)]
    thx2 = MX+SEC_PAD; thy2 = SEC_Y+28
    SCALE2 = 0.12
    for tl2, tw3, th3 in thumb_sizes2:
        dw3 = max(int(tw3*SCALE2), 30); dh3 = max(int(th3*SCALE2), 12)
        rr(d, thx2, thy2, dw3, dh3, fill=(220,225,238), ol=BORDER2, r=3)
        rr(d, thx2+2, thy2+2, dw3//3, dh3-4, fill=NAVY_L, r=2)
        rr(d, thx2+dw3-int(24*SCALE2), thy2+2, int(22*SCALE2)+8, dh3-4, fill=ORANGE, r=2)
        t(d, tl2, thx2, thy2+dh3+6, 10, col=TEXT3)
        thx2 += dw3 + 40
    SEC_Y = thy2 + max(dh3 for _, tw3, th3 in thumb_sizes2
                       for dh3 in [max(int(th3*SCALE2), 12)]) + 34

    SEC_Y = summary_section('예산 & 일정', [
        ('총 예산',    '₩8,400,000',   ''),
        ('집행 기간',  '05/01 – 05/31', '31일'),
        ('일 예산',    '₩271,000 /일',  ''),
    ], SEC_Y)

    # ── RIGHT: 예상 성과 ──────────────────────────────────────
    rr(d, RCX2, SPLIT_Y, RCW2, SPLIT_H, fill=CARD, ol=BORDER, r=12)

    rr(d, RCX2, SPLIT_Y, RCW2, 52, fill=NAVY, r=12)
    d.rectangle([RCX2, SPLIT_Y+30, RCX2+RCW2, SPLIT_Y+52], fill=NAVY)
    tc(d, '예상 캠페인 성과', RCX2+RCW2//2, SPLIT_Y+15, 15, col=WHITE, bold=True)

    perf_metrics = [
        ('예상 노출수', '4,800,000', ORANGE),
        ('예상 클릭수', '96,000',    SUCCESS),
        ('예상 전환',   '1,440',     PURPLE),
        ('예상 ROAS',   '380 %',     WARN),
    ]
    pm_y = SPLIT_Y + 64
    for i, (plbl, pval, pc2) in enumerate(perf_metrics):
        pry = pm_y + i * 66
        rr(d, RCX2+16, pry, RCW2-32, 58, fill=BG, ol=BORDER, r=8)
        rr(d, RCX2+16, pry, 4, 58, fill=pc2, r=2)
        t(d, plbl, RCX2+32, pry+10, 11, col=TEXT3)
        t(d, pval, RCX2+32, pry+28, 20, col=TEXT, bold=True)

    # Mini bar chart below metrics
    CHART_Y = pm_y + len(perf_metrics)*66 + 16
    CHART_H = SPLIT_H - (CHART_Y - SPLIT_Y) - 16
    if CHART_H > 80:
        t(d, '매체별 예상 클릭수', RCX2+16, CHART_Y, 12, col=TEXT3, bold=True)
        bar_items2 = [('맘카페', 78000), ('베이비뉴스', 18000)]
        BAR_MAX = 78000; BAR_W_FULL = RCW2 - 100 - 32
        by5 = CHART_Y + 22
        for bname2, bval2 in bar_items2:
            t(d, bname2, RCX2+20, by5+5, 11, col=TEXT3)
            bw5 = int(BAR_W_FULL * bval2 / BAR_MAX)
            rr(d, RCX2+100, by5, bw5, 26, fill=ORANGE, r=6)
            t(d, f'{bval2:,}', RCX2+100+bw5+8, by5+5, 11, col=TEXT3)
            by5 += 40

    # ── Big CTA button ────────────────────────────────────────
    CTA_Y2 = H - 66
    d.rectangle([0, CTA_Y2-10, W, H], fill=WHITE)
    d.line([(0, CTA_Y2-10), (W, CTA_Y2-10)], fill=BORDER, width=1)

    # Disclaimer
    t(d, '* 예상 성과는 과거 캠페인 데이터 기반 추정치이며 실제 결과와 다를 수 있습니다.',
      MX, CTA_Y2+4, 11, col=TEXT3)

    CTA_W = 280; CTA_H = 48
    CTA_X = W - MX - CTA_W
    btn(d, CTA_X, CTA_Y2-2, CTA_W, CTA_H,
        '🚀  캠페인 시작하기', sz=16, r=24)
    rr(d, CTA_X - 150, CTA_Y2-2, 136, CTA_H, ol=BORDER2, r=24)
    tc(d, '← 이전으로', CTA_X-150+68, CTA_Y2+14, 13, col=TEXT2)

    path = str(OUT / 'admix_05_review.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: admix_05_review.png')


# ── FIX placeholder variable name ─────────────────────────────
RW_right = 320   # global fallback (used in screen_04)

if __name__ == '__main__':
    print('AdMix Platform UI 생성 시작 (5 screens, 1440x900)')
    screen_01()
    screen_02()
    screen_03()
    screen_04()
    screen_05()
    print()
    expected = [
        'admix_01_onboarding.png', 'admix_02_dashboard.png',
        'admix_03_media_select.png', 'admix_04_creative_editor.png',
        'admix_05_review.png',
    ]
    all_ok = True
    for fname in expected:
        fp = OUT / fname
        if os.path.exists(str(fp)):
            print(f'  {fname}: {fp.stat().st_size // 1024} KB')
        else:
            print(f'  MISSING: {fname}')
            all_ok = False
    if all_ok:
        print(f'\n완료! 저장: {OUT}')
    else:
        import sys; sys.exit(1)
