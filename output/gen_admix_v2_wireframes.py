# -*- coding: utf-8 -*-
"""AdMix MVP 와이어프레임 v2 — 5개 화면 (1280x800)
01_dashboard.png         / 02_new_campaign.png / 03_media_selection.png
04_creative_editor.png   / 05_contract_flow.png
"""
import sys, io, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('C:/Agent/pepper/output/admix_wireframes')
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1280, 800

C = {
    'white':    (255, 255, 255),
    'bg':       (249, 250, 251),
    'border':   (229, 231, 235),
    'border2':  (209, 213, 219),
    'text':     (17,  24,  39),
    'text2':    (75,  85,  99),
    'text3':    (156, 163, 175),
    'primary':  (59,  130, 246),
    'priml':    (219, 234, 254),
    'success':  (16,  185, 129),
    'succl':    (209, 250, 229),
    'warn':     (245, 158, 11),
    'warnl':    (254, 243, 199),
    'danger':   (239, 68,  68),
    'dangl':    (254, 226, 226),
    'g100':     (243, 244, 246),
    'g200':     (229, 231, 235),
    'g300':     (209, 213, 219),
    'g400':     (156, 163, 175),
    'g500':     (107, 114, 128),
    'g600':     (75,  85,  99),
    'g700':     (55,  65,  81),
    'g800':     (31,  41,  55),
    'g900':     (17,  24,  39),
    'nav':      (15,  23,  42),
}
WHITE = (255, 255, 255)

_font_cache = {}
def fnt(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        fp = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
        try:
            _font_cache[key] = ImageFont.truetype(fp, size)
        except Exception:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]

def new_img():
    img = Image.new('RGB', (W, H), C['white'])
    return img, ImageDraw.Draw(img)

def rr(d, x, y, w, h, fill=None, ol=None, lw=1, r=6):
    d.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=fill, outline=ol, width=lw)

def t(d, s, x, y, f, col=None):
    d.text((x, y), str(s), font=f, fill=col or C['text'])

