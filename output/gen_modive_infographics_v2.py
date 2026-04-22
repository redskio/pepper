# -*- coding: utf-8 -*-
"""모다이브 제안서 인포그래픽 v2 (댓글 반영)
- ott_problems_v2  : 새 6개 Pain Points (댓글 8)
- subscriber_funnel_v2 : CleverTap → 인게이지먼트 플랫폼 (댓글 1/6)
- implementation_v2    : CleverTap 제거 (댓글 1/6)
"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path

OUT = Path('C:/Agent/pepper/output/modive_assets')
OUT.mkdir(parents=True, exist_ok=True)

OCEAN  = '#041520'
DEEP   = '#061E35'
CARD   = '#0A2236'
CARD2  = '#0D2D48'
TEAL   = '#00D4AA'
CYAN   = '#00B4FF'
WHITE  = '#FFFFFF'
GRAY   = '#8AADCC'
GOLD   = '#FFC84B'
PURPLE = '#A78BFA'
RED    = '#FF6B6B'
GREEN  = '#34D399'

def kfont(size=14, bold=False):
    fp = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
    if Path(fp).exists():
        return fm.FontProperties(fname=fp, size=size)
    return fm.FontProperties(size=size)


# ─────────────────────────────────────────────────────────────
# 1. OTT Pain Points v2 (댓글 8 반영 — 6개 신규 항목)
# ─────────────────────────────────────────────────────────────
def gen_ott_problems_v2():
    fig, ax = plt.subplots(figsize=(19.2, 6.5), facecolor=OCEAN)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    problems = [
        ("01", "리텐션 증대 중요성",
         "구독자 유지가 신규 유치보다\n5배 이상 비용 효율적",
         RED),
        ("02", "지속적인 데이터 관리 필요",
         "수집·정제·분석 사이클이\n일회성이 아닌 운영 체계화 필요",
         CYAN),
        ("03", "관측과 보고의 효율화",
         "마케팅 성과를 실시간으로\n한눈에 파악하는 리포팅 체계",
         GOLD),
        ("04", "캔버스 관점의 CRM",
         "고객 여정 전체를 설계하는\n통합 CRM 전략 관점",
         TEAL),
        ("05", "ROI 측정 필요",
         "모든 마케팅 캠페인의\n효과를 수치화·정량화",
         PURPLE),
        ("06", "실험기반의 액션 필요",
         "가설 수립 → 테스트 → 분석\n반복하는 그로스 사이클",
         GREEN),
    ]

    cols = 3
    col_w = 19.2 / cols
    row_h = 2.9

    for i, (num, title, body, c) in enumerate(problems):
        row = i // cols
        col = i % cols
        cx = col * col_w + col_w / 2
        cy = 5.8 - row * row_h

        card = FancyBboxPatch((cx - 2.85, cy - 1.15), 5.7, 2.2,
                               boxstyle='round,pad=0.12', linewidth=2,
                               edgecolor=c, facecolor=CARD)
        ax.add_patch(card)
        badge = plt.Circle((cx - 2.3, cy + 0.72), 0.3, color=c, zorder=3)
        ax.add_patch(badge)
        ax.text(cx - 2.3, cy + 0.72, num, ha='center', va='center',
                fontsize=11, fontweight='bold', color=OCEAN, zorder=4,
                fontfamily='DejaVu Sans')
        ax.text(cx, cy + 0.52, title, ha='center', va='center',
                fontproperties=kfont(15, bold=True), color=c)
        ax.plot([cx - 2.1, cx + 2.1], [cy + 0.22, cy + 0.22],
                color=c, lw=0.8, alpha=0.4)
        ax.text(cx, cy - 0.32, body, ha='center', va='center',
                fontproperties=kfont(11.5), color=GRAY, linespacing=1.55)

    ax.text(9.6, 0.28,
            'OTT/미디어 플랫폼이 공통적으로 직면하는 MarTech 도입 필요성',
            ha='center', va='center', fontproperties=kfont(12), color=GRAY,
            style='italic')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_ott_problems_v2.png'), dpi=100,
                bbox_inches='tight', facecolor=OCEAN)
    plt.close(fig)
    print('OK: infographic_ott_problems_v2.png')


# ─────────────────────────────────────────────────────────────
# 2. 구독자 라이프사이클 퍼널 v2 (CleverTap 제거)
# ─────────────────────────────────────────────────────────────
def gen_subscriber_funnel_v2():
    fig, ax = plt.subplots(figsize=(19.2, 6.8), facecolor=OCEAN)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 6.8)
    ax.axis('off')

    stages = [
        ('ACQUISITION',  '신규 유입',    '광고/검색/추천',      CYAN,   3.8, 5.2),
        ('ONBOARDING',   '온보딩',        '첫 콘텐츠 경험',     TEAL,   3.2, 4.3),
        ('ENGAGEMENT',   '인게이지먼트',  '구독 유지·시청 증가', GREEN,  2.6, 3.4),
        ('RETENTION',    '리텐션',        '이탈 방지 캠페인',    GOLD,   2.0, 2.5),
        ('CONVERSION',   '전환',          '유료 구독 전환',      PURPLE, 1.4, 1.6),
    ]

    for i, (eng, kor, sub, c, w, h) in enumerate(stages):
        y_bot = 0.5 + i * 1.18
        box = FancyBboxPatch((9.6 - w/2, y_bot), w, 0.9,
                              boxstyle='round,pad=0.05', linewidth=2,
                              edgecolor=c, facecolor=CARD2, alpha=0.9)
        ax.add_patch(box)
        fill_bar = FancyBboxPatch((9.6 - w/2, y_bot), w * (0.95 - i*0.1), 0.9,
                                   boxstyle='round,pad=0', linewidth=0,
                                   facecolor=c, alpha=0.18)
        ax.add_patch(fill_bar)
        ax.text(9.6, y_bot + 0.62, eng, ha='center', va='center',
                fontsize=11, color=c, fontfamily='DejaVu Sans', fontweight='bold')
        ax.text(9.6, y_bot + 0.38, kor, ha='center', va='center',
                fontproperties=kfont(13, bold=True), color=WHITE)
        ax.text(9.6, y_bot + 0.14, sub, ha='center', va='center',
                fontproperties=kfont(11), color=GRAY)
        ax.text(9.6 - w/2 - 0.2, y_bot + 0.42, f'Step {i+1}',
                ha='right', va='center', fontsize=10, color=c,
                fontfamily='DejaVu Sans')

    # 우측 개입 포인트 (특정 툴명 제거)
    ws_points = [
        (5, 'GA4 이벤트 설계\n트래킹 구축'),
        (4, 'Push 온보딩\n시퀀스'),
        (3, '인게이지먼트 플랫폼\n세그먼트 캠페인'),
        (2, '이탈방지\nWin-back'),
        (1, 'LTV 분석\n전환 최적화'),
    ]
    for i, (step, label) in enumerate(ws_points):
        y = 0.5 + i * 1.18 + 0.45
        w = stages[i][4]
        ax.annotate('', xy=(9.6 + w/2 + 1.5, y), xytext=(9.6 + w/2 + 0.15, y),
                    arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.5,
                                    mutation_scale=14))
        ax.text(9.6 + w/2 + 1.65, y, label, ha='left', va='center',
                fontproperties=kfont(10), color=TEAL, linespacing=1.4)

    ax.text(9.6, 6.5, 'Subscriber Lifecycle  |  Weirdsector MarTech Touchpoints',
            ha='center', va='center', fontsize=13, color=GRAY,
            fontfamily='DejaVu Sans', style='italic')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_subscriber_funnel_v2.png'), dpi=100,
                bbox_inches='tight', facecolor=OCEAN)
    plt.close(fig)
    print('OK: infographic_subscriber_funnel_v2.png')


# ─────────────────────────────────────────────────────────────
# 3. 3개월 도입 타임라인 v2 (CleverTap 제거)
# ─────────────────────────────────────────────────────────────
def gen_implementation_v2():
    fig, ax = plt.subplots(figsize=(19.2, 6.2), facecolor=OCEAN)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    months = [
        ('MONTH 1', '1개월차', 'Foundation',
         ['GA4 이벤트 택소노미 설계', 'GTM 재구조화 & 배포',
          '인게이지먼트 플랫폼 환경 구성', '기존 데이터 감사 및 정리'],
         TEAL, 2.0),
        ('MONTH 2', '2개월차', 'Automation',
         ['온보딩 자동화 플로우 구축', 'Push/인앱/이메일 캠페인 설계',
          '세그멘테이션 기준 수립', 'A/B 테스트 첫 사이클 실행'],
         CYAN, 9.6),
        ('MONTH 3', '3개월차', 'Optimization',
         ['성과 데이터 기반 캠페인 최적화', 'D7/D30 리텐션 지표 개선',
          'ROI 리포팅 대시보드 완성', '다음 분기 그로스 전략 수립'],
         GOLD, 17.2),
    ]

    ax.plot([0.8, 18.4], [3.8, 3.8], color=TEAL, lw=2.0, alpha=0.35, zorder=1)

    for cx, (eng_m, kor_m, theme, tasks, c, _cx) in zip([2.0, 9.6, 17.2], months):
        cx = _cx
        circle = plt.Circle((cx, 3.8), 0.55, color=c, zorder=4)
        ax.add_patch(circle)
        ax.text(cx, 3.95, eng_m, ha='center', va='center',
                fontsize=9, fontweight='bold', color=OCEAN,
                fontfamily='DejaVu Sans', zorder=5)
        ax.text(cx, 3.65, kor_m, ha='center', va='center',
                fontsize=8, color=OCEAN, fontfamily='DejaVu Sans', zorder=5)

        ax.plot([cx, cx], [4.35, 4.75], color=c, lw=1.5, alpha=0.7)
        card = FancyBboxPatch((cx - 2.7, 4.75), 5.4, 1.15,
                               boxstyle='round,pad=0.12', linewidth=2,
                               edgecolor=c, facecolor=CARD)
        ax.add_patch(card)
        ax.text(cx, 5.6, theme, ha='center', va='center',
                fontsize=14, fontweight='bold', color=c,
                fontfamily='DejaVu Sans')

        ax.plot([cx, cx], [3.25, 2.85], color=c, lw=1.5, alpha=0.7)
        for j, task in enumerate(tasks):
            ty = 2.55 - j * 0.62
            task_box = FancyBboxPatch((cx - 2.55, ty - 0.22), 5.1, 0.46,
                                      boxstyle='round,pad=0.05', linewidth=1,
                                      edgecolor=c + '55', facecolor=CARD2)
            ax.add_patch(task_box)
            ax.plot([cx - 2.55, cx - 2.55 + 0.1], [ty, ty], color=c, lw=2.5)
            ax.text(cx - 2.3, ty, task, ha='left', va='center',
                    fontproperties=kfont(11), color=WHITE)

    ax.text(9.6, 0.28,
            'Weirdsector  |  3-Month Implementation Roadmap for Modive',
            ha='center', va='center', fontsize=12, color=GRAY,
            fontfamily='DejaVu Sans', style='italic')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_implementation_v2.png'), dpi=100,
                bbox_inches='tight', facecolor=OCEAN)
    plt.close(fig)
    print('OK: infographic_implementation_v2.png')


if __name__ == '__main__':
    gen_ott_problems_v2()
    gen_subscriber_funnel_v2()
    gen_implementation_v2()
    print('\nAll 3 Modive v2 infographics generated.')
