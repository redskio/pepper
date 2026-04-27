# -*- coding: utf-8 -*-
"""AdMix MVP 와이어프레임 생성기 — 5개 화면 PNG (1440×900)"""
import sys, io, math
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1440, 900
OUT = Path('C:/Agent/pepper/output/admix_wireframes')
OUT.mkdir(parents=True, exist_ok=True)

# ── Color Palette ────────────────────────────────────────────
C = {
    'bg':       (248, 249, 250),
    'white':    (255, 255, 255),
    'primary':  (79, 70, 229),
    'plight':   (238, 242, 255),
    'pdark':    (67, 56, 202),
    'text':     (17, 24, 39),
    'text2':    (107, 114, 128),
    'text3':    (156, 163, 175),
    'border':   (229, 231, 235),
    'border2':  (209, 213, 219),
    'sidebar':  (17, 24, 39),
    'success':  (16, 185, 129),
    'succ_l':   (209, 250, 229),
    'warn':     (245, 158, 11),
    'warn_l':   (254, 243, 199),
    'danger':   (239, 68, 68),
    'dang_l':   (254, 226, 226),
    'gray100':  (243, 244, 246),
    'gray200':  (229, 231, 235),
    'gray300':  (209, 213, 219),
    'gray400':  (156, 163, 175),
    'gray500':  (107, 114, 128),
    'gray600':  (75, 85, 99),
    'gray700':  (55, 65, 81),
    'gray800':  (31, 41, 55),
    'gray900':  (17, 24, 39),
}

# ── Font Cache ────────────────────────────────────────────────
_fc = {}
def fnt(size, bold=False):
    k = (size, bold)
    if k not in _fc:
        p = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
        try: _fc[k] = ImageFont.truetype(p, size)
        except: _fc[k] = ImageFont.load_default()
    return _fc[k]

# ── Drawing Primitives ────────────────────────────────────────
def new_img():
    img = Image.new('RGB', (W, H), C['bg'])
    return img, ImageDraw.Draw(img)

def rr(d, x, y, w, h, fill=None, ol=None, lw=1, r=8):
    """Rounded rectangle helper."""
    fill = fill if fill is not None else C['white']
    kw = {'radius': r, 'fill': fill}
    if ol: kw['outline'] = ol; kw['width'] = lw
    d.rounded_rectangle([x, y, x+w, y+h], **kw)

def t(d, s, x, y, f, col=None):
    """Left-top text."""
    d.text((x, y), str(s), fill=col or C['text'], font=f)

