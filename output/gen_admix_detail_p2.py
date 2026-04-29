# -*- coding: utf-8 -*-
"""AdMix Detail Wireframes — Part 2: screens 40~62 + sitemap"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from pathlib import Path

OUT = Path('C:/Agent/pepper/admix_wireframes')
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1440, 900

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
ORANGE  = (249, 115, 22)
ORANGE_L= (255, 237, 213)
SIDEBAR = (30,  41,  59)

_fc = {}
def fnt(sz, bold=False):
    key = (sz, bold)
    if key not in _fc:
        fp = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
        try:   _fc[key] = ImageFont.truetype(fp, sz)
        except:_fc[key] = ImageFont.load_default()
    return _fc[key]

def rr(d, x, y, w, h, fill=None, ol=None, lw=1, r=8):
    if w > 0 and h > 0:
        d.rounded_rectangle([x, y, x+w, y+h], radius=min(r, w//2, h//2),
                             fill=fill, outline=ol, width=lw)

def t(d, x, y, txt, f, fill=DARK, anchor='la'):
    d.text((x, y), str(txt), font=f, fill=fill, anchor=anchor)

def tc(d, x, y, txt, f, fill=DARK):
    d.text((x, y), str(txt), font=f, fill=fill, anchor='mm')

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

def input_box(d, x, y, w, h, placeholder='', value=''):
    rr(d, x, y, w, h, fill=WHITE, ol=GRAY3, lw=1, r=8)
    tx2 = x + 12
    ty = y + h//2
    if value:
        t(d, tx2, ty, value, fnt(14), fill=DARK, anchor='lm')
    else:
        t(d, tx2, ty, placeholder, fnt(14), fill=GRAY4, anchor='lm')

def kpi(d, x, y, w, h, label, val, chg='', up=True, acc=INDIGO):
    rr(d, x, y, w, h, fill=WHITE, ol=GRAY3, lw=1, r=12)
    t(d, x+16, y+14, label, fnt(12), fill=GRAY5)
    t(d, x+16, y+40, val, fnt(22, True), fill=DARK)
    if chg:
        col = GREEN if up else RED
        arrow = '+' if up else ''
        t(d, x+16, y+74, f'{arrow}{chg}', fnt(12, True), fill=col)

def gv(w, h, c1, c2):
    a = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        t2 = y / max(h-1, 1)
        for c in range(3): a[y,:,c] = int(c1[c]*(1-t2)+c2[c]*t2)
    return Image.fromarray(a)

def linechart(d, x, y, w, h, data, col=INDIGO, label=''):
    rr(d, x, y, w, h, fill=GRAY1, r=0)
    if not data: return
    mn, mx = min(data), max(data)
    if mx == mn: mx = mn + 1
    pts = []
    for i, v in enumerate(data):
        px2 = x + int(i/(max(len(data)-1,1))*w)
        py2 = y + h - int((v-mn)/(mx-mn)*(h-20)) - 10
        pts.append((px2, py2))
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=col, width=2)
    for px2, py2 in pts:
        d.ellipse([px2-3, py2-3, px2+3, py2+3], fill=col)

def barchart_v(d, x, y, w, h, data, labels=None, col=INDIGO):
    if not data: return
    mx = max(data) if data else 1
    bw = max(8, (w-(len(data)+1)*8)//len(data))
    for i, v in enumerate(data):
        bx = x+8+i*(bw+8)
        bh = int((v/mx)*(h-30)) if mx else 0
        by = y+h-30-bh
        rr(d, bx, by, bw, bh, fill=col, r=4)
        if labels:
            tc(d, bx+bw//2, y+h-14, labels[i], fnt(10), fill=GRAY5)

def section_title(d, x, y, title, subtitle=''):
    t(d, x, y, title, fnt(22, True), fill=DARK)
    if subtitle:
        t(d, x, y+32, subtitle, fnt(14), fill=GRAY5)

def app_nav(img, d, user='김재우'):
    rr(d, 0, 0, W, 56, fill=DARK, r=0)
    t(d, 24, 16, 'AdMix', fnt(20, True), fill=WHITE)
    t(d, W-200, 18, user, fnt(14), fill=GRAY4)
    rr(d, W-50, 16, 30, 24, fill=GRAY6, r=12)
    tc(d, W-35, 28, user[0], fnt(13, True), fill=WHITE)

def sidebar(img, d, active='dashboard'):
    rr(d, 0, 56, 220, H-56, fill=SIDEBAR, r=0)
    items = [
        ('dashboard', '대시보드'),
        ('campaign', '캠페인'),
        ('material', '소재 관리'),
        ('report', '리포트'),
        ('credit', '크레딧'),
        ('settings', '설정'),
    ]
    for i, (key, label) in enumerate(items):
        y0 = 80+i*52
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

# ================================================================
def s40_budget_campaign_info():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '예산소진 캠페인 설정', '예산을 AI가 최적 매체에 자동 배분합니다')

    rr(d, cx, cy+60, W-280, 720, fill=WHITE, ol=GRAY3, r=16)
    y = cy+84

    # Campaign name
    t(d, cx+24, y, '캠페인명 *', fnt(13, True), fill=GRAY6)
    input_box(d, cx+24, y+26, W-360, 44, '', '4월 봄 시즌 전체 채널 예산소진')
    y += 90

    # Total budget
    t(d, cx+24, y, '총 예산 *', fnt(14, True), fill=DARK)
    rr(d, cx+24, y+26, 320, 52, fill=WHITE, ol=INDIGO, lw=2, r=8)
    t(d, cx+40, y+46, '₩', fnt(20), fill=GRAY5)
    t(d, cx+68, y+44, '3,000,000', fnt(24, True), fill=DARK)
    t(d, cx+260, y+46, '원', fnt(16), fill=GRAY5)
    quick_amounts = ['₩500K', '₩1M', '₩3M', '₩5M']
    for i, qa in enumerate(quick_amounts):
        is_sel = i == 2
        rr(d, cx+360+i*120, y+32, 100, 36, fill=INDIGO if is_sel else GRAY2,
           ol=INDIGO if is_sel else GRAY3, r=8)
        tc(d, cx+360+i*120+50, y+50, qa, fnt(13, is_sel), fill=WHITE if is_sel else GRAY6)
    y += 96

    # Period
    t(d, cx+24, y, '집행 기간 *', fnt(14, True), fill=DARK)
    input_box(d, cx+24, y+26, 260, 44, '시작일', '2026.05.01')
    t(d, cx+296, y+44, '~', fnt(18), fill=GRAY4)
    input_box(d, cx+316, y+26, 260, 44, '종료일', '2026.05.31')
    t(d, cx+596, y+38, '30일', fnt(14, True), fill=INDIGO)
    y += 90

    # Auto optimize toggle
    t(d, cx+24, y, 'AI 자동 최적화', fnt(14, True), fill=DARK)
    t(d, cx+24, y+24, '매체별 성과를 실시간으로 분석해 예산을 자동 재배분합니다', fnt(13), fill=GRAY5)
    # Toggle ON
    rr(d, cx+24, y+56, 56, 28, fill=GREEN, r=14)
    d.ellipse([cx+50, y+60, cx+76, y+80], fill=WHITE)
    t(d, cx+92, y+63, 'ON — 권장', fnt(13, True), fill=GREEN)
    y += 110

    # Initial media distribution
    t(d, cx+24, y, '초기 매체 배분 (AI가 자동 조정)', fnt(14, True), fill=DARK)
    media_data = [
        ('인스타그램', 40, INDIGO),
        ('카카오', 30, AMBER),
        ('네이버', 20, GREEN),
        ('유튜브', 10, PURPLE),
    ]
    bar_total_w = W-360
    for i, (nm, pct, col) in enumerate(media_data):
        my = y+36+i*52
        t(d, cx+24, my+10, nm, fnt(13), fill=GRAY6)
        bw = int(bar_total_w*pct/100*0.7)
        rr(d, cx+160, my+8, bw, 28, fill=col, r=4)
        t(d, cx+160+bw+8, my+14, f'{pct}%', fnt(13, True), fill=DARK)
    y += 260

    # Expected
    rr(d, cx+24, y, W-328, 72, fill=INDIGO, r=12)
    t(d, cx+48, y+14, '예상 결과', fnt(14, True), fill=WHITE)
    exp = [('일평균 지출', '₩ 100,000'), ('예상 총 노출', '4.5M ~ 7.2M'), ('예상 CTR', '1.1%~1.8%'), ('예상 전환', '120~280건')]
    for i, (k, v) in enumerate(exp):
        ex = cx+48+i*280
        t(d, ex, y+36, k, fnt(11), fill=(180,180,240))
        t(d, ex, y+54, v, fnt(13, True), fill=WHITE)

    btn(d, cx+24, y+88, 200, 44, '← 이전', bg=GRAY2, fg=GRAY6)
    btn(d, W-304, y+88, 200, 44, '캠페인 시작 →', bg=INDIGO)

    fp = OUT / '40_budget_campaign_info.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s41_budget_auto_optimize():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, 'AI 자동 최적화 현황', '4월 봄 시즌 전체 채널 예산소진')

    # KPI row
    kpis = [('총 지출', '₩ 1,840,000', '61.3% 소진', False),
            ('잔여 예산', '₩ 1,160,000', '19일 남음', True),
            ('총 노출', '2,840,500', '+22.4%', True),
            ('평균 CTR', '1.48%', '+0.3%p', True)]
    kw = (W-280-40)//4-8
    for i, (lbl, val, chg, up) in enumerate(kpis):
        kpi(d, cx+i*(kw+8), cy+60, kw, 96, lbl, val, chg, up)

    # Media allocation chart
    rr(d, cx, cy+178, 500, 340, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+194, '매체별 예산 배분 현황', fnt(15, True), fill=DARK)
    t(d, cx+16, cy+214, 'AI가 성과 기반으로 자동 조정 중', fnt(11), fill=INDIGO)

    media_alloc = [
        ('인스타그램', 48, 40, INDIGO, '성과 우수로 예산 증가'),
        ('카카오', 25, 30, AMBER, '효율 하락으로 축소'),
        ('네이버', 22, 20, GREEN, '안정적 유지'),
        ('유튜브', 5, 10, PURPLE, '전환 저조로 축소'),
    ]
    for i, (nm, cur, init, col, note) in enumerate(media_alloc):
        my = cy+244+i*64
        t(d, cx+16, my, nm, fnt(13, True), fill=DARK)
        # Initial bar
        t(d, cx+130, my-2, f'초기 {init}%', fnt(10), fill=GRAY4)
        rr(d, cx+130, my+14, int(340*init/100), 12, fill=GRAY3, r=2)
        # Current bar
        t(d, cx+130, my+30, f'현재 {cur}%', fnt(10), fill=col)
        rr(d, cx+130, my+44, int(340*cur/100), 14, fill=col, r=2)
        t(d, cx+16, my+46, note, fnt(9), fill=GRAY5)

    # Adjustment history
    rr(d, cx+516, cy+178, W-280-516, 340, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+532, cy+194, '자동 조정 내역', fnt(15, True), fill=DARK)

    adj_items = [
        ('04/29 14:30', '인스타그램 +8%p 증가', '피드 CTR 2.1% 달성', GREEN),
        ('04/28 09:00', '카카오 -5%p 축소', 'CPM 대비 전환률 저조', RED),
        ('04/27 18:00', '유튜브 -5%p 축소', '조회 완료율 12% 미만', RED),
        ('04/26 12:00', '네이버 +2%p 증가', '검색 연동 전환 개선', GREEN),
        ('04/25 09:00', '초기 예산 배분 설정', '자동 최적화 시작', INDIGO),
    ]
    for i, (dt, action, reason, col) in enumerate(adj_items):
        ay = cy+222+i*58
        rr(d, cx+532, ay, W-280-532-16, 50, fill=GRAY1 if i%2==0 else WHITE, r=6)
        d.ellipse([cx+548, ay+18, cx+558, ay+28], fill=col)
        t(d, cx+568, ay+8, dt, fnt(10), fill=GRAY4)
        t(d, cx+568, ay+26, action, fnt(13, True), fill=DARK)
        t(d, cx+568, ay+42, reason, fnt(11), fill=GRAY5)

    # Performance timeline
    rr(d, cx, cy+538, W-280, 260, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+554, '일별 매체 성과 추이', fnt(15, True), fill=DARK)

    # Multi-line chart
    data_sets = [
        ([100,120,145,168,195,210,185,225,240,215,260], INDIGO, '인스타그램'),
        ([80, 90, 85, 78, 72, 68, 65, 62, 60, 58, 55], AMBER, '카카오'),
        ([60, 65, 68, 70, 72, 74, 72, 75, 78, 80, 82], GREEN, '네이버'),
    ]
    for data, col, lbl in data_sets:
        linechart(d, cx+16, cy+576, W-328, 160, data, col=col)
    # Legend
    for i, (_, col, lbl) in enumerate(data_sets):
        lx = cx+W-280-220+i*90
        d.ellipse([lx, cy+560, lx+12, cy+572], fill=col)
        t(d, lx+16, cy+558, lbl, fnt(11), fill=GRAY6)

    fp = OUT / '41_budget_auto_optimize.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s50_campaign_list():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '캠페인 목록', '내 캠페인 현황을 확인하세요')

    # Filter row
    for i, (flt, sel) in enumerate([('전체 (12)', True), ('집행중 (5)', False),
                                     ('검수중 (2)', False), ('종료 (4)', False), ('임시저장 (1)', False)]):
        is_sel = i == 0
        btn(d, cx+i*160, cy+60, 148, 34,
            flt, bg=INDIGO if is_sel else WHITE, fg=WHITE if is_sel else GRAY6, sz=13)

    # Search + new button
    input_box(d, cx, cy+108, 560, 40, '캠페인명 검색...')
    btn(d, W-360, cy+108, 200, 40, '+ 새 캠페인', bg=INDIGO)

    # Table header
    rr(d, cx, cy+164, W-280, 36, fill=GRAY2, r=8)
    headers = ['캠페인명', '유형', '매체', '기간', '예산', '노출', 'CTR', '상태', '관리']
    col_x = [cx+12, cx+260, cx+360, cx+480, cx+620, cx+720, cx+840, cx+920, cx+1040]
    for hdr, hx in zip(headers, col_x):
        t(d, hx, cy+172, hdr, fnt(12, True), fill=GRAY5)

    d.line([(cx, cy+200), (W-160, cy+200)], fill=GRAY3, width=1)

    rows = [
        ['봄 시즌 신상품 프로모션', '버티컬', '인스타·카카오', '05.01~05.31', '₩50K/일', '245,800', '1.32%', '집행중'],
        ['4월 예산소진 전채널', '예산소진', '전체 매체', '04.01~04.30', '₩3,000K', '2,840,500', '1.48%', '집행중'],
        ['신규 회원 유치 이벤트', '버티컬', '인스타그램', '04.20~05.10', '₩30K/일', '98,400', '1.67%', '검수중'],
        ['브랜드 봄 캠페인', '버티컬', '카카오·네이버', '04.01~04.30', '₩100K/일', '580,200', '1.15%', '종료'],
        ['3월 신규가입 유도', '버티컬', '인스타그램', '03.15~03.31', '₩20K/일', '320,100', '1.88%', '종료'],
    ]
    status_colors = {
        '집행중': (GREEN, GREEN_L),
        '검수중': (AMBER, AMBER_L),
        '종료': (GRAY5, GRAY2),
        '임시저장': (GRAY4, GRAY2),
    }
    for ri, row in enumerate(rows):
        ry = cy+208+ri*56
        if ri%2==0: rr(d, cx, ry, W-280, 48, fill=GRAY1, r=0)
        for j, (cell, hx) in enumerate(zip(row, col_x)):
            if j == 7:
                col, bg = status_colors.get(cell, (GRAY5, GRAY2))
                pill(d, hx, ry+14, cell, bg=bg, fg=col, sz=11)
            elif j == 5:
                t(d, hx, ry+16, cell, fnt(12), fill=GRAY6)
            else:
                t(d, hx, ry+16, cell, fnt(12), fill=GRAY6)
        # Action buttons
        btn(d, cx+1040, ry+10, 60, 28, '상세', bg=GRAY2, fg=GRAY6, sz=11)
        btn(d, cx+1110, ry+10, 50, 28, '수정', bg=GRAY2, fg=GRAY6, sz=11)

    # Pagination
    for i, p in enumerate(['<', '1', '2', '3', '4', '5', '>']):
        px2 = W//2-80+i*36
        is_cur = p == '2'
        rr(d, px2, cy+496, 32, 32, fill=INDIGO if is_cur else WHITE,
           ol=INDIGO if is_cur else GRAY3, r=6)
        tc(d, px2+16, cy+512, p, fnt(13, is_cur), fill=WHITE if is_cur else GRAY6)

    fp = OUT / '50_campaign_list.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s51_campaign_detail():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '봄 시즌 신상품 프로모션', '캠페인 상세 성과 분석')

    # Status bar
    rr(d, cx, cy+60, W-280, 56, fill=WHITE, ol=GRAY3, r=10)
    status_items = [('상태', '집행중', GREEN), ('기간', '05.01~05.31', DARK),
                    ('매체', '인스타그램·카카오', DARK), ('일예산', '₩50,000', DARK), ('소재', '3개', DARK)]
    for i, (k, v, col) in enumerate(status_items):
        sx = cx+16+i*220
        t(d, sx, cy+68, k, fnt(11), fill=GRAY4)
        t(d, sx, cy+84, v, fnt(13, True), fill=col)
    btn(d, W-400, cy+70, 80, 32, '수정', bg=GRAY2, fg=GRAY6, sz=12)
    btn(d, W-310, cy+70, 100, 32, '일시정지', bg=AMBER_L, fg=AMBER, sz=12)

    # KPI row
    kpis = [
        ('총 노출수', '245,800', '+18.2%', True),
        ('총 클릭수', '3,240', '+12.4%', True),
        ('평균 CTR', '1.32%', '+0.2%p', True),
        ('총 지출', '₩ 740,000', '14.8일', True),
        ('전환수', '128건', '+8.3%', True),
    ]
    kw = (W-300)//5-8
    for i, (lbl, val, chg, up) in enumerate(kpis):
        kpi(d, cx+i*(kw+8), cy+134, kw, 88, lbl, val, chg, up)

    # Chart area
    rr(d, cx, cy+242, W-280-520, 280, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+258, '일별 노출/클릭 추이', fnt(14, True), fill=DARK)

    data_imp = [8200,9100,7800,10200,11400,12100,10800,13200,14400,12800,15600,16800,15200,17800]
    data_clk = [108,120,102,135,150,159,141,174,189,168,205,220,199,234]
    linechart(d, cx+16, cy+284, W-280-520-32, 200, data_imp, col=INDIGO)
    linechart(d, cx+16, cy+284, W-280-520-32, 200, data_clk, col=AMBER)

    # Legend
    d.ellipse([cx+16, cy+494, cx+28, cy+506], fill=INDIGO)
    t(d, cx+32, cy+492, '노출', fnt(11), fill=GRAY6)
    d.ellipse([cx+80, cy+494, cx+92, cy+506], fill=AMBER)
    t(d, cx+96, cy+492, '클릭', fnt(11), fill=GRAY6)

    # Media breakdown (right of chart)
    rr(d, cx+W-280-512, cy+242, 500, 280, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+W-280-496, cy+258, '매체별 성과', fnt(14, True), fill=DARK)

    media_perf = [
        ('인스타그램', '154,200', '2,040', '1.32%', INDIGO),
        ('카카오', '91,600', '1,200', '1.31%', AMBER),
    ]
    mp_headers = ['매체', '노출', '클릭', 'CTR']
    mp_x = [cx+W-280-496, cx+W-280-360, cx+W-280-240, cx+W-280-130]
    for hx, hdr in zip(mp_x, mp_headers):
        t(d, hx, cy+282, hdr, fnt(11, True), fill=GRAY5)
    d.line([(cx+W-280-496, cy+300), (cx+W-280-16, cy+300)], fill=GRAY3)
    for ri, (nm, imp, clk, ctr, col) in enumerate(media_perf):
        for hx, cell in zip(mp_x, [nm, imp, clk, ctr]):
            t(d, hx, cy+312+ri*52, cell, fnt(13, ri==0), fill=col if ri==0 else GRAY6)

    # Material performance
    rr(d, cx, cy+542, W-280, 260, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+558, '소재별 성과', fnt(14, True), fill=DARK)

    mat_headers = ['소재', '타입', '노출', '클릭', 'CTR', 'CPC', '상태']
    mat_x = [cx+16, cx+220, cx+320, cx+460, cx+580, cx+680, cx+800]
    for hx, hdr in zip(mat_headers, mat_headers):
        pass
    for j, (hdr, hx) in enumerate(zip(mat_headers, mat_x)):
        t(d, hx, cy+576, hdr, fnt(11, True), fill=GRAY5)
    d.line([(cx+8, cy+594), (W-168, cy+594)], fill=GRAY3)

    mat_rows = [
        ('product_main.jpg', '이미지', '145,200', '1,920', '1.32%', '₩385', '집행중'),
        ('product_lifestyle.jpg', '이미지', '62,400', '820', '1.31%', '₩402', '집행중'),
        ('brand_video.mp4', '영상', '38,200', '500', '1.31%', '₩420', '검수중'),
    ]
    for ri, row in enumerate(mat_rows):
        ry = cy+602+ri*52
        if ri%2==0: rr(d, cx+8, ry-4, W-296, 44, fill=GRAY1, r=4)
        for j, (cell, hx) in enumerate(zip(row, mat_x)):
            if j == 6:
                col = GREEN if cell=='집행중' else AMBER
                pill(d, hx, ry+8, cell, bg=GREEN_L if cell=='집행중' else AMBER_L, fg=col, sz=11)
            else:
                t(d, hx, ry+12, cell, fnt(12), fill=GRAY6)

    fp = OUT / '51_campaign_detail.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s52_campaign_edit():
    img, d = base_app('campaign')
    cx, cy = 240, 76

    section_title(d, cx, cy, '캠페인 수정', '봄 시즌 신상품 프로모션')

    # Tabs
    tabs = ['기본 정보', '예산/기간', '타겟', '소재 관리']
    for i, tab in enumerate(tabs):
        is_sel = i == 1
        tx2 = cx+i*220
        col = INDIGO if is_sel else GRAY5
        t(d, tx2, cy+62, tab, fnt(14, is_sel), fill=col)
        if is_sel:
            d.line([(tx2, cy+82), (tx2+d.textlength(tab, font=fnt(14, True)), cy+82)], fill=INDIGO, width=3)

    d.line([(cx, cy+86), (W-160, cy+86)], fill=GRAY3)

    rr(d, cx, cy+100, W-280, 680, fill=WHITE, ol=GRAY3, r=12)
    y = cy+124

    # Period section
    t(d, cx+24, y, '집행 기간 수정', fnt(16, True), fill=DARK)
    t(d, cx+24, y+28, '현재: 2026.05.01 ~ 2026.05.31 (30일)', fnt(13), fill=GRAY5)
    y += 72

    t(d, cx+24, y, '새 종료일', fnt(13, True), fill=GRAY6)
    input_box(d, cx+24, y+26, 260, 44, '종료일', '2026.06.30')
    rr(d, cx+300, y+26, 180, 44, fill=INDIGO, r=8)
    tc(d, cx+390, y+48, '60일로 연장 (+30일)', fnt(12, True), fill=WHITE)
    t(d, cx+24, y+80, '연장 후: 2026.05.01 ~ 2026.06.30 (60일)', fnt(12), fill=GREEN)
    y += 120

    # Budget section
    t(d, cx+24, y, '예산 수정', fnt(16, True), fill=DARK)
    t(d, cx+24, y+28, '현재 일일 예산: ₩ 50,000', fnt(13), fill=GRAY5)
    y += 72

    t(d, cx+24, y, '새 일일 예산', fnt(13, True), fill=GRAY6)
    rr(d, cx+24, y+26, 260, 52, fill=WHITE, ol=INDIGO, lw=2, r=8)
    t(d, cx+40, y+46, '₩', fnt(18), fill=GRAY5)
    t(d, cx+68, y+44, '80,000', fnt(22, True), fill=DARK)
    t(d, cx+24, y+88, '변경 후 월 지출 예상: ₩ 1,680,000 (변경 전: ₩ 1,050,000)', fnt(12), fill=GRAY4)
    y += 120

    # Material swap
    t(d, cx+24, y, '소재 추가/교체', fnt(16, True), fill=DARK)
    y += 36

    # Current materials
    for i in range(3):
        mx = cx+24+i*360
        rr(d, mx, y, 340, 100, fill=WHITE, ol=GRAY3, r=8)
        rr(d, mx+12, y+12, 80, 60, fill=GRAY2, r=4)
        t(d, mx+104, y+20, f'소재 {i+1}', fnt(13, True), fill=DARK)
        t(d, mx+104, y+40, '집행중' if i < 2 else '검수중', fnt(11), fill=GREEN if i < 2 else AMBER)
        btn(d, mx+104, y+64, 80, 28, '교체', bg=GRAY2, fg=GRAY6, sz=12)
        btn(d, mx+196, y+64, 80, 28, '삭제', bg=RED_L, fg=RED, sz=12)

    rr(d, cx+24+3*360, y, 340, 100, ol=GRAY3, lw=2, r=8)
    tc(d, cx+24+3*360+170, y+50, '+ 소재 추가', fnt(14), fill=GRAY4)
    y += 120

    # Warning
    rr(d, cx+24, y, W-328, 60, fill=AMBER_L, r=10)
    t(d, cx+48, y+16, '주의: 집행 중인 캠페인을 수정하면 승인 검토 후 변경사항이 적용됩니다 (약 2~4시간 소요)', fnt(13), fill=AMBER)

    btn(d, cx+24, y+80, 180, 44, '취소', bg=GRAY2, fg=GRAY6)
    btn(d, W-304, y+80, 200, 44, '변경 저장', bg=INDIGO)

    fp = OUT / '52_campaign_edit.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s60_report_overview():
    img, d = base_app('report')
    cx, cy = 240, 76

    section_title(d, cx, cy, '통합 리포트', '전체 캠페인 성과 분석')

    # Date range + export
    rr(d, cx, cy+60, 480, 40, fill=WHITE, ol=GRAY3, r=8)
    t(d, cx+12, cy+76, '2026.04.01', fnt(13), fill=DARK)
    t(d, cx+140, cy+76, '~', fnt(14), fill=GRAY4)
    t(d, cx+160, cy+76, '2026.04.30', fnt(13), fill=DARK)
    for i, period in enumerate(['오늘', '7일', '30일', '90일']):
        is_sel = i == 2
        rr(d, cx+500+i*88, cy+60, 80, 40, fill=INDIGO if is_sel else WHITE,
           ol=INDIGO if is_sel else GRAY3, r=8)
        tc(d, cx+500+i*88+40, cy+80, period, fnt(13, is_sel), fill=WHITE if is_sel else GRAY6)
    btn(d, W-300, cy+60, 120, 40, '내보내기', bg=GRAY2, fg=GRAY6, sz=13)

    # KPI cards
    kpis = [
        ('총 노출수', '8,240,500', '+22.4%', True, INDIGO),
        ('총 클릭수', '108,320', '+15.8%', True, BLUE),
        ('평균 CTR', '1.31%', '+0.2%p', True, GREEN),
        ('총 광고비', '₩ 3,840,000', '', False, AMBER),
        ('평균 CPC', '₩ 354', '-8.2%', True, PURPLE),
    ]
    kw = (W-300)//5-8
    for i, (lbl, val, chg, up, col) in enumerate(kpis):
        rr(d, cx+i*(kw+8), cy+120, kw, 96, fill=WHITE, ol=GRAY3, r=12)
        rr(d, cx+i*(kw+8), cy+120, 4, 96, fill=col, r=12)
        t(d, cx+i*(kw+8)+16, cy+136, lbl, fnt(11), fill=GRAY5)
        t(d, cx+i*(kw+8)+16, cy+160, val, fnt(18, True), fill=DARK)
        if chg:
            c2 = GREEN if up else RED
            t(d, cx+i*(kw+8)+16, cy+188, chg, fnt(11, True), fill=c2)

    # Main chart — impressions by media
    rr(d, cx, cy+236, W-280-440, 340, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+252, '매체별 일별 노출 추이', fnt(15, True), fill=DARK)
    data_sets = [
        ([80,90,85,105,120,115,130,145,135,155,170,160,180,195,185,205,220,210,230,245,235,255,270,260,280,290,285,300,315,310], INDIGO, '인스타그램'),
        ([50,55,52,60,65,62,70,75,72,80,85,82,90,95,92,100,105,102,110,115,112,120,125,122,130,135,132,140,145,142], AMBER, '카카오'),
        ([30,32,31,35,38,36,40,42,41,45,47,46,50,52,51,55,57,56,60,62,61,65,67,66,70,72,71,75,77,76], GREEN, '네이버'),
    ]
    for data, col, lbl in data_sets:
        linechart(d, cx+16, cy+276, W-280-440-32, 268, data[:30], col=col)
    for i, (_, col, lbl) in enumerate(data_sets):
        lx = cx+16+i*150
        d.ellipse([lx, cy+558, lx+12, cy+570], fill=col)
        t(d, lx+16, cy+556, lbl, fnt(11), fill=GRAY6)

    # Media comparison bar
    rr(d, cx+W-280-432, cy+236, 420, 340, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+W-280-416, cy+252, '매체별 성과 비교', fnt(15, True), fill=DARK)

    media_comp = [
        ('인스타그램', 4840500, INDIGO),
        ('카카오', 2150300, AMBER),
        ('네이버', 980200, GREEN),
        ('유튜브', 270000, PURPLE),
    ]
    barchart_v(d, cx+W-280-416, cy+280, 400, 268, [v for _, v, _ in media_comp],
               labels=[n for n, _, _ in media_comp],
               col=INDIGO)

    # Summary table
    rr(d, cx, cy+596, W-280, 220, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+612, '캠페인별 성과 요약', fnt(15, True), fill=DARK)
    headers2 = ['캠페인', '기간', '노출', '클릭', 'CTR', '광고비', 'CPC']
    hx2 = [cx+16, cx+220, cx+380, cx+520, cx+620, cx+720, cx+860]
    for hdr, hx in zip(headers2, hx2):
        t(d, hx, cy+636, hdr, fnt(11, True), fill=GRAY5)
    d.line([(cx+8, cy+654), (W-168, cy+654)], fill=GRAY3)
    rows2 = [
        ('봄 시즌 신상품', '05.01~05.31', '245,800', '3,240', '1.32%', '₩740K', '₩229'),
        ('4월 예산소진', '04.01~04.30', '5,840,500', '86,200', '1.48%', '₩2,400K', '₩279'),
        ('신규 회원 유치', '04.20~05.10', '98,400', '1,640', '1.67%', '₩400K', '₩244'),
        ('브랜드 봄', '04.01~04.30', '2,056,000', '24,800', '1.21%', '₩3,100K', '₩125'),
    ]
    for ri, row in enumerate(rows2):
        ry = cy+662+ri*38
        if ri%2==0: rr(d, cx+8, ry-2, W-296, 32, fill=GRAY1, r=4)
        for cell, hx in zip(row, hx2):
            t(d, hx, ry+6, cell, fnt(11), fill=GRAY6)

    fp = OUT / '60_report_overview.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s61_report_material():
    img, d = base_app('report')
    cx, cy = 240, 76

    section_title(d, cx, cy, '소재별 성과 리포트', '소재별 상세 성과를 분석합니다')

    # Period selector
    rr(d, cx, cy+60, 480, 40, fill=WHITE, ol=GRAY3, r=8)
    t(d, cx+12, cy+76, '2026.04.01 ~ 2026.04.30', fnt(13), fill=DARK)
    for i, period in enumerate(['7일', '30일', '90일']):
        is_sel = i == 1
        rr(d, cx+500+i*88, cy+60, 80, 40, fill=INDIGO if is_sel else WHITE,
           ol=INDIGO if is_sel else GRAY3, r=8)
        tc(d, cx+500+i*88+40, cy+80, period, fnt(13, is_sel), fill=WHITE if is_sel else GRAY6)

    # Filter by campaign
    rr(d, W-380, cy+60, 220, 40, fill=WHITE, ol=GRAY3, r=8)
    t(d, W-364, cy+76, '전체 캠페인', fnt(13), fill=DARK)
    t(d, W-180, cy+76, '▾', fnt(12), fill=GRAY4)

    # Top performing materials
    rr(d, cx, cy+120, W-280, 180, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+136, '소재별 성과 비교 (CTR 기준)', fnt(15, True), fill=DARK)

    materials = ['product_main', 'lifestyle_shot', 'brand_video', 'promo_banner', 'story_ad']
    ctrs = [1.67, 1.52, 1.38, 1.24, 1.08]
    cpms = [2840, 3120, 2680, 2900, 2450]
    barchart_v(d, cx+16, cy+158, W-328, 120, ctrs, labels=materials, col=INDIGO)

    # Detailed table
    rr(d, cx, cy+320, W-280, 500, fill=WHITE, ol=GRAY3, r=12)
    t(d, cx+16, cy+336, '소재 상세 성과', fnt(15, True), fill=DARK)

    headers3 = ['소재', '유형', '캠페인', '노출수', '클릭수', 'CTR', 'CPM', 'CPC', '전환', '상태']
    hx3 = [cx+16, cx+160, cx+260, cx+400, cx+520, cx+620, cx+720, cx+820, cx+920, cx+1020]
    for hdr, hx in zip(headers3, hx3):
        t(d, hx, cy+360, hdr, fnt(10, True), fill=GRAY5)
    d.line([(cx+8, cy+378), (W-168, cy+378)], fill=GRAY3)

    mat_rows2 = [
        ('product_main.jpg', '이미지', '봄 시즌', '145,200', '2,426', '1.67%', '₩2,840', '₩170', '48', '집행중'),
        ('lifestyle_shot.jpg', '이미지', '봄 시즌', '62,400', '949', '1.52%', '₩3,120', '₩205', '22', '집행중'),
        ('brand_video.mp4', '영상', '예산소진', '2,840,500', '39,204', '1.38%', '₩2,680', '₩194', '312', '집행중'),
        ('promo_banner.jpg', '이미지', '예산소진', '1,450,200', '17,982', '1.24%', '₩2,900', '₩234', '189', '집행중'),
        ('story_ad.jpg', '이미지', '신규유치', '98,400', '1,063', '1.08%', '₩2,450', '₩227', '31', '검수중'),
    ]
    for ri, row in enumerate(mat_rows2):
        ry = cy+386+ri*60
        if ri%2==0: rr(d, cx+8, ry-4, W-296, 52, fill=GRAY1, r=4)
        # Thumbnail
        rr(d, cx+16, ry+4, 40, 40, fill=GRAY3, r=4)
        for j, (cell, hx) in enumerate(zip(row, hx3)):
            if j == 0:
                t(d, cx+62, ry+14, cell[:14], fnt(11, True), fill=DARK)
            elif j == 9:
                col = GREEN if cell=='집행중' else AMBER
                pill(d, hx, ry+12, cell, bg=GREEN_L if cell=='집행중' else AMBER_L, fg=col, sz=10)
            else:
                t(d, hx, ry+14, cell, fnt(11), fill=GRAY6)

    fp = OUT / '61_report_material.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def s62_report_export():
    img, d = base_app('report')
    cx, cy = 240, 76

    section_title(d, cx, cy, '리포트 내보내기', '성과 데이터를 다양한 형식으로 내보냅니다')

    rr(d, cx, cy+60, W-280, 720, fill=WHITE, ol=GRAY3, r=16)
    y = cy+84

    # Report type
    t(d, cx+24, y, '리포트 유형', fnt(15, True), fill=DARK)
    types = [
        ('통합 리포트', '전체 캠페인 통합 성과', True),
        ('캠페인별', '캠페인 단위 상세 분석', False),
        ('소재별', '소재 단위 성과 분석', False),
        ('매체별', '매체별 성과 비교', False),
    ]
    for i, (nm, desc, sel) in enumerate(types):
        tx2 = cx+24+i*280
        rr(d, tx2, y+32, 260, 72, fill=INDIGO if sel else WHITE,
           ol=INDIGO if sel else GRAY3, lw=2 if sel else 1, r=8)
        t(d, tx2+16, y+46, nm, fnt(14, True), fill=WHITE if sel else DARK)
        t(d, tx2+16, y+68, desc, fnt(11), fill=(200,200,255) if sel else GRAY4)
    y += 126

    # Period
    t(d, cx+24, y, '기간 선택', fnt(15, True), fill=DARK)
    input_box(d, cx+24, y+32, 240, 44, '시작일', '2026.04.01')
    t(d, cx+280, y+50, '~', fnt(18), fill=GRAY4)
    input_box(d, cx+300, y+32, 240, 44, '종료일', '2026.04.30')
    for i, period in enumerate(['이번달', '지난달', '최근 3개월', '직접 입력']):
        is_sel = i == 1
        rr(d, cx+560+i*168, y+32, 156, 44, fill=INDIGO if is_sel else GRAY2,
           ol=INDIGO if is_sel else GRAY3, r=8)
        tc(d, cx+560+i*168+78, y+54, period, fnt(12, is_sel), fill=WHITE if is_sel else GRAY6)
    y += 100

    # Metrics
    t(d, cx+24, y, '포함 지표', fnt(15, True), fill=DARK)
    metrics = ['노출수', '클릭수', 'CTR', 'CPM', 'CPC', '광고비', '전환수', '전환율', 'ROAS', '빈도수']
    xpos = cx+24
    row2_start = False
    for i, metric in enumerate(metrics):
        if xpos + 120 > cx+W-320:
            xpos = cx+24
            y += 44
        is_sel = metric in ['노출수', '클릭수', 'CTR', '광고비', '전환수', 'ROAS']
        tw2 = int(d.textlength(metric, font=fnt(12, True)))+24
        rr(d, xpos, y+32, tw2, 36, fill=INDIGO if is_sel else WHITE,
           ol=INDIGO if is_sel else GRAY3, r=18)
        tc(d, xpos+tw2//2, y+50, metric, fnt(12, True), fill=WHITE if is_sel else GRAY6)
        xpos += tw2+10
    y += 90

    # Format
    t(d, cx+24, y, '출력 형식', fnt(15, True), fill=DARK)
    formats = [
        ('Excel (.xlsx)', '데이터 분석에 최적', True, INDIGO),
        ('CSV', '외부 툴 연동', False, GREEN),
        ('PDF', '보고용 문서', False, RED),
        ('Google Sheets', '실시간 공유', False, BLUE),
    ]
    for i, (fmt, desc, sel, col) in enumerate(formats):
        fx = cx+24+i*280
        rr(d, fx, y+32, 260, 72, fill=col if sel else WHITE,
           ol=col if sel else GRAY3, lw=2 if sel else 1, r=8)
        t(d, fx+16, y+46, fmt, fnt(14, True), fill=WHITE if sel else DARK)
        t(d, fx+16, y+68, desc, fnt(11), fill=(200,200,255) if sel else GRAY4)
    y += 126

    # Preview
    rr(d, cx+24, y, W-328, 80, fill=GRAY1, r=8)
    t(d, cx+40, y+16, '미리보기: 통합 리포트 | 2026.04.01 ~ 04.30 | 6개 지표 | Excel', fnt(13), fill=GRAY6)
    t(d, cx+40, y+40, '예상 파일 크기: 약 240KB | 예상 행 수: 1,240행', fnt(12), fill=GRAY4)
    btn(d, W-304, y+16, 160, 44, '파일 열기 미리보기', bg=GRAY2, fg=GRAY6, sz=12)
    y += 100

    # Export buttons
    btn(d, cx+24, y, W-328-120, 52, 'Excel로 내보내기', bg=INDIGO, sz=16)
    btn(d, W-304, y, 160, 52, '이메일로 전송', bg=GRAY2, fg=GRAY6, sz=14)

    fp = OUT / '62_report_export.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

def sitemap():
    """Full sitemap image"""
    SW, SH = 1440, 900
    img = Image.new('RGB', (SW, SH), (250, 250, 252))
    d = ImageDraw.Draw(img)

    # Title
    tc(d, SW//2, 32, 'AdMix 플랫폼 사이트맵', fnt(24, True), fill=DARK)
    t(d, 40, 56, '버티컬 광고매체 플랫폼 | AI 소재 자동최적화', fnt(13), fill=GRAY5)

    # Color legend
    legend = [
        ('공통', (150,150,150)),
        ('광고주 대시보드', BLUE),
        ('캠페인 생성', GREEN),
        ('소재/AI', PURPLE),
        ('리포트', ORANGE),
    ]
    for i, (lbl, col) in enumerate(legend):
        lx = SW-600+i*110
        rr(d, lx, 16, 14, 14, fill=col, r=3)
        t(d, lx+18, 14, lbl, fnt(10), fill=GRAY6)

    # Node drawing helper
    def node(x, y, w, h, label, col=(150,150,150), sz=11, sub=''):
        rr(d, x, y, w, h, fill=col, r=6)
        lines = label.split('\n')
        for i, line in enumerate(lines):
            ty = y+h//2 - (len(lines)-1)*7 + i*14
            tc(d, x+w//2, ty, line, fnt(sz, True), fill=WHITE)
        if sub:
            tc(d, x+w//2, y+h+10, sub, fnt(8), fill=GRAY5)

    def arrow(x1, y1, x2, y2):
        d.line([(x1, y1), (x2, y2)], fill=GRAY4, width=1)
        # Arrowhead
        import math
        angle = math.atan2(y2-y1, x2-x1)
        for da in [0.4, -0.4]:
            ax = x2 - 8*math.cos(angle-da)
            ay = y2 - 8*math.sin(angle-da)
            d.line([(x2, y2), (int(ax), int(ay))], fill=GRAY4, width=1)

    # ─ Landing (top center)
    node(SW//2-60, 78, 120, 32, '랜딩', (100,100,120))
    node(SW//2-180, 78, 110, 32, '서비스 소개', (120,120,130))
    node(SW//2+70, 78, 110, 32, '요금제', (120,120,130))

    # Auth row
    node(SW//2-60, 140, 120, 30, '로그인 / 회원가입', (120,120,140))
    arrow(SW//2, 110, SW//2, 140)

    # Main Dashboard
    node(SW//2-80, 200, 160, 32, '메인 대시보드', BLUE)
    arrow(SW//2, 170, SW//2, 200)

    # Branch lines from dashboard
    branches = [
        (SW//2-80+80, 232, SW//2-80+80, 260),  # center-down
    ]

    # Level 3 — main sections
    sections = [
        (60,  260, 160, 30, '크레딧 관리', BLUE),
        (260, 260, 160, 30, '캠페인 목록', GREEN),
        (500, 260, 160, 30, '소재 관리', PURPLE),
        (700, 260, 160, 30, '리포트', ORANGE),
        (940, 260, 160, 30, '설정', (130,130,150)),
    ]
    for sx, sy, sw2, sh2, lbl, col in sections:
        node(sx, sy, sw2, sh2, lbl, col)
        # line from dashboard
        mx = sx+sw2//2
        d.line([(SW//2, 232), (mx, 260)], fill=GRAY3, width=1)

    # Sub-nodes for each section
    CREDIT_X = 60
    credit_subs = [('충전 화면', 80, 316), ('내역 조회', 180, 316)]
    for lbl, sx, sy in credit_subs:
        node(sx-10, sy, 100, 26, lbl, BLUE_L if True else BLUE, sz=9, sub='')
        rr(d, sx-10, sy, 100, 26, fill=BLUE, r=4)
        tc(d, sx+40, sy+13, lbl, fnt(9, True), fill=WHITE)
        mid_x = 60+160//2
        arrow(mid_x, 290, sx+40, 316)

    # Campaign subs
    camp_x = 260
    camp_subs = [
        (220, 316, '유형 선택'),
        (340, 316, '버티컬 설정'),
        (460, 316, '예산소진 설정'),
    ]
    for sx, sy, lbl in camp_subs:
        rr(d, sx, sy, 110, 26, fill=GREEN, r=4)
        tc(d, sx+55, sy+13, lbl, fnt(9, True), fill=WHITE)
        arrow(camp_x+80, 290, sx+55, 316)

    # Vertical sub-steps
    vsteps = [
        (200, 370, '기본 정보'),
        (280, 370, '타겟 설정'),
        (360, 370, '예산 설정'),
        (440, 370, '매체 선택'),
    ]
    for sx, sy, lbl in vsteps:
        rr(d, sx, sy, 72, 22, fill=(80,160,100), r=4)
        tc(d, sx+36, sy+11, lbl, fnt(8, True), fill=WHITE)
        arrow(340+55, 342, sx+36, 370)

    # Material subs
    mat_x = 500
    mat_subs = [
        (470, 316, '소재 업로드'),
        (590, 316, '사이즈 선택'),
        (710, 316, 'AI 크롭'),
    ]
    for sx, sy, lbl in mat_subs:
        rr(d, sx, sy, 108, 26, fill=PURPLE, r=4)
        tc(d, sx+54, sy+13, lbl, fnt(9, True), fill=WHITE)
        arrow(mat_x+80, 290, sx+54, 316)

    mat_subs2 = [
        (466, 370, 'AI 후킹 생성'),
        (586, 370, '매체 미리보기'),
        (706, 370, '최종 확인'),
    ]
    for sx, sy, lbl in mat_subs2:
        rr(d, sx, sy, 108, 22, fill=(100,60,180), r=4)
        tc(d, sx+54, sy+11, lbl, fnt(8, True), fill=WHITE)

    # Report subs
    rep_x = 700
    rep_subs = [
        (680, 316, '통합 리포트'),
        (800, 316, '소재별 리포트'),
        (920, 316, '내보내기'),
    ]
    for sx, sy, lbl in rep_subs:
        rr(d, sx, sy, 108, 26, fill=ORANGE, r=4)
        tc(d, sx+54, sy+13, lbl, fnt(9, True), fill=WHITE)
        arrow(rep_x+80, 290, sx+54, 316)

    # Campaign detail / edit
    rr(d, 220, 414, 110, 26, fill=(60,140,80), r=4)
    tc(d, 275, 427, '캠페인 상세', fnt(9, True), fill=WHITE)
    rr(d, 340, 414, 110, 26, fill=(60,140,80), r=4)
    tc(d, 395, 427, '캠페인 수정', fnt(9, True), fill=WHITE)
    arrow(220+55, 342, 275, 414)
    arrow(220+55, 342, 395, 414)

    # Flow labels
    flow_labels = [
        (SW//2-420, 460, '신규가입 플로우: 랜딩 → 회원가입 → 온보딩 → 대시보드', INDIGO2),
        (SW//2-420, 484, '캠페인 생성 플로우: 대시보드 → 유형선택 → 기본정보 → 타겟 → 예산 → 매체 → 소재업로드', GREEN),
        (SW//2-420, 508, 'AI 소재 자동화 플로우: 소재업로드 → 사이즈선택 → AI크롭 → AI후킹생성 → 미리보기 → 최종확인', PURPLE),
    ]
    rr(d, 40, 448, SW-80, 96, fill=WHITE, ol=GRAY3, r=8)
    t(d, 60, 452, '주요 사용자 플로우', fnt(13, True), fill=DARK)
    for x, y2, lbl, col in flow_labels:
        d.ellipse([x, y2+4, x+10, y2+14], fill=col)
        t(d, x+16, y2, lbl, fnt(10), fill=GRAY6)

    # Page count summary
    rr(d, 40, 558, SW-80, 80, fill=INDIGO, r=12)
    tc(d, SW//2, 578, '총 28개 화면 | 공통 4 · 대시보드 3 · 캠페인 생성 5 · 소재/AI 6 · 예산소진 2 · 캠페인관리 3 · 리포트 3 · 사이트맵 1', fnt(14, True), fill=WHITE)
    tc(d, SW//2, 608, '인디고 컬러 시스템 #6366F1 | Malgun Gothic | 1440x900px 데스크탑 기준', fnt(12), fill=(200,200,255))

    # Bottom: screen index
    t(d, 40, 660, '화면 인덱스', fnt(14, True), fill=DARK)
    index_items = [
        '00_landing', '01_service_intro', '02_login', '03_signup',
        '10_dashboard', '11_credit_charge', '12_credit_history',
        '20_campaign_type', '21_campaign_info', '22_target', '23_budget', '24_media_select',
        '30_material_upload', '31_size_select', '32_ai_crop', '33_ai_hook', '34_preview', '35_confirm',
        '40_budget_info', '41_auto_optimize',
        '50_campaign_list', '51_campaign_detail', '52_campaign_edit',
        '60_report_overview', '61_report_material', '62_report_export', 'sitemap',
    ]
    for i, item in enumerate(index_items):
        ix = 40 + (i%9)*166
        iy = 684 + (i//9)*28
        col = [INDIGO, BLUE, GREEN, PURPLE, ORANGE, (100,100,120)][(i//4)%6]
        rr(d, ix, iy, 156, 22, fill=col, r=4)
        t(d, ix+6, iy+5, item, fnt(8, True), fill=WHITE)

    fp = OUT / 'sitemap.png'
    img.save(fp)
    assert fp.exists()
    print(f'OK {fp}')

# ── Run ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    funcs = [
        s40_budget_campaign_info, s41_budget_auto_optimize,
        s50_campaign_list, s51_campaign_detail, s52_campaign_edit,
        s60_report_overview, s61_report_material, s62_report_export,
        sitemap,
    ]
    for fn in funcs:
        try:
            fn()
        except Exception as e:
            print(f'FAIL {fn.__name__}: {e}')
            import traceback; traceback.print_exc()

    print(f'\nPart 2 done: {len(funcs)} screens')
