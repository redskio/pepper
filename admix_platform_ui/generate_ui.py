"""AdMix Platform UI Image Generator — Pillow-based"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"C:\Agent\pepper\admix_platform_ui"
FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\malgunbd.ttf"  # malgun bold

# ── colours ──────────────────────────────────────────────
BG        = (15, 23, 41)         # #0F1729
ACCENT    = (45, 111, 247)       # #2D6FF7
ACCENT2   = (99, 150, 255)       # lighter accent
WHITE     = (255, 255, 255)
GRAY      = (148, 163, 184)
GRAY_DIM  = (71, 85, 105)
CARD_BG   = (22, 34, 60)         # slightly lighter than BG
CARD_BG2  = (30, 45, 80)
BORDER    = (45, 64, 100)
SUCCESS   = (34, 197, 94)
WARN      = (251, 191, 36)
HERO_GRAD = (20, 40, 90)
DARK_CARD = (18, 28, 50)

def font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_PATH
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.truetype(FONT_PATH, size)

def draw_rect(draw, x, y, w, h, fill, radius=8, border=None, border_width=1):
    """Draw rounded rectangle."""
    draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill,
                            outline=border, width=border_width)

def draw_button(draw, x, y, w, h, text, f, fill=ACCENT, text_color=WHITE, radius=6):
    draw_rect(draw, x, y, w, h, fill, radius=radius)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text((x + (w-tw)//2, y + (h-th)//2 - 1), text, font=f, fill=text_color)

def draw_nav(draw, W, y0, active=""):
    """Draw consistent navigation bar."""
    nav_h = 64
    # nav background
    draw.rectangle([0, y0, W, y0+nav_h], fill=(12, 18, 35))
    draw.line([0, y0+nav_h-1, W, y0+nav_h-1], fill=BORDER, width=1)
    # logo
    f_logo = font(20, bold=True)
    draw.text((48, y0+20), "AdMix", font=f_logo, fill=WHITE)
    draw.ellipse([40, y0+18, 56, y0+34], fill=ACCENT)
    draw.text((41, y0+18), "A", font=font(12, bold=True), fill=WHITE)
    # nav items
    f_nav = font(14)
    items = ["서비스 소개", "매체 현황", "요금제"]
    nx = 200
    for item in items:
        draw.text((nx, y0+24), item, font=f_nav, fill=GRAY)
        nx += 110
    # CTA button right
    draw_button(draw, W-196, y0+16, 148, 32, "광고 관리 시작하기", font(13, bold=True), radius=6)
    return y0 + nav_h

def draw_shadow_card(draw, x, y, w, h, fill=CARD_BG, radius=12):
    # fake shadow by drawing slightly larger dark rect first
    draw.rounded_rectangle([x+3, y+3, x+w+3, y+h+3], radius=radius, fill=(8,14,28))
    draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill, outline=BORDER, width=1)

def draw_badge(draw, x, y, text, f, fill=ACCENT, text_color=WHITE):
    bb = draw.textbbox((0,0), text, font=f)
    tw = bb[2]-bb[0]
    pw = 12
    draw_rect(draw, x, y, tw+pw*2, 24, fill=fill, radius=12)
    draw.text((x+pw, y+4), text, font=f, fill=text_color)
    return tw + pw*2


# ═══════════════════════════════════════════════════════════
#  1. LANDING PAGE  (1440 × 3200)
# ═══════════════════════════════════════════════════════════
def make_landing():
    W, H = 1440, 3200
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ── NAV ──────────────────────────────────────────────
    y = draw_nav(draw, W, 0)

    # ── HERO ─────────────────────────────────────────────
    # gradient-ish background for hero
    for i in range(600):
        t = i / 600
        r = int(BG[0] + (HERO_GRAD[0]-BG[0])*t)
        g = int(BG[1] + (HERO_GRAD[1]-BG[1])*t)
        b = int(BG[2] + (HERO_GRAD[2]-BG[2])*t)
        draw.line([0, y+i, W, y+i], fill=(r, g, b))
    # hero accent glow blob
    for r_size in range(300, 0, -10):
        alpha = int(8 * (1 - r_size/300))
        draw.ellipse([W//2-r_size, y+180-r_size//2, W//2+r_size, y+180+r_size//2],
                     fill=(45, 111, 247, alpha))

    hero_y = y + 80
    # badge
    draw_badge(draw, W//2-100, hero_y, "AI 기반 버티컬 광고 플랫폼", font(13), fill=(30, 60, 120))
    hero_y += 48

    # headline
    f_h1 = font(56, bold=True)
    line1 = "버티컬 매체 광고,"
    line2 = "이제 AI가 알아서 합니다"
    for i, line in enumerate([line1, line2]):
        bb = draw.textbbox((0,0), line, font=f_h1)
        tw = bb[2]-bb[0]
        draw.text(((W-tw)//2, hero_y + i*72), line, font=f_h1, fill=WHITE)
    hero_y += 170

    # sub copy
    f_sub = font(20)
    sub = "맘카페, 인벤 등 버티컬 매체에 소재 자동 제작부터 집행까지. 대행사 없이 혼자 해도 됩니다."
    bb = draw.textbbox((0,0), sub, font=f_sub)
    tw = bb[2]-bb[0]
    draw.text(((W-tw)//2, hero_y), sub, font=f_sub, fill=GRAY)
    hero_y += 52

    # CTA buttons
    btn_w, btn_h = 200, 52
    gap = 20
    total = btn_w*2 + gap
    bx = (W-total)//2
    draw_button(draw, bx, hero_y, btn_w, btn_h, "무료 체험 시작", font(16, bold=True), fill=ACCENT, radius=8)
    draw_button(draw, bx+btn_w+gap, hero_y, btn_w, btn_h, "서비스 소개 보기", font(16), fill=(35,50,85), text_color=GRAY, radius=8)
    # border on second button
    draw.rounded_rectangle([bx+btn_w+gap, hero_y, bx+btn_w+gap+btn_w, hero_y+btn_h], radius=8, outline=BORDER, width=1)
    hero_y += 90

    # ── HERO SCREEN MOCKUP ────────────────────────────────
    mock_w, mock_h = 900, 340
    mock_x = (W-mock_w)//2
    draw_shadow_card(draw, mock_x, hero_y, mock_w, mock_h, fill=CARD_BG, radius=12)
    # mock nav bar in mockup
    draw.rectangle([mock_x, hero_y, mock_x+mock_w, hero_y+36], fill=(18,28,50))
    for cx, col in [(mock_x+14, (237,99,85)), (mock_x+30, (251,191,36)), (mock_x+46, (52,199,89))]:
        draw.ellipse([cx, hero_y+12, cx+12, hero_y+24], fill=col)
    # mock content inside
    my = hero_y + 50
    # left panel (sizes)
    draw_shadow_card(draw, mock_x+16, my, 180, 260, fill=DARK_CARD, radius=8)
    draw.text((mock_x+30, my+14), "사이즈 목록", font=font(11, bold=True), fill=GRAY)
    sizes = [("맘카페 728×90", True), ("맘카페 300×250", True), ("인벤 970×90", False), ("인벤 300×600", False)]
    for si, (sz, chk) in enumerate(sizes):
        sy = my + 42 + si*40
        col = ACCENT if chk else GRAY_DIM
        draw.rounded_rectangle([mock_x+26, sy, mock_x+38, sy+12], radius=3, fill=col)
        draw.text((mock_x+46, sy-1), sz, font=font(10), fill=WHITE if chk else GRAY_DIM)
    # center canvas
    cx_start = mock_x+210
    draw_shadow_card(draw, cx_start, my, 460, 260, fill=DARK_CARD, radius=8)
    # ad preview inside canvas
    draw.rounded_rectangle([cx_start+20, my+20, cx_start+440, my+80], radius=4, fill=ACCENT)
    draw.text((cx_start+160, my+40), "728 × 90 배너 프리뷰", font=font(12), fill=WHITE)
    # 300x250
    draw.rounded_rectangle([cx_start+20, my+100, cx_start+170, my+240], radius=4, fill=(30,50,100))
    draw.text((cx_start+40, my+162), "300×250", font=font(11), fill=GRAY)
    # toolbar
    for ti, tb in enumerate(["크롭", "위치", "텍스트", "배경"]):
        tx = cx_start + 200 + ti*60
        draw_rect(draw, tx, my+210, 50, 28, fill=(35,55,100), radius=5)
        draw.text((tx+8, my+218), tb, font=font(10), fill=GRAY)
    # right panel (AI copy)
    draw_shadow_card(draw, mock_x+684, my, 200, 260, fill=DARK_CARD, radius=8)
    draw.text((mock_x+698, my+14), "AI 후킹 문구", font=font(11, bold=True), fill=GRAY)
    tones = [("임팩트형", True), ("친근형", False), ("프리미엄형", False)]
    for ti, (tone, act) in enumerate(tones):
        tx = mock_x+694 + ti*58
        col = ACCENT if act else (35,50,85)
        draw_rect(draw, tx, my+36, 52, 22, fill=col, radius=11)
        draw.text((tx+4, my+40), tone, font=font(9), fill=WHITE)
    copies = ["지금 가입하면 첫 달 무료!", "우리 동네 맘들이 선택한", "프리미엄 경험을 합리적으로"]
    for ci, cp in enumerate(copies):
        cy2 = my + 72 + ci*56
        draw_rect(draw, mock_x+694, cy2, 184, 44, fill=(25,40,75), radius=6, border=BORDER, border_width=1)
        draw.text((mock_x+702, cy2+8), cp[:12], font=font(10), fill=WHITE)
        draw.text((mock_x+702, cy2+24), "[적용]", font=font(9), fill=ACCENT)

    hero_y += mock_h + 60

    # ── STATS ROW ─────────────────────────────────────────
    draw.line([0, hero_y, W, hero_y], fill=BORDER, width=1)
    stats = [("2,000+", "등록 광고주"), ("15개+", "제휴 버티컬 매체"), ("3.2배", "평균 CTR 향상률"), ("5분", "평균 캠페인 세팅 시간")]
    sw = W // len(stats)
    for si, (val, label) in enumerate(stats):
        sx = si*sw + sw//2
        f_val = font(36, bold=True)
        bb = draw.textbbox((0,0), val, font=f_val)
        draw.text((sx - (bb[2]-bb[0])//2, hero_y+30), val, font=f_val, fill=ACCENT2)
        bb2 = draw.textbbox((0,0), label, font=font(14))
        draw.text((sx - (bb2[2]-bb2[0])//2, hero_y+76), label, font=font(14), fill=GRAY)
    hero_y += 130

    # ── FEATURES ─────────────────────────────────────────
    draw.line([0, hero_y, W, hero_y], fill=BORDER, width=1)
    hero_y += 60
    f_sec = font(36, bold=True)
    sec_title = "AdMix의 핵심 기능"
    bb = draw.textbbox((0,0), sec_title, font=f_sec)
    draw.text(((W-(bb[2]-bb[0]))//2, hero_y), sec_title, font=f_sec, fill=WHITE)
    hero_y += 54
    sec_sub = "복잡한 광고 대행 과정을 AI가 자동화합니다"
    bb = draw.textbbox((0,0), sec_sub, font=font(18))
    draw.text(((W-(bb[2]-bb[0]))//2, hero_y), sec_sub, font=font(18), fill=GRAY)
    hero_y += 70

    features = [
        ("🤖", "AI 소재 자동 편집",
         "제품 이미지 1장 업로드로\n후킹 문구 자동 생성 + 텍스트\n레이어 자동 최적화"),
        ("📐", "매체별 사이즈 자동 조정",
         "맘카페 728×90부터 인벤\n300×600까지 1클릭으로\n전체 사이즈 자동 변환"),
        ("🎯", "룰베이스 매체 매칭",
         "업종 × 예산 × 타겟 조건\n으로 최적 버티컬 매체를\n자동으로 추천"),
    ]
    card_w = 380
    total_cw = card_w*3 + 40*2
    cx0 = (W - total_cw)//2
    for fi, (icon, title, desc) in enumerate(features):
        fx = cx0 + fi*(card_w+40)
        draw_shadow_card(draw, fx, hero_y, card_w, 280, fill=CARD_BG, radius=14)
        # icon circle
        draw.ellipse([fx+28, hero_y+28, fx+76, hero_y+76], fill=(30,60,130))
        draw.text((fx+36, hero_y+33), icon, font=font(24), fill=WHITE)
        draw.text((fx+28, hero_y+94), title, font=font(20, bold=True), fill=WHITE)
        # accent underline
        draw.line([fx+28, hero_y+124, fx+60, hero_y+124], fill=ACCENT, width=3)
        for li, line in enumerate(desc.split('\n')):
            draw.text((fx+28, hero_y+140+li*26), line, font=font(14), fill=GRAY)
    hero_y += 330

    # ── HOW IT WORKS ─────────────────────────────────────
    draw.line([0, hero_y, W, hero_y], fill=BORDER, width=1)
    hero_y += 60
    ht = "이렇게 작동합니다"
    bb = draw.textbbox((0,0), ht, font=f_sec)
    draw.text(((W-(bb[2]-bb[0]))//2, hero_y), ht, font=f_sec, fill=WHITE)
    hero_y += 80

    steps = [
        ("01", "예산 & 타겟 설정", "업종, 지역, 연령, 성별, 예산을\n입력하면 끝"),
        ("02", "매체 자동 추천", "룰베이스 엔진이 최적 매체를\nMAU, CTR 기준으로 선정"),
        ("03", "이미지 업로드", "제품 이미지 1장만\n업로드하면 됩니다"),
        ("04", "AI 소재 자동 완성", "모든 매체 사이즈 + 후킹 문구\n자동 생성"),
        ("05", "집행 & 모니터링", "1클릭 집행 후 실시간\nCTR / 노출 확인"),
    ]
    sw2 = 240
    total_sw = sw2*len(steps) + 20*(len(steps)-1)
    sx0 = (W-total_sw)//2
    for si, (num, stitle, sdesc) in enumerate(steps):
        sx = sx0 + si*(sw2+20)
        draw_shadow_card(draw, sx, hero_y, sw2, 200, fill=CARD_BG, radius=12)
        # number badge
        draw_badge(draw, sx+16, hero_y+16, num, font(12, bold=True), fill=ACCENT)
        draw.text((sx+16, hero_y+54), stitle, font=font(15, bold=True), fill=WHITE)
        for li, line in enumerate(sdesc.split('\n')):
            draw.text((sx+16, hero_y+84+li*22), line, font=font(12), fill=GRAY)
        # arrow connector
        if si < len(steps)-1:
            ax = sx+sw2+2
            ay = hero_y+90
            draw.polygon([(ax, ay), (ax+16, ay+12), (ax, ay+24)], fill=ACCENT)
    hero_y += 260

    # ── MEDIA LOGOS ──────────────────────────────────────
    draw.line([0, hero_y, W, hero_y], fill=BORDER, width=1)
    hero_y += 50
    ml = "제휴 버티컬 매체"
    bb = draw.textbbox((0,0), ml, font=font(18))
    draw.text(((W-(bb[2]-bb[0]))//2, hero_y), ml, font=font(18), fill=GRAY)
    hero_y += 50
    media_list = ["맘카페", "인벤", "보배드림", "SLR클럽", "82쿡", "클리앙", "MLB파크", "에펨코리아"]
    mw_each = 160
    total_mw = mw_each*len(media_list) + 16*(len(media_list)-1)
    mx0 = (W-total_mw)//2
    for mi, mname in enumerate(media_list):
        mx = mx0 + mi*(mw_each+16)
        draw_shadow_card(draw, mx, hero_y, mw_each, 56, fill=CARD_BG, radius=8)
        bb = draw.textbbox((0,0), mname, font=font(14, bold=True))
        tw = bb[2]-bb[0]
        draw.text((mx+(mw_each-tw)//2, hero_y+18), mname, font=font(14, bold=True), fill=GRAY)
    hero_y += 100

    # ── BOTTOM CTA BANNER ────────────────────────────────
    draw.rectangle([0, hero_y, W, hero_y+200], fill=ACCENT)
    ct = "지금 바로 시작하세요"
    f_ct = font(40, bold=True)
    bb = draw.textbbox((0,0), ct, font=f_ct)
    draw.text(((W-(bb[2]-bb[0]))//2, hero_y+36), ct, font=f_ct, fill=WHITE)
    cs = "설치 없이 브라우저에서 바로. 첫 30일 무료."
    bb2 = draw.textbbox((0,0), cs, font=font(18))
    draw.text(((W-(bb2[2]-bb2[0]))//2, hero_y+90), cs, font=font(18), fill=(200,220,255))
    draw_button(draw, (W-200)//2, hero_y+132, 200, 48, "무료 체험 시작", font(16, bold=True),
                fill=WHITE, text_color=ACCENT, radius=8)
    hero_y += 200

    # ── FOOTER ───────────────────────────────────────────
    draw.rectangle([0, hero_y, W, H], fill=(8, 14, 28))
    draw.text((60, hero_y+40), "AdMix", font=font(18, bold=True), fill=WHITE)
    draw.text((60, hero_y+72), "AI 기반 버티컬 광고 자동화 플랫폼", font=font(13), fill=GRAY_DIM)
    fcols = [("서비스", ["서비스 소개", "요금제", "매체 현황"]),
             ("지원", ["이용약관", "개인정보처리방침", "고객센터"]),
             ("회사", ["소개", "블로그", "채용"])]
    for fci, (fhdr, flinks) in enumerate(fcols):
        fx = 400 + fci*180
        draw.text((fx, hero_y+40), fhdr, font=font(14, bold=True), fill=WHITE)
        for fli, fl in enumerate(flinks):
            draw.text((fx, hero_y+68+fli*24), fl, font=font(13), fill=GRAY_DIM)
    draw.line([60, hero_y+170, W-60, hero_y+170], fill=BORDER, width=1)
    draw.text((60, hero_y+184), "© 2026 AdMix Inc. All rights reserved.", font=font(12), fill=GRAY_DIM)

    path = os.path.join(OUT, "landing_page.png")
    img.save(path, "PNG")
    print("[OK] landing_page.png saved")
    return path


# ═══════════════════════════════════════════════════════════
#  2. SERVICE INTRO PAGE  (1440 × 3000)
# ═══════════════════════════════════════════════════════════
def make_service_intro():
    W, H = 1440, 3000
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    y = draw_nav(draw, W, 0)

    # ── PAGE TITLE ────────────────────────────────────────
    y += 60
    pt = "AdMix가 하는 일"
    f_pt = font(52, bold=True)
    bb = draw.textbbox((0,0), pt, font=f_pt)
    draw.text(((W-(bb[2]-bb[0]))//2, y), pt, font=f_pt, fill=WHITE)
    y += 70
    ps = "광고 대행의 모든 번거로움을 AI가 대신합니다"
    bb = draw.textbbox((0,0), ps, font=font(20))
    draw.text(((W-(bb[2]-bb[0]))//2, y), ps, font=font(20), fill=GRAY)
    y += 80

    # ── SECTION 1: 문제 정의 ──────────────────────────────
    draw.line([0, y, W, y], fill=BORDER, width=1)
    y += 60
    s1t = "기존 광고 대행의 문제점"
    bb = draw.textbbox((0,0), s1t, font=font(34, bold=True))
    draw.text(((W-(bb[2]-bb[0]))//2, y), s1t, font=font(34, bold=True), fill=WHITE)
    y += 60

    problems = [
        ("💸", "높은 대행 비용", "대행사 수수료 15~20%.\n월 500만원 이상 광고비에서만\n대행사가 본격 움직입니다."),
        ("📋", "소재 규격의 복잡함", "매체마다 다른 배너 사이즈.\n728×90, 300×250, 320×100...\n각각 따로 제작해야 합니다."),
        ("🔍", "매체 선정의 어려움", "어느 매체에 광고해야 효과적인지\n알기 어렵습니다. 데이터도\n없고 비교도 힘듭니다."),
    ]
    pw = 400
    total_pw = pw*3 + 30*2
    px0 = (W-total_pw)//2
    for pi, (icon, ptitle, pdesc) in enumerate(problems):
        px = px0 + pi*(pw+30)
        draw_shadow_card(draw, px, y, pw, 260, fill=(30, 20, 40), radius=14)
        # red accent top
        draw.rounded_rectangle([px, y, px+pw, y+4], radius=0, fill=(220, 60, 60))
        draw.text((px+28, y+30), icon, font=font(32), fill=WHITE)
        draw.text((px+28, y+80), ptitle, font=font(20, bold=True), fill=WHITE)
        for li, line in enumerate(pdesc.split('\n')):
            draw.text((px+28, y+116+li*26), line, font=font(14), fill=GRAY)
    y += 310

    # ── SECTION 2: SOLUTION FLOW ─────────────────────────
    draw.line([0, y, W, y], fill=BORDER, width=1)
    y += 60
    s2t = "AdMix의 자동화 솔루션 플로우"
    bb = draw.textbbox((0,0), s2t, font=font(34, bold=True))
    draw.text(((W-(bb[2]-bb[0]))//2, y), s2t, font=font(34, bold=True), fill=WHITE)
    y += 70

    flows = [
        ("1", "이미지 업로드", "제품 사진 1장만\n업로드합니다"),
        ("2", "AI 후킹 문구 생성", "단순도 분석 후\n3가지 문구 제안"),
        ("3", "사이즈 자동 조정", "모든 매체 규격에\n맞게 자동 변환"),
        ("4", "매체 자동 매칭", "타겟 조건으로\n최적 매체 선정"),
        ("5", "집행 & 보고", "1클릭 집행 후\n실시간 성과 확인"),
    ]
    fw = 220
    total_fw = fw*5 + 20*4
    fx0 = (W-total_fw)//2
    # flow arrows bg
    draw.line([fx0+fw//2, y+50, fx0+total_fw-fw//2, y+50], fill=BORDER, width=2)
    for fli, (num, ftitle, fdesc) in enumerate(flows):
        fx = fx0 + fli*(fw+20)
        # circle
        cx, cy = fx+fw//2, y+50
        draw.ellipse([cx-32, cy-32, cx+32, cy+32], fill=ACCENT)
        draw.ellipse([cx-28, cy-28, cx+28, cy+28], fill=(25,60,170))
        bb = draw.textbbox((0,0), num, font=font(20, bold=True))
        draw.text((cx-(bb[2]-bb[0])//2, cy-(bb[3]-bb[1])//2-1), num, font=font(20, bold=True), fill=WHITE)
        # card below
        draw_shadow_card(draw, fx+10, y+100, fw-20, 170, fill=CARD_BG, radius=10)
        bb = draw.textbbox((0,0), ftitle, font=font(14, bold=True))
        tw = bb[2]-bb[0]
        draw.text((fx+(fw-tw)//2, y+120), ftitle, font=font(14, bold=True), fill=WHITE)
        for li, line in enumerate(fdesc.split('\n')):
            bb = draw.textbbox((0,0), line, font=font(12))
            tw = bb[2]-bb[0]
            draw.text((fx+(fw-tw)//2, y+152+li*22), line, font=font(12), fill=GRAY)
        # arrow between circles
        if fli < len(flows)-1:
            ax = cx+32
            ay = y+50
            draw.polygon([(ax, ay-6), (ax+16, ay), (ax, ay+6)], fill=ACCENT)
    y += 320

    # ── SECTION 3: 지원 매체 ─────────────────────────────
    draw.line([0, y, W, y], fill=BORDER, width=1)
    y += 60
    s3t = "지원 버티컬 매체"
    bb = draw.textbbox((0,0), s3t, font=font(34, bold=True))
    draw.text(((W-(bb[2]-bb[0]))//2, y), s3t, font=font(34, bold=True), fill=WHITE)
    y += 60

    media_cards = [
        ("맘카페", "육아 / 생활", "MAU 120만", "CTR 2.1%", "#FF6B9D"),
        ("인벤", "게임 / IT", "MAU 90만", "CTR 3.4%", "#4ECDC4"),
        ("보배드림", "자동차", "MAU 65만", "CTR 2.8%", "#45B7D1"),
        ("82쿡", "요리 / 생활", "MAU 50만", "CTR 2.3%", "#96CEB4"),
        ("SLR클럽", "카메라 / 취미", "MAU 40만", "CTR 3.1%", "#FFEAA7"),
        ("클리앙", "IT / 테크", "MAU 35만", "CTR 3.6%", "#DDA0DD"),
    ]
    mcw, mch = 400, 180
    mcols = 3
    total_mcw = mcw*mcols + 24*(mcols-1)
    mx0 = (W-total_mcw)//2
    for mci, (mname, mcategory, mau, ctr, accent_hex) in enumerate(media_cards):
        col = mci % mcols
        row = mci // mcols
        mx = mx0 + col*(mcw+24)
        my = y + row*(mch+20)
        draw_shadow_card(draw, mx, my, mcw, mch, fill=CARD_BG, radius=12)
        # top accent line
        acc_rgb = tuple(int(accent_hex.lstrip('#')[i:i+2], 16) for i in (0,2,4))
        draw.rounded_rectangle([mx, my, mx+mcw, my+4], radius=0, fill=acc_rgb)
        draw.text((mx+20, my+22), mname, font=font(20, bold=True), fill=WHITE)
        draw_badge(draw, mx+20, my+54, mcategory, font(11), fill=(30,50,90))
        # stats
        for si, (sl, sv) in enumerate([("MAU", mau), ("CTR", ctr)]):
            sx2 = mx+20+si*160
            draw.text((sx2, my+90), sl, font=font(11), fill=GRAY)
            draw.text((sx2, my+110), sv, font=font(16, bold=True), fill=acc_rgb)
        # mini bar
        draw.rounded_rectangle([mx+20, my+148, mx+mcw-20, my+158], radius=3, fill=(30,40,70))
        fill_w = int((mcw-40) * (float(ctr.replace('%','').replace('CTR','').strip())/5.0))
        draw.rounded_rectangle([mx+20, my+148, mx+20+fill_w, my+158], radius=3, fill=acc_rgb)
    y += (len(media_cards)//mcols)*(mch+20) + 30

    # ── SECTION 4: 요금제 ────────────────────────────────
    draw.line([0, y, W, y], fill=BORDER, width=1)
    y += 60
    s4t = "요금제"
    bb = draw.textbbox((0,0), s4t, font=font(34, bold=True))
    draw.text(((W-(bb[2]-bb[0]))//2, y), s4t, font=font(34, bold=True), fill=WHITE)
    y += 60

    plans = [
        ("스타터", "무료", ["월 광고비 50만원 이하", "매체 3개 선택 가능", "기본 소재 편집", "이메일 지원"], False),
        ("프로", "월 49,000원", ["월 광고비 무제한", "매체 10개 선택 가능", "AI 후킹 문구 생성", "우선 지원", "캠페인 분석 리포트"], True),
        ("엔터프라이즈", "문의", ["무제한 광고비", "전체 매체 접근", "전담 매니저", "API 연동", "커스텀 계약"], False),
    ]
    plw = 380
    total_plw = plw*3 + 30*2
    plx0 = (W-total_plw)//2
    for pli, (pname, pprice, pfeats, featured) in enumerate(plans):
        px = plx0 + pli*(plw+30)
        plh = 380
        bg_fill = ACCENT if featured else CARD_BG
        draw_shadow_card(draw, px, y, plw, plh, fill=bg_fill, radius=14)
        if featured:
            draw_badge(draw, px+plw//2-50, y-14, "가장 인기", font(12, bold=True), fill=WARN, text_color=(0,0,0))
        draw.text((px+28, y+28), pname, font=font(20, bold=True), fill=WHITE)
        draw.text((px+28, y+66), pprice, font=font(30, bold=True), fill=WHITE)
        draw.line([px+28, y+110, px+plw-28, y+110], fill=WHITE if featured else BORDER, width=1)
        for fei, feat in enumerate(pfeats):
            draw.text((px+44, y+126+fei*36), "✓  " + feat, font=font(14), fill=WHITE if featured else GRAY)
        btn_fill = WHITE if featured else ACCENT
        btn_text_col = ACCENT if featured else WHITE
        draw_button(draw, px+28, y+plh-60, plw-56, 44,
                    "시작하기" if pname != "엔터프라이즈" else "문의하기",
                    font(15, bold=True), fill=btn_fill, text_color=btn_text_col, radius=8)
    y += 430

    # ── BOTTOM CTA ────────────────────────────────────────
    draw.rectangle([0, y, W, y+200], fill=(18, 35, 80))
    ct = "지금 무료로 시작해보세요"
    bb = draw.textbbox((0,0), ct, font=font(40, bold=True))
    draw.text(((W-(bb[2]-bb[0]))//2, y+36), ct, font=font(40, bold=True), fill=WHITE)
    cs = "신용카드 없이 30일 무료. 언제든 취소 가능."
    bb2 = draw.textbbox((0,0), cs, font=font(16))
    draw.text(((W-(bb2[2]-bb2[0]))//2, y+90), cs, font=font(16), fill=GRAY)
    draw_button(draw, (W-200)//2, y+132, 200, 48, "무료 체험 시작", font(16, bold=True), fill=ACCENT, radius=8)
    y += 200

    # footer
    draw.rectangle([0, y, W, H], fill=(8, 14, 28))
    draw.text((60, y+40), "AdMix", font=font(18, bold=True), fill=WHITE)
    draw.text((60, y+70), "© 2026 AdMix Inc.", font=font(13), fill=GRAY_DIM)

    path = os.path.join(OUT, "service_intro.png")
    img.save(path, "PNG")
    print("[OK] service_intro.png saved")
    return path


# ═══════════════════════════════════════════════════════════
#  3. SITE STRUCTURE DIAGRAM  (1600 × 900)
# ═══════════════════════════════════════════════════════════
def make_site_structure():
    W, H = 1600, 900
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # title
    draw.text((50, 30), "AdMix 사이트 구조", font=font(26, bold=True), fill=WHITE)
    draw.text((50, 68), "공개 영역(비로그인)과 광고 관리 영역(로그인 후)의 구분", font=font(14), fill=GRAY)

    # ── ROOT NODE ─────────────────────────────────────────
    root_w, root_h = 160, 46
    root_x = W//2 - root_w//2
    root_y = 115
    draw_shadow_card(draw, root_x, root_y, root_w, root_h, fill=ACCENT, radius=10)
    bb = draw.textbbox((0,0), "AdMix.io", font=font(17, bold=True))
    draw.text((root_x+(root_w-(bb[2]-bb[0]))//2, root_y+12), "AdMix.io", font=font(17, bold=True), fill=WHITE)

    root_mid_x = root_x + root_w//2
    root_bot_y = root_y + root_h

    # ── LEFT BRANCH: PUBLIC (x: 50 ~ 480) ────────────────
    pub_w, pub_h = 240, 48
    pub_x = 120
    pub_y = 225
    pub_mid_x = pub_x + pub_w//2

    # root → pub connector
    draw.line([root_mid_x, root_bot_y, root_mid_x, root_bot_y+20], fill=BORDER, width=2)
    draw.line([root_mid_x, root_bot_y+20, pub_mid_x, root_bot_y+20], fill=BORDER, width=2)
    draw.line([pub_mid_x, root_bot_y+20, pub_mid_x, pub_y], fill=BORDER, width=2)

    draw_shadow_card(draw, pub_x, pub_y, pub_w, pub_h, fill=(25, 55, 35), radius=10)
    draw.rectangle([pub_x, pub_y, pub_x+pub_w, pub_y+4], fill=SUCCESS)
    bb = draw.textbbox((0,0), "공개 영역 (비로그인)", font=font(14, bold=True))
    draw.text((pub_x+(pub_w-(bb[2]-bb[0]))//2, pub_y+14), "공개 영역 (비로그인)", font=font(14, bold=True), fill=WHITE)

    # vertical spine for public children
    spine_x = pub_mid_x
    pub_pages = [
        ("랜딩 페이지", ["메인 히어로, 핵심 기능", "매체 목록, CTA"]),
        ("서비스 소개", ["문제 정의, 솔루션 플로우", "지원 매체 카드"]),
        ("요금제", ["스타터 / 프로", "엔터프라이즈"]),
    ]
    node_w_pub = 220
    node_h_pub = 80
    child_gap = 18
    total_pub_h = len(pub_pages)*(node_h_pub+child_gap) - child_gap
    child_start_y = pub_y + pub_h + 30

    draw.line([spine_x, pub_y+pub_h, spine_x, child_start_y + total_pub_h//2], fill=BORDER, width=1)

    for pi, (pname, pfeats) in enumerate(pub_pages):
        ny = child_start_y + pi*(node_h_pub+child_gap)
        nx = pub_x + (pub_w - node_w_pub)//2
        # horizontal stub
        draw.line([spine_x, ny+node_h_pub//2, nx, ny+node_h_pub//2], fill=BORDER, width=1)
        draw_shadow_card(draw, nx, ny, node_w_pub, node_h_pub, fill=CARD_BG, radius=8)
        draw.rectangle([nx, ny, nx+node_w_pub, ny+3], fill=SUCCESS)
        draw.text((nx+12, ny+10), pname, font=font(13, bold=True), fill=WHITE)
        for li, feat in enumerate(pfeats):
            draw.text((nx+12, ny+32+li*20), feat, font=font(11), fill=GRAY)

    # ── RIGHT BRANCH: PRIVATE (x: 530 ~ 1550) ────────────
    priv_w, priv_h = 280, 48
    priv_x = W//2 + 60
    priv_y = 225
    priv_mid_x = priv_x + priv_w//2

    # root → priv connector
    draw.line([root_mid_x, root_bot_y+20, priv_mid_x, root_bot_y+20], fill=BORDER, width=2)
    draw.line([priv_mid_x, root_bot_y+20, priv_mid_x, priv_y], fill=BORDER, width=2)

    draw_shadow_card(draw, priv_x, priv_y, priv_w, priv_h, fill=(20, 35, 75), radius=10)
    draw.rectangle([priv_x, priv_y, priv_x+priv_w, priv_y+4], fill=ACCENT)
    bb = draw.textbbox((0,0), "광고 관리 영역 (로그인 후)", font=font(13, bold=True))
    draw.text((priv_x+(priv_w-(bb[2]-bb[0]))//2, priv_y+14), "광고 관리 영역 (로그인 후)", font=font(13, bold=True), fill=WHITE)

    priv_pages = [
        ("대시보드", ["전체 KPI 요약", "CTR 벤치마크", "예산 소진"]),
        ("캠페인 관리", ["위자드 Step 1~4", "예산/타겟/매체", "채널 믹스"]),
        ("소재 편집 스튜디오", ["이미지 업로드", "AI 후킹 문구", "사이즈 편집"]),
        ("매체 현황", ["매체 리스트", "MAU/CTR", "매체 비교"]),
        ("계정 설정", ["프로필 관리", "결제 정보", "알림 설정"]),
    ]

    node_w_priv = 190
    node_h_priv = 110
    col_gap = 22
    nodes_per_row = 3
    rows = (len(priv_pages) + nodes_per_row - 1) // nodes_per_row

    # row 1 x positions centered around priv_mid_x
    row1_count = min(nodes_per_row, len(priv_pages))
    row1_total = row1_count * node_w_priv + (row1_count-1)*col_gap
    row1_x0 = priv_mid_x - row1_total//2
    child_start_y_priv = priv_y + priv_h + 36

    # vertical spine
    draw.line([priv_mid_x, priv_y+priv_h, priv_mid_x, child_start_y_priv+20], fill=BORDER, width=1)

    for pi, (pname, pfeats) in enumerate(priv_pages):
        col = pi % nodes_per_row
        row = pi // nodes_per_row
        # for row 2, center remaining items
        if row == 1:
            row2_count = len(priv_pages) - nodes_per_row
            row2_total = row2_count * node_w_priv + (row2_count-1)*col_gap
            row2_x0 = priv_mid_x - row2_total//2
            nx = row2_x0 + col*(node_w_priv+col_gap)
        else:
            nx = row1_x0 + col*(node_w_priv+col_gap)
        ny = child_start_y_priv + row*(node_h_priv+18)

        # connector
        node_mid_x = nx + node_w_priv//2
        if row == 0:
            draw.line([priv_mid_x, child_start_y_priv+20, node_mid_x, child_start_y_priv+20], fill=BORDER, width=1)
            draw.line([node_mid_x, child_start_y_priv+20, node_mid_x, ny], fill=BORDER, width=1)
        else:
            row1_bot = child_start_y_priv + node_h_priv + 18
            draw.line([node_mid_x, row1_bot, node_mid_x, ny], fill=BORDER, width=1)

        draw_shadow_card(draw, nx, ny, node_w_priv, node_h_priv, fill=CARD_BG2, radius=8)
        draw.rectangle([nx, ny, nx+node_w_priv, ny+3], fill=ACCENT)
        draw.text((nx+12, ny+10), pname, font=font(12, bold=True), fill=WHITE)
        for fli, feat in enumerate(pfeats):
            draw.text((nx+12, ny+32+fli*22), feat, font=font(11), fill=GRAY)

    # ── LEGEND ────────────────────────────────────────────
    legend_y = H - 56
    draw.line([0, legend_y-10, W, legend_y-10], fill=BORDER, width=1)
    for li, (lc, lt) in enumerate([(SUCCESS, "공개 영역"), (ACCENT, "로그인 필요"), (GRAY_DIM, "연결선")]):
        lx = 60 + li*220
        draw.ellipse([lx, legend_y+6, lx+14, legend_y+20], fill=lc)
        draw.text((lx+22, legend_y+4), lt, font=font(13), fill=GRAY)

    path = os.path.join(OUT, "site_structure.png")
    img.save(path, "PNG")
    print("[OK] site_structure.png saved")
    return path


if __name__ == "__main__":
    p1 = make_landing()
    p2 = make_service_intro()
    p3 = make_site_structure()
    print("\nAll done!")
    print(f"  {p1}")
    print(f"  {p2}")
    print(f"  {p3}")