def tc(d, s, x, y, w, f, col=None):
    """Horizontally centered text in box of width w."""
    bb = f.getbbox(str(s))
    tw = bb[2] - bb[0]
    d.text((x + max(0, (w - tw) // 2), y), str(s), fill=col or C['text'], font=f)

def btn(d, x, y, w, h, lbl, sz=14, fill=None, col=None, r=6, bold=True):
    fill = fill or C['primary']; col = col or C['white']
    rr(d, x, y, w, h, fill=fill, r=r)
    tc(d, lbl, x, y + max(2, (h - sz - 4) // 2), w, fnt(sz, bold=bold), col=col)

def btn_ghost(d, x, y, w, h, lbl, sz=13, border=None, col=None, r=6):
    border = border or C['primary']; col = col or C['primary']
    rr(d, x, y, w, h, fill=C['white'], ol=border, lw=2, r=r)
    tc(d, lbl, x, y + max(2, (h - sz - 4) // 2), w, fnt(sz), col=col)

def inp(d, x, y, w, h, ph='', sz=13, val='', r=6):
    rr(d, x, y, w, h, fill=C['white'], ol=C['border2'], lw=1, r=r)
    label = val if val else ph
    col = C['text'] if val else C['text3']
    t(d, label, x + 14, y + max(2, (h - sz) // 2), fnt(sz), col=col)

def tag(d, x, y, lbl, sz=10, fill=None, col=None, r=4):
    fill = fill or C['plight']; col = col or C['primary']
    f = fnt(sz, bold=True)
    bb = f.getbbox(lbl)
    bw = bb[2] - bb[0] + 18
    bh = max(22, bb[3] - bb[1] + 8)
    rr(d, x, y, bw, bh, fill=fill, r=r)
    t(d, lbl, x + 9, y + 5, f, col=col)
    return bw

def divider(d, x, y, w, col=None):
    d.line([(x, y), (x+w, y)], fill=col or C['border'], width=1)

def pbar(d, x, y, w, h, pct, fill=None, bg=None, r=3):
    rr(d, x, y, w, h, fill=bg or C['gray200'], r=r)
    pw = max(0, int(w * pct / 100))
    if pw > 0: rr(d, x, y, pw, h, fill=fill or C['primary'], r=r)

def placeholder(d, x, y, w, h, lbl='', col=None, r=6):
    rr(d, x, y, w, h, fill=col or C['gray200'], r=r)
    if lbl: tc(d, lbl, x, y + h//2 - 8, w, fnt(11), col=C['gray500'])


# ── Global Nav Bar ─────────────────────────────────────────────
def draw_nav(d, active=''):
    rr(d, 0, 0, W, 64, fill=C['white'], r=0)
    divider(d, 0, 64, W)
    t(d, 'Ad', 28, 18, fnt(26, bold=True), col=C['primary'])
    t(d, 'Mix', 62, 18, fnt(26, bold=True), col=C['gray800'])

    nav_items = ['대시보드', '매체 탐색', '소재 관리', '캠페인']
    nx = 160
    for item in nav_items:
        is_act = item == active
        f = fnt(14, bold=is_act)
        bb = f.getbbox(item)
        iw = bb[2] - bb[0]
        t(d, item, nx, 23, f, col=C['primary'] if is_act else C['gray500'])
        if is_act:
            d.rectangle([nx, 60, nx + iw, 64], fill=C['primary'])
        nx += iw + 48

    rr(d, W - 112, 16, 86, 34, fill=C['gray100'], r=6)
    t(d, '홍길동', W - 99, 25, fnt(13), col=C['gray700'])
    btn(d, W - 210, 16, 88, 34, '업그레이드', sz=12)


# ════════════════════════════════════════════════════════════════
# SCREEN 01  —  랜딩 / 온보딩
# ════════════════════════════════════════════════════════════════
def screen_01():
    img, d = new_img()
    draw_nav(d, '매체 탐색')

    # Hero band
    rr(d, 0, 64, W, 272, fill=(245, 246, 255), r=0)
    divider(d, 0, 336, W)

    # Hero left
    tag(d, 80, 98, 'BETA', sz=11)
    t(d, '버티컬 광고매체, 한 번에 집행하세요', 80, 132, fnt(36, bold=True))
    t(d, '맘카페, 게임포털, 커뮤니티 — 타겟에 맞는 매체를 자동 추천받고,', 80, 184, fnt(14), col=C['text2'])
    t(d, '소재 사이즈까지 자동 조정됩니다. 광고 집행의 모든 과정을 단순하게.', 80, 206, fnt(14), col=C['text2'])
    btn(d, 80, 248, 190, 50, '지금 무료 시작하기', sz=15)
    btn_ghost(d, 284, 248, 136, 50, '데모 보기', sz=15)

    # Hero right — mini dashboard preview
    rr(d, 830, 78, 528, 242, fill=(232, 234, 255), r=16)
    rr(d, 854, 100, 480, 190, fill=C['white'], r=10)
    for i, (lbl, val, col) in enumerate([
        ('총 노출수', '1.24M', C['primary']),
        ('평균 CTR', '3.8%', C['success']),
        ('집행액', '₩2.45M', C['warn']),
    ]):
        bx = 874 + i * 148
        rr(d, bx, 116, 132, 72, fill=C['gray100'], r=8)
        t(d, lbl, bx + 12, 126, fnt(11), col=C['text2'])
        t(d, val, bx + 12, 148, fnt(20, bold=True), col=col)
    # Mini bar chart
    for i in range(7):
        bh = [40, 65, 50, 80, 55, 90, 70][i]
        bx = 874 + i * 66
        rr(d, bx, 256 - bh, 50, bh, fill=C['primary'] if i == 5 else C['gray200'], r=4)

    # ── Onboarding card ──────────────────────────────────────────
    rr(d, 60, 352, W - 120, 512, fill=C['white'], r=16)
    divider(d, 60, 352, W - 120)

    # Step indicators
    for i, (snum, slbl) in enumerate([(1, '광고 타겟 선택'), (2, '예산 설정'), (3, '기간 설정')]):
        sx = 92 + i * 432
        col = C['primary'] if i == 0 else C['gray300']
        rr(d, sx, 370, 30, 30, fill=col, r=15)
        tc(d, str(snum), sx, 376, 30, fnt(13, bold=True), col=C['white'])
        t(d, slbl, sx + 40, 377, fnt(14, bold=(i == 0)),
          col=C['primary'] if i == 0 else C['text3'])
        if i < 2:
            d.line([(sx + 332, 385), (sx + 422, 385)], fill=C['gray200'], width=2)

    divider(d, 84, 416, W - 200)

    # Step 1 — target category
    t(d, '어떤 타겟에게 광고하시나요?', 84, 434, fnt(20, bold=True))
    t(d, '관련 버티컬 채널을 선택하세요 (중복 선택 가능)', 84, 465, fnt(13), col=C['text2'])

    cats = [
        ('맘카페 / 육아', True), ('게임 / 인벤', True),
        ('자동차 커뮤니티', False), ('뷰티 / 패션', False),
        ('부동산 카페', False), ('스포츠 / 건강', False),
        ('IT / 테크', False), ('여행 / 레저', False),
    ]
    for i, (cat, sel) in enumerate(cats):
        cx = 84 + (i % 4) * 334
        cy = 494 + (i // 4) * 54
        fill = C['primary'] if sel else C['white']
        ol = C['primary'] if sel else C['border2']
        rr(d, cx, cy, 318, 42, fill=fill, ol=ol, lw=2, r=8)
        cb_x, cb_y = cx + 14, cy + 13
        rr(d, cb_x, cb_y, 18, 18, fill=C['white'], ol=C['white'] if sel else C['gray300'], lw=1, r=3)
        if sel:
            t(d, '✓', cb_x + 2, cb_y + 2, fnt(12, bold=True), col=C['primary'])
        t(d, cat, cx + 40, cy + 13, fnt(14, bold=sel), col=C['white'] if sel else C['text'])

    # Step 2 — budget
    t(d, '총 광고 예산', 84, 620, fnt(18, bold=True))
    rr(d, 84, 648, 380, 50, fill=C['white'], ol=C['border2'], lw=2, r=8)
    t(d, '₩', 102, 663, fnt(17), col=C['text2'])
    t(d, '3,000,000', 126, 660, fnt(20, bold=True))
    t(d, '/ 월', 310, 665, fnt(13), col=C['text3'])
    chips_b = ['₩500만', '₩1,000만', '₩3,000만', '직접입력']
    cx2 = 476
    for i, ch in enumerate(chips_b):
        f = fnt(12)
        bb = f.getbbox(ch); cw = bb[2] - bb[0] + 24
        sel2 = i == 2
        rr(d, cx2, 658, cw, 30, fill=C['plight'] if sel2 else C['gray100'], r=15)
        t(d, ch, cx2 + 12, 666, f, col=C['primary'] if sel2 else C['gray600'])
        cx2 += cw + 8

    # Step 3 — period
    t(d, '광고 기간', 940, 620, fnt(18, bold=True))
    inp(d, 940, 646, 200, 50, sz=14, val='2026.05.01')
    t(d, '→', 1152, 662, fnt(18), col=C['text3'])
    inp(d, 1172, 646, 200, 50, sz=14, val='2026.05.31')

    # CTA
    btn(d, W // 2 - 160, 760, 320, 56, '매체 추천받기  →', sz=18)
    tc(d, '무료로 시작 · 신용카드 불필요', 0, 828, W, fnt(12), col=C['text3'])

    img.save(str(OUT / '01_landing_onboarding.png'))
    print('OK: 01_landing_onboarding.png')


# ════════════════════════════════════════════════════════════════
# SCREEN 02  —  매체 추천 결과
# ════════════════════════════════════════════════════════════════
def screen_02():
    img, d = new_img()
    draw_nav(d, '매체 탐색')

    SB_W = 280

    # Left sidebar
    rr(d, 0, 64, SB_W, H - 64, fill=C['white'], r=0)
    d.line([(SB_W, 64), (SB_W, H)], fill=C['border'], width=1)

    t(d, '캠페인 정보', 24, 88, fnt(11, bold=True), col=C['text3'])
    divider(d, 16, 110, SB_W - 16)

    info = [
        ('캠페인명', '5월 신상품 런칭'),
        ('타겟 채널', '맘카페 · 게임'),
        ('총 예산', '₩ 3,000,000'),
        ('기간', '05.01 ~ 05.31'),
        ('목표', '브랜드 인지도'),
    ]
    for i, (k, v) in enumerate(info):
        iy = 122 + i * 54
        t(d, k, 24, iy, fnt(11), col=C['text3'])
        t(d, v, 24, iy + 18, fnt(14, bold=True))
        if i < len(info) - 1:
            divider(d, 16, iy + 46, SB_W - 16)

    t(d, '예산 배분', 24, 406, fnt(11, bold=True), col=C['text3'])
    divider(d, 16, 426, SB_W - 16)
    for i, (lbl, pct, col) in enumerate([('맘카페', 40, C['primary']),
                                          ('인벤', 35, C['success']),
                                          ('미배분', 25, C['gray300'])]):
        by = 438 + i * 44
        t(d, lbl, 24, by, fnt(13))
        t(d, f'{pct}%', SB_W - 50, by, fnt(13, bold=True), col=col)
        pbar(d, 24, by + 22, SB_W - 56, 8, pct, fill=col)

    divider(d, 16, 580, SB_W - 16)
    rr(d, 20, 594, SB_W - 40, 42, fill=C['white'], ol=C['primary'], lw=2, r=8)
    tc(d, '캠페인 수정', 20, 608, SB_W - 40, fnt(14), col=C['primary'])

    # Main area
    MX = SB_W + 28
    MW = W - MX - 28

    t(d, '추천 매체', MX, 84, fnt(24, bold=True))
    tag(d, MX + 138, 90, '5개 매체', sz=11, fill=C['succ_l'], col=C['success'])
    t(d, '타겟·예산·기간을 기반으로 최적 매체를 선별했습니다', MX, 120, fnt(13), col=C['text2'])

    # Sort bar
    rr(d, MX, 148, MW, 42, fill=C['white'], r=8)
    t(d, '정렬 기준:', MX + 16, 164, fnt(13), col=C['text2'])
    for i, s in enumerate(['추천순', '노출량순', 'CPM순', '타겟 적합도순']):
        sx = MX + 90 + i * 112
        sel3 = i == 0
        rr(d, sx, 158, 104, 28, fill=C['plight'] if sel3 else None, ol=C['primary'] if sel3 else None, lw=1, r=14)
        tc(d, s, sx, 163, 104, fnt(12, bold=sel3), col=C['primary'] if sel3 else C['text2'])
    btn(d, MX + MW - 120, 158, 110, 30, '전체 선택', sz=12, fill=C['gray100'], col=C['text2'])

    # Media cards
    media = [
        ('맘카페\n맘스홀릭', '육아 / 엄마', '월 850만 UV', '₩4,200', '₩1,200,000', 40, 94, C['primary'], True),
        ('인벤\n게임포털', '게임', '월 620만 UV', '₩3,800', '₩1,050,000', 35, 88, C['success'], True),
        ('클리앙\nIT커뮤니티', 'IT / 테크', '월 290만 UV', '₩5,100', '₩450,000', 15, 71, C['warn'], False),
        ('보배드림\n자동차', '자동차', '월 180만 UV', '₩4,600', '₩300,000', 10, 63, C['danger'], False),
    ]
    CW = (MW - 24) // 2
    CH = 188

    for i, (nm, cat, uv, cpm, bgt, pct, match, col, sel) in enumerate(media):
        cx3 = MX + (i % 2) * (CW + 24)
        cy3 = 206 + (i // 2) * (CH + 18)
        rr(d, cx3, cy3, CW, CH, fill=C['white'], ol=col if sel else C['border'], lw=2 if sel else 1, r=12)
        if sel:
            rr(d, cx3, cy3, CW, 5, fill=col, r=0)

        # Logo circle
        rr(d, cx3 + 16, cy3 + 16, 50, 50, fill=col, r=25)
        tc(d, nm.split('\n')[0][0], cx3 + 16, cy3 + 22, 50, fnt(22, bold=True), col=C['white'])

        # Name
        for li, line in enumerate(nm.split('\n')):
            t(d, line, cx3 + 80, cy3 + 14 + li * 20, fnt(14 if li == 0 else 12, bold=(li == 0)),
              col=C['text'] if li == 0 else C['text2'])

        # Category tag
        tag(d, cx3 + 80, cy3 + 58, cat, sz=10, fill=C['gray100'], col=C['gray600'])

        # Match score
        mcol = C['success'] if match >= 80 else C['warn'] if match >= 65 else C['danger']
        t(d, f'적합도 {match}%', cx3 + CW - 110, cy3 + 18, fnt(13, bold=True), col=mcol)

        divider(d, cx3 + 16, cy3 + 82, CW - 32)

        # Stats
        stats3 = [('월간 UV', uv), ('CPM', cpm), ('배정 예산', bgt)]
        sw = (CW - 32) // 3
        for si, (sk, sv) in enumerate(stats3):
            sx2 = cx3 + 16 + si * sw
            t(d, sk, sx2, cy3 + 92, fnt(10), col=C['text3'])
            t(d, sv, sx2, cy3 + 108, fnt(12, bold=True))

        # Progress bar
        if pct > 0:
            pbar(d, cx3 + 16, cy3 + 148, CW - 88, 6, pct, fill=col)
            t(d, f'{pct}%', cx3 + CW - 64, cy3 + 143, fnt(11), col=col)

        # Button
        if sel:
            btn(d, cx3 + CW - 108, cy3 + CH - 44, 94, 32, '선택됨 ✓', sz=12, fill=col)
        else:
            rr(d, cx3 + CW - 108, cy3 + CH - 44, 94, 32, fill=C['white'], ol=C['border2'], lw=1, r=6)
            tc(d, '+ 추가', cx3 + CW - 108, cy3 + CH - 34, 94, fnt(12), col=C['text2'])

    # Bottom bar
    rr(d, 0, H - 76, W, 76, fill=C['white'], r=0)
    d.line([(0, H - 76), (W, H - 76)], fill=C['border'], width=1)
    t(d, '선택: 2개 매체', MX, H - 50, fnt(14), col=C['text2'])
    t(d, '|', MX + 130, H - 50, fnt(14), col=C['border2'])
    t(d, '총 배정 예산  ₩ 2,250,000', MX + 146, H - 50, fnt(14, bold=True))
    t(d, '/ ₩ 3,000,000', MX + 400, H - 50, fnt(13), col=C['text3'])
    btn_ghost(d, W - 380, H - 62, 160, 44, '← 다시 설정', sz=14)
    btn(d, W - 208, H - 62, 184, 44, '소재 등록하기  →', sz=15)

    img.save(str(OUT / '02_media_recommendation.png'))
    print('OK: 02_media_recommendation.png')


# ════════════════════════════════════════════════════════════════
# SCREEN 03  —  소재 편집 (핵심 화면)
# ════════════════════════════════════════════════════════════════
def screen_03():
    img, d = new_img()
    draw_nav(d, '소재 관리')

    # Step progress bar
    rr(d, 0, 64, W, 50, fill=C['white'], r=0)
    divider(d, 0, 114, W)
    steps3 = ['1  매체 선택', '2  소재 편집', '3  검수 & 발행']
    for i, s in enumerate(steps3):
        sx = 80 + i * 290
        is_cur = i == 1
        is_done = i < 1
        col = C['primary'] if is_cur else (C['success'] if is_done else C['text3'])
        rr(d, sx, 77, 26, 26, fill=col, r=13)
        tc(d, '✓' if is_done else str(i + 1), sx, 82, 26, fnt(12, bold=True), col=C['white'])
        t(d, s.split('  ')[1], sx + 34, 82, fnt(13, bold=is_cur), col=col)
        if i < 2:
            d.line([(sx + 210, 90), (sx + 278, 90)], fill=C['gray300'], width=2)

    CT = 114  # Content top
    LP_W, RP_W = 280, 360
    CP_W = W - LP_W - RP_W  # 800

    # ── LEFT PANEL ───────────────────────────────────────────────
    rr(d, 0, CT, LP_W, H - CT, fill=C['white'], r=0)
    d.line([(LP_W, CT), (LP_W, H)], fill=C['border'], width=1)
    LX = 16

    t(d, '소재 이미지', LX, CT + 14, fnt(13, bold=True))

    # Upload zone
    rr(d, LX, CT + 38, LP_W - 32, 148, fill=C['gray100'], ol=C['gray300'], lw=1, r=8)
    rr(d, LX + 95, CT + 68, 50, 50, fill=C['gray300'], r=25)
    tc(d, '↑', LX + 95, CT + 80, 50, fnt(20), col=C['gray500'])
    tc(d, '클릭 또는 드래그', LX, CT + 134, LP_W - 32, fnt(11), col=C['text3'])
    tc(d, 'JPG, PNG, GIF 지원', LX, CT + 150, LP_W - 32, fnt(10), col=C['text3'])

    # Uploaded image preview
    rr(d, LX, CT + 196, LP_W - 32, 110, fill=(220, 224, 255), r=6)
    tc(d, '업로드된 원본 이미지', LX, CT + 240, LP_W - 32, fnt(11), col=C['primary'])
    t(d, '제품_이미지_최종.png', LX, CT + 316, fnt(10), col=C['text3'])

    divider(d, LX, CT + 338, LP_W - 16)

    t(d, '후킹 문구', LX, CT + 352, fnt(13, bold=True))
    t(d, 'AI 자동 생성', LX, CT + 372, fnt(10), col=C['text3'])
    btn(d, LX, CT + 392, LP_W - 32, 36, '✨  후킹 문구 자동 생성', sz=12,
        fill=C['plight'], col=C['primary'], bold=False)

    copies = [
        ('육아맘이 선택한 #1 브랜드', True),
        ('아이와 함께하는 특별한 순간', False),
        ('지금 첫 구매 20% 할인', False),
    ]
    for ci, (cp, sel) in enumerate(copies):
        cy2 = CT + 440 + ci * 56
        rr(d, LX, cy2, LP_W - 32, 46, fill=C['plight'] if sel else C['white'],
           ol=C['primary'] if sel else C['border'], lw=2 if sel else 1, r=6)
        if sel:
            t(d, '✓', LX + 10, cy2 + 16, fnt(11, bold=True), col=C['primary'])
        t(d, cp, LX + (26 if sel else 10), cy2 + 16, fnt(12, bold=sel),
          col=C['primary'] if sel else C['text'])

    inp(d, LX, CT + 614, LP_W - 32, 38, ph='직접 입력...', sz=12)

    # ── CENTER PANEL (Canvas) ────────────────────────────────────
    CPX = LP_W
    rr(d, CPX, CT, CP_W, H - CT, fill=C['gray100'], r=0)

    # Toolbar
    rr(d, CPX, CT, CP_W, 42, fill=C['white'], r=0)
    divider(d, CPX, CT + 42, CP_W)
    tools = ['선택', '텍스트', '이미지', '도형', '|', '↩ 되돌리기', '↪ 다시실행', '|', '100%  ▾']
    tx4 = CPX + 16
    for tool in tools:
        if tool == '|':
            d.line([(tx4 + 4, CT + 8), (tx4 + 4, CT + 34)], fill=C['border2'], width=1)
            tx4 += 14
        else:
            f = fnt(12)
            bb = f.getbbox(tool); tw = bb[2] - bb[0]
            is_act = tool == '선택'
            rr(d, tx4, CT + 7, tw + 16, 28,
               fill=C['plight'] if is_act else None,
               ol=C['primary'] if is_act else None, lw=1, r=4)
            t(d, tool, tx4 + 8, CT + 13, f, col=C['primary'] if is_act else C['text2'])
            tx4 += tw + 24

    # Canvas area — 맘카페 배너 320×100 at 2× = 640×200
    CAN_X = CPX + (CP_W - 640) // 2
    CAN_Y = CT + 64
    CAN_W, CAN_H = 640, 200

    rr(d, CAN_X + 5, CAN_Y + 5, CAN_W, CAN_H, fill=C['gray300'], r=4)  # shadow
    rr(d, CAN_X, CAN_Y, CAN_W, CAN_H, fill=(240, 242, 255), r=4)

    # Ad creative content
    rr(d, CAN_X + 400, CAN_Y + 22, 210, 158, fill=C['gray200'], r=4)
    tc(d, '제품 이미지', CAN_X + 400, CAN_Y + 88, 210, fnt(13), col=C['gray400'])

    # Selection box
    sel_rect = [CAN_X + 398, CAN_Y + 20, CAN_X + 612, CAN_Y + 182]
    d.rectangle(sel_rect, outline=C['primary'], width=2)
    for hx2, hy2 in [(CAN_X + 393, CAN_Y + 15), (CAN_X + 606, CAN_Y + 15),
                     (CAN_X + 393, CAN_Y + 176), (CAN_X + 606, CAN_Y + 176),
                     (CAN_X + 500, CAN_Y + 15), (CAN_X + 500, CAN_Y + 176),
                     (CAN_X + 393, CAN_Y + 96), (CAN_X + 606, CAN_Y + 96)]:
        rr(d, hx2, hy2, 10, 10, fill=C['white'], ol=C['primary'], lw=2, r=2)

    t(d, '육아맘이 선택한', CAN_X + 28, CAN_Y + 32, fnt(18, bold=True), col=C['primary'])
    t(d, '#1 브랜드', CAN_X + 28, CAN_Y + 58, fnt(30, bold=True))
    t(d, '지금 바로 확인하기  →', CAN_X + 28, CAN_Y + 108, fnt(14), col=C['text2'])

    # Canvas label
    tc(d, '맘카페 배너  320 × 100 px  |  2× 미리보기', CPX, CT + 280, CP_W, fnt(12), col=C['text3'])

    # Layer panel
    t(d, 'LAYERS', CPX + 20, CT + 308, fnt(11, bold=True), col=C['text3'])
    layers4 = [('텍스트: 육아맘이 선택한...', True), ('이미지: 제품사진_최종', False), ('배경 레이어', False)]
    for li, (ln, lsel) in enumerate(layers4):
        ly2 = CT + 330 + li * 36
        rr(d, CPX + 16, ly2, CP_W - 32, 30, fill=C['plight'] if lsel else C['gray100'], r=4)
        t(d, '▶' if lsel else '▷', CPX + 28, ly2 + 9, fnt(11), col=C['primary'] if lsel else C['gray400'])
        t(d, ln, CPX + 48, ly2 + 9, fnt(12), col=C['primary'] if lsel else C['text2'])

    # Align tools row
    t(d, '정렬', CPX + 20, CT + 444, fnt(11, bold=True), col=C['text3'])
    for ai, al in enumerate(['⊞ 좌', '⊟ 중', '⊠ 우', '⊡ 상', '⊞ 중', '⊡ 하']):
        ax2 = CPX + 20 + ai * 48
        rr(d, ax2, CT + 466, 40, 28, fill=C['gray100'], r=4)
        tc(d, al, ax2, CT + 472, 40, fnt(10), col=C['text2'])

    # ── RIGHT PANEL (Size list) ──────────────────────────────────
    RPX = LP_W + CP_W
    rr(d, RPX, CT, RP_W, H - CT, fill=C['white'], r=0)
    d.line([(RPX, CT), (RPX, H)], fill=C['border'], width=1)

    t(d, '매체별 사이즈', RPX + 16, CT + 14, fnt(14, bold=True))
    t(d, '사이즈 클릭 → 캔버스 전환', RPX + 16, CT + 36, fnt(10), col=C['text3'])
    divider(d, RPX + 12, CT + 56, RP_W - 24)

    sizes5 = [
        ('맘카페 배너', '320 × 100', True, 4, 1, C['primary']),
        ('인벤 사이드바', '160 × 600', False, 1, 4, C['success']),
        ('모바일 전면', '320 × 480', False, 2, 3, C['warn']),
        ('네이버 배너', '728 × 90', False, 5, 1, C['primary']),
        ('인스타 피드', '1080 × 1080', False, 1, 1, C['danger']),
    ]
    for si, (sn, sd, ssel5, rw, rh, scol) in enumerate(sizes5):
        sy = CT + 68 + si * 114

        rr(d, RPX + 12, sy, RP_W - 24, 102, fill=C['plight'] if ssel5 else C['gray100'],
           ol=C['primary'] if ssel5 else None, lw=2, r=8)

        # Thumbnail
        th_max = 72
        if rw >= rh:
            tw = min(th_max, 86)
            th = max(6, int(tw * rh / max(rw, 1)))
        else:
            th = min(th_max, 86)
            tw = max(6, int(th * rw / max(rh, 1)))

        th_x = RPX + 22
        th_y = sy + (102 - th) // 2
        rr(d, th_x, th_y, tw, th, fill=scol if ssel5 else C['gray300'], r=3)
        if rw >= rh:
            rr(d, th_x + 4, th_y + 4, tw - 8, max(4, th - 8),
               fill=(200, 210, 255) if ssel5 else C['gray200'], r=2)

        t(d, sn, RPX + 118, sy + 22, fnt(14, bold=ssel5),
          col=C['primary'] if ssel5 else C['text'])
        t(d, sd, RPX + 118, sy + 44, fnt(12), col=C['text2'])

        if ssel5:
            tag(d, RPX + 118, sy + 66, '편집 중', sz=10, fill=C['primary'], col=C['white'])
        else:
            tag(d, RPX + 118, sy + 66, '미편집', sz=10, fill=C['gray200'], col=C['gray500'])

    # Export bottom
    divider(d, RPX, H - 76, RP_W)
    rr(d, RPX, H - 76, RP_W, 76, fill=C['white'], r=0)
    btn(d, RPX + 16, H - 58, RP_W - 32, 42, '전체 내보내기 (5개 사이즈)', sz=13)

    # Bottom bar
    rr(d, 0, H - 76, LP_W + CP_W, 76, fill=C['white'], r=0)
    d.line([(0, H - 76), (LP_W + CP_W, H - 76)], fill=C['border'], width=1)
    btn_ghost(d, LP_W + 20, H - 58, 140, 42, '← 이전 단계', sz=14)
    btn(d, LP_W + CP_W - 180, H - 58, 162, 42, '다음 단계  →', sz=14)

    img.save(str(OUT / '03_creative_editor.png'))
    print('OK: 03_creative_editor.png')


# ════════════════════════════════════════════════════════════════
# SCREEN 04  —  소재 사이즈 조정
# ════════════════════════════════════════════════════════════════
def screen_04():
    img, d = new_img()
    draw_nav(d, '소재 관리')

    # Sub toolbar
    rr(d, 0, 64, W, 50, fill=C['white'], r=0)
    divider(d, 0, 114, W)
    t(d, '소재 사이즈 조정', 24, 78, fnt(16, bold=True))
    t(d, 'ㅣ  맘카페 배너 320×100 편집 중', 210, 82, fnt(13), col=C['text2'])
    btn_ghost(d, W - 290, 76, 130, 32, '← 소재 편집으로', sz=12)
    btn(d, W - 148, 76, 124, 32, '저장 & 적용', sz=13)

    CT = 114
    SP_W, RP_W = 300, 320
    CP_W = W - SP_W - RP_W  # 820

    # ── LEFT: Size list ──────────────────────────────────────────
    rr(d, 0, CT, SP_W, H - CT, fill=C['white'], r=0)
    d.line([(SP_W, CT), (SP_W, H)], fill=C['border'], width=1)
    t(d, '매체별 사이즈 선택', 16, CT + 14, fnt(13, bold=True))
    divider(d, 12, CT + 40, SP_W - 12)

    slist = [
        ('맘카페 배너', '320 × 100', '맘카페', True, C['primary'], 4, 1),
        ('인벤 사이드바', '160 × 600', '인벤', False, C['success'], 1, 4),
        ('모바일 전면', '320 × 480', '공통', False, C['warn'], 2, 3),
        ('네이버 배너', '728 × 90', '네이버', False, C['primary'], 5, 1),
        ('카카오 배너', '300 × 250', '카카오', False, C['warn'], 6, 5),
        ('인스타 피드', '1080 × 1080', 'SNS', False, C['danger'], 1, 1),
    ]
    for si, (sn, sd, plat, ssel, scol, rw, rh) in enumerate(slist):
        sy = CT + 50 + si * 94
        rr(d, 12, sy, SP_W - 24, 82, fill=C['plight'] if ssel else C['white'],
           ol=C['primary'] if ssel else C['border'], lw=2 if ssel else 1, r=8)

        # Radio
        rr(d, 28, sy + 30, 20, 20, fill=C['white'], ol=C['primary'] if ssel else C['gray300'], lw=2, r=10)
        if ssel:
            rr(d, 33, sy + 35, 10, 10, fill=C['primary'], r=5)

        # Thumbnail
        if rw >= rh:
            tw = min(60, SP_W - 80)
            th = max(5, int(tw * rh / max(rw, 1)))
        else:
            th = min(60, 70)
            tw = max(5, int(th * rw / max(rh, 1)))
        th_x = SP_W - 32 - tw
        th_y = sy + (82 - th) // 2
        rr(d, th_x, th_y, tw, th, fill=scol if ssel else C['gray200'], r=2)

        t(d, sn, 58, sy + 14, fnt(13, bold=ssel), col=C['primary'] if ssel else C['text'])
        t(d, sd, 58, sy + 34, fnt(11), col=C['text2'])
        tag(d, 58, sy + 56, plat, sz=9, fill=C['gray100'], col=C['gray600'])

    # ── CENTER: Canvas ────────────────────────────────────────────
    CPX = SP_W
    rr(d, CPX, CT, CP_W, H - CT, fill=C['gray100'], r=0)

    # Ruler
    for i in range(11):
        rx = CPX + i * (CP_W // 10)
        t(d, f'{i * 32}', rx + 2, CT + 5, fnt(9), col=C['gray400'])
        d.line([(rx, CT), (rx, CT + 5)], fill=C['gray400'], width=1)

    # Canvas (320×100 at 2× = 640×200)
    CAN_X = CPX + (CP_W - 640) // 2
    CAN_Y = CT + 50
    CAN_W, CAN_H = 640, 200

    rr(d, CAN_X + 5, CAN_Y + 5, CAN_W, CAN_H, fill=C['gray300'], r=4)
    rr(d, CAN_X, CAN_Y, CAN_W, CAN_H, fill=(240, 242, 255), r=0)

    # Ad content
    rr(d, CAN_X + 400, CAN_Y + 20, 210, 160, fill=C['gray200'], r=4)
    tc(d, '제품 이미지', CAN_X + 400, CAN_Y + 88, 210, fnt(13), col=C['gray400'])
    # Selection handles
    d.rectangle([CAN_X + 398, CAN_Y + 18, CAN_X + 612, CAN_Y + 182], outline=C['primary'], width=2)
    for hx3, hy3 in [(CAN_X + 393, CAN_Y + 13), (CAN_X + 606, CAN_Y + 13),
                     (CAN_X + 393, CAN_Y + 177), (CAN_X + 606, CAN_Y + 177),
                     (CAN_X + 500, CAN_Y + 13), (CAN_X + 500, CAN_Y + 177),
                     (CAN_X + 393, CAN_Y + 95), (CAN_X + 606, CAN_Y + 95)]:
        rr(d, hx3, hy3, 10, 10, fill=C['white'], ol=C['primary'], lw=2, r=2)

    t(d, '육아맘이 선택한', CAN_X + 28, CAN_Y + 30, fnt(18, bold=True), col=C['primary'])
    t(d, '#1 브랜드', CAN_X + 28, CAN_Y + 56, fnt(30, bold=True))
    t(d, '지금 바로 확인하기  →', CAN_X + 28, CAN_Y + 106, fnt(14), col=C['text2'])

    # Dimension guides
    d.line([(CAN_X, CAN_Y + CAN_H + 18), (CAN_X + CAN_W, CAN_Y + CAN_H + 18)], fill=C['primary'], width=1)
    d.line([(CAN_X, CAN_Y + CAN_H + 14), (CAN_X, CAN_Y + CAN_H + 22)], fill=C['primary'], width=1)
    d.line([(CAN_X + CAN_W, CAN_Y + CAN_H + 14), (CAN_X + CAN_W, CAN_Y + CAN_H + 22)], fill=C['primary'], width=1)
    tc(d, '320px  (2× = 640px 미리보기)', CAN_X, CAN_Y + CAN_H + 26, CAN_W, fnt(11), col=C['primary'])

    d.line([(CAN_X + CAN_W + 18, CAN_Y), (CAN_X + CAN_W + 18, CAN_Y + CAN_H)], fill=C['primary'], width=1)
    t(d, '100px', CAN_X + CAN_W + 26, CAN_Y + CAN_H // 2, fnt(11), col=C['primary'])

    # Other size mini strip
    t(d, '다른 사이즈 미리보기', CPX + 24, CAN_Y + CAN_H + 58, fnt(13, bold=True), col=C['text2'])
    strip = [('160×600', 1, 4), ('320×480', 2, 3), ('728×90', 4, 1), ('1080×1080', 1, 1)]
    stx = CPX + 24
    for sdim5, srw, srh in strip:
        SH2 = 68
        sw = max(10, int(SH2 * srw / max(srh, 1)))
        if sw > 110: sw = 110; SH2 = max(10, int(sw * srh / max(srw, 1)))
        rr(d, stx, CAN_Y + CAN_H + 82, sw, SH2, fill=C['white'], ol=C['border2'], lw=1, r=2)
        rr(d, stx + 2, CAN_Y + CAN_H + 84, sw - 4, SH2 - 4, fill=C['gray100'], r=2)
        tc(d, sdim5, stx, CAN_Y + CAN_H + 158, sw, fnt(9), col=C['text3'])
        stx += sw + 22

    # ── RIGHT: Adjustment panel ──────────────────────────────────
    RPX = SP_W + CP_W
    rr(d, RPX, CT, RP_W, H - CT, fill=C['white'], r=0)
    d.line([(RPX, CT), (RPX, H)], fill=C['border'], width=1)

    def section(title, y_off):
        t(d, title, RPX + 16, CT + y_off, fnt(11, bold=True), col=C['text3'])
        divider(d, RPX + 12, CT + y_off + 18, RP_W - 24)

    # Position
    section('위치 (POSITION)', 14)
    for i2, (lbl6, val6, off) in enumerate([('X', '400', 0), ('Y', '20', 148)]):
        t(d, lbl6, RPX + off + 22, CT + 50, fnt(12), col=C['text2'])
        inp(d, RPX + off + 38, CT + 42, 106, 34, sz=13, val=val6)
    for i2, (lbl6, val6, off) in enumerate([('W', '210', 0), ('H', '160', 148)]):
        t(d, lbl6, RPX + off + 22, CT + 96, fnt(12), col=C['text2'])
        inp(d, RPX + off + 38, CT + 88, 106, 34, sz=13, val=val6)
    rr(d, RPX + 144, CT + 58, 22, 54, fill=C['plight'], r=4)
    tc(d, '⛓', RPX + 144, CT + 76, 22, fnt(13), col=C['primary'])

    # Scale
    section('크기 (SCALE)', 148)
    t(d, '배율', RPX + 20, CT + 182, fnt(12), col=C['text2'])
    pbar(d, RPX + 58, CT + 188, 204, 8, 65, fill=C['primary'])
    knob_x = RPX + 58 + int(204 * 0.65) - 6
    rr(d, knob_x, CT + 184, 12, 16, fill=C['white'], ol=C['primary'], lw=2, r=6)
    t(d, '65%', RPX + 272, CT + 182, fnt(12, bold=True), col=C['primary'])
    for i2, (fl, fsel) in enumerate([('원본', False), ('꽉 채우기', True), ('맞춤', False)]):
        fx = RPX + 20 + i2 * 96
        rr(d, fx, CT + 210, 86, 28, fill=C['primary'] if fsel else C['gray100'], r=4)
        tc(d, fl, fx, CT + 217, 86, fnt(12), col=C['white'] if fsel else C['text2'])

    # Crop
    section('크롭 (CROP)', 264)
    rr(d, RPX + 20, CT + 300, RP_W - 40, 78, fill=C['gray100'], r=8)
    placeholder(d, RPX + 36, CT + 308, 58, 62, col=C['gray200'])
    t(d, '드래그하여 크롭 영역 조정', RPX + 108, CT + 318, fnt(11), col=C['text2'])
    t(d, '또는 직접 값을 입력하세요', RPX + 108, CT + 336, fnt(10), col=C['text3'])
    rr(d, RPX + 108, CT + 354, 120, 24, fill=C['white'], ol=C['primary'], lw=1, r=4)
    tc(d, '크롭 편집기 열기', RPX + 108, CT + 359, 120, fnt(10), col=C['primary'])

    # Text settings
    section('텍스트 설정', 406)
    t(d, '폰트', RPX + 20, CT + 442, fnt(12), col=C['text2'])
    inp(d, RPX + 58, CT + 434, 246, 30, sz=12, val='Noto Sans KR Bold')
    t(d, '크기', RPX + 20, CT + 480, fnt(12), col=C['text2'])
    inp(d, RPX + 58, CT + 472, 68, 30, sz=12, val='20')
    t(d, '색상', RPX + 144, CT + 480, fnt(12), col=C['text2'])
    rr(d, RPX + 192, CT + 474, 24, 24, fill=C['primary'], r=4)
    t(d, '불투명도', RPX + 20, CT + 522, fnt(12), col=C['text2'])
    pbar(d, RPX + 90, CT + 528, 190, 6, 100, fill=C['primary'])
    t(d, '100%', RPX + 290, CT + 522, fnt(11), col=C['text2'])

    divider(d, RPX + 12, H - 76, RP_W - 24)
    btn(d, RPX + 20, H - 58, RP_W - 40, 42, '이 사이즈 적용', sz=14)

    img.save(str(OUT / '04_size_adjustment.png'))
    print('OK: 04_size_adjustment.png')


# ════════════════════════════════════════════════════════════════
# SCREEN 05  —  캠페인 관리 대시보드
# ════════════════════════════════════════════════════════════════
def screen_05():
    img, d = new_img()
    draw_nav(d, '대시보드')

    SB_W = 220
    MX = SB_W + 24
    MW = W - MX - 24

    # ── DARK SIDEBAR ─────────────────────────────────────────────
    rr(d, 0, 64, SB_W, H - 64, fill=C['gray900'], r=0)
    t(d, '내 캠페인', 18, 84, fnt(11, bold=True), col=C['gray500'])

    campaigns5 = [
        ('5월 신상품 런칭', '진행중', True),
        ('브랜드 인지도', '일시중지', False),
        ('여름 프로모션', '예약', False),
    ]
    for ci, (cn, cs, csel) in enumerate(campaigns5):
        cy5 = 104 + ci * 72
        rr(d, 12, cy5, SB_W - 24, 58,
           fill=(31, 41, 55) if csel else (24, 33, 47), r=8)
        if csel:
            rr(d, 12, cy5, 4, 58, fill=C['primary'], r=2)
        t(d, cn[:9] + '...' if len(cn) > 9 else cn, 28, cy5 + 10,
          fnt(13, bold=csel), col=C['white'] if csel else C['gray400'])
        scol5 = C['success'] if cs == '진행중' else C['warn'] if cs == '예약' else C['gray500']
        tag(d, 28, cy5 + 34, cs, sz=10, fill=(40, 52, 64), col=scol5)

    btn(d, 16, 328, SB_W - 32, 34, '+ 새 캠페인', sz=13, fill=(31, 41, 55))

    for li, ln in enumerate(['매체 설정', '소재 관리', '리포트', '설정']):
        ly = 384 + li * 44
        t(d, ln, 24, ly + 4, fnt(13), col=C['gray500'])
        divider(d, 16, ly + 38, SB_W - 16, col=(31, 41, 55))

    # ── MAIN CONTENT ─────────────────────────────────────────────
    # Page header
    t(d, '5월 신상품 런칭', MX, 80, fnt(22, bold=True))
    tag(d, MX + 232, 86, '진행중', sz=11, fill=C['succ_l'], col=C['success'])
    t(d, '2026.05.01 ~ 05.31  |  맘카페 · 인벤  |  예산 ₩3,000,000',
      MX, 116, fnt(13), col=C['text2'])
    btn_ghost(d, W - 248, 82, 100, 34, '일시중지', sz=13, border=C['warn'], col=C['warn'])
    btn(d, W - 138, 82, 114, 34, '소재 편집', sz=13)

    divider(d, MX, 140, MW)

    # ── KPI Cards ────────────────────────────────────────────────
    kpis5 = [
        ('총 집행액', '₩1,248,000', '₩3,000,000 대비', 41.6, C['primary'], '예산 소진 41.6%'),
        ('총 노출수', '487,200', '목표 1,200,000', 40.6, C['success'], '목표 대비 40.6%'),
        ('총 클릭수', '18,512', '평균 CTR 3.8%', None, C['warn'], '업계 평균 2.1% ↑'),
        ('전환 수', '342건', 'CPA ₩3,649', None, C['danger'], '전환율 1.85%'),
    ]
    KCW = (MW - 36) // 4
    for ki, (kt, kv, ks, kp, kc, kn) in enumerate(kpis5):
        kx = MX + ki * (KCW + 12)
        ky = 156
        rr(d, kx, ky, KCW, 124, fill=C['white'], r=12)
        rr(d, kx, ky, KCW, 4, fill=kc, r=0)
        t(d, kt, kx + 16, ky + 16, fnt(12), col=C['text3'])
        t(d, kv, kx + 16, ky + 38, fnt(20, bold=True))
        t(d, ks, kx + 16, ky + 70, fnt(11), col=C['text3'])
        if kp is not None:
            pbar(d, kx + 16, ky + 90, KCW - 32, 6, kp, fill=kc)
        t(d, kn, kx + 16, ky + 104, fnt(10), col=kc)

    # ── Charts row ────────────────────────────────────────────────
    CHTOP = 300
    LCW = MW * 6 // 10
    RCW = MW - LCW - 16

    # Left: line chart
    rr(d, MX, CHTOP, LCW, 222, fill=C['white'], r=12)
    t(d, '예산 소진율 (일별)', MX + 16, CHTOP + 14, fnt(14, bold=True))
    tag(d, MX + LCW - 116, CHTOP + 16, '05.01~15 실제', sz=10, fill=C['plight'])

    GX = MX + 52
    GY = CHTOP + 48
    GW = LCW - 72
    GH = 130

    # Grid
    for gi in range(5):
        gy6 = GY + gi * GH // 4
        d.line([(GX, gy6), (GX + GW, gy6)], fill=C['gray100'], width=1)
        t(d, f'{100 - gi * 25}%', MX + 14, gy6 - 8, fnt(10), col=C['text3'])

    # X axis labels
    for day6 in [1, 5, 10, 15, 20, 25, 30]:
        dx6 = GX + int((day6 - 1) / 30 * GW)
        t(d, str(day6), dx6 - 5, GY + GH + 6, fnt(10), col=C['text3'])

    # Actual line (21 days)
    pts = []
    for day6 in range(1, 22):
        dx6 = GX + int((day6 - 1) / 30 * GW)
        spend = day6 / 30 * 1248000 * (1 + math.sin(day6 * 0.7) * 0.04)
        pct6 = min(100, spend / 3000000 * 100)
        pts.append((dx6, int(GY + GH * (1 - pct6 / 100))))
    if len(pts) > 1:
        d.line(pts, fill=C['primary'], width=3)
        # Area fill (simplified — just a few vertical lines)
        for i in range(len(pts) - 1):
            d.line([(pts[i][0], pts[i][1]), (pts[i][0], GY + GH)],
                   fill=(79, 70, 229, 30), width=1)

    # Target dashed
    for day6 in range(0, 30, 2):
        dx6 = GX + int(day6 / 30 * GW)
        dx6b = GX + int((day6 + 1) / 30 * GW)
        ty6 = int(GY + GH * (1 - day6 / 30))
        ty6b = int(GY + GH * (1 - (day6 + 1) / 30))
        d.line([(dx6, ty6), (dx6b, ty6b)], fill=C['gray300'], width=2)

    # Legend
    d.rectangle([MX + 16, CHTOP + 196, MX + 32, CHTOP + 204], fill=C['primary'])
    t(d, '실제 집행', MX + 36, CHTOP + 194, fnt(11), col=C['text2'])
    d.rectangle([MX + 118, CHTOP + 196, MX + 134, CHTOP + 204], fill=C['gray300'])
    t(d, '목표 페이스', MX + 138, CHTOP + 194, fnt(11), col=C['text2'])

    # Right: stacked bar per media
    RCX = MX + LCW + 16
    rr(d, RCX, CHTOP, RCW, 222, fill=C['white'], r=12)
    t(d, '매체별 집행 현황', RCX + 16, CHTOP + 14, fnt(14, bold=True))

    media5 = [('맘카페', 40, '₩ 499,200', C['primary']),
              ('인벤', 35, '₩ 436,800', C['success']),
              ('기타', 25, '₩ 312,000', C['gray300'])]
    bar_x5 = RCX + 16
    bar_y5 = CHTOP + 50
    bar_h5 = 148
    for i, (mn, pct7, amt, mc) in enumerate(media5):
        bh7 = int(bar_h5 * pct7 / 100)
        rr(d, bar_x5, bar_y5, 22, bh7, fill=mc, r=3)
        t(d, mn, bar_x5 + 30, bar_y5 + bh7 // 2 - 10, fnt(12))
        t(d, f'{pct7}%  {amt}', bar_x5 + 30, bar_y5 + bh7 // 2 + 6, fnt(11), col=C['text2'])
        bar_y5 += bh7 + 4

    # ── Table ─────────────────────────────────────────────────────
    TTOP = CHTOP + 238
    TH = H - TTOP - 16
    rr(d, MX, TTOP, MW, TH, fill=C['white'], r=12)
    t(d, '집행 내역', MX + 16, TTOP + 14, fnt(14, bold=True))
    btn(d, MX + MW - 148, TTOP + 12, 132, 30, '리포트 다운로드', sz=11,
        fill=C['gray100'], col=C['text2'])

    divider(d, MX + 12, TTOP + 50, MW - 24)

    COLS = ['날짜', '매체', '노출수', '클릭수', 'CTR', '집행액', '상태']
    CWS = [120, 160, 140, 110, 90, 140, 100]
    hx7 = MX + 16
    for col7, cw7 in zip(COLS, CWS):
        t(d, col7, hx7, TTOP + 58, fnt(11, bold=True), col=C['text3'])
        hx7 += cw7

    divider(d, MX + 12, TTOP + 76, MW - 24)

    rows5 = [
        ('05.15 목', '맘카페', '24,680', '1,042', '4.2%', '₩ 103,656', '완료'),
        ('05.15 목', '인벤', '18,420', '614', '3.3%', '₩ 70,000', '완료'),
        ('05.14 수', '맘카페', '22,940', '918', '4.0%', '₩ 96,348', '완료'),
        ('05.14 수', '인벤', '17,200', '568', '3.3%', '₩ 65,360', '완료'),
    ]
    for ri, row in enumerate(rows5):
        ry = TTOP + 82 + ri * 42
        if ri % 2 == 0:
            rr(d, MX + 8, ry - 2, MW - 16, 38, fill=C['gray100'], r=4)
        rx7 = MX + 16
        for ci3, (cell, cw7) in enumerate(zip(row, CWS)):
            if ci3 == 6:
                scol7 = C['success'] if cell == '완료' else C['warn']
                tag(d, rx7, ry + 8, cell, sz=10,
                    fill=C['succ_l'] if cell == '완료' else C['warn_l'], col=scol7)
            else:
                t(d, cell, rx7, ry + 11, fnt(13),
                  col=C['text2'] if ci3 == 0 else C['text'])
            rx7 += cw7

    img.save(str(OUT / '05_campaign_dashboard.png'))
    print('OK: 05_campaign_dashboard.png')


# ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('AdMix 와이어프레임 생성 시작 (5개 화면, 1440×900)\n')
    screen_01()
    screen_02()
    screen_03()
    screen_04()
    screen_05()
    print(f'\n✅ 완료! 저장 위치: {OUT}')
