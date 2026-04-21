# -*- coding: utf-8 -*-
"""위어드섹터 인포그래픽 생성 스크립트"""
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

# Windows Korean font
_KR_FONT = None
for _fp in ['C:/Windows/Fonts/malgun.ttf', 'C:/Windows/Fonts/malgunbd.ttf']:
    if Path(_fp).exists():
        _KR_FONT = fm.FontProperties(fname=_fp)
        break

def kfont(size=14, bold=False):
    fp_path = 'C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf'
    if Path(fp_path).exists():
        return fm.FontProperties(fname=fp_path, size=size)
    return fm.FontProperties(size=size)

OUT   = Path('C:/Agent/pepper/output/wirdsector_assets')
NAVY2 = '#060E18'
NAVY  = '#0D1B2A'
CARD  = '#131926'
CARD2 = '#1A3050'
TEAL  = '#00D4AA'
WHITE = '#FFFFFF'
GRAY  = '#8A9BB0'
GOLD  = '#FFC84B'
PURPLE= '#A78BFA'
RED   = '#FF6B6B'
GREEN = '#34D399'


# ─────────────────────────────────────────────────────────────
# 1. 서비스 프로세스 플로우
# ─────────────────────────────────────────────────────────────
def gen_process():
    fig, ax = plt.subplots(figsize=(19.2, 5.0), facecolor=NAVY2)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 5.0)
    ax.axis('off')

    steps = [
        ('01', 'DISCOVER',  'Situation Analysis\n& Goal Setting'),
        ('02', 'DESIGN',    'Strategy Design\n& Roadmap'),
        ('03', 'BUILD',     'Implementation\n& Integration'),
        ('04', 'OPTIMIZE',  'Testing\n& Optimization'),
        ('05', 'REPORT',    'Performance\n& Reporting'),
    ]

    for i, (num, title, sub) in enumerate(steps):
        cx = 1.9 + i * 3.8
        # Card
        box = FancyBboxPatch((cx - 1.55, 0.55), 3.1, 3.55,
                             boxstyle='round,pad=0.12', linewidth=2,
                             edgecolor=TEAL, facecolor=CARD)
        ax.add_patch(box)
        # Circle badge
        circle = plt.Circle((cx, 3.62), 0.38, color=TEAL, zorder=3)
        ax.add_patch(circle)
        ax.text(cx, 3.62, num, ha='center', va='center',
                fontsize=12, fontweight='bold', color=NAVY2, zorder=4,
                fontfamily='DejaVu Sans')
        # Title
        ax.text(cx, 2.75, title, ha='center', va='center',
                fontsize=16, fontweight='bold', color=WHITE,
                fontfamily='DejaVu Sans')
        # Divider
        ax.plot([cx - 1.1, cx + 1.1], [2.38, 2.38],
                color=TEAL, linewidth=1.2, alpha=0.5)
        # Subtitle
        ax.text(cx, 1.62, sub, ha='center', va='center',
                fontsize=12, color=GRAY, linespacing=1.65,
                fontfamily='DejaVu Sans')
        # Arrow to next
        if i < 4:
            ax.annotate('',
                        xy=(cx + 1.62, 2.3),
                        xytext=(cx + 1.55, 2.3),
                        arrowprops=dict(
                            arrowstyle='->',
                            color=TEAL, lw=2.5,
                            mutation_scale=22))

    ax.text(9.6, 0.18,
            'Weirdsector  |  Data-Driven Marketing Process',
            ha='center', va='center', fontsize=13,
            color=GRAY, fontfamily='DejaVu Sans', style='italic')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_process.png'), dpi=100,
                bbox_inches='tight', facecolor=NAVY2, edgecolor='none')
    plt.close(fig)
    print('OK: infographic_process.png')


# ─────────────────────────────────────────────────────────────
# 2. 핵심 수치 카드
# ─────────────────────────────────────────────────────────────
def gen_stats():
    fig, ax = plt.subplots(figsize=(19.2, 4.8), facecolor=NAVY2)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 4.8)
    ax.axis('off')

    stats = [
        ('50+',  '완료 프로젝트',   'Completed Projects',  TEAL),
        ('30+',  '파트너 고객사',   'Partner Clients',     GOLD),
        ('200+', 'GA4 이벤트 설계', 'GA4 Events Designed', TEAL),
        ('3x',   '평균 ROI 개선',  'Avg ROI Improvement', GOLD),
    ]

    for i, (val, kor, eng, c) in enumerate(stats):
        cx = 2.4 + i * 4.8
        # Card body
        box = FancyBboxPatch((cx - 2.1, 0.28), 4.2, 4.2,
                             boxstyle='round,pad=0.15', linewidth=2,
                             edgecolor=c, facecolor=CARD, alpha=0.92)
        ax.add_patch(box)
        # Top color bar
        bar = FancyBboxPatch((cx - 2.1, 4.1), 4.2, 0.38,
                             boxstyle='round,pad=0.0', linewidth=0,
                             facecolor=c)
        ax.add_patch(bar)
        # Big number
        ax.text(cx, 2.92, val, ha='center', va='center',
                fontsize=58, fontweight='bold', color=c,
                fontfamily='DejaVu Sans')
        # Korean label
        ax.text(cx, 1.72, kor, ha='center', va='center',
                fontsize=16, fontweight='bold', color=WHITE,
                fontproperties=kfont(16, bold=True))
        # English sub-label
        ax.text(cx, 1.10, eng, ha='center', va='center',
                fontsize=12, color=GRAY, fontfamily='DejaVu Sans')

    ax.text(9.6, 0.04,
            'Based on average client performance data',
            ha='center', va='bottom', fontsize=11, color=GRAY,
            fontfamily='DejaVu Sans', style='italic')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_stats.png'), dpi=100,
                bbox_inches='tight', facecolor=NAVY2, edgecolor='none')
    plt.close(fig)
    print('OK: infographic_stats.png')