def tc(d, s, cx, y, f, col=None):
    bb = d.textbbox((0, 0), str(s), font=f)
    w = bb[2] - bb[0]
    d.text((cx - w // 2, y), str(s), font=f, fill=col or C['text'])

def pill(d, x, y, label, sz=10, fill=None, col=None, r=10):
    f = fnt(sz)
    bb = d.textbbox((0, 0), label, font=f)
    pw = bb[2]-bb[0]+16
    ph = bb[3]-bb[0]+10
    rr(d, x, y, pw, ph, fill=fill or C['g200'], r=r)
    t(d, label, x+8, y+5, f, col=col or C['g600'])
    return pw

def status_badge(d, x, y, status):
    cfg = {
        '집행중': (C['success'], C['succl']),
        '완료':   (C['g500'],   C['g200']),
        '대기':   (C['warn'],   C['warnl']),
        '검토중': (C['primary'], C['priml']),
    }
    col, bg = cfg.get(status, (C['g500'], C['g200']))
    f = fnt(11)
    bb = d.textbbox((0,0), status, font=f)
    pw = bb[2]-bb[0]+16
    rr(d, x, y, pw, 22, fill=bg, r=11)
    tc(d, status, x+pw//2, y+4, f, col=col)
    return pw

def nav_bar(d, active='대시보드'):
    d.rectangle([0, 0, W, 52], fill=C['nav'])
    t(d, 'AdMix', 20, 15, fnt(18, bold=True), col=WHITE)
    items = ['대시보드', '캠페인', '매체', '소재', '리포트']
    x = 140
    for item in items:
        is_a = item == active
        t(d, item, x, 17, fnt(13), col=WHITE if is_a else C['g400'])
        if is_a:
            bb = d.textbbox((x, 17), item, font=fnt(13))
            d.rectangle([x, 48, bb[2], 52], fill=C['primary'])
        x += 90
    rr(d, W-108, 12, 88, 28, ol=C['g500'], r=14)
    t(d, '재우  ▾', W-96, 17, fnt(12), col=WHITE)

def sidebar(d, active='대시보드'):
    d.rectangle([0, 52, 200, H], fill=C['g100'])
    d.line([(200, 52), (200, H)], fill=C['border2'], width=1)
    items = [
        '대시보드', '새 캠페인', '매체 관리', '소재 관리',
        '계약 관리', '정산 관리', '리포트', '설정',
    ]
    y = 72
    for item in items:
        is_a = active in item or item in active
        if is_a:
            rr(d, 8, y-4, 184, 32, fill=C['priml'], r=6)
        t(d, item, 40, y, fnt(13, bold=is_a), col=C['primary'] if is_a else C['g600'])
        y += 44

def step_bar(d, active_idx, MX, MY, MW):
    labels = ['캠페인 기본 설정', '매체 선택', '소재 업로드', '계약 확인']
    sw = MW // 4
    for i, label in enumerate(labels):
        sx = MX + i*sw + sw//2
        sy = MY
        done  = i < active_idx
        cur   = i == active_idx
        col_c = C['success'] if done else (C['primary'] if cur else C['g300'])
        d.ellipse([sx-16, sy-16, sx+16, sy+16], fill=col_c, outline=col_c)
        mark = '✓' if done else str(i+1)
        tc(d, mark, sx, sy-8, fnt(13, bold=True), col=WHITE)
        lbl_col = C['primary'] if cur else (C['success'] if done else C['g400'])
        tc(d, label, sx, sy+20, fnt(11), col=lbl_col)
        if i < 3:
            lc = C['success'] if done else C['g200']
            d.line([(sx+16, sy), (sx+sw-16, sy)], fill=lc, width=2)


# ═══════════════════════════════════════════════════════════════
# Screen 01 — 대시보드
# ═══════════════════════════════════════════════════════════════
def screen_01():
    img, d = new_img()
    nav_bar(d, '대시보드')
    sidebar(d, '대시보드')

    MX, MY = 220, 72
    MW = W - MX - 24

    # Title row
    t(d, '대시보드', MX, MY+14, fnt(20, bold=True))
    rr(d, W-174, MY+12, 150, 34, fill=C['primary'], r=6)
    tc(d, '+ 새 캠페인 시작', W-174+75, MY+20, fnt(13, bold=True), col=WHITE)

    # ── KPI cards ──
    kpis = [
        ('활성 캠페인', '7', '이번 달 +2'),
        ('총 예산',     '₩48.2M', '집행 중 ₩32.9M'),
        ('예산 소진율', '68.4 %', '▲ 3.2%p 전월比'),
        ('계약 완료',   '12 건', '이번 달'),
    ]
    cw = (MW - 36) // 4
    for i, (lbl, val, sub) in enumerate(kpis):
        cx = MX + i*(cw+12)
        rr(d, cx, MY+60, cw, 86, fill=WHITE, ol=C['border'], r=8)
        t(d, lbl, cx+14, MY+74, fnt(11), col=C['g500'])
        t(d, val, cx+14, MY+94, fnt(20, bold=True))
        t(d, sub, cx+14, MY+122, fnt(11), col=C['g400'])

    # ── Section header + filter tabs ──
    t(d, '캠페인 목록', MX, MY+164, fnt(15, bold=True))
    tabs = ['전체', '집행중', '대기', '완료']
    tx = MX + 140
    for i, tab in enumerate(tabs):
        is_s = i == 0
        rr(d, tx, MY+162, 58, 26, fill=C['primary'] if is_s else C['g100'], r=13)
        tc(d, tab, tx+29, MY+169, fnt(12), col=WHITE if is_s else C['g500'])
        tx += 66

    # ── Table ──
    TY = MY + 202
    d.rectangle([MX, TY, MX+MW, TY+36], fill=C['g100'])
    d.line([(MX, TY+36), (MX+MW, TY+36)], fill=C['border2'], width=1)
    cols = [('캠페인명', 240), ('매체', 140), ('상태', 90), ('예산', 110), ('소진율', 110), ('집행 기간', 135), ('관리', 70)]
    hx = MX+14
    for cn, cw2 in cols:
        t(d, cn, hx, TY+10, fnt(11, bold=True), col=C['g500'])
        hx += cw2

    rows = [
        ('맘카페 유아식품 캠페인',    '맘카페 · 베이비뉴스', '집행중', '₩8,400,000', 72),
        ('인벤 게이밍 디바이스 광고', '인벤 · 루리웹',       '집행중', '₩5,200,000', 41),
        ('뽐뿌 생활가전 프로모션',    '뽐뿌',                 '대기',   '₩3,600,000',  0),
        ('클리앙 테크 제품 리뷰 광고','클리앙',               '완료',   '₩2,800,000', 100),
        ('맘카페 육아용품 시즌',       '맘카페',               '검토중', '₩6,100,000',  0),
    ]
    periods = ['04/01 – 04/30', '04/10 – 05/09', '05/01 – 05/31', '03/01 – 03/31', '05/15 – 06/14']
    for ri, ((name, media, status, budget, pct), period) in enumerate(zip(rows, periods)):
        ry = TY + 36 + ri*52
        d.rectangle([MX, ry, MX+MW, ry+52], fill=WHITE if ri%2==0 else (250,251,252))
        d.line([(MX, ry+52), (MX+MW, ry+52)], fill=C['border'], width=1)
        rx = MX+14
        t(d, name,   rx, ry+12, fnt(13, bold=True))
        t(d, media,  rx, ry+30, fnt(10), col=C['g400'])
        rx += 240
        rx += 140  # media col skip (already in name)
        status_badge(d, rx, ry+17, status)
        rx += 90
        t(d, budget, rx, ry+20, fnt(12))
        rx += 110
        bw = 72
        rr(d, rx, ry+22, bw, 8, fill=C['g200'], r=4)
        if pct:
            pc = C['success'] if pct==100 else (C['warn'] if pct>70 else C['primary'])
            rr(d, rx, ry+22, int(bw*pct/100), 8, fill=pc, r=4)
        t(d, f'{pct}%', rx, ry+34, fnt(9), col=C['g400'])
        rx += 110
        t(d, period, rx, ry+20, fnt(11), col=C['g500'])
        rx += 135
        rr(d, rx, ry+15, 56, 24, ol=C['border2'], r=4)
        tc(d, '상세보기', rx+28, ry+21, fnt(10), col=C['g500'])

    t(d, '총 5개 캠페인 | 페이지 1 / 1', MX, H-28, fnt(11), col=C['g400'])

    path = str(OUT / '01_dashboard.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: 01_dashboard.png')


# ═══════════════════════════════════════════════════════════════
# Screen 02 — 새 캠페인 생성
# ═══════════════════════════════════════════════════════════════
def screen_02():
    img, d = new_img()
    nav_bar(d, '캠페인')
    sidebar(d, '새 캠페인')

    MX, MY = 220, 72
    MW = W - MX - 24

    t(d, '대시보드  >  새 캠페인 생성', MX, MY+10, fnt(11), col=C['g400'])
    t(d, '새 캠페인 생성', MX, MY+28, fnt(20, bold=True))

    step_bar(d, 0, MX, MY+78, MW)

    # Form card
    FY = MY + 118
    rr(d, MX, FY, MW, 504, fill=WHITE, ol=C['border'], r=10)

    FX = MX + 32
    FW = MW - 64

    t(d, '캠페인 기본 설정', FX, FY+18, fnt(15, bold=True))
    d.line([(MX, FY+48), (MX+MW, FY+48)], fill=C['border'], width=1)

    def field(lbl, x, y, w, ph='', val='', req=True):
        marker = ' *' if req else ''
        t(d, lbl+marker, x, y, fnt(12, bold=True), col=C['g700'])
        rr(d, x, y+22, w, 36, fill=WHITE, ol=C['border2'], r=6)
        txt  = val if val else ph
        col2 = C['text'] if val else C['text3']
        t(d, txt, x+12, y+31, fnt(12), col=col2)

    # Row 1: Campaign name
    field('캠페인 이름', FX, FY+60, FW, '예: 2024 여름 신제품 런칭', '여름 신제품 맘카페 광고')

    # Row 2: Category + Brand
    half = (FW - 20) // 2
    field('제품 카테고리', FX, FY+128, half, '카테고리 선택  ▾')
    # Open dropdown
    rr(d, FX, FY+186, half, 116, fill=WHITE, ol=C['border2'], r=6, lw=1)
    cats = ['유아/육아', '생활가전', 'IT/테크', '뷰티/패션', '식품/건강']
    for ci, cat in enumerate(cats):
        cy = FY+192 + ci*22
        if ci == 0:
            d.rectangle([FX, cy-2, FX+half, cy+20], fill=C['priml'])
        t(d, cat, FX+10, cy+2, fnt(11), col=C['primary'] if ci==0 else C['text'])
    field('제품 / 브랜드명', FX+half+20, FY+128, half, '예: 아기사랑 분유')

    # Row 3: Budget + Period
    field('총 캠페인 예산', FX, FY+224, half, '', '8,400,000')
    t(d, '원', FX+half-36, FY+264, fnt(12), col=C['g500'])
    t(d, '집행 기간 *', FX+half+20, FY+224, fnt(12, bold=True), col=C['g700'])
    half2 = (half-12) // 2
    rr(d, FX+half+20, FY+246, half2, 36, fill=WHITE, ol=C['border2'], r=6)
    t(d, '2024-05-01  📅', FX+half+32, FY+256, fnt(11), col=C['g400'])
    t(d, '~', FX+half+20+half2+2, FY+258, fnt(13), col=C['g500'])
    rr(d, FX+half+20+half2+18, FY+246, half2, 36, fill=WHITE, ol=C['border2'], r=6)
    t(d, '2024-05-31  📅', FX+half+32+half2+18, FY+256, fnt(11), col=C['g400'])

    # Row 4: Target country chips
    t(d, '타겟 국가 *', FX, FY+302, fnt(12, bold=True), col=C['g700'])
    countries = [('한국', True), ('미국', False), ('일본', False), ('중국', False), ('동남아시아', False), ('유럽', False)]
    cx2 = FX
    for ctr, sel in countries:
        bb = d.textbbox((0,0), ctr, font=fnt(11))
        cw3 = bb[2]-bb[0]+22
        rr(d, cx2, FY+322, cw3, 28, fill=C['primary'] if sel else WHITE, ol=C['primary'] if sel else C['border2'], r=14)
        tc(d, ctr, cx2+cw3//2, FY+328, fnt(11), col=WHITE if sel else C['g500'])
        cx2 += cw3+8

    # Row 5: Goal
    t(d, '캠페인 목표 *', FX, FY+368, fnt(12, bold=True), col=C['g700'])
    goals = [('인지도 향상', True), ('트래픽 증가', False), ('리드 수집', False), ('전환/구매', False)]
    gx = FX
    for glbl, gsel in goals:
        bb = d.textbbox((0,0), glbl, font=fnt(11))
        gw2 = bb[2]-bb[0]+22
        rr(d, gx, FY+388, gw2, 28, fill=C['priml'] if gsel else WHITE, ol=C['primary'] if gsel else C['border2'], r=14)
        tc(d, glbl, gx+gw2//2, FY+394, fnt(11), col=C['primary'] if gsel else C['g500'])
        gx += gw2+8

    # Buttons
    BY = FY+456
    rr(d, MX, BY, 106, 36, ol=C['border2'], r=6)
    tc(d, '← 이전', MX+53, BY+10, fnt(13), col=C['g500'])
    rr(d, MX+MW-144, BY, 140, 36, fill=C['primary'], r=6)
    tc(d, '다음 단계 →', MX+MW-144+70, BY+10, fnt(13, bold=True), col=WHITE)

    path = str(OUT / '02_new_campaign.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: 02_new_campaign.png')


# ═══════════════════════════════════════════════════════════════
# Screen 03 — 매체 선택
# ═══════════════════════════════════════════════════════════════
def screen_03():
    img, d = new_img()
    nav_bar(d, '캠페인')
    sidebar(d, '매체 관리')

    MX, MY = 220, 72
    MW = W - MX - 24

    t(d, '새 캠페인  >  매체 선택', MX, MY+10, fnt(11), col=C['g400'])
    t(d, '매체 선택', MX, MY+28, fnt(20, bold=True))
    step_bar(d, 1, MX, MY+78, MW)

    LY = MY + 118
    LW = int(MW * 0.64)
    RX = MX + LW + 14
    RW = MW - LW - 14

    # Search + filter row
    rr(d, MX, LY, LW-10, 36, fill=WHITE, ol=C['border2'], r=6)
    t(d, '  매체 검색...', MX+10, LY+10, fnt(12), col=C['text3'])
    cats = ['전체', '육아/맘', '게임', 'IT/테크', '생활정보', '뷰티']
    cx3 = MX
    for ci, cat in enumerate(cats):
        sel = ci == 0
        bb = d.textbbox((0,0), cat, font=fnt(11))
        cw4 = bb[2]-bb[0]+20
        rr(d, cx3, LY+42, cw4, 26, fill=C['primary'] if sel else C['g100'], r=13)
        tc(d, cat, cx3+cw4//2, LY+48, fnt(11), col=WHITE if sel else C['g600'])
        cx3 += cw4+8

    # Media cards grid (2×3)
    CARD_Y = LY + 78
    CARD_W = (LW - 22) // 2
    CARD_H = 142
    medias = [
        ('맘카페',    '육아/맘',  '월 UV 2,400만', 'CPM ₩3,200', True,  True),
        ('인벤',      '게임',     '월 UV 1,800만', 'CPM ₩2,800', False, True),
        ('뽐뿌',      '생활정보', '월 UV 950만',   'CPM ₩2,100', False, False),
        ('클리앙',    'IT/테크',  '월 UV 680만',   'CPM ₩3,800', True,  False),
        ('베이비뉴스','육아/맘',  '월 UV 420만',   'CPM ₩4,200', True,  True),
        ('루리웹',    '게임',     '월 UV 540만',   'CPM ₩2,600', False, False),
    ]
    for ci, (name, cat_tag, uv, cpm, recommended, selected) in enumerate(medias):
        col_i = ci % 2
        row_i = ci // 2
        cx4 = MX + col_i*(CARD_W+10)
        cy4 = CARD_Y + row_i*(CARD_H+10)
        border_c = C['primary'] if selected else C['border2']
        bg4      = C['priml']   if selected else WHITE
        rr(d, cx4, cy4, CARD_W, CARD_H, fill=bg4, ol=border_c, lw=2 if selected else 1, r=8)
        # Checkbox
        cb_col = C['primary'] if selected else C['g200']
        rr(d, cx4+CARD_W-30, cy4+8, 20, 20, fill=cb_col, r=4)
        if selected:
            tc(d, '✓', cx4+CARD_W-20, cy4+9, fnt(12, bold=True), col=WHITE)
        # Recommended star
        if recommended:
            rr(d, cx4+8, cy4+8, 56, 18, fill=C['warnl'], r=9)
            t(d, '추천', cx4+16, cy4+10, fnt(9), col=C['warn'])
        t(d, name, cx4+12, cy4+32, fnt(16, bold=True))
        pw = pill(d, cx4+12, cy4+54, cat_tag, sz=10)
        t(d, uv,  cx4+12, cy4+80,  fnt(11), col=C['g500'])
        t(d, cpm, cx4+12, cy4+96,  fnt(13, bold=True))
        t(d, '728×90  300×250  160×600', cx4+12, cy4+118, fnt(9), col=C['g400'])

    # RIGHT panel — budget allocation
    rr(d, RX, LY, RW, H-LY-24, fill=WHITE, ol=C['border'], r=8)
    t(d, '예산 배분', RX+14, LY+14, fnt(14, bold=True))
    d.line([(RX, LY+44), (RX+RW, LY+44)], fill=C['border'], width=1)
    t(d, '총 예산', RX+14, LY+56, fnt(11), col=C['g500'])
    t(d, '₩8,400,000', RX+14, LY+72, fnt(16, bold=True))
    d.line([(RX, LY+100), (RX+RW, LY+100)], fill=C['border'], width=1)

    alloc = [('맘카페', 70, C['primary']), ('클리앙', 30, C['success'])]
    sy2 = LY + 114
    slider_w = RW - 28
    for mname, pct, slcol in alloc:
        t(d, mname, RX+14, sy2, fnt(12, bold=True))
        tc(d, f'{pct}%', RX+RW-14, sy2, fnt(11), col=C['g500'])
        sy2 += 20
        rr(d, RX+14, sy2, slider_w, 6, fill=C['g200'], r=3)
        rr(d, RX+14, sy2, int(slider_w*pct/100), 6, fill=slcol, r=3)
        tx4 = RX+14 + int(slider_w*pct/100)
        d.ellipse([tx4-7, sy2-5, tx4+7, sy2+11], fill=slcol)
        amt = int(8400000*pct/100)
        t(d, f'₩{amt:,}', RX+14, sy2+12, fnt(10), col=C['g400'])
        sy2 += 46

    d.line([(RX, sy2+6), (RX+RW, sy2+6)], fill=C['border'], width=1)
    t(d, '선택 매체: 2개', RX+14, sy2+16, fnt(11), col=C['g600'])
    t(d, '배분 합계: 100 %', RX+14, sy2+32, fnt(11), col=C['success'])

    btn_y = H - 68
    rr(d, RX+8, btn_y, RW-16, 38, fill=C['primary'], r=6)
    tc(d, '다음: 소재 업로드 →', RX+8+(RW-16)//2, btn_y+11, fnt(13, bold=True), col=WHITE)

    path = str(OUT / '03_media_selection.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: 03_media_selection.png')


# ═══════════════════════════════════════════════════════════════
# Screen 04 — 소재 편집
# ═══════════════════════════════════════════════════════════════
def screen_04():
    img, d = new_img()
    nav_bar(d, '소재')
    sidebar(d, '소재 관리')

    MX, MY = 220, 72
    MW = W - MX - 24

    t(d, '소재 편집', MX, MY+10, fnt(20, bold=True))
    t(d, '여름 신제품 맘카페 광고', MX, MY+34, fnt(12), col=C['g400'])

    # Size preset tabs
    TY = MY + 58
    size_tabs = ['728×90 (리더보드)', '300×250 (미디엄 렉탱글)', '160×600 (와이드 스카이)', '320×100 (모바일 배너)']
    tx5 = MX
    for ti, tab in enumerate(size_tabs):
        is_a = ti == 0
        bg5  = C['primary'] if is_a else C['g100']
        t_col = WHITE if is_a else C['g500']
        bb = d.textbbox((0,0), tab, font=fnt(11))
        tw5 = bb[2]-bb[0]+22
        rr(d, tx5, TY, tw5, 30, fill=bg5, r=5)
        t(d, tab, tx5+11, TY+9, fnt(11), col=t_col)
        tx5 += tw5+4

    PY  = TY + 40
    PH  = H - PY - 66

    # ── LEFT PANEL: 원본 소재 ──
    LP_W = int(MW * 0.25)
    rr(d, MX, PY, LP_W, PH, fill=WHITE, ol=C['border'], r=8)
    t(d, '원본 소재', MX+12, PY+12, fnt(13, bold=True))
    d.line([(MX, PY+36), (MX+LP_W, PY+36)], fill=C['border'], width=1)

    # Upload zone
    UY  = PY+46
    UH  = int(PH*0.48)
    rr(d, MX+12, UY, LP_W-24, UH, fill=C['g100'], ol=C['g300'], r=8)
    ic_y = UY + UH//2 - 28
    tc(d, '🖼', MX+12+LP_W//2, ic_y, fnt(32), col=C['g300'])
    tc(d, '이미지 드래그 또는 클릭', MX+12+LP_W//2, ic_y+40, fnt(11), col=C['g400'])
    tc(d, 'PNG · JPG · 최대 10MB',   MX+12+LP_W//2, ic_y+58, fnt(10), col=C['text3'])

    # Uploaded file preview
    FY2 = UY+UH+12
    rr(d, MX+12, FY2, LP_W-24, 76, fill=C['g100'], ol=C['border2'], r=6)
    t(d, '분유_메인이미지.jpg', MX+20, FY2+10, fnt(10), col=C['g600'])
    t(d, '1920×1080 · 2.4 MB',  MX+20, FY2+26, fnt(10), col=C['g400'])
    rr(d, MX+20, FY2+46, 58, 22, fill=C['priml'], ol=C['primary'], r=4)
    t(d, '교체',  MX+30,  FY2+50, fnt(10), col=C['primary'])
    rr(d, MX+86, FY2+46, 58, 22, ol=C['danger'], r=4)
    t(d, '삭제',  MX+96, FY2+50, fnt(10), col=C['danger'])

    # Crop option
    t(d, '크롭 방식', MX+12, FY2+98, fnt(11, bold=True))
    opts = [('중앙 크롭', False), ('상단 크롭', False), ('스마트 크롭', True)]
    ox = MX+12
    for olbl, osel in opts:
        bb = d.textbbox((0,0), olbl, font=fnt(10))
        ow = bb[2]-bb[0]+14
        rr(d, ox, FY2+114, ow, 22, fill=C['primary'] if osel else C['g100'], r=4)
        t(d, olbl, ox+7, FY2+117, fnt(10), col=WHITE if osel else C['g500'])
        ox += ow+6

    # ── CENTER PANEL: 미리보기 ──
    CP_X = MX + LP_W + 12
    CP_W = int(MW * 0.45)
    rr(d, CP_X, PY, CP_W, PH, fill=C['bg'], ol=C['border'], r=8)
    t(d, '미리보기  [728 × 90]', CP_X+12, PY+12, fnt(13, bold=True))
    d.line([(CP_X, PY+36), (CP_X+CP_W, PY+36)], fill=C['border'], width=1)

    # Canvas banner preview
    CV_X = CP_X+20
    CV_Y = PY+50
    CV_W = CP_W-40
    CV_H = max(int(CV_W*90/728), 44)
    rr(d, CV_X, CV_Y, CV_W, CV_H, fill=C['g200'], ol=C['border2'], r=4)
    rr(d, CV_X+4, CV_Y+4, CV_W//4, CV_H-8, fill=C['g300'], r=3)
    tc(d, '로고', CV_X+CV_W//8, CV_Y+CV_H//2-7, fnt(10), col=C['g600'])
    t(d, '여름 특가! 아기사랑 분유 10% 할인', CV_X+CV_W//4+12, CV_Y+CV_H//2-7, fnt(11, bold=True), col=C['g800'])
    rr(d, CV_X+CV_W-78, CV_Y+5, 68, CV_H-10, fill=C['primary'], r=4)
    tc(d, '지금 구매', CV_X+CV_W-44, CV_Y+CV_H//2-7, fnt(10, bold=True), col=WHITE)
    # Guide corners
    for gx2, gy2 in [(CV_X,CV_Y),(CV_X+CV_W,CV_Y),(CV_X,CV_Y+CV_H),(CV_X+CV_W,CV_Y+CV_H)]:
        d.line([(gx2-8,gy2),(gx2+8,gy2)], fill=C['primary'], width=2)
        d.line([(gx2,gy2-8),(gx2,gy2+8)], fill=C['primary'], width=2)

    # Multi-size thumbnails
    TH_Y = CV_Y + CV_H + 22
    t(d, '다른 사이즈 미리보기', CP_X+12, TH_Y, fnt(11, bold=True))
    thumb_defs = [(300,250,'300×250'),(160,600,'160×600'),(320,100,'320×100')]
    thx = CP_X+12
    for tw6, th6, tlbl in thumb_defs:
        sc  = 0.12
        dw6 = max(int(tw6*sc), 30)
        dh6 = max(int(th6*sc), 20)
        if dh6 > 80: dh6=80; dw6=max(int(tw6*80/th6*sc),20)
        rr(d, thx, TH_Y+18, dw6, dh6, fill=C['g200'], ol=C['border2'], r=3)
        t(d, tlbl, thx, TH_Y+20+dh6, fnt(9), col=C['g400'])
        thx += dw6+24

    # AI copy generation panel
    AI_Y = TH_Y + 100
    rr(d, CP_X+12, AI_Y, CP_W-24, 76, fill=C['priml'], ol=C['primary'], r=8)
    t(d, '✨  AI 후킹 문구 자동생성', CP_X+20, AI_Y+10, fnt(13, bold=True), col=C['primary'])
    t(d, '"여름 특가! 아기사랑 분유 10% 할인 — 지금 바로!"', CP_X+20, AI_Y+30, fnt(11), col=C['g700'])
    rr(d, CP_X+CP_W-116, AI_Y+46, 104, 24, fill=C['primary'], r=12)
    tc(d, '✨  문구 재생성', CP_X+CP_W-116+52, AI_Y+51, fnt(10, bold=True), col=WHITE)

    # ── RIGHT PANEL: 속성 ──
    RP_X = CP_X + CP_W + 12
    RP_W = MW - LP_W - CP_W - 24
    rr(d, RP_X, PY, RP_W, PH, fill=WHITE, ol=C['border'], r=8)
    t(d, '속성', RP_X+12, PY+12, fnt(13, bold=True))
    d.line([(RP_X, PY+36), (RP_X+RP_W, PY+36)], fill=C['border'], width=1)

    py3 = PY+48
    for lbl2, val2 in [('너비','728 px'),('높이','90 px'),('파일 형식','PNG'),('용량 제한','150 KB')]:
        t(d, lbl2, RP_X+12, py3, fnt(10), col=C['g400'])
        rr(d, RP_X+12, py3+16, RP_W-24, 28, fill=C['g100'], ol=C['border2'], r=4)
        t(d, val2, RP_X+20, py3+22, fnt(12), col=C['g700'])
        py3 += 54

    # Toggle
    t(d, '텍스트 오버레이', RP_X+12, py3, fnt(10), col=C['g400'])
    tg_x = RP_X+RP_W-44
    rr(d, tg_x, py3+14, 36, 18, fill=C['primary'], r=9)
    d.ellipse([tg_x+18, py3+15, tg_x+34, py3+31], fill=WHITE)
    py3 += 50

    t(d, '출력 품질', RP_X+12, py3, fnt(10), col=C['g400'])
    qopts = [('고품질',True),('표준',False),('최적화',False)]
    qx2 = RP_X+12
    for qlbl, qsel in qopts:
        bb = d.textbbox((0,0), qlbl, font=fnt(9))
        qw = bb[2]-bb[0]+12
        rr(d, qx2, py3+16, qw, 22, fill=C['primary'] if qsel else C['g100'], r=4)
        t(d, qlbl, qx2+6, py3+19, fnt(9), col=WHITE if qsel else C['g500'])
        qx2 += qw+6

    # Bottom buttons
    BTN_Y = H - 60
    d.line([(MX, BTN_Y), (W-24, BTN_Y)], fill=C['border'], width=1)
    rr(d, MX, BTN_Y+10, 116, 36, ol=C['border2'], r=6)
    tc(d, '← 이전 단계', MX+58, BTN_Y+20, fnt(12), col=C['g500'])
    rr(d, MX+MW-138, BTN_Y+10, 134, 36, fill=C['primary'], r=6)
    tc(d, '계약 진행 →', MX+MW-138+67, BTN_Y+20, fnt(12, bold=True), col=WHITE)

    path = str(OUT / '04_creative_editor.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: 04_creative_editor.png')


# ═══════════════════════════════════════════════════════════════
# Screen 05 — 계약 진행
# ═══════════════════════════════════════════════════════════════
def screen_05():
    img, d = new_img()
    nav_bar(d, '캠페인')
    sidebar(d, '계약 관리')

    MX, MY = 220, 72
    MW = W - MX - 24

    t(d, '계약 진행', MX, MY+10, fnt(20, bold=True))
    t(d, '여름 신제품 맘카페 광고  |  2024-05-01 ~ 2024-05-31', MX, MY+34, fnt(12), col=C['g400'])
    step_bar(d, 3, MX, MY+78, MW)

    # Alert banner
    SY = MY + 112
    rr(d, MX, SY, MW, 54, fill=C['succl'], ol=C['success'], r=8)
    t(d, '소재 준비 완료 — 매체와 계약을 진행하세요.',       MX+16, SY+10, fnt(13), col=C['success'])
    t(d, '선택 매체: 맘카페, 클리앙  |  총 예산: ₩8,400,000  |  집행 기간: 31일', MX+16, SY+30, fnt(11), col=C['g600'])

    COL_Y = SY + 70
    COL_H = H - COL_Y - 72
    LCW   = int(MW * 0.60)
    RCX   = MX + LCW + 14
    RCW   = MW - LCW - 14

    # ── LEFT: 매체별 계약 현황 ──
    rr(d, MX, COL_Y, LCW, COL_H, fill=WHITE, ol=C['border'], r=8)
    t(d, '매체별 계약 현황', MX+16, COL_Y+14, fnt(14, bold=True))
    d.line([(MX, COL_Y+42), (MX+LCW, COL_Y+42)], fill=C['border'], width=1)

    timeline_medias = [
        ('맘카페', [
            ('계약서 발송', 'done',   '04/20'),
            ('계약서 서명', 'done',   '04/22'),
            ('매체사 확인', 'active', '검토 중'),
            ('집행 시작',   'wait',   '05/01'),
        ]),
        ('클리앙', [
            ('계약서 발송', 'done',   '04/21'),
            ('계약서 서명', 'active', '서명 대기'),
            ('매체사 확인', 'wait',   '—'),
            ('집행 시작',   'wait',   '05/01'),
        ]),
    ]

    my3 = COL_Y + 56
    step_sp = (LCW - 60) // 4
    for media_nm, tl in timeline_medias:
        t(d, media_nm, MX+16, my3, fnt(14, bold=True), col=C['g800'])
        for ti, (step_nm, status, date) in enumerate(tl):
            tx7 = MX + 30 + ti*step_sp
            ty7 = my3 + 32
            if status == 'done':
                fill7, mark7 = C['success'], '✓'
            elif status == 'active':
                fill7, mark7 = C['primary'], ''
            else:
                fill7, mark7 = C['g300'], ''
            d.ellipse([tx7-13, ty7-13, tx7+13, ty7+13], fill=fill7, outline=fill7)
            if mark7:
                tc(d, mark7, tx7, ty7-7, fnt(12, bold=True), col=WHITE)
            elif status == 'active':
                d.ellipse([tx7-4, ty7-4, tx7+4, ty7+4], fill=WHITE)
            else:
                d.ellipse([tx7-4, ty7-4, tx7+4, ty7+4], fill=C['g400'])
            if ti < 3:
                lc2 = C['success'] if status == 'done' else C['g200']
                d.line([(tx7+13, ty7), (tx7+step_sp-13, ty7)], fill=lc2, width=2)
            tc(d, step_nm, tx7, ty7+16, fnt(10), col=C['g600'])
            date_col = C['success'] if status=='done' else (C['primary'] if status=='active' else C['g400'])
            tc(d, date, tx7, ty7+30, fnt(9), col=date_col)
        my3 += 86
        if media_nm != timeline_medias[-1][0]:
            d.line([(MX+14, my3-4), (MX+LCW-14, my3-4)], fill=C['border'], width=1)

    # Action buttons
    abx = MX+16
    for albl, abg, acol in [('계약서 재발송', C['g100'], C['g500']), ('계약 촉구 알림 발송', C['warnl'], C['warn'])]:
        bb = d.textbbox((0,0), albl, font=fnt(12))
        aw = bb[2]-bb[0]+24
        rr(d, abx, my3+8, aw, 30, fill=abg, ol=C['border2'] if abg==C['g100'] else None, r=6)
        t(d, albl, abx+12, my3+13, fnt(12), col=acol)
        abx += aw+12

    # ── RIGHT: 서류 체크리스트 ──
    rr(d, RCX, COL_Y, RCW, COL_H, fill=WHITE, ol=C['border'], r=8)
    t(d, '필요 서류 체크리스트', RCX+14, COL_Y+14, fnt(13, bold=True))
    d.line([(RCX, COL_Y+42), (RCX+RCW, COL_Y+42)], fill=C['border'], width=1)

    checklist = [
        ('사업자등록증 사본',  True,  '04/20 확인'),
        ('통장 사본',          True,  '04/20 확인'),
        ('계약서 (맘카페)',    True,  '04/22 서명'),
        ('계약서 (클리앙)',    False, '서명 대기'),
        ('인보이스 발행',      False, '미완료'),
        ('세금계산서',         False, '집행 후 발행'),
    ]
    cy3 = COL_Y + 54
    for item, done, note in checklist:
        cb_fill = C['success'] if done else C['g200']
        rr(d, RCX+14, cy3, 18, 18, fill=cb_fill, r=4)
        if done:
            tc(d, '✓', RCX+23, cy3+1, fnt(11, bold=True), col=WHITE)
        t(d, item, RCX+40, cy3+1,  fnt(12, bold=done), col=C['text'] if done else C['g500'])
        note_col = C['success'] if done else C['text3']
        t(d, note, RCX+40, cy3+20, fnt(10), col=note_col)
        cy3 += 44

    cy3 += 8
    rr(d, RCX+14, cy3, RCW-28, 32, ol=C['border2'], r=6)
    tc(d, '+ 서류 업로드', RCX+14+(RCW-28)//2, cy3+9, fnt(12), col=C['g500'])

    # Bottom buttons
    BTN_Y = H - 60
    d.line([(MX, BTN_Y), (W-24, BTN_Y)], fill=C['border'], width=1)
    rr(d, MX, BTN_Y+10, 116, 36, ol=C['border2'], r=6)
    tc(d, '← 이전 단계', MX+58, BTN_Y+20, fnt(12), col=C['g500'])
    rr(d, MX+MW-168, BTN_Y+10, 164, 36, fill=C['success'], r=6)
    tc(d, '캠페인 최종 확정', MX+MW-168+82, BTN_Y+20, fnt(12, bold=True), col=WHITE)

    path = str(OUT / '05_contract_flow.png')
    img.save(path)
    assert os.path.exists(path)
    print('OK: 05_contract_flow.png')


if __name__ == '__main__':
    print('AdMix v2 와이어프레임 생성 시작 (5개 화면, 1280x800)')
    screen_01()
    screen_02()
    screen_03()
    screen_04()
    screen_05()
    print()

    expected = [
        '01_dashboard.png', '02_new_campaign.png', '03_media_selection.png',
        '04_creative_editor.png', '05_contract_flow.png',
    ]
    all_ok = True
    for fname in expected:
        fp = OUT / fname
        exists = os.path.exists(str(fp))
        if exists:
            print(f'  {fname}: {fp.stat().st_size // 1024} KB')
        else:
            print(f'  MISSING: {fname}')
            all_ok = False

    if all_ok:
        print('\n완료! 저장 위치:', str(OUT))
    else:
        print('\n일부 파일 누락')
        sys.exit(1)
