# -*- coding: utf-8 -*-
"""위어드섹터 v4 추가 인포그래픽 생성"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm
import matplotlib.patheffects as pe
import numpy as np
from pathlib import Path

OUT   = Path('C:/Agent/pepper/output/wirdsector_assets')
OUT.mkdir(parents=True, exist_ok=True)

NAVY2 = '#060E18'
NAVY  = '#0D1B2A'
CARD  = '#131926'
CARD2 = '#1A2840'
TEAL  = '#00D4AA'
WHITE = '#FFFFFF'
GRAY  = '#8A9BB0'
GOLD  = '#FFC84B'
PURPLE= '#A78BFA'
RED   = '#FF6B6B'
GREEN = '#34D399'
BLUE  = '#38BDF8'

def kfont(size=14, bold=False):
    fp_path = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
    if Path(fp_path).exists():
        return fm.FontProperties(fname=fp_path, size=size)
    return fm.FontProperties(size=size)


# ──────────────────────────────────────────────────────────────────
# 5. Before / After 비교 인포그래픽 (문제 → 해결)
# ──────────────────────────────────────────────────────────────────
def gen_before_after():
    fig, ax = plt.subplots(figsize=(19.2, 7.5), facecolor=NAVY2)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 7.5)
    ax.axis('off')

    # 좌측 BEFORE 패널
    left_bg = FancyBboxPatch((0.3, 0.3), 8.5, 6.9,
                              boxstyle='round,pad=0.12', linewidth=2,
                              edgecolor='#FF6B6B', facecolor='#1A0A0A')
    ax.add_patch(left_bg)

    # 우측 AFTER 패널
    right_bg = FancyBboxPatch((10.4, 0.3), 8.5, 6.9,
                               boxstyle='round,pad=0.12', linewidth=2,
                               edgecolor=TEAL, facecolor='#081814')
    ax.add_patch(right_bg)

    # BEFORE / AFTER 레이블
    ax.text(4.55, 6.7, 'BEFORE', ha='center', va='center',
            fontsize=28, fontweight='bold', color='#FF6B6B',
            fontfamily='DejaVu Sans')
    ax.text(14.65, 6.7, 'AFTER', ha='center', va='center',
            fontsize=28, fontweight='bold', color=TEAL,
            fontfamily='DejaVu Sans')

    # 중앙 화살표 배지
    circle = plt.Circle((9.6, 3.75), 0.72, color=TEAL, zorder=5)
    ax.add_patch(circle)
    ax.annotate('', xy=(10.2, 3.75), xytext=(9.0, 3.75),
                arrowprops=dict(arrowstyle='->', color=NAVY2, lw=3.5,
                                mutation_scale=28), zorder=6)
    ax.text(9.6, 3.1, 'WS', ha='center', va='center',
            fontsize=13, fontweight='bold', color=NAVY2, zorder=7,
            fontfamily='DejaVu Sans')

    befores = [
        ("데이터 누락 & 오류", "트래킹 설계 없이 수집→분석 불가"),
        ("채널별 파편화",       "Push/Email/SMS 통합 불가"),
        ("ROI 측정 불가",       "광고비 집행 근거 없음"),
        ("수동 캠페인",         "타겟팅 없는 일괄 발송"),
        ("2주+ 개발 대기",     "마케팅-개발 커뮤니케이션 병목"),
    ]
    afters = [
        ("100% 데이터 정확도", "GA4 이벤트 택소노미 완전 설계"),
        ("통합 CRM 자동화",    "CleverTap 기반 옴니채널 운영"),
        ("실시간 ROI 대시보드","기여도 분석 + 성과 가시화"),
        ("AI 개인화 캠페인",   "세그먼트 기반 자동화 플로우"),
        ("즉시 실행 가능",     "전담팀이 다음날 바로 착수"),
    ]

    for i, ((bt, bs), (at, as_)) in enumerate(zip(befores, afters)):
        y = 5.7 - i * 1.08

        # Before 행
        b_box = FancyBboxPatch((0.55, y - 0.38), 8.0, 0.78,
                                boxstyle='round,pad=0.06', linewidth=1,
                                edgecolor='#FF6B6B55', facecolor='#2A0A0A')
        ax.add_patch(b_box)
        ax.plot([0.55, 0.55], [y - 0.38, y + 0.4], color='#FF6B6B', lw=3)
        ax.text(0.85, y + 0.13, bt, ha='left', va='center',
                fontproperties=kfont(13, bold=True), color='#FF9999')
        ax.text(0.85, y - 0.18, bs, ha='left', va='center',
                fontproperties=kfont(11), color=GRAY)

        # After 행
        a_box = FancyBboxPatch((10.65, y - 0.38), 8.0, 0.78,
                                boxstyle='round,pad=0.06', linewidth=1,
                                edgecolor='#00D4AA55', facecolor='#041A14')
        ax.add_patch(a_box)
        ax.plot([10.65, 10.65], [y - 0.38, y + 0.4], color=TEAL, lw=3)
        ax.text(10.95, y + 0.13, at, ha='left', va='center',
                fontproperties=kfont(13, bold=True), color='#80FFEE')
        ax.text(10.95, y - 0.18, as_, ha='left', va='center',
                fontproperties=kfont(11), color=GRAY)

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_before_after.png'), dpi=100,
                bbox_inches='tight', facecolor=NAVY2)
    plt.close(fig)
    print('OK: infographic_before_after.png')


# ──────────────────────────────────────────────────────────────────
# 6. 비즈니스 모델 다이어그램
# ──────────────────────────────────────────────────────────────────
def gen_bizmodel():
    fig, ax = plt.subplots(figsize=(19.2, 6.5), facecolor=NAVY2)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # 타이틀
    ax.text(9.6, 6.1, 'Weirdsector Business Model', ha='center', va='center',
            fontsize=22, fontweight='bold', color=WHITE, fontfamily='DejaVu Sans')

    # 클라이언트 → WS → 산출물 → 성과 흐름
    layers = [
        # (x_center, y_center, label, sublabel, color, width, height)
        (1.6,  3.2, 'CLIENT', 'App/Web\nService', BLUE,   2.4, 3.8),
        (5.5,  3.2, 'DATA\nENGINEERING', 'GA4 · GTM\nBigQuery', TEAL,  2.6, 1.6),
        (5.5,  1.5, 'MarTech\nPLATFORM', 'CleverTap\nBraze', GOLD,   2.6, 1.6),
        (9.6,  3.2, 'WEIRDSECTOR', 'Integrated\nExecution', WHITE,  2.8, 3.8),
        (13.7, 4.1, 'CRM\nOPERATIONS', 'Segmentation\nCampaign', TEAL,  2.6, 1.6),
        (13.7, 2.3, 'DATA\nPRODUCTS', 'Labbit\nDataNugget', GOLD,   2.6, 1.6),
        (17.6, 3.2, 'GROWTH', 'Retention+\nROI+', GREEN,  1.8, 3.8),
    ]

    def draw_node(cx, cy, label, sub, c, w, h):
        fc = '#041410' if c == TEAL else ('#1A1200' if c == GOLD else '#040C14')
        box = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                              boxstyle='round,pad=0.15', linewidth=2,
                              edgecolor=c, facecolor=fc)
        ax.add_patch(box)
        ax.text(cx, cy + 0.25, label, ha='center', va='center',
                fontsize=13, fontweight='bold', color=c,
                fontfamily='DejaVu Sans')
        ax.text(cx, cy - 0.35, sub, ha='center', va='center',
                fontsize=10, color=GRAY, fontfamily='DejaVu Sans', linespacing=1.4)

    for cx, cy, label, sub, c, w, h in layers:
        draw_node(cx, cy, label, sub, c, w, h)

    # 화살표
    arrows = [
        (2.8, 3.2, 4.2, 3.2),   # client → data eng
        (2.8, 3.2, 4.2, 1.5),   # client → martech
        (6.8, 3.2, 8.2, 3.2),   # data eng → WS
        (6.8, 1.5, 8.2, 2.8),   # martech → WS
        (11.0, 3.2, 12.4, 4.1), # WS → CRM
        (11.0, 3.2, 12.4, 2.3), # WS → data products
        (14.95, 4.1, 16.7, 3.4), # CRM → growth
        (14.95, 2.3, 16.7, 3.0), # data products → growth
    ]
    for x1, y1, x2, y2 in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=TEAL,
                                    lw=1.8, mutation_scale=16))

    # M/M 배지
    mm_box = FancyBboxPatch((8.3, 0.2), 2.6, 0.7,
                             boxstyle='round,pad=0.08', linewidth=1.5,
                             edgecolor=GOLD, facecolor='#1A1000')
    ax.add_patch(mm_box)
    ax.text(9.6, 0.55, 'Monthly Retainer (M/M)', ha='center', va='center',
            fontsize=12, color=GOLD, fontfamily='DejaVu Sans')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_bizmodel.png'), dpi=100,
                bbox_inches='tight', facecolor=NAVY2)
    plt.close(fig)
    print('OK: infographic_bizmodel.png')


# ──────────────────────────────────────────────────────────────────
# 7. 비전 & 로드맵 타임라인
# ──────────────────────────────────────────────────────────────────
def gen_roadmap():
    fig, ax = plt.subplots(figsize=(19.2, 5.5), facecolor=NAVY2)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # 메인 타임라인 선
    ax.plot([0.8, 18.4], [2.75, 2.75], color=TEAL, lw=2.5, alpha=0.4, zorder=1)

    milestones = [
        (1.8,  '2022',    'Founded',        'GA4 전문 에이전시\n창업', TEAL, 'above'),
        (4.8,  '2023',    'Scale Up',       '파트너 10+ 확보\nLabbit 출시', GOLD, 'below'),
        (7.8,  '2024',    'MarTech',        'CleverTap 파트너\nCRM 자동화', TEAL, 'above'),
        (10.8, '2025',    'DataNugget',     '자체 데이터 서비스\n출시', GOLD, 'below'),
        (13.8, '2026 H1', 'Growth Engine',  '파트너 30+ 달성\nROI 3× 평균', TEAL, 'above'),
        (17.0, '2026 H2+','AI Personalize', 'AI 기반 개인화\n캠페인 자동화', PURPLE, 'below'),
    ]

    for cx, year, title, body, c, pos in milestones:
        # 타임라인 점
        circle = plt.Circle((cx, 2.75), 0.22, color=c, zorder=4)
        ax.add_patch(circle)
        ax.plot([cx, cx], [2.75 - 0.22, 2.75 + 0.22], color=c, lw=2, zorder=3)

        if pos == 'above':
            stem_y0, stem_y1 = 2.97, 3.3
            label_y = 3.4
            body_y  = 4.2
        else:
            stem_y0, stem_y1 = 2.53, 2.2
            label_y = 1.95
            body_y  = 1.15

        ax.plot([cx, cx], [stem_y0, stem_y1], color=c, lw=1.5, alpha=0.6)

        # 카드
        card = FancyBboxPatch((cx - 1.3, label_y - 0.35 if pos == 'above' else body_y - 0.25),
                               2.6, 1.2 if pos == 'above' else 1.2,
                               boxstyle='round,pad=0.1', linewidth=1.5,
                               edgecolor=c, facecolor=CARD)
        ax.add_patch(card)

        ax.text(cx, label_y + (0.5 if pos == 'above' else 0.45),
                year, ha='center', va='center',
                fontsize=11, color=c, fontfamily='DejaVu Sans')
        ax.text(cx, label_y + (0.12 if pos == 'above' else 0.08),
                title, ha='center', va='center',
                fontsize=13, fontweight='bold', color=WHITE,
                fontfamily='DejaVu Sans')
        ax.text(cx, label_y + (-0.28 if pos == 'above' else -0.28),
                body, ha='center', va='center',
                fontsize=10, color=GRAY, fontfamily='DejaVu Sans', linespacing=1.4)

    ax.text(9.6, 0.22, 'Weirdsector  |  Growth Journey & Vision Roadmap',
            ha='center', va='center', fontsize=12, color=GRAY,
            fontfamily='DejaVu Sans', style='italic')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_roadmap.png'), dpi=100,
                bbox_inches='tight', facecolor=NAVY2)
    plt.close(fig)
    print('OK: infographic_roadmap.png')


# ──────────────────────────────────────────────────────────────────
# 8. 팀 역량 매트릭스 (스킬 바 차트)
# ──────────────────────────────────────────────────────────────────
def gen_team():
    fig, ax = plt.subplots(figsize=(19.2, 6.0), facecolor=NAVY2)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 6.0)
    ax.axis('off')

    # 4개 역할 카드
    roles = [
        ('DATA\nENGINEER', ['GA4 / GTM', 'BigQuery', 'SDK 연동', 'Privacy'],
         [95, 88, 90, 85], TEAL),
        ('MarTech\nSPECIALIST', ['CleverTap', 'Braze / MoEngage', 'A/B Testing', 'Campaign'],
         [96, 82, 91, 88], GOLD),
        ('CRM\nANALYST', ['Segmentation', 'LTV Analysis', 'Funnel Opt.', 'Reporting'],
         [90, 86, 89, 92], PURPLE),
        ('GROWTH\nMANAGER', ['Strategy', 'Performance', 'Client Mgmt', 'Roadmap'],
         [88, 93, 95, 87], BLUE),
    ]

    card_w = 4.3
    for i, (role, skills, vals, c) in enumerate(roles):
        cx = 0.5 + i * 4.65
        # 카드
        card = FancyBboxPatch((cx, 0.3), card_w, 5.4,
                               boxstyle='round,pad=0.15', linewidth=2,
                               edgecolor=c, facecolor=CARD)
        ax.add_patch(card)
        # 상단 색상 바
        bar = FancyBboxPatch((cx, 5.38), card_w, 0.32,
                              boxstyle='round,pad=0', linewidth=0,
                              facecolor=c)
        ax.add_patch(bar)

        # 역할명
        ax.text(cx + card_w/2, 4.78, role, ha='center', va='center',
                fontsize=14, fontweight='bold', color=c,
                fontfamily='DejaVu Sans', linespacing=1.3)

        # 스킬 바
        bar_x = cx + 0.2
        bar_max_w = card_w - 0.4
        for j, (skill, val) in enumerate(zip(skills, vals)):
            by = 3.85 - j * 0.9
            # 배경 바
            bg = FancyBboxPatch((bar_x, by - 0.12), bar_max_w, 0.26,
                                 boxstyle='round,pad=0', linewidth=0,
                                 facecolor='#0A1520')
            ax.add_patch(bg)
            # 값 바
            filled_w = bar_max_w * val / 100
            fg = FancyBboxPatch((bar_x, by - 0.12), filled_w, 0.26,
                                 boxstyle='round,pad=0', linewidth=0,
                                 facecolor=c, alpha=0.85)
            ax.add_patch(fg)
            # 레이블
            ax.text(bar_x, by - 0.35, skill, ha='left', va='center',
                    fontsize=10, color=GRAY, fontfamily='DejaVu Sans')
            ax.text(bar_x + bar_max_w, by - 0.35, f'{val}%', ha='right', va='center',
                    fontsize=10, color=c, fontfamily='DejaVu Sans', fontweight='bold')

    ax.text(9.6, 0.1, 'Hybrid Team  |  Full-stack MarTech Expertise',
            ha='center', va='center', fontsize=12, color=GRAY,
            fontfamily='DejaVu Sans', style='italic')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_team.png'), dpi=100,
                bbox_inches='tight', facecolor=NAVY2)
    plt.close(fig)
    print('OK: infographic_team.png')


if __name__ == '__main__':
    gen_before_after()
    gen_bizmodel()
    gen_roadmap()
    gen_team()
    print('\nAll 4 new infographics generated.')