# ─────────────────────────────────────────────────────────────
# 3. 역량 그리드 (2x2)
# ─────────────────────────────────────────────────────────────
def gen_capabilities():
    fig, ax = plt.subplots(figsize=(14.0, 8.0), facecolor=NAVY2)
    ax.set_xlim(0, 14.0)
    ax.set_ylim(0, 8.0)
    ax.axis('off')

    caps = [
        ('DATA ENGINEERING',  ['GA4 Event Taxonomy Design', 'GTM Restructuring',
                                'BigQuery Pipeline', 'Log Definition Management'],
         TEAL,  0.2, 4.2),
        ('MarTech PLATFORM',  ['CleverTap / Braze Operation', 'Automated Campaign Design',
                                'Push / Email / SMS', 'A/B Testing'],
         GOLD,  7.2, 4.2),
        ('CRM OPERATIONS',   ['Customer Segmentation', 'Churn Prevention Campaign',
                               'LTV Analysis', 'Funnel Optimization'],
         TEAL,  0.2, 0.2),
        ('CODE MANAGEMENT',   ['SDK Integration', 'GitHub Management',
                                'Technical Debt Resolution', 'Privacy Compliance'],
         GOLD,  7.2, 0.2),
    ]

    for title, items, c, bx, by in caps:
        box = FancyBboxPatch((bx, by), 6.5, 3.6,
                             boxstyle='round,pad=0.18', linewidth=2,
                             edgecolor=c, facecolor=CARD)
        ax.add_patch(box)
        ax.text(bx + 3.25, by + 3.1, title, ha='center', va='center',
                fontsize=17, fontweight='bold', color=c,
                fontfamily='DejaVu Sans')
        for j, item in enumerate(items):
            ax.text(bx + 0.45, by + 2.45 - j * 0.58,
                    f'- {item}', ha='left', va='center',
                    fontsize=13,
                    color=WHITE if j == 0 else GRAY,
                    fontfamily='DejaVu Sans')

    # Crosshair lines
    ax.plot([7.0, 7.0], [0.2, 7.8], color=TEAL, lw=1.0, alpha=0.25, ls='--')
    ax.plot([0.2, 13.8], [4.0, 4.0], color=TEAL, lw=1.0, alpha=0.25, ls='--')
    # Center badge
    circle = plt.Circle((7.0, 4.0), 0.56, color=TEAL, zorder=5)
    ax.add_patch(circle)
    ax.text(7.0, 4.0, 'WS', ha='center', va='center',
            fontsize=15, fontweight='bold', color=NAVY2, zorder=6,
            fontfamily='DejaVu Sans')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_capabilities.png'), dpi=100,
                bbox_inches='tight', facecolor=NAVY2, edgecolor='none')
    plt.close(fig)
    print('OK: infographic_capabilities.png')


# ─────────────────────────────────────────────────────────────
# 4. 레퍼런스 로고 그리드
# ─────────────────────────────────────────────────────────────
def gen_references():
    fig, ax = plt.subplots(figsize=(19.2, 5.5), facecolor=NAVY2)
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    clients = [
        ('MBC 모다이브',       'Media / OTT',         RED),
        ('E-Commerce Platform', 'Retail / Shopping',  TEAL),
        ('FinTech Startup',     'Financial Tech',     GOLD),
        ('B2B SaaS',            'Software / Cloud',   PURPLE),
        ('Media Agency',        'Marketing',          TEAL),
        ('Healthcare App',      'Health / Wellness',  GREEN),
    ]

    for i, (name, industry, c) in enumerate(clients):
        row, col = divmod(i, 3)
        cx = 3.2 + col * 6.4
        cy = 4.0 - row * 2.6
        box = FancyBboxPatch((cx - 2.7, cy - 1.0), 5.4, 2.0,
                             boxstyle='round,pad=0.14', linewidth=2,
                             edgecolor=c, facecolor=CARD, alpha=0.92)
        ax.add_patch(box)
        ax.text(cx, cy + 0.35, name, ha='center', va='center',
                fontsize=17, fontweight='bold', color=WHITE,
                fontproperties=kfont(17, bold=True), linespacing=1.2)
        ax.text(cx, cy - 0.42, industry, ha='center', va='center',
                fontsize=12, color=c, fontfamily='DejaVu Sans')

    ax.text(9.6, 0.22,
            'Various industry partners across Media, E-Commerce, FinTech, Healthcare, and more',
            ha='center', va='center', fontsize=12, color=GRAY,
            fontfamily='DejaVu Sans', style='italic')

    fig.tight_layout(pad=0)
    fig.savefig(str(OUT / 'infographic_references.png'), dpi=100,
                bbox_inches='tight', facecolor=NAVY2, edgecolor='none')
    plt.close(fig)
    print('OK: infographic_references.png')


if __name__ == '__main__':
    gen_process()
    gen_stats()
    gen_capabilities()
    gen_references()
    print('\nAll 4 infographics generated.')
