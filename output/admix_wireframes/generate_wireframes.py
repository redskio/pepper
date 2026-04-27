"""
AdMix — 와이어프레임 이미지 생성 스크립트
18장 / 1280×800px / Deep blue + Orange accent
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── 색상 팔레트 ─────────────────────────────────────────────
BG          = "#0F1829"        # 배경: 딥 네이비
PANEL       = "#162035"        # 패널/카드 배경
PANEL2      = "#1C2A45"        # 2차 패널
BORDER      = "#263354"        # 테두리
ACCENT      = "#FF6B35"        # 오렌지 액센트 (CTA, 강조)
ACCENT2     = "#2D6FF7"        # 블루 액센트
WHITE       = "#FFFFFF"
GRAY_L      = "#C8D4E8"        # 밝은 텍스트
GRAY_M      = "#7A8DAD"        # 중간 텍스트 / 라벨
GRAY_D      = "#3D4F6E"        # 구분선 / 비활성
SUCCESS     = "#22C55E"        # 초록 (성공/진행중)
WARNING     = "#F59E0B"        # 노랑 (경고)
DANGER      = "#EF4444"        # 빨강 (에러)
CHIP_BG     = "#1A2F52"        # 칩 배경
CHART_LINE  = "#2D6FF7"        # 차트 선

# ── 캔버스 설정 ─────────────────────────────────────────────
W, H = 1280, 800
OUT = os.path.dirname(os.path.abspath(__file__))

# ── 폰트 로드 ────────────────────────────────────────────────
FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"

def font(size, bold=False):
    try:
        path = FONT_BOLD if bold else FONT_PATH
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

F_XS  = font(11)
F_SM  = font(13)
F_MD  = font(15)
F_LG  = font(18)
F_XL  = font(22)
F_2XL = font(28)
F_3XL = font(36)
F_H1  = font(48, bold=True)
F_B_SM = font(13, bold=True)
F_B_MD = font(15, bold=True)
F_B_LG = font(18, bold=True)
F_B_XL = font(22, bold=True)
F_B_2XL = font(28, bold=True)

# ── 공통 유틸 ────────────────────────────────────────────────
def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    return img, d

def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path)
    print(f"[OK] {name}")

def rect(d, x1, y1, x2, y2, fill=None, outline=None, radius=6, width=1):
    if radius:
        d.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)
    else:
        d.rectangle([x1, y1, x2, y2], fill=fill, outline=outline, width=width)

def text(d, x, y, s, f=None, fill=WHITE, anchor="la"):
    if f is None: f = F_MD
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def cta_btn(d, x, y, w, h, label, f=None, color=ACCENT, radius=8):
    if f is None: f = F_B_MD
    rect(d, x, y, x+w, y+h, fill=color, radius=radius)
    cx, cy = x + w//2, y + h//2
    d.text((cx, cy), label, font=f, fill=WHITE, anchor="mm")

def outline_btn(d, x, y, w, h, label, f=None, color=GRAY_M, radius=8):
    if f is None: f = F_MD
    rect(d, x, y, x+w, y+h, fill=None, outline=color, radius=radius)
    cx, cy = x + w//2, y + h//2
    d.text((cx, cy), label, font=f, fill=color, anchor="mm")

def chip(d, x, y, label, active=False, f=None):
    if f is None: f = F_SM
    pw = 14
    bbox = f.getbbox(label)
    tw = bbox[2] - bbox[0]
    cw = tw + pw*2
    ch = 28
    bg = ACCENT2 if active else CHIP_BG
    ol = ACCENT2 if active else GRAY_D
    rect(d, x, y, x+cw, y+ch, fill=bg, outline=ol, radius=14)
    d.text((x+pw, y+14), label, font=f, fill=WHITE, anchor="lm")
    return x + cw + 8

def gnb(d, title="AdMix", with_nav=True):
    """공통 상단 네비게이션 바"""
    rect(d, 0, 0, W, 56, fill=PANEL, radius=0)
    d.line([(0, 56), (W, 56)], fill=BORDER, width=1)
    # 로고
    rect(d, 20, 12, 82, 44, fill=ACCENT2, radius=6)
    d.text((51, 28), "AdMix", font=F_B_MD, fill=WHITE, anchor="mm")
    if with_nav:
        navs = ["매체 탐색", "광고주", "퍼블리셔", "가격"]
        nx = 120
        for n in navs:
            d.text((nx, 28), n, font=F_SM, fill=GRAY_L, anchor="lm")
            nx += 90
    # 우측 CTA
    cta_btn(d, W-140, 12, 120, 32, "무료 시작하기", f=F_B_SM, color=ACCENT, radius=6)
    d.text((W-160, 28), "로그인", font=F_SM, fill=GRAY_M, anchor="rm")

def sidebar(d, items, active_idx=0, top=56, sidebar_w=200):
    """사이드바"""
    rect(d, 0, top, sidebar_w, H, fill=PANEL, radius=0)
    d.line([(sidebar_w, top), (sidebar_w, H)], fill=BORDER, width=1)
    y = top + 20
    for i, (icon, label) in enumerate(items):
        is_active = i == active_idx
        if is_active:
            rect(d, 8, y-4, sidebar_w-8, y+32, fill=CHIP_BG, radius=6)
            d.line([(8, y-4), (8, y+32)], fill=ACCENT, width=3)
        color = WHITE if is_active else GRAY_M
        d.text((30, y+14), f"{icon}  {label}", font=F_SM, fill=color, anchor="lm")
        y += 44

def stat_card(d, x, y, w, h, label, value, sub="", trend="", color=ACCENT2):
    rect(d, x, y, x+w, y+h, fill=PANEL, outline=BORDER, radius=8)
    d.text((x+16, y+16), label, font=F_SM, fill=GRAY_M)
    d.text((x+16, y+40), value, font=F_B_XL, fill=WHITE)
    if sub:
        d.text((x+16, y+70), sub, font=F_XS, fill=GRAY_M)
    if trend:
        tc = SUCCESS if "+" in trend else DANGER
        d.text((x+w-12, y+16), trend, font=F_B_SM, fill=tc, anchor="ra")

def progress_bar(d, x, y, w, h, pct, color=ACCENT2, bg=PANEL2):
    rect(d, x, y, x+w, y+h, fill=bg, radius=h//2)
    if pct > 0:
        fw = max(h, int(w * pct / 100))
        rect(d, x, y, x+fw, y+h, fill=color, radius=h//2)

def step_indicator(d, steps, active, top=70, left=200, spacing=180):
    x = left
    for i, s in enumerate(steps):
        is_done = i < active
        is_active = i == active
        if is_done:
            rect(d, x-12, top-12, x+12, top+12, fill=SUCCESS, radius=12)
            d.text((x, top), "✓", font=F_SM, fill=WHITE, anchor="mm")
        elif is_active:
            rect(d, x-12, top-12, x+12, top+12, fill=ACCENT, radius=12)
            d.text((x, top), str(i+1), font=F_B_SM, fill=WHITE, anchor="mm")
        else:
            rect(d, x-12, top-12, x+12, top+12, fill=GRAY_D, radius=12)
            d.text((x, top), str(i+1), font=F_SM, fill=GRAY_M, anchor="mm")
        d.text((x, top+22), s, font=F_XS, fill=GRAY_M if not is_active else WHITE, anchor="mm")
        if i < len(steps)-1:
            lx = x + 14
            lcolor = SUCCESS if is_done else GRAY_D
            d.line([(lx, top), (lx + spacing - 28, top)], fill=lcolor, width=2)
        x += spacing

def input_field(d, x, y, w, h, label, placeholder="", value=""):
    d.text((x, y-18), label, font=F_SM, fill=GRAY_M)
    rect(d, x, y, x+w, y+h, fill=PANEL2, outline=BORDER, radius=6)
    if value:
        d.text((x+12, y+h//2), value, font=F_MD, fill=WHITE, anchor="lm")
    elif placeholder:
        d.text((x+12, y+h//2), placeholder, font=F_MD, fill=GRAY_D, anchor="lm")

def mini_chart(d, x, y, w, h, data, color=CHART_LINE):
    """간단한 라인 차트"""
    rect(d, x, y, x+w, y+h, fill=PANEL2, outline=BORDER, radius=6)
    if len(data) < 2: return
    mn, mx = min(data), max(data)
    rng = mx - mn if mx != mn else 1
    pad = 12
    pts = []
    for i, v in enumerate(data):
        px = x + pad + int((w - pad*2) * i / (len(data)-1))
        py = y + h - pad - int((h - pad*2) * (v - mn) / rng)
        pts.append((px, py))
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill=color, width=2)
    for px, py in pts:
        d.ellipse([px-3, py-3, px+3, py+3], fill=color)

def table_row(d, x, y, cols, widths, is_header=False, fill_bg=None):
    if fill_bg:
        rect(d, x, y, x+sum(widths), y+36, fill=fill_bg, radius=0)
    cx = x
    for i, (col, w) in enumerate(zip(cols, widths)):
        f = F_B_SM if is_header else F_SM
        fc = GRAY_M if is_header else GRAY_L
        d.text((cx+10, y+18), col, font=f, fill=fc, anchor="lm")
        cx += w
    d.line([(x, y+36), (x+sum(widths), y+36)], fill=BORDER, width=1)


# ═══════════════════════════════════════════════════════════
# 01 — Landing Page
# ═══════════════════════════════════════════════════════════
def gen_01_landing():
    img, d = new_canvas()
    gnb(d)

    # Hero Section
    d.text((640, 160), "버티컬 미디어, AI로 연결하다", font=F_H1, fill=WHITE, anchor="mm")
    d.text((640, 210), "광고주와 전문 퍼블리셔를 직접 연결 — 타겟 정밀도 3배, 집행 시간 80% 절감", font=F_LG, fill=GRAY_L, anchor="mm")

    # Dual CTA
    cta_btn(d, 390, 244, 200, 48, "광고주로 시작하기", color=ACCENT, radius=8)
    cta_btn(d, 606, 244, 200, 48, "퍼블리셔 등록하기", color=ACCENT2, radius=8)

    # 3-feature cards
    features = [
        ("🎯", "버티컬 매체 매칭", "300+ 전문 매체\nAI 자동 추천"),
        ("⚡", "소재 자동화", "1회 업로드\n전 사이즈 자동 생성"),
        ("📊", "실시간 성과 분석", "업종 평균 CTR\n벤치마크 비교"),
    ]
    fx = 140
    for icon, title, desc in features:
        rect(d, fx, 320, fx+300, 480, fill=PANEL, outline=BORDER, radius=12)
        d.text((fx+150, 360), icon, font=F_3XL, fill=WHITE, anchor="mm")
        d.text((fx+150, 405), title, font=F_B_LG, fill=WHITE, anchor="mm")
        for li, line in enumerate(desc.split("\n")):
            d.text((fx+150, 432+li*20), line, font=F_SM, fill=GRAY_M, anchor="mm")
        fx += 330

    # Social Proof
    rect(d, 0, 510, W, 630, fill=PANEL, radius=0)
    d.text((640, 545), "도입 성과", font=F_B_LG, fill=GRAY_M, anchor="mm")
    stats = [("300+", "파트너 매체"), ("2.3배", "평균 CTR 향상"), ("80%", "집행 시간 절감"), ("15,000+", "집행 캠페인")]
    sx = 160
    for val, label in stats:
        d.text((sx, 575), val, font=F_B_2XL, fill=ACCENT, anchor="mm")
        d.text((sx, 605), label, font=F_SM, fill=GRAY_M, anchor="mm")
        sx += 240

    # CTA Banner
    rect(d, 80, 650, W-80, 760, fill=ACCENT2, radius=12)
    d.text((400, 705), "지금 바로 무료로 시작하세요", font=F_B_XL, fill=WHITE, anchor="mm")
    cta_btn(d, 840, 675, 220, 60, "무료 캠페인 만들기", color=ACCENT, radius=8)

    save(img, "01_landing.png")

# ═══════════════════════════════════════════════════════════
# 02 — Service Intro
# ═══════════════════════════════════════════════════════════
def gen_02_service_intro():
    img, d = new_canvas()
    gnb(d)

    d.text((640, 100), "AdMix가 작동하는 방법", font=F_B_2XL, fill=WHITE, anchor="mm")
    d.text((640, 132), "3단계로 완성되는 버티컬 광고 플랫폼", font=F_LG, fill=GRAY_M, anchor="mm")

    # How it works — 3 steps
    steps_data = [
        ("01", ACCENT, "매체 선택", "AI가 업종·예산·타겟에\n맞는 전문 매체 추천"),
        ("02", ACCENT2, "소재 제작", "1회 업로드로\n모든 사이즈 자동 생성"),
        ("03", SUCCESS, "성과 집행", "실시간 모니터링 &\n업종 평균 벤치마크"),
    ]
    arrow_x = [300, 600, 900]
    for i, (num, color, title, desc) in enumerate(steps_data):
        x = arrow_x[i]
        rect(d, x-80, 170, x+80, 430, fill=PANEL, outline=color, radius=12)
        rect(d, x-22, 188, x+22, 232, fill=color, radius=22)
        d.text((x, 210), num, font=F_B_XL, fill=WHITE, anchor="mm")
        d.text((x, 270), title, font=F_B_LG, fill=WHITE, anchor="mm")
        for li, line in enumerate(desc.split("\n")):
            d.text((x, 305+li*22), line, font=F_SM, fill=GRAY_M, anchor="mm")
        if i < 2:
            d.text((x+100, 300), "→", font=F_2XL, fill=GRAY_D, anchor="mm")

    # 버티컬 미디어 카테고리
    d.text((640, 460), "전문 버티컬 미디어 카테고리", font=F_B_LG, fill=WHITE, anchor="mm")
    cats = ["패션/뷰티", "게임", "육아/맘카페", "금융", "의료/헬스", "교육", "스포츠", "IT/테크"]
    cx_start = 80
    cx = cx_start
    cy = 490
    for i, cat in enumerate(cats):
        if i == 4:
            cx = cx_start
            cy = 530
        chip(d, cx, cy, cat, active=(i % 3 == 0))
        bbox = F_SM.getbbox(cat)
        tw = bbox[2] - bbox[0]
        cx += tw + 44

    # 자동화 비교
    rect(d, 80, 580, 580, 760, fill=PANEL, outline=BORDER, radius=10)
    d.text((330, 605), "기존 방식", font=F_B_MD, fill=DANGER, anchor="mm")
    pain_points = ["• 매체별 개별 협상 (평균 2주)", "• 사이즈별 소재 별도 제작", "• 엑셀 집계 성과 보고"]
    for i, p in enumerate(pain_points):
        d.text((110, 640+i*36), p, font=F_MD, fill=GRAY_M)

    rect(d, 620, 580, W-80, 760, fill=PANEL, outline=SUCCESS, radius=10)
    d.text((950, 605), "AdMix", font=F_B_MD, fill=SUCCESS, anchor="mm")
    goods = ["• AI 매체 추천 즉시 (5분)", "• 1회 업로드 → 전 사이즈 자동", "• 실시간 대시보드 + 벤치마크"]
    for i, g in enumerate(goods):
        d.text((640, 640+i*36), g, font=F_MD, fill=GRAY_L)

    d.text((640, 765), "→  AdMix로 전환", font=F_B_SM, fill=ACCENT, anchor="mm")

    save(img, "02_service_intro.png")

# ═══════════════════════════════════════════════════════════
# 03 — Media Publishers (매체 탐색)
# ═══════════════════════════════════════════════════════════
def gen_03_media_publishers():
    img, d = new_canvas()
    gnb(d)

    # Sidebar filters
    rect(d, 0, 56, 220, H, fill=PANEL, radius=0)
    d.line([(220, 56), (220, H)], fill=BORDER, width=1)
    d.text((20, 78), "카테고리", font=F_B_SM, fill=WHITE)
    cats = ["전체", "패션/뷰티", "게임", "육아/맘카페", "금융", "의료", "교육"]
    for i, c in enumerate(cats):
        is_active = i == 2
        rect(d, 12, 100+i*38, 208, 132+i*38, fill=CHIP_BG if is_active else None, radius=6)
        col = WHITE if is_active else GRAY_M
        d.text((20, 116+i*38), c, font=F_SM, fill=col, anchor="lm")
        if is_active:
            d.line([(12, 100+i*38), (12, 132+i*38)], fill=ACCENT, width=3)

    d.text((20, 378), "광고 형식", font=F_B_SM, fill=WHITE)
    formats = ["배너", "네이티브", "동영상", "텍스트링크"]
    for i, f in enumerate(formats):
        rect(d, 12, 400+i*34, 208, 428+i*34, fill=None, radius=4)
        d.rectangle([20, 408+i*34, 34, 422+i*34], outline=GRAY_D)
        if i == 0 or i == 1:
            d.rectangle([21, 409+i*34, 33, 421+i*34], fill=ACCENT2)
        d.text((44, 415+i*34), f, font=F_SM, fill=GRAY_M, anchor="lm")

    d.text((20, 550), "최소 예산", font=F_B_SM, fill=WHITE)
    d.text((20, 574), "10만원 ~ 500만원", font=F_SM, fill=GRAY_M)
    progress_bar(d, 20, 598, 180, 6, 65, color=ACCENT2)

    # Main area
    d.text((440, 78), "버티컬 매체 탐색", font=F_B_XL, fill=WHITE, anchor="lm")
    d.text((440, 106), "게임 카테고리 · 24개 매체", font=F_SM, fill=GRAY_M, anchor="lm")

    # Sort / search
    rect(d, 700, 68, 960, 98, fill=PANEL2, outline=BORDER, radius=6)
    d.text((712, 83), "🔍  매체명 검색", font=F_SM, fill=GRAY_D, anchor="lm")
    outline_btn(d, 970, 68, 120, 30, "MAU 높은 순 ▾", f=F_SM, color=GRAY_M, radius=6)
    cta_btn(d, 1100, 65, 156, 36, "+ 비교하기 (0/3)", color=GRAY_D, radius=6)

    # Media cards (2x3 grid)
    media = [
        ("인벤", "게임", "MAU 220만", "CTR 3.4%", "30만원/주~", True),
        ("루리웹", "게임", "MAU 180만", "CTR 2.9%", "20만원/주~", False),
        ("디시인사이드", "커뮤니티", "MAU 310만", "CTR 1.8%", "50만원/주~", False),
        ("게임메카", "게임", "MAU 95만", "CTR 4.1%", "15만원/주~", True),
        ("플레이포럼", "게임", "MAU 70만", "CTR 3.7%", "10만원/주~", False),
        ("더쿠", "커뮤니티", "MAU 140만", "CTR 2.3%", "25만원/주~", False),
    ]
    gx, gy = 236, 130
    for i, (name, cat, mau, ctr, price, selected) in enumerate(media):
        row, col = divmod(i, 3)
        mx = gx + col * 340
        my = gy + row * 300
        border_col = ACCENT if selected else BORDER
        rect(d, mx, my, mx+320, my+270, fill=PANEL, outline=border_col, radius=10)
        # 매체 헤더
        rect(d, mx, my, mx+320, my+60, fill=PANEL2, radius=10)
        rect(d, mx+16, my+15, mx+50, my+49, fill=ACCENT2, radius=8)
        d.text((mx+33, my+32), name[:1], font=F_B_LG, fill=WHITE, anchor="mm")
        d.text((mx+60, my+24), name, font=F_B_MD, fill=WHITE)
        d.text((mx+60, my+44), cat, font=F_XS, fill=GRAY_M)
        if selected:
            d.text((mx+300, my+20), "✓ 선택됨", font=F_B_SM, fill=SUCCESS, anchor="rm")
        # KPI
        for ki, (klabel, kval) in enumerate([("MAU", mau), ("CTR", ctr), ("최소단가", price)]):
            d.text((mx+16, my+78+ki*44), klabel, font=F_XS, fill=GRAY_M)
            d.text((mx+16, my+96+ki*44), kval, font=F_B_MD, fill=WHITE)
        # Buttons
        cta_btn(d, mx+16, my+224, 130, 34, "선택하기", color=ACCENT if not selected else GRAY_D, radius=6)
        outline_btn(d, mx+160, my+224, 144, 34, "상세보기 →", color=GRAY_M, radius=6)

    save(img, "03_media_publishers.png")

# ═══════════════════════════════════════════════════════════
# 04 — Signup / Onboarding
# ═══════════════════════════════════════════════════════════
def gen_04_signup_onboarding():
    img, d = new_canvas()
    gnb(d)

    # Left: steps
    rect(d, 0, 56, 340, H, fill=PANEL, radius=0)
    d.line([(340, 56), (340, H)], fill=BORDER, width=1)
    d.text((170, 100), "가입 단계", font=F_B_LG, fill=WHITE, anchor="mm")
    steps = [("✓", "계정 유형 선택", True, False), ("2", "기본 정보", False, True), ("3", "비즈니스 정보", False, False), ("4", "완료", False, False)]
    sy = 148
    for icon, label, done, active in steps:
        color = SUCCESS if done else (ACCENT if active else GRAY_D)
        rect(d, 44, sy-2, 80, sy+34, fill=color, radius=18)
        d.text((62, sy+16), icon, font=F_B_SM, fill=WHITE, anchor="mm")
        d.text((96, sy+16), label, font=F_MD, fill=WHITE if active or done else GRAY_M, anchor="lm")
        if not done and not active and len(steps) > 1:
            d.line([(62, sy+34), (62, sy+72)], fill=GRAY_D, width=2)
        sy += 88

    d.text((170, 520), "이미 계정이 있으신가요?", font=F_SM, fill=GRAY_M, anchor="mm")
    d.text((170, 546), "로그인하기 →", font=F_B_SM, fill=ACCENT2, anchor="mm")

    # Right: form
    d.text((810, 100), "기본 정보 입력", font=F_B_2XL, fill=WHITE, anchor="mm")
    d.text((810, 136), "5분 안에 캠페인을 시작해보세요", font=F_MD, fill=GRAY_M, anchor="mm")

    # Form fields
    fields = [
        (380, 180, 380, 44, "이름 *", "", "홍길동"),
        (800, 180, 380, 44, "이메일 *", "", "user@company.com"),
        (380, 270, 380, 44, "비밀번호 *", "", "••••••••"),
        (800, 270, 380, 44, "비밀번호 확인 *", "", "••••••••"),
        (380, 360, 800, 44, "회사명 *", "", "주식회사 마케팅플러스"),
    ]
    for fx, fy, fw, fh, label, placeholder, value in fields:
        input_field(d, fx, fy, fw, fh, label, placeholder, value)

    # 업종 선택
    d.text((380, 440), "업종 *", font=F_SM, fill=GRAY_M)
    industry_cats = ["패션/뷰티", "게임", "육아", "금융", "의료", "교육", "식품", "기타"]
    ix = 380
    for i, ic in enumerate(industry_cats):
        ix = chip(d, ix, 460, ic, active=(i == 1))

    # 개인정보 동의
    rect(d, 380, 512, 1180, 548, fill=PANEL2, outline=BORDER, radius=6)
    rect(d, 396, 524, 416, 544, fill=ACCENT2, radius=3)
    d.text((424, 530), "✓", font=F_SM, fill=WHITE)
    d.text((440, 530), "[필수] 개인정보 수집 및 이용 동의  |  [필수] 서비스 이용약관 동의", font=F_SM, fill=GRAY_M)
    d.text((1164, 530), "전체보기 →", font=F_SM, fill=ACCENT2, anchor="rm")

    cta_btn(d, 380, 570, 800, 52, "다음 단계: 비즈니스 정보 입력 →", color=ACCENT, radius=8)
    d.text((780, 640), "소셜 계정으로 가입하기", font=F_SM, fill=GRAY_M, anchor="mm")
    cta_btn(d, 490, 660, 250, 44, "G  Google로 계속하기", color=PANEL2, radius=8)
    cta_btn(d, 760, 660, 250, 44, "🔵  Kakao로 계속하기", color=PANEL2, radius=8)

    save(img, "04_signup_onboarding.png")

# ═══════════════════════════════════════════════════════════
# 05 — Campaign: Step 1 (광고 유형 선택)
# ═══════════════════════════════════════════════════════════
def gen_05_campaign_ad_type():
    img, d = new_canvas()
    gnb(d)
    step_indicator(d, ["광고 유형", "매체 선택", "예산 설정", "소재 편집", "검토/제출"], active=0, top=90, left=220, spacing=195)

    d.text((640, 140), "어떤 광고를 집행하시겠습니까?", font=F_B_2XL, fill=WHITE, anchor="mm")
    d.text((640, 174), "광고 유형에 따라 적합한 매체와 소재 사이즈가 자동으로 안내됩니다", font=F_MD, fill=GRAY_M, anchor="mm")

    ad_types = [
        ("🖼️", "디스플레이 배너", "이미지/GIF 배너\n클릭률 평균 2.1%", True),
        ("📰", "네이티브 광고", "콘텐츠 형태 자연 노출\n클릭률 평균 3.5%", False),
        ("🎬", "동영상 광고", "15/30초 인스트림\n조회율 평균 65%", False),
        ("🔗", "텍스트 링크", "키워드 타겟 텍스트\nCPC 최저 50원~", False),
    ]
    cx = 80
    for i, (icon, title, desc, selected) in enumerate(ad_types):
        bc = ACCENT if selected else BORDER
        bg = CHIP_BG if selected else PANEL
        rect(d, cx, 210, cx+270, 430, fill=bg, outline=bc, radius=12, width=2 if selected else 1)
        d.text((cx+135, 260), icon, font=font(40), fill=WHITE, anchor="mm")
        d.text((cx+135, 300), title, font=F_B_LG, fill=WHITE, anchor="mm")
        for li, line in enumerate(desc.split("\n")):
            d.text((cx+135, 332+li*22), line, font=F_SM, fill=GRAY_M, anchor="mm")
        if selected:
            rect(d, cx+95, 400, cx+175, 424, fill=ACCENT, radius=6)
            d.text((cx+135, 412), "선택됨 ✓", font=F_B_SM, fill=WHITE, anchor="mm")
        else:
            outline_btn(d, cx+75, 400, 120, 24, "선택하기", f=F_SM, color=GRAY_M, radius=6)
        cx += 290

    # 권장 표시
    rect(d, 200, 450, 1080, 520, fill=PANEL, outline=BORDER, radius=8)
    d.text((220, 476), "💡 권장:", font=F_B_MD, fill=ACCENT)
    d.text((310, 476), "게임·IT 업종에는 디스플레이 배너 + 네이티브 혼합이 CTR 1.8배 높습니다", font=F_MD, fill=GRAY_L)

    # 플로우 정보
    d.text((640, 540), "선택한 유형에 따라:", font=F_SM, fill=GRAY_M, anchor="mm")
    flow_items = ["맞춤 매체 자동 필터링", "지원 소재 사이즈 안내", "예상 단가 범위 표시"]
    for i, item in enumerate(flow_items):
        d.text((400+i*260, 568), f"✓  {item}", font=F_SM, fill=SUCCESS, anchor="mm")

    cta_btn(d, 490, 610, 300, 52, "다음: 매체 선택 →", color=ACCENT, radius=8)
    d.text((640, 680), "* 광고 유형은 나중에 변경할 수 있습니다", font=F_XS, fill=GRAY_D, anchor="mm")

    save(img, "05_campaign_ad_type.png")

# ═══════════════════════════════════════════════════════════
# 06 — Campaign: Step 2 (매체 선택)
# ═══════════════════════════════════════════════════════════
def gen_06_campaign_media_select():
    img, d = new_canvas()
    gnb(d)
    step_indicator(d, ["광고 유형", "매체 선택", "예산 설정", "소재 편집", "검토/제출"], active=1, top=90, left=220, spacing=195)

    d.text((250, 130), "AI 추천 매체", font=F_B_XL, fill=WHITE)
    d.text((250, 162), "업종·예산·타겟 기반 상위 추천", font=F_SM, fill=GRAY_M)

    # Category filter chips
    cats = ["전체", "게임", "커뮤니티", "여성", "금융", "교육"]
    cx = 250
    for i, c in enumerate(cats):
        cx = chip(d, cx, 186, c, active=(i == 1))

    # Media list (5 rows)
    media_rows = [
        ("인벤", "게임", "220만", "3.4%", "30만원~", "95", True),
        ("루리웹", "게임", "180만", "2.9%", "20만원~", "88", True),
        ("디시인사이드", "커뮤니티", "310만", "1.8%", "50만원~", "72", False),
        ("게임메카", "게임", "95만", "4.1%", "15만원~", "91", False),
        ("플레이포럼", "게임", "70만", "3.7%", "10만원~", "85", False),
    ]
    headers = ["", "매체명", "카테고리", "MAU", "CTR", "최소단가", "AdMix 점수", "액션"]
    widths = [50, 160, 110, 90, 80, 110, 130, 120]
    table_row(d, 230, 232, headers, widths, is_header=True)
    for ri, (name, cat, mau, ctr, price, score, selected) in enumerate(media_rows):
        ry = 270 + ri * 74
        bg = CHIP_BG if selected else (PANEL if ri % 2 == 0 else PANEL2)
        rect(d, 230, ry, 1050, ry+68, fill=bg, outline=ACCENT if selected else None, radius=4)
        # checkbox
        rect(d, 252, ry+18, 276, ry+44, fill=ACCENT2 if selected else None, outline=GRAY_D if not selected else None, radius=4)
        if selected:
            d.text((264, ry+31), "✓", font=F_SM, fill=WHITE, anchor="mm")
        cols = [name, cat, mau, ctr, price]
        cx2 = 280 + widths[0]
        for ci, col in enumerate(cols):
            d.text((cx2+10, ry+34), col, font=F_SM, fill=WHITE, anchor="lm")
            cx2 += widths[ci+1]
        # Score badge
        sc = int(score)
        sc_color = SUCCESS if sc >= 90 else (ACCENT2 if sc >= 75 else GRAY_M)
        rect(d, cx2+10, ry+18, cx2+70, ry+50, fill=sc_color, radius=14)
        d.text((cx2+40, ry+34), f"{score}점", font=F_B_SM, fill=WHITE, anchor="mm")
        cta_btn(d, cx2+80, ry+18, 80, 32, "선택" if not selected else "해제", color=ACCENT if not selected else GRAY_D, radius=6)

    # Right panel — 선택 요약
    rect(d, 1070, 120, W-20, H-20, fill=PANEL, outline=BORDER, radius=10)
    d.text((1168, 145), "선택 매체", font=F_B_MD, fill=WHITE, anchor="mm")
    d.text((1168, 170), "2 / 3 선택됨", font=F_SM, fill=GRAY_M, anchor="mm")
    for si, (name, _) in enumerate([("인벤", ""), ("루리웹", "")]):
        ry2 = 196 + si * 52
        rect(d, 1086, ry2, 1254, ry2+44, fill=PANEL2, radius=6)
        d.text((1100, ry2+22), name, font=F_MD, fill=WHITE, anchor="lm")
        d.text((1248, ry2+22), "×", font=F_LG, fill=GRAY_M, anchor="rm")

    d.text((1168, 320), "예상 주간 도달", font=F_XS, fill=GRAY_M, anchor="mm")
    d.text((1168, 346), "390만+", font=F_B_XL, fill=ACCENT, anchor="mm")
    d.text((1168, 374), "예상 CTR 범위", font=F_XS, fill=GRAY_M, anchor="mm")
    d.text((1168, 400), "3.1% ~ 3.7%", font=F_B_MD, fill=WHITE, anchor="mm")

    cta_btn(d, 1086, 700, 180, 44, "다음: 예산 설정 →", color=ACCENT, radius=8)

    save(img, "06_campaign_media_select.png")

# ═══════════════════════════════════════════════════════════
# 07 — Campaign: Step 3 (예산 설정)
# ═══════════════════════════════════════════════════════════
def gen_07_campaign_budget():
    img, d = new_canvas()
    gnb(d)
    step_indicator(d, ["광고 유형", "매체 선택", "예산 설정", "소재 편집", "검토/제출"], active=2, top=90, left=220, spacing=195)

    # Left: budget form
    d.text((380, 140), "예산 및 일정 설정", font=F_B_XL, fill=WHITE)

    # Total budget
    input_field(d, 250, 190, 400, 44, "총 예산 *", "", "1,000,000원")
    input_field(d, 700, 190, 280, 44, "일 예산 (자동 계산)", "", "71,428원")

    # Budget type
    d.text((250, 258), "예산 유형 *", font=F_SM, fill=GRAY_M)
    for i, (label, desc) in enumerate([("CPM", "1,000회 노출당"), ("CPC", "클릭당"), ("CPV", "조회당")]):
        is_active = i == 0
        rect(d, 250+i*220, 278, 440+i*220, 322, fill=ACCENT2 if is_active else PANEL, outline=ACCENT2 if is_active else GRAY_D, radius=8)
        d.text((345+i*220, 295), label, font=F_B_MD, fill=WHITE, anchor="mm")
        d.text((345+i*220, 313), desc, font=F_XS, fill=GRAY_M if not is_active else GRAY_L, anchor="mm")

    # Spend pacing
    d.text((250, 338), "예산 소진 방식", font=F_SM, fill=GRAY_M)
    for i, label in enumerate(["균등 배분", "빠른 소진"]):
        rect(d, 250+i*200, 358, 430+i*200, 396, fill=ACCENT2 if i == 0 else PANEL, outline=ACCENT2 if i == 0 else GRAY_D, radius=8)
        d.text((340+i*200, 377), label, font=F_MD, fill=WHITE, anchor="mm")

    # Date picker
    d.text((250, 418), "캠페인 기간 *", font=F_SM, fill=GRAY_M)
    rect(d, 250, 438, 470, 482, fill=PANEL2, outline=BORDER, radius=6)
    d.text((360, 460), "📅  2026.05.01", font=F_MD, fill=WHITE, anchor="mm")
    d.text((500, 460), "~", font=F_XL, fill=GRAY_M, anchor="mm")
    rect(d, 530, 438, 750, 482, fill=PANEL2, outline=BORDER, radius=6)
    d.text((640, 460), "📅  2026.05.14", font=F_MD, fill=WHITE, anchor="mm")
    d.text((790, 460), "14일", font=F_SM, fill=ACCENT, anchor="lm")

    # 매체별 예산 배분
    d.text((250, 510), "매체별 예산 배분", font=F_B_MD, fill=WHITE)
    media_budgets = [("인벤", 60, "600,000원"), ("루리웹", 40, "400,000원")]
    for i, (name, pct, amt) in enumerate(media_budgets):
        my = 540 + i * 80
        d.text((250, my), name, font=F_MD, fill=WHITE)
        d.text((250, my+26), f"{pct}%", font=F_B_SM, fill=ACCENT, anchor="lm")
        progress_bar(d, 320, my+22, 400, 12, pct, color=ACCENT2)
        d.text((740, my+28), amt, font=F_SM, fill=GRAY_M, anchor="lm")
        d.text((900, my+28), "조정하기 ✎", font=F_SM, fill=ACCENT2, anchor="lm")

    # Right: summary
    rect(d, 1020, 130, W-20, H-20, fill=PANEL, outline=BORDER, radius=10)
    d.text((1160, 155), "예산 요약", font=F_B_MD, fill=WHITE, anchor="mm")
    summary_items = [
        ("총 예산", "1,000,000원"),
        ("VAT (10%)", "100,000원"),
        ("VAT 포함 합계", "1,100,000원"),
        ("캠페인 기간", "14일"),
        ("일 예산", "71,428원"),
        ("예상 노출", "580,000회+"),
        ("예상 클릭", "18,000회+"),
    ]
    sy = 185
    for label, val in summary_items:
        d.text((1038, sy), label, font=F_SM, fill=GRAY_M)
        d.text((1270, sy), val, font=F_B_SM, fill=WHITE, anchor="rm")
        sy += 38
    d.line([(1038, sy), (1272, sy)], fill=BORDER, width=1)
    d.text((1038, sy+16), "최종 결제 금액", font=F_B_MD, fill=WHITE)
    d.text((1272, sy+16), "1,100,000원", font=F_B_LG, fill=ACCENT, anchor="rm")

    cta_btn(d, 1038, 700, 230, 44, "다음: 소재 편집 →", color=ACCENT, radius=8)

    save(img, "07_campaign_budget.png")

# ═══════════════════════════════════════════════════════════
# 08 — Campaign: Step 4 (소재 편집) ★ CORE
# ═══════════════════════════════════════════════════════════
def gen_08_campaign_creative():
    img, d = new_canvas()
    gnb(d)
    step_indicator(d, ["광고 유형", "매체 선택", "예산 설정", "소재 편집", "검토/제출"], active=3, top=90, left=220, spacing=195)

    # Left: size list (130px wide)
    rect(d, 0, 110, 160, H, fill=PANEL, radius=0)
    d.line([(160, 110), (160, H)], fill=BORDER, width=1)
    d.text((80, 130), "사이즈", font=F_B_SM, fill=GRAY_M, anchor="mm")

    sizes = [
        ("인벤", None, False),
        ("728×90", "✓", True),
        ("300×250", "✓", True),
        ("970×90", "", False),
        ("320×50", "", False),
        ("맘카페", None, False),
        ("728×90", "✓", True),
        ("320×100", "", False),
        ("320×480", "", False),
    ]
    sy = 152
    for name, check, active in sizes:
        if check is None:
            d.text((12, sy), name, font=F_B_XS if hasattr(d, 'F_B_XS') else F_B_SM, fill=GRAY_M)
        else:
            bg = CHIP_BG if active else None
            if bg:
                rect(d, 6, sy-4, 154, sy+20, fill=bg, radius=4)
            d.text((16, sy+8), f"{'☑' if active else '☐'}  {name}", font=F_XS, fill=WHITE if active else GRAY_M, anchor="lm")
        sy += 28

    # Center: canvas
    rect(d, 160, 110, 960, H-60, fill=PANEL2, radius=0)
    d.text((560, 130), "소재 편집 캔버스", font=F_B_SM, fill=GRAY_M, anchor="mm")

    # Simulated canvas area
    rect(d, 200, 150, 920, 560, fill=BG, outline=GRAY_D, radius=4)
    # Mock banner image
    rect(d, 240, 190, 880, 360, fill=PANEL, outline=BORDER, radius=4)
    d.text((560, 250), "🖼️ 이미지 영역", font=F_2XL, fill=GRAY_D, anchor="mm")
    d.text((560, 300), "728 × 90 프리뷰", font=F_SM, fill=GRAY_D, anchor="mm")
    # Text layer overlay
    rect(d, 240, 370, 880, 430, fill=PANEL2, outline=ACCENT, radius=4)
    d.text((560, 400), "텍스트 레이어 — 클릭하여 편집", font=F_MD, fill=ACCENT, anchor="mm")

    # Canvas toolbar
    rect(d, 200, 576, 920, 616, fill=PANEL, radius=0)
    tools = ["✂️ 크롭", "↔️ 위치", "T 텍스트", "⬜ 패딩", "↩️ 실행취소", "↺ 재실행"]
    tx = 220
    for t in tools:
        outline_btn(d, tx, 581, 100, 30, t, f=F_XS, color=GRAY_M, radius=6)
        tx += 118

    # Upload zone
    rect(d, 200, 628, 920, H-20, fill=PANEL, outline=BORDER, radius=6)
    d.text((560, 660), "📂  드래그 & 드롭 또는 클릭해서 소재 업로드 (PNG/JPG/GIF, 최대 10MB)", font=F_SM, fill=GRAY_M, anchor="mm")
    d.text((560, 688), "진행 중: admix_banner_v3.png ■■■■■■□□□□  60%", font=F_XS, fill=ACCENT2, anchor="mm")

    # Right: AI copy panel
    rect(d, 960, 110, W, H, fill=PANEL, radius=0)
    d.line([(960, 110), (960, H)], fill=BORDER, width=1)
    d.text((1120, 130), "AI 후킹 문구", font=F_B_SM, fill=WHITE, anchor="mm")

    # Tone tabs
    tones = ["임팩트형", "친근형", "프리미엄형"]
    tx2 = 968
    for i, tone in enumerate(tones):
        active = i == 0
        bg2 = ACCENT2 if active else PANEL2
        rect(d, tx2, 148, tx2+90, 174, fill=bg2, radius=6)
        d.text((tx2+45, 161), tone, font=F_XS, fill=WHITE, anchor="mm")
        tx2 += 96

    # Copy cards
    copies = [
        "지금 바로 인벤에서\n클릭률 3배 높은\n광고를 시작하세요!",
        "게임 유저가\n몰리는 그 곳,\nAdMix가 연결합니다",
        "전략적 광고 집행의\n시작, 지금\n당신의 차례입니다",
    ]
    cy2 = 186
    for i, copy in enumerate(copies):
        bg3 = CHIP_BG if i == 0 else PANEL2
        rect(d, 968, cy2, W-16, cy2+100, fill=bg3, outline=ACCENT if i == 0 else BORDER, radius=8)
        for li, line in enumerate(copy.split("\n")):
            d.text((984, cy2+20+li*22), line, font=F_SM, fill=WHITE if i == 0 else GRAY_M)
        if i == 0:
            d.text((1240, cy2+80), "적용하기 →", font=F_B_SM, fill=ACCENT, anchor="rm")
        cy2 += 116

    d.text((1120, 570), "단순도 스코어: 0.42", font=F_SM, fill=WARNING, anchor="mm")
    d.text((1120, 596), "⚠️ AI 후킹 패널 자동 오픈됨", font=F_XS, fill=WARNING, anchor="mm")
    rect(d, 968, 620, W-16, 644, fill=None, outline=GRAY_D, radius=6)
    d.text((1120, 632), "직접 문구 입력...", font=F_SM, fill=GRAY_D, anchor="mm")
    cta_btn(d, 968, 660, 292, 40, "새 문구 생성", color=ACCENT2, radius=6)

    save(img, "08_campaign_creative.png")

# ═══════════════════════════════════════════════════════════
# 09 — Campaign: Step 5 (검토/제출)
# ═══════════════════════════════════════════════════════════
def gen_09_campaign_review():
    img, d = new_canvas()
    gnb(d)
    step_indicator(d, ["광고 유형", "매체 선택", "예산 설정", "소재 편집", "검토/제출"], active=4, top=90, left=220, spacing=195)

    d.text((640, 140), "캠페인 최종 검토", font=F_B_2XL, fill=WHITE, anchor="mm")
    d.text((640, 172), "아래 내용을 확인하고 캠페인을 제출하세요", font=F_MD, fill=GRAY_M, anchor="mm")

    # Review sections (2 columns)
    sections = [
        (80, 200, "광고 유형", [("유형", "디스플레이 배너"), ("목표", "브랜드 인지도")]),
        (660, 200, "예산 & 일정", [("총 예산", "1,100,000원 (VAT 포함)"), ("기간", "2026.05.01 ~ 05.14 (14일)")]),
        (80, 390, "선택 매체", [("인벤", "600,000원 / 주간"), ("루리웹", "400,000원 / 주간")]),
        (660, 390, "소재", [("728×90", "admix_banner_v3.png ✓"), ("300×250", "auto-generated ✓")]),
    ]
    for sx, sy2, title, items in sections:
        rect(d, sx, sy2, sx+540, sy2+170, fill=PANEL, outline=BORDER, radius=10)
        rect(d, sx, sy2, sx+540, sy2+40, fill=PANEL2, radius=10)
        d.text((sx+20, sy2+20), title, font=F_B_MD, fill=WHITE)
        d.text((sx+510, sy2+20), "수정하기 ✎", font=F_SM, fill=ACCENT2, anchor="rm")
        for ii, (label, val) in enumerate(items):
            d.text((sx+20, sy2+60+ii*44), label, font=F_SM, fill=GRAY_M)
            d.text((sx+520, sy2+60+ii*44), val, font=F_SM, fill=WHITE, anchor="rm")

    # Payment section
    rect(d, 80, 580, 760, 740, fill=PANEL, outline=BORDER, radius=10)
    d.text((100, 600), "결제 정보", font=F_B_MD, fill=WHITE)
    d.text((100, 636), "신용카드", font=F_SM, fill=GRAY_M)
    d.text((100, 660), "**** **** **** 1234  |  유효기간 12/27", font=F_MD, fill=WHITE)
    d.text((100, 686), "결제 금액:  1,100,000원  (VAT 10% 포함)", font=F_B_MD, fill=ACCENT)
    cta_btn(d, 100, 710, 200, 36, "결제 수단 변경", color=PANEL2, radius=6)

    # Terms
    rect(d, 800, 580, W-80, 740, fill=PANEL, outline=BORDER, radius=10)
    d.text((820, 600), "계약 및 동의", font=F_B_MD, fill=WHITE)
    terms = ["[필수] AdMix 광고 집행 약관 동의", "[필수] 환불 정책 확인 및 동의", "[선택] 마케팅 정보 수신 동의"]
    for i, term in enumerate(terms):
        rect(d, 820, 632+i*36, 844, 656+i*36, fill=ACCENT2 if i < 2 else None, outline=None if i < 2 else GRAY_D, radius=4)
        if i < 2:
            d.text((832, 644+i*36), "✓", font=F_XS, fill=WHITE, anchor="mm")
        d.text((856, 644+i*36), term, font=F_SM, fill=GRAY_L if i < 2 else GRAY_M, anchor="lm")
    d.text((820, 748), "계약서 PDF 다운로드 →", font=F_SM, fill=ACCENT2)

    cta_btn(d, 300, 758, 680, 56, "캠페인 제출 및 결제  →  1,100,000원", color=ACCENT, radius=10)
    d.text((640, 738), "제출 후 24시간 내 검토 완료, 승인 즉시 집행 시작", font=F_XS, fill=GRAY_D, anchor="mm")

    save(img, "09_campaign_review.png")

# ═══════════════════════════════════════════════════════════
# 10 — Advertiser Dashboard
# ═══════════════════════════════════════════════════════════
def gen_10_ad_dashboard():
    img, d = new_canvas()
    gnb(d, with_nav=False)
    sidebar_items = [("🏠", "대시보드"), ("📣", "캠페인"), ("📊", "분석"), ("🖼️", "소재"), ("💳", "결제"), ("⚙️", "설정")]
    sidebar(d, sidebar_items, active_idx=0)

    # Main content
    mx = 220
    d.text((mx+10, 74), "안녕하세요, 홍길동님 👋", font=F_B_XL, fill=WHITE)
    d.text((mx+10, 104), "현재 집행 중인 캠페인 2개 | 마지막 업데이트: 방금 전", font=F_SM, fill=GRAY_M)
    cta_btn(d, W-200, 68, 168, 40, "+ 새 캠페인 만들기", color=ACCENT, radius=8)

    # KPI cards
    kpis = [
        ("총 노출", "1,240,000", "+12.4%", "이번 달"),
        ("총 클릭", "38,200", "+8.1%", "이번 달"),
        ("평균 CTR", "3.08%", "+0.8%p", "업종 평균 2.3%"),
        ("예산 소진율", "67%", None, "잔여 330,000원"),
    ]
    kw = (W - mx - 60) // 4
    for i, (label, val, trend, sub) in enumerate(kpis):
        stat_card(d, mx+10+i*(kw+10), 128, kw, 90, label, val, sub=sub, trend=trend or "")

    # Campaign list
    d.text((mx+10, 236), "캠페인 현황", font=F_B_LG, fill=WHITE)
    campaigns = [
        ("게임 유저 타겟 배너 캠페인", "집행중", "인벤 + 루리웹", "820,000", "540,000", 66, "3.2%", "2026.05.01~05.14"),
        ("봄 신상품 런칭 캠페인", "검토중", "맘카페 + 여성포털", "500,000", "0", 0, "-", "2026.05.10~05.24"),
    ]
    ch = [("캠페인명", 260), ("상태", 80), ("매체", 150), ("총예산", 110), ("소진액", 110), ("소진율", 180), ("CTR", 80), ("기간", 160)]
    cx2 = mx + 10
    for label, cw in ch:
        d.text((cx2+6, 264), label, font=F_B_SM, fill=GRAY_M)
        cx2 += cw
    d.line([(mx+10, 282), (W-20, 282)], fill=BORDER, width=1)

    for ri, (name, status, media, total, spent, pct, ctr, period) in enumerate(campaigns):
        ry = 290 + ri * 120
        rect(d, mx+10, ry, W-20, ry+110, fill=PANEL, outline=BORDER, radius=8)
        cx3 = mx + 20
        # Status badge
        sc2 = SUCCESS if status == "집행중" else WARNING
        d.text((cx3, ry+18), name, font=F_B_MD, fill=WHITE)
        rect(d, cx3, ry+44, cx3+60, ry+66, fill=sc2, radius=10)
        d.text((cx3+30, ry+55), status, font=F_XS, fill=WHITE, anchor="mm")
        cx3 += 266
        d.text((cx3+6, ry+36), media, font=F_SM, fill=GRAY_L)
        cx3 += 150
        d.text((cx3+6, ry+36), f"{total}원", font=F_SM, fill=WHITE)
        cx3 += 110
        d.text((cx3+6, ry+36), f"{spent}원" if spent != "0" else "0원", font=F_SM, fill=ACCENT)
        cx3 += 110
        progress_bar(d, cx3+6, ry+40, 160, 10, pct, color=ACCENT2 if pct < 80 else WARNING)
        d.text((cx3+6, ry+60), f"{pct}%", font=F_XS, fill=GRAY_M)
        cx3 += 180
        ctr_col = SUCCESS if ctr != "-" else GRAY_M
        d.text((cx3+6, ry+36), ctr, font=F_B_SM, fill=ctr_col)
        cx3 += 80
        d.text((cx3+6, ry+36), period, font=F_XS, fill=GRAY_M)
        # Action buttons
        cta_btn(d, W-220, ry+30, 90, 32, "상세보기", color=ACCENT2, radius=6)
        outline_btn(d, W-120, ry+30, 80, 32, "일시정지", color=GRAY_M, radius=6)

    # Benchmark section
    rect(d, mx+10, 548, W-20, 720, fill=PANEL, outline=BORDER, radius=10)
    d.text((mx+20, 568), "업종 평균 벤치마크 (게임)", font=F_B_MD, fill=WHITE)
    d.text((mx+20, 596), "내 캠페인 CTR  3.2%", font=F_MD, fill=SUCCESS)
    d.text((mx+20, 620), "업종 평균 CTR  2.3%", font=F_MD, fill=GRAY_M)
    d.text((mx+20, 644), "▲ 업종 평균 대비 +0.9%p 아웃퍼폼", font=F_B_MD, fill=SUCCESS)
    # mini chart
    mini_chart(d, mx+430, 560, 560, 140, [2.1, 2.4, 2.2, 2.8, 3.0, 2.9, 3.2, 3.5, 3.2], color=ACCENT2)
    d.text((mx+430+280, 556), "CTR 추이 (최근 9일)", font=F_XS, fill=GRAY_M, anchor="mm")

    # Next action
    rect(d, mx+10, 728, W-20, H-20, fill=CHIP_BG, outline=ACCENT, radius=8)
    d.text((mx+30, 758), "💡 다음 액션: 루리웹 CTR이 4.1%로 인벤(2.8%)보다 높습니다. 루리웹 예산 비중을 40% → 60%로 늘려보세요.", font=F_SM, fill=WHITE)
    cta_btn(d, W-230, 742, 200, 36, "예산 조정하기 →", color=ACCENT, radius=6)

    save(img, "10_ad_dashboard.png")

# ═══════════════════════════════════════════════════════════
# 11 — Campaign Analytics
# ═══════════════════════════════════════════════════════════
def gen_11_campaign_analytics():
    img, d = new_canvas()
    gnb(d, with_nav=False)
    sidebar_items = [("🏠", "대시보드"), ("📣", "캠페인"), ("📊", "분석"), ("🖼️", "소재"), ("💳", "결제"), ("⚙️", "설정")]
    sidebar(d, sidebar_items, active_idx=2)

    mx = 220
    d.text((mx+10, 74), "캠페인 분석", font=F_B_XL, fill=WHITE)
    d.text((mx+10, 102), "게임 유저 타겟 배너 캠페인  |  2026.05.01 ~ 05.14", font=F_SM, fill=GRAY_M)

    # Date range selector
    for i, label in enumerate(["7일", "14일", "30일", "직접설정"]):
        active = i == 1
        rect(d, W-280+i*60, 72, W-226+i*60, 96, fill=ACCENT2 if active else PANEL2, outline=BORDER, radius=4)
        d.text((W-253+i*60, 84), label, font=F_XS, fill=WHITE, anchor="mm")

    # Summary KPI
    kpis = [("노출", "1,240,000", "+12.4%"), ("클릭", "38,200", "+8.1%"), ("CTR", "3.08%", "+0.8%p"), ("CPM", "18,200원", "-3.2%"), ("CPC", "280원", "-5.1%")]
    kw2 = (W - mx - 30) // 5
    for i, (lbl, val, trend) in enumerate(kpis):
        stat_card(d, mx+10+i*(kw2+4), 122, kw2-4, 72, lbl, val, trend=trend)

    # Daily trend chart (area simulation)
    rect(d, mx+10, 210, W-20, 420, fill=PANEL, outline=BORDER, radius=10)
    d.text((mx+26, 228), "일별 성과 추이", font=F_B_MD, fill=WHITE)
    d.text((W-100, 228), "CTR ● 클릭수 ●", font=F_XS, fill=GRAY_M, anchor="rm")
    chart_data = [2.1, 2.8, 3.0, 2.7, 3.2, 3.5, 3.1, 3.4, 3.6, 3.2, 3.8, 3.5, 3.2, 3.0]
    mini_chart(d, mx+26, 248, W-mx-56, 152, chart_data, color=ACCENT2)
    # X-axis labels
    days = ["5/1","5/2","5/3","5/4","5/5","5/6","5/7","5/8","5/9","5/10","5/11","5/12","5/13","5/14"]
    lw = (W-mx-82) / (len(days)-1)
    for i, day in enumerate(days):
        d.text((mx+26+int(i*lw), 408), day, font=F_XS, fill=GRAY_M, anchor="mm")

    # Media comparison
    rect(d, mx+10, 432, (mx+W)//2-10, H-20, fill=PANEL, outline=BORDER, radius=10)
    d.text((mx+26, 450), "매체별 성과 비교", font=F_B_MD, fill=WHITE)
    media_perf = [
        ("인벤", "620,000", "19,500", "3.1%", "290원", 60),
        ("루리웹", "420,000", "18,700", "4.1%", "230원", 40),
    ]
    hdr = ["매체", "노출", "클릭", "CTR", "CPC", "예산비중"]
    hw = [100, 110, 80, 80, 90, 120]
    hx = mx + 26
    for h, hw2 in zip(hdr, hw):
        d.text((hx, 476), h, font=F_B_SM, fill=GRAY_M)
        hx += hw2
    for ri2, (mname, imp, clk, ctr, cpc, bpct) in enumerate(media_perf):
        ry2 = 500 + ri2 * 50
        bg4 = PANEL2 if ri2 == 0 else None
        if bg4:
            rect(d, mx+16, ry2-4, (mx+W)//2-16, ry2+44, fill=bg4, radius=4)
        vals = [mname, imp, clk, ctr, cpc, f"{bpct}%"]
        vx = mx + 26
        for vi, (v, vw) in enumerate(zip(vals, hw)):
            col2 = SUCCESS if vi == 3 and ri2 == 1 else WHITE
            d.text((vx, ry2+18), v, font=F_SM, fill=col2, anchor="lm")
            vx += vw
        progress_bar(d, mx+400, ry2+12, 100, 8, bpct, color=ACCENT2)

    # Creative performance
    rect(d, (mx+W)//2+10, 432, W-20, H-20, fill=PANEL, outline=BORDER, radius=10)
    cx_start2 = (mx+W)//2 + 26
    d.text((cx_start2, 450), "소재별 성과", font=F_B_MD, fill=WHITE)
    creative_data = [
        ("728×90 v3", "3.8%", "우수"),
        ("300×250 v2", "2.4%", "보통"),
        ("320×50 v1", "1.9%", "개선 필요"),
    ]
    for ri3, (cname, ctr2, status3) in enumerate(creative_data):
        ry3 = 486 + ri3 * 72
        rect(d, cx_start2, ry3, W-36, ry3+64, fill=PANEL2, radius=6)
        rect(d, cx_start2+8, ry3+8, cx_start2+60, ry3+56, fill=BORDER, radius=4)
        d.text((cx_start2+34, ry3+32), "IMG", font=F_XS, fill=GRAY_D, anchor="mm")
        d.text((cx_start2+72, ry3+22), cname, font=F_B_SM, fill=WHITE)
        d.text((cx_start2+72, ry3+44), f"CTR {ctr2}", font=F_SM, fill=ACCENT2)
        sc3_col = SUCCESS if status3 == "우수" else (WARNING if status3 == "보통" else DANGER)
        rect(d, W-120, ry3+20, W-44, ry3+44, fill=sc3_col, radius=10)
        d.text((W-82, ry3+32), status3, font=F_XS, fill=WHITE, anchor="mm")

    save(img, "11_campaign_analytics.png")

# ═══════════════════════════════════════════════════════════
# 12 — Creative Management (소재 관리)
# ═══════════════════════════════════════════════════════════
def gen_12_creative_management():
    img, d = new_canvas()
    gnb(d, with_nav=False)
    sidebar_items = [("🏠", "대시보드"), ("📣", "캠페인"), ("📊", "분석"), ("🖼️", "소재"), ("💳", "결제"), ("⚙️", "설정")]
    sidebar(d, sidebar_items, active_idx=3)

    mx = 220
    d.text((mx+10, 74), "소재 라이브러리", font=F_B_XL, fill=WHITE)
    cta_btn(d, W-200, 68, 168, 40, "소재 업로드 +", color=ACCENT, radius=8)

    # Filter tabs
    tabs = ["전체 소재", "집행중", "승인대기", "반려됨", "보관됨"]
    tx3 = mx + 10
    for i, tab in enumerate(tabs):
        active = i == 0
        bg5 = ACCENT2 if active else PANEL
        rect(d, tx3, 102, tx3+110, 130, fill=bg5, outline=BORDER if not active else None, radius=6)
        d.text((tx3+55, 116), tab, font=F_SM, fill=WHITE, anchor="mm")
        tx3 += 120

    # Creative grid
    creatives = [
        ("728×90", "v3", "승인됨", SUCCESS, "3.8%", "admix_banner_v3"),
        ("300×250", "v2", "승인됨", SUCCESS, "2.4%", "admix_box_v2"),
        ("970×90", "v1", "승인대기", WARNING, "-", "admix_lb_v1"),
        ("320×50", "v1", "승인됨", SUCCESS, "1.9%", "admix_mob_v1"),
        ("320×480", "v2", "반려됨", DANGER, "-", "admix_inter_v2"),
        ("728×90", "v4", "초안", GRAY_M, "-", "admix_banner_v4"),
    ]
    gx2, gy2 = mx+10, 148
    for i, (size, ver, status4, sc4, ctr3, fname) in enumerate(creatives):
        row, col = divmod(i, 3)
        cx4 = gx2 + col * 348
        cy4 = gy2 + row * 290
        rect(d, cx4, cy4, cx4+330, cy4+270, fill=PANEL, outline=BORDER, radius=10)
        # Thumbnail
        rect(d, cx4+12, cy4+12, cx4+318, cy4+170, fill=PANEL2, radius=6)
        d.text((cx4+165, cy4+91), f"[ {size} ]", font=F_LG, fill=GRAY_D, anchor="mm")
        d.text((cx4+165, cy4+120), fname, font=F_XS, fill=GRAY_D, anchor="mm")
        # Status badge
        rect(d, cx4+12, cy4+178, cx4+100, cy4+198, fill=sc4, radius=8)
        d.text((cx4+56, cy4+188), status4, font=F_XS, fill=WHITE, anchor="mm")
        # Labels
        d.text((cx4+12, cy4+208), f"{size}  {ver}", font=F_B_SM, fill=WHITE)
        d.text((cx4+12, cy4+232), f"CTR: {ctr3}", font=F_SM, fill=GRAY_M)
        # Actions
        cta_btn(d, cx4+140, cy4+234, 90, 28, "편집", color=ACCENT2, radius=6)
        cta_btn(d, cx4+240, cy4+234, 80, 28, "복사", color=PANEL2, radius=6)
        if status4 == "반려됨":
            d.text((cx4+12, cy4+254), "⚠ 사유: 이미지 해상도 부족 (최소 72dpi)", font=F_XS, fill=DANGER)

    save(img, "12_creative_management.png")

# ═══════════════════════════════════════════════════════════
# 13 — Publisher Onboarding
# ═══════════════════════════════════════════════════════════
def gen_13_publisher_onboarding():
    img, d = new_canvas()
    gnb(d)

    # Split layout
    rect(d, 0, 56, 520, H, fill=PANEL, radius=0)
    d.line([(520, 56), (520, H)], fill=BORDER, width=1)

    # Left: value prop
    d.text((260, 110), "퍼블리셔로 수익을 만드세요", font=F_B_2XL, fill=WHITE, anchor="mm")
    d.text((260, 148), "전문 버티컬 매체로 광고 수익 극대화", font=F_MD, fill=GRAY_M, anchor="mm")

    perks = [
        ("💰", "업계 최고 수익 배분", "광고주 예산의 75% 퍼블리셔 지급"),
        ("⚡", "즉시 게재 가능", "신청 후 24시간 내 승인"),
        ("📊", "실시간 수익 대시보드", "일별/월별 수익 및 정산 현황"),
        ("🤝", "전담 매니저 지원", "광고 최적화 1:1 컨설팅"),
    ]
    py2 = 200
    for icon2, title2, desc2 in perks:
        d.text((80, py2), icon2, font=F_2XL, fill=WHITE, anchor="mm")
        d.text((120, py2-10), title2, font=F_B_MD, fill=WHITE)
        d.text((120, py2+14), desc2, font=F_SM, fill=GRAY_M)
        py2 += 90

    # Revenue estimate
    rect(d, 40, 570, 480, 680, fill=CHIP_BG, outline=ACCENT, radius=10)
    d.text((260, 598), "수익 시뮬레이터", font=F_B_MD, fill=WHITE, anchor="mm")
    d.text((260, 626), "MAU 10만 기준 예상 월 수익", font=F_SM, fill=GRAY_M, anchor="mm")
    d.text((260, 658), "800,000원 ~ 3,200,000원", font=F_B_2XL, fill=ACCENT, anchor="mm")

    # Right: registration form
    d.text((810, 100), "퍼블리셔 신청", font=F_B_2XL, fill=WHITE, anchor="mm")
    d.text((810, 134), "간단한 정보를 입력해 바로 시작하세요", font=F_MD, fill=GRAY_M, anchor="mm")

    fields2 = [
        (540, 170, 560, 44, "사이트 URL *", "", "https://www.yourmedia.com"),
        (540, 258, 260, 44, "매체명 *", "", "게임인사이드"),
        (820, 258, 280, 44, "월 UV (순방문자) *", "", "150,000"),
        (540, 346, 560, 44, "주요 카테고리 *", "", ""),
    ]
    for fx, fy, fw, fh, label, ph, val in fields2:
        input_field(d, fx, fy, fw, fh, label, ph, val)

    # Category chips
    cats2 = ["게임", "IT/테크", "스포츠", "엔터테인먼트", "뉴스"]
    cx5 = 540
    for i, c in enumerate(cats2):
        cx5 = chip(d, cx5, 382, c, active=(i == 0))

    # Media types
    d.text((540, 430), "지원 광고 형식 *", font=F_SM, fill=GRAY_M)
    for i, mtype in enumerate(["배너", "네이티브", "동영상", "텍스트링크"]):
        rect(d, 540+i*145, 450, 670+i*145, 490, fill=ACCENT2 if i <= 1 else PANEL, outline=BORDER, radius=8)
        d.text((605+i*145, 470), mtype, font=F_SM, fill=WHITE, anchor="mm")

    # File upload (사업자등록증)
    rect(d, 540, 510, 1100, 560, fill=PANEL2, outline=BORDER, radius=6)
    d.text((820, 535), "📎  사업자등록증 첨부 (PDF/JPG, 선택)", font=F_SM, fill=GRAY_D, anchor="mm")

    cta_btn(d, 540, 578, 560, 52, "퍼블리셔 신청하기 →", color=ACCENT, radius=8)
    d.text((820, 648), "✓ 신청 후 1영업일 내 검토 및 안내 메일 발송", font=F_SM, fill=SUCCESS, anchor="mm")

    save(img, "13_publisher_onboarding.png")

# ═══════════════════════════════════════════════════════════
# 14 — Publisher Slots (광고 슬롯 등록)
# ═══════════════════════════════════════════════════════════
def gen_14_publisher_slots():
    img, d = new_canvas()
    gnb(d, with_nav=False)
    sidebar_items = [("🏠", "대시보드"), ("📐", "슬롯 관리"), ("📊", "수익 분석"), ("💰", "정산"), ("⚙️", "설정")]
    sidebar(d, sidebar_items, active_idx=1)

    mx = 220
    d.text((mx+10, 74), "광고 슬롯 관리", font=F_B_XL, fill=WHITE)
    cta_btn(d, W-200, 68, 168, 40, "+ 슬롯 추가하기", color=ACCENT, radius=8)

    # Slot list table
    headers2 = ["슬롯명", "게재 위치", "사이즈", "카테고리", "일 UV", "상태", "월 수익", "액션"]
    widths2 = [160, 220, 110, 110, 80, 90, 120, 120]
    table_row(d, mx+10, 112, headers2, widths2, is_header=True)

    slots = [
        ("게임인사이드_LB", "메인 상단 / 게시글 상단", "728×90", "게임", "12만", "집행중", "820,000원", SUCCESS),
        ("게임인사이드_BOX", "사이드바 우측", "300×250", "게임", "8만", "집행중", "440,000원", SUCCESS),
        ("게임인사이드_MOB", "모바일 하단 고정", "320×50", "게임", "15만", "승인대기", "-", WARNING),
        ("게임인사이드_INT", "기사 중간 인터스티셜", "320×480", "게임", "5만", "비활성", "0원", GRAY_M),
    ]
    for ri4, (sname, pos, size2, cat3, uv, status5, rev, sc5) in enumerate(slots):
        ry4 = 150 + ri4 * 72
        bg6 = PANEL if ri4 % 2 == 0 else PANEL2
        rect(d, mx+10, ry4, mx+1030, ry4+64, fill=bg6, radius=4)
        vals2 = [sname, pos, size2, cat3, uv]
        vx2 = mx + 20
        for vi2, (v2, vw2) in enumerate(zip(vals2, widths2[:5])):
            d.text((vx2+4, ry4+32), v2, font=F_SM, fill=WHITE, anchor="lm")
            vx2 += vw2
        # Status
        rect(d, vx2+4, ry4+18, vx2+80, ry4+46, fill=sc5, radius=12)
        d.text((vx2+42, ry4+32), status5, font=F_XS, fill=WHITE, anchor="mm")
        vx2 += widths2[5]
        d.text((vx2+4, ry4+32), rev, font=F_B_SM, fill=ACCENT if rev != "0원" and rev != "-" else GRAY_D, anchor="lm")
        vx2 += widths2[6]
        cta_btn(d, vx2+4, ry4+18, 60, 28, "편집", color=ACCENT2, radius=6)
        outline_btn(d, vx2+70, ry4+18, 50, 28, "삭제", color=DANGER, radius=6)

    # Add slot form
    rect(d, mx+10, 446, W-20, H-20, fill=PANEL, outline=BORDER, radius=10)
    d.text((mx+26, 466), "새 광고 슬롯 추가", font=F_B_LG, fill=WHITE)

    input_field(d, mx+26, 510, 300, 40, "슬롯명 *", "", "게임인사이드_NEW")
    input_field(d, mx+346, 510, 400, 40, "게재 페이지 URL *", "", "https://gameinside.com/main")

    d.text((mx+26, 578), "광고 사이즈 *", font=F_SM, fill=GRAY_M)
    sizes2 = ["728×90", "300×250", "320×50", "320×480", "970×90", "300×600"]
    sx2 = mx + 26
    for s2 in sizes2:
        sx2 = chip(d, sx2, 598, s2, active=(s2 == "728×90"))

    input_field(d, mx+700, 578, 250, 40, "예상 일 UV *", "", "50,000")
    cta_btn(d, mx+970, 578, 200, 40, "슬롯 등록하기 →", color=ACCENT, radius=8)

    d.text((mx+26, 658), "슬롯 가이드: 최소 MAU 1만 이상, 청소년 유해 콘텐츠 페이지 제외, 광고 차단 스크립트 미설치", font=F_XS, fill=GRAY_D)
    d.text((mx+26, 680), "승인 기준: 브랜드 세이프티 점수 70점 이상, 트래픽 검증 (SimilarWeb 기준)", font=F_XS, fill=GRAY_D)

    save(img, "14_publisher_slots.png")

# ═══════════════════════════════════════════════════════════
# 15 — Publisher Dashboard
# ═══════════════════════════════════════════════════════════
def gen_15_publisher_dashboard():
    img, d = new_canvas()
    gnb(d, with_nav=False)
    sidebar_items = [("🏠", "대시보드"), ("📐", "슬롯 관리"), ("📊", "수익 분석"), ("💰", "정산"), ("⚙️", "설정")]
    sidebar(d, sidebar_items, active_idx=0)

    mx = 220
    d.text((mx+10, 74), "수익 대시보드", font=F_B_XL, fill=WHITE)
    d.text((mx+10, 102), "게임인사이드  |  2026년 5월", font=F_SM, fill=GRAY_M)

    # KPI cards
    pub_kpis = [
        ("이번 달 수익", "1,260,000원", "+18.4%", "지난달 1,064,000원"),
        ("총 노출", "892,000회", "+22.1%", "이번 달"),
        ("평균 CPM", "1,412원", "+4.2%", "업종 평균 1,100원"),
        ("정산 잔액", "480,000원", None, "다음 정산: 6/10"),
    ]
    kw3 = (W - mx - 50) // 4
    for i, (lbl2, val2, trend2, sub2) in enumerate(pub_kpis):
        stat_card(d, mx+10+i*(kw3+8), 122, kw3, 90, lbl2, val2, sub=sub2, trend=trend2 or "")

    # Revenue chart
    rect(d, mx+10, 228, W-20, 430, fill=PANEL, outline=BORDER, radius=10)
    d.text((mx+26, 248), "일별 수익 추이 (5월)", font=F_B_MD, fill=WHITE)
    rev_data = [38, 42, 36, 45, 52, 48, 55, 60, 58, 62, 70, 65, 58, 62, 68]
    mini_chart(d, mx+26, 268, W-mx-56, 140, rev_data, color=ACCENT)
    days2 = [f"5/{i+1}" for i in range(15)]
    dw = (W-mx-82) / (len(days2)-1)
    for i, day in enumerate(days2):
        d.text((mx+26+int(i*dw), 418), day, font=F_XS, fill=GRAY_M, anchor="mm")

    # Slot performance table
    rect(d, mx+10, 440, 760, H-20, fill=PANEL, outline=BORDER, radius=10)
    d.text((mx+26, 460), "슬롯별 수익 현황", font=F_B_MD, fill=WHITE)
    pub_slots = [
        ("게임인사이드_LB", "728×90", "820,000원", "65%"),
        ("게임인사이드_BOX", "300×250", "440,000원", "35%"),
    ]
    ph = ["슬롯명", "사이즈", "이번달 수익", "비중"]
    pw2 = [180, 100, 150, 100]
    px2 = mx + 26
    for ph2, pw3 in zip(ph, pw2):
        d.text((px2, 488), ph2, font=F_B_SM, fill=GRAY_M)
        px2 += pw3
    d.line([(mx+26, 504), (750, 504)], fill=BORDER, width=1)
    for ri5, (sn2, sz2, rev2, pct2) in enumerate(pub_slots):
        ry5 = 514 + ri5 * 60
        vals3 = [sn2, sz2, rev2, pct2]
        vx3 = mx + 26
        for vi3, (v3, pw4) in enumerate(zip(vals3, pw2)):
            col3 = ACCENT if vi3 == 2 else WHITE
            d.text((vx3, ry5+18), v3, font=F_SM, fill=col3, anchor="lm")
            vx3 += pw4
        progress_bar(d, vx3-100+50, ry5+14, 80, 8, int(pct2[:-1]), color=ACCENT)

    # Settlement section
    rect(d, 770, 440, W-20, H-20, fill=PANEL, outline=BORDER, radius=10)
    d.text((790, 460), "정산 현황", font=F_B_MD, fill=WHITE)
    d.text((790, 492), "잔액", font=F_SM, fill=GRAY_M)
    d.text((790, 516), "480,000원", font=F_B_2XL, fill=ACCENT)
    d.text((790, 556), "최소 정산 금액: 100,000원 ✓", font=F_SM, fill=SUCCESS)
    d.text((790, 580), "다음 정산일: 2026.06.10", font=F_SM, fill=GRAY_M)
    d.text((790, 604), "정산 계좌: 국민은행 ****1234", font=F_SM, fill=GRAY_M)
    cta_btn(d, 790, 636, 200, 44, "정산 신청하기", color=ACCENT, radius=8)
    outline_btn(d, 1004, 636, 150, 44, "계좌 변경", color=GRAY_M, radius=8)

    d.text((790, 700), "이번 달 누적 세금계산서", font=F_SM, fill=GRAY_M)
    d.text((790, 724), "780,000원 (지급 완료)", font=F_B_SM, fill=SUCCESS)
    d.text((790, 748), "세금계산서 다운로드 →", font=F_SM, fill=ACCENT2)

    save(img, "15_publisher_dashboard.png")

# ═══════════════════════════════════════════════════════════
# 16 — Login
# ═══════════════════════════════════════════════════════════
def gen_16_login():
    img, d = new_canvas()
    gnb(d)

    # Center modal
    rect(d, 390, 100, 890, 700, fill=PANEL, outline=BORDER, radius=16)
    d.text((640, 145), "AdMix에 로그인", font=F_B_2XL, fill=WHITE, anchor="mm")
    d.text((640, 180), "광고주 · 퍼블리셔 통합 로그인", font=F_MD, fill=GRAY_M, anchor="mm")

    # Social login
    cta_btn(d, 430, 210, 420, 52, "G   Google로 계속하기", color=PANEL2, radius=10)
    cta_btn(d, 430, 274, 420, 52, "🔵   Kakao로 계속하기", color=PANEL2, radius=10)

    d.line([(430, 346), (590, 346)], fill=GRAY_D, width=1)
    d.text((640, 346), "또는 이메일로 로그인", font=F_SM, fill=GRAY_M, anchor="mm")
    d.line([(690, 346), (850, 346)], fill=GRAY_D, width=1)

    input_field(d, 430, 368, 420, 48, "이메일", "", "user@company.com")
    input_field(d, 430, 458, 420, 48, "비밀번호", "", "••••••••")

    d.text((840, 460), "비밀번호 찾기 →", font=F_SM, fill=ACCENT2, anchor="rm")

    # Login type selection
    d.text((430, 520), "로그인 유형:", font=F_SM, fill=GRAY_M)
    for i, ltype in enumerate(["광고주", "퍼블리셔"]):
        active = i == 0
        rect(d, 540+i*130, 514, 650+i*130, 540, fill=ACCENT2 if active else PANEL2, outline=BORDER, radius=6)
        d.text((595+i*130, 527), ltype, font=F_SM, fill=WHITE, anchor="mm")

    cta_btn(d, 430, 554, 420, 52, "로그인", color=ACCENT, radius=10)
    d.text((640, 624), "계정이 없으신가요?", font=F_SM, fill=GRAY_M, anchor="mm")
    d.text((640, 648), "무료로 시작하기 →", font=F_B_SM, fill=ACCENT2, anchor="mm")

    # Security note
    d.text((640, 678), "🔒  SSL 암호화로 보호됩니다", font=F_XS, fill=GRAY_D, anchor="mm")

    save(img, "16_login.png")

# ═══════════════════════════════════════════════════════════
# 17 — Notifications
# ═══════════════════════════════════════════════════════════
def gen_17_notifications():
    img, d = new_canvas()
    gnb(d, with_nav=False)
    sidebar_items = [("🏠", "대시보드"), ("📣", "캠페인"), ("📊", "분석"), ("🖼️", "소재"), ("💳", "결제"), ("🔔", "알림")]
    sidebar(d, sidebar_items, active_idx=5)

    mx = 220
    d.text((mx+10, 74), "알림 센터", font=F_B_XL, fill=WHITE)
    outline_btn(d, W-200, 68, 160, 40, "전체 읽음 처리", color=GRAY_M, radius=8)

    # Filter tabs
    notif_tabs = ["전체", "캠페인", "소재 승인", "결제", "시스템"]
    tx4 = mx + 10
    for i, tab2 in enumerate(notif_tabs):
        active2 = i == 0
        rect(d, tx4, 106, tx4+100, 130, fill=ACCENT2 if active2 else PANEL, outline=BORDER if not active2 else None, radius=6)
        d.text((tx4+50, 118), tab2, font=F_SM, fill=WHITE, anchor="mm")
        tx4 += 110

    notifications = [
        ("🎯", SUCCESS, "캠페인 승인 완료", "게임 유저 타겟 배너 캠페인이 승인되었습니다. 집행이 시작됩니다.", "방금 전", False),
        ("📊", ACCENT2, "성과 알림", "인벤 CTR이 4.1%를 달성했습니다. 업종 평균 대비 +1.8%p 아웃퍼폼 중입니다.", "10분 전", False),
        ("💳", ACCENT, "결제 완료", "봄 신상품 런칭 캠페인 결제가 완료되었습니다. 금액: 1,100,000원", "1시간 전", True),
        ("🖼️", WARNING, "소재 검토 필요", "320×480 소재 (admix_inter_v2)가 반려되었습니다. 해상도 기준 미달.", "3시간 전", True),
        ("⚠️", WARNING, "예산 경고", "게임 유저 타겟 배너 캠페인 예산이 80% 소진되었습니다. 증액을 고려해 보세요.", "어제", True),
        ("🔔", GRAY_M, "시스템 공지", "AdMix 정기 점검 안내 (2026.05.15 02:00~04:00)", "3일 전", True),
        ("💰", SUCCESS, "정산 완료", "2026년 4월 퍼블리셔 정산이 완료되었습니다. 금액: 1,064,000원", "5일 전", True),
    ]

    ny = 148
    for i, (icon3, color4, title3, desc3, time3, read3) in enumerate(notifications):
        nh = 80
        bg7 = PANEL if not read3 else PANEL2
        rect(d, mx+10, ny, W-20, ny+nh, fill=bg7, outline=BORDER, radius=8)
        if not read3:
            rect(d, mx+10, ny, mx+14, ny+nh, fill=color4, radius=4)
        rect(d, mx+26, ny+18, mx+58, ny+58, fill=color4, radius=20)
        d.text((mx+42, ny+38), icon3, font=F_LG, fill=WHITE, anchor="mm")
        d.text((mx+72, ny+24), title3, font=F_B_MD, fill=WHITE if not read3 else GRAY_L)
        d.text((mx+72, ny+46), desc3[:80] + ("..." if len(desc3) > 80 else ""), font=F_SM, fill=GRAY_M)
        d.text((W-36, ny+24), time3, font=F_XS, fill=GRAY_D, anchor="rm")
        if not read3:
            rect(d, W-80, ny+44, W-36, ny+64, fill=None, outline=ACCENT2, radius=12)
            d.text((W-58, ny+54), "자세히", font=F_XS, fill=ACCENT2, anchor="mm")
        ny += nh + 6

    save(img, "17_notifications.png")

# ═══════════════════════════════════════════════════════════
# 18 — Billing / Payment
# ═══════════════════════════════════════════════════════════
def gen_18_billing():
    img, d = new_canvas()
    gnb(d, with_nav=False)
    sidebar_items = [("🏠", "대시보드"), ("📣", "캠페인"), ("📊", "분석"), ("🖼️", "소재"), ("💳", "결제"), ("⚙️", "설정")]
    sidebar(d, sidebar_items, active_idx=4)

    mx = 220
    d.text((mx+10, 74), "결제 및 청구", font=F_B_XL, fill=WHITE)

    # Summary cards
    bill_kpis = [
        ("이번 달 청구", "1,100,000원", "미결제"),
        ("지난 달 청구", "820,000원", "결제완료"),
        ("연간 누적", "3,280,000원", "2026년"),
    ]
    bw = (W - mx - 50) // 3
    for i, (lbl3, val3, sub3) in enumerate(bill_kpis):
        sc6 = WARNING if "미결제" in sub3 else SUCCESS
        rect(d, mx+10+i*(bw+10), 108, mx+10+i*(bw+10)+bw, 188, fill=PANEL, outline=BORDER, radius=8)
        d.text((mx+26+i*(bw+10), 128), lbl3, font=F_SM, fill=GRAY_M)
        d.text((mx+26+i*(bw+10), 150), val3, font=F_B_XL, fill=WHITE)
        rect(d, mx+bw-60+i*(bw+10), 126, mx+bw-2+i*(bw+10), 146, fill=sc6, radius=8)
        d.text((mx+bw-31+i*(bw+10), 136), sub3, font=F_XS, fill=WHITE, anchor="mm")

    # Current invoice
    rect(d, mx+10, 204, 800, 500, fill=PANEL, outline=WARNING, radius=10)
    d.text((mx+26, 224), "현재 청구서 — 2026년 5월", font=F_B_LG, fill=WHITE)
    d.text((mx+26, 252), "미결제  |  납부 기한: 2026.05.31", font=F_SM, fill=WARNING)
    line_items = [
        ("게임 유저 타겟 배너 캠페인", "인벤 (05.01~05.14)", "600,000원"),
        ("게임 유저 타겟 배너 캠페인", "루리웹 (05.01~05.14)", "400,000원"),
        ("소계", "", "1,000,000원"),
        ("VAT (10%)", "", "100,000원"),
    ]
    ly = 288
    for item_name, item_desc, item_price in line_items:
        is_sub = "소계" in item_name or "VAT" in item_name
        fc2 = GRAY_M if is_sub else WHITE
        d.text((mx+26, ly), item_name, font=F_B_SM if is_sub else F_SM, fill=fc2)
        if item_desc:
            d.text((mx+26, ly+18), item_desc, font=F_XS, fill=GRAY_D)
        d.text((780, ly), item_price, font=F_B_SM if is_sub else F_SM, fill=fc2, anchor="rm")
        if is_sub:
            d.line([(mx+26, ly-4), (780, ly-4)], fill=BORDER, width=1)
        ly += 44
    d.line([(mx+26, ly), (780, ly)], fill=GRAY_D, width=1)
    d.text((mx+26, ly+16), "합계 (VAT 포함)", font=F_B_LG, fill=WHITE)
    d.text((780, ly+16), "1,100,000원", font=F_B_LG, fill=ACCENT, anchor="rm")

    cta_btn(d, mx+26, ly+50, 340, 48, "지금 결제하기  →  1,100,000원", color=ACCENT, radius=8)
    outline_btn(d, mx+380, ly+50, 150, 48, "청구서 다운로드", color=GRAY_M, radius=8)

    # Payment methods
    rect(d, 820, 204, W-20, 500, fill=PANEL, outline=BORDER, radius=10)
    d.text((840, 224), "결제 수단", font=F_B_MD, fill=WHITE)

    # Cards on file
    d.text((840, 254), "등록된 카드", font=F_SM, fill=GRAY_M)
    rect(d, 840, 272, W-36, 322, fill=CHIP_BG, outline=ACCENT, radius=8)
    d.text((856, 292), "🏦  신한카드 **** 1234", font=F_MD, fill=WHITE)
    d.text((856, 312), "만료일 12/27  |  기본 결제 수단", font=F_XS, fill=GRAY_M)
    d.text((W-50, 292), "×", font=F_LG, fill=GRAY_D, anchor="rm")

    cta_btn(d, 840, 334, 300, 38, "+ 카드 추가하기", color=PANEL2, radius=8)
    cta_btn(d, 840, 382, 300, 38, "계좌이체 (세금계산서)", color=PANEL2, radius=8)

    # Payment history
    rect(d, mx+10, 516, W-20, H-20, fill=PANEL, outline=BORDER, radius=10)
    d.text((mx+26, 534), "결제 내역", font=F_B_MD, fill=WHITE)
    history = [
        ("2026.04.01", "4월 캠페인 집행", "820,000원", "결제완료", SUCCESS),
        ("2026.03.01", "3월 캠페인 집행", "640,000원", "결제완료", SUCCESS),
        ("2026.02.01", "2월 캠페인 집행", "720,000원", "결제완료", SUCCESS),
    ]
    hy = 566
    for hdate, hdesc, hamt, hstatus, hcolor in history:
        d.text((mx+26, hy), hdate, font=F_SM, fill=GRAY_M)
        d.text((mx+160, hy), hdesc, font=F_SM, fill=WHITE)
        d.text((mx+480, hy), hamt, font=F_B_SM, fill=WHITE)
        rect(d, mx+620, hy-6, mx+720, hy+18, fill=hcolor, radius=8)
        d.text((mx+670, hy+6), hstatus, font=F_XS, fill=WHITE, anchor="mm")
        d.text((W-36, hy), "영수증 ↓", font=F_SM, fill=ACCENT2, anchor="rm")
        hy += 42

    save(img, "18_billing.png")


# ══════════════════════════════════
# 실행
# ══════════════════════════════════
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("AdMix wireframe generation START...")
    gen_01_landing()
    gen_02_service_intro()
    gen_03_media_publishers()
    gen_04_signup_onboarding()
    gen_05_campaign_ad_type()
    gen_06_campaign_media_select()
    gen_07_campaign_budget()
    gen_08_campaign_creative()
    gen_09_campaign_review()
    gen_10_ad_dashboard()
    gen_11_campaign_analytics()
    gen_12_creative_management()
    gen_13_publisher_onboarding()
    gen_14_publisher_slots()
    gen_15_publisher_dashboard()
    gen_16_login()
    gen_17_notifications()
    gen_18_billing()
    print(f"\nDONE! 18 images -> {OUT}")
