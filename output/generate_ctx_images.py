# -*- coding: utf-8 -*-
"""
CleverTap 슬라이드 컨텍스트 맞춤 UI 목업 이미지 생성기
- matplotlib + Pillow로 슬라이드별 제품 UI 시각화
- 다크 테마 (CleverTap 브랜드 컬러: #1A1A2E 배경, #6B4EFF 퍼플)
- 실제 제품 UI처럼 보이는 프로페셔널한 디자인
"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
# Korean font setup
try:
    fm.fontManager.addfont('C:/Windows/Fonts/malgun.ttf')
    matplotlib.rcParams['font.family'] = 'Malgun Gothic'
except Exception:
    pass
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

ASSETS = Path("C:/Agent/pepper/output/clevertap_assets")
ASSETS.mkdir(parents=True, exist_ok=True)

# CleverTap Brand Colors
BG_DARK   = '#1A1A2E'
BG_MID    = '#16213E'
BG_CARD   = '#2D2D4E'
PURPLE    = '#6B4EFF'
PURPLE_L  = '#9B8AFF'
WHITE     = '#FFFFFF'
GRAY      = '#6C758D'
LIGHT     = '#F4F4F8'
GREEN     = '#00C985'
ORANGE    = '#FF6B35'
CYAN      = '#00D4FF'

W, H = 1280, 720
DPI = 96


# ─────────────────────────────────────────────────────────────
# 1. ANALYTICS DASHBOARD
# ─────────────────────────────────────────────────────────────
def make_analytics():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax_main = fig.add_axes([0, 0, 1, 1])
    ax_main.set_facecolor(BG_DARK)
    ax_main.set_xlim(0, W); ax_main.set_ylim(0, H)
    ax_main.axis('off')

    # Top bar
    ax_main.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID, zorder=1))
    ax_main.text(20, H-26, 'Analytics Dashboard', color=WHITE, fontsize=13, fontweight='bold', va='center')
    for i, tab in enumerate(['Funnel', 'Cohort', 'Flow', 'Events', 'Pivot']):
        x = 200 + i*120
        col = PURPLE if i == 0 else GRAY
        ax_main.add_patch(patches.Rectangle((x-5, H-52), 110, 52, color=PURPLE if i==0 else 'none', alpha=0.2 if i==0 else 0, zorder=1))
        ax_main.text(x+50, H-26, tab, color=WHITE if i==0 else GRAY, fontsize=10, va='center', ha='center')
    # Date range chip
    ax_main.add_patch(FancyBboxPatch((W-200, H-42), 180, 32, boxstyle='round,pad=4', color=BG_CARD, zorder=2))
    ax_main.text(W-110, H-26, 'Last 30 Days  ▾', color=LIGHT, fontsize=9, va='center', ha='center')

    # KPI cards row
    kpis = [('Total Users', '2.4M', '+12.3%', GREEN), ('Sessions', '8.7M', '+8.1%', GREEN),
            ('Avg Session', '4m 32s', '+5.2%', GREEN), ('Retention D7', '42.1%', '-2.1%', ORANGE)]
    for i, (label, val, chg, color) in enumerate(kpis):
        x = 20 + i*310; y = H-160
        ax_main.add_patch(FancyBboxPatch((x, y), 290, 90, boxstyle='round,pad=6', color=BG_CARD, zorder=2))
        ax_main.add_patch(patches.Rectangle((x, y+84), 290, 6, color=PURPLE, zorder=3))
        ax_main.text(x+14, y+60, label, color=GRAY, fontsize=9, va='center')
        ax_main.text(x+14, y+28, val, color=WHITE, fontsize=20, fontweight='bold', va='center')
        ax_main.text(x+160, y+28, chg, color=color, fontsize=10, va='center')

    # Funnel chart (left)
    ax_f = fig.add_axes([0.02, 0.04, 0.38, 0.48])
    ax_f.set_facecolor(BG_CARD)
    ax_f.set_xlim(0, 10); ax_f.set_ylim(0, 6)
    ax_f.axis('off')
    ax_f.text(0.3, 5.5, 'Conversion Funnel', color=WHITE, fontsize=10, fontweight='bold')
    stages = [('App Open', 100, PURPLE), ('Product View', 68, PURPLE_L),
              ('Add to Cart', 41, CYAN), ('Purchase', 22, GREEN)]
    for j, (stage, pct, col) in enumerate(stages):
        y = 4.5 - j*1.1
        w = pct/100 * 8
        ax_f.add_patch(FancyBboxPatch((5-w/2, y-0.35), w, 0.7, boxstyle='round,pad=3', color=col, alpha=0.85, zorder=2))
        ax_f.text(0.3, y, stage, color=LIGHT, fontsize=8.5, va='center')
        ax_f.text(9.7, y, f'{pct}%', color=WHITE, fontsize=9, fontweight='bold', va='center', ha='right')

    # Line chart (right)
    ax_l = fig.add_axes([0.42, 0.04, 0.56, 0.48])
    ax_l.set_facecolor(BG_CARD)
    ax_l.spines[['top','right','bottom','left']].set_color(BG_MID)
    ax_l.tick_params(colors=GRAY, labelsize=8)
    ax_l.set_facecolor(BG_CARD)
    days = np.arange(1, 31)
    sessions = 200 + 50*np.sin(days/5) + 80*(days/30) + np.random.randint(-15,15,30)
    dau = 80 + 20*np.sin(days/4+1) + 30*(days/30) + np.random.randint(-8,8,30)
    ax_l.fill_between(days, sessions*0+0, sessions, alpha=0.15, color=PURPLE)
    ax_l.plot(days, sessions, color=PURPLE, linewidth=2, label='Sessions')
    ax_l.fill_between(days, dau*0+0, dau, alpha=0.15, color=GREEN)
    ax_l.plot(days, dau, color=GREEN, linewidth=2, linestyle='--', label='DAU')
    ax_l.set_xlabel('Day', color=GRAY, fontsize=8)
    ax_l.set_title('Activity Trend', color=WHITE, fontsize=10, fontweight='bold', pad=8)
    ax_l.legend(loc='upper left', fontsize=8, labelcolor=LIGHT, framealpha=0.2, facecolor=BG_CARD)
    ax_l.grid(axis='y', color=BG_MID, linestyle='--', alpha=0.5)
    for spine in ax_l.spines.values():
        spine.set_color('#3D3D5E')

    out = ASSETS / 'ctx_analytics.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_analytics.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# 2. SEGMENTATION BUILDER
# ─────────────────────────────────────────────────────────────
def make_segmentation():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off')

    # Header bar
    ax.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID))
    ax.text(20, H-26, 'Segments', color=WHITE, fontsize=13, fontweight='bold', va='center')
    ax.add_patch(FancyBboxPatch((W-180, H-44), 160, 34, boxstyle='round,pad=4', color=PURPLE))
    ax.text(W-100, H-27, '+ New Segment', color=WHITE, fontsize=9, fontweight='bold', va='center', ha='center')

    # Left panel: Segment builder
    ax.add_patch(FancyBboxPatch((16, 60), 500, H-130, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(30, H-80, 'Segment Builder', color=WHITE, fontsize=11, fontweight='bold')
    ax.text(30, H-100, 'Define conditions to group users', color=GRAY, fontsize=8.5)

    # Segment type chips
    seg_types = ['Static', 'Dynamic', 'RFM', 'Predictive']
    for i, st in enumerate(seg_types):
        x = 30 + i*120
        is_sel = i == 1
        ax.add_patch(FancyBboxPatch((x, H-136), 108, 28, boxstyle='round,pad=4',
                                     color=PURPLE if is_sel else BG_MID))
        ax.text(x+54, H-122, st, color=WHITE if is_sel else GRAY, fontsize=9, va='center', ha='center')

    # Filter conditions
    filters = [
        ('Event', 'App Opened', 'in last', '7 days'),
        ('Property', 'Country', 'equals', 'South Korea'),
        ('Property', 'Plan Type', 'is not', 'Free'),
        ('Event', 'Purchase', 'at least', '1 times'),
    ]
    y_start = H - 185
    for i, (ftype, field, op, val) in enumerate(filters):
        y = y_start - i*72
        ax.add_patch(FancyBboxPatch((26, y-52), 478, 60, boxstyle='round,pad=4', color=BG_MID))
        # AND badge
        if i > 0:
            ax.add_patch(FancyBboxPatch((225, y+12), 40, 18, boxstyle='round,pad=2', color=BG_DARK))
            ax.text(245, y+21, 'AND', color=PURPLE_L, fontsize=7, va='center', ha='center', fontweight='bold')
        # Type badge
        ax.add_patch(FancyBboxPatch((34, y-44), 52, 18, boxstyle='round,pad=2',
                                     color=CYAN+'33'))
        ax.text(60, y-35, ftype, color=CYAN, fontsize=7.5, va='center', ha='center')
        # Fields
        ax.text(98, y-35, field, color=WHITE, fontsize=9, va='center', fontweight='bold')
        ax.text(230, y-35, op, color=GRAY, fontsize=9, va='center')
        ax.add_patch(FancyBboxPatch((290, y-46), 100, 22, boxstyle='round,pad=2', color=PURPLE+'44'))
        ax.text(340, y-35, val, color=PURPLE_L, fontsize=9, va='center', ha='center')
        # Delete button
        ax.text(490, y-35, '×', color=GRAY, fontsize=12, va='center', ha='center')

    # Estimated reach
    y_reach = 105
    ax.add_patch(FancyBboxPatch((26, y_reach), 478, 56, boxstyle='round,pad=4', color=BG_MID))
    ax.text(30+14, y_reach+36, 'Estimated Reach', color=GRAY, fontsize=9, va='center')
    ax.text(30+14, y_reach+12, '284,920  users', color=GREEN, fontsize=16, fontweight='bold', va='center')
    ax.text(380, y_reach+20, '11.9% of base', color=GRAY, fontsize=9, va='center')

    # Right panel: Segment list
    ax.add_patch(FancyBboxPatch((536, 60), 728, H-130, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(550, H-80, 'Saved Segments', color=WHITE, fontsize=11, fontweight='bold')

    segs = [
        ('High Value Users', '142K', 'Dynamic', '14m ago', GREEN),
        ('Churn Risk — 30d', '89K', 'Predictive', '2h ago', ORANGE),
        ('New Registrations', '38K', 'Static', 'Today', CYAN),
        ('Premium — KR', '21K', 'RFM', '1d ago', PURPLE_L),
        ('Inactive 7 Days', '312K', 'Dynamic', '30m ago', GRAY),
    ]
    for i, (name, size, stype, updated, color) in enumerate(segs):
        y = H - 130 - i*82
        ax.add_patch(FancyBboxPatch((546, y-62), 708, 68, boxstyle='round,pad=4', color=BG_MID))
        ax.add_patch(patches.Rectangle((546, y+2), 4, 64, color=color))
        ax.text(562, y-16, name, color=WHITE, fontsize=10, fontweight='bold', va='center')
        ax.add_patch(FancyBboxPatch((562, y-48), 72, 20, boxstyle='round,pad=2', color=color+'33'))
        ax.text(598, y-38, stype, color=color, fontsize=8, va='center', ha='center')
        ax.text(648, y-38, f'Updated {updated}', color=GRAY, fontsize=8, va='center')
        ax.text(1200, y-16, size, color=WHITE, fontsize=14, fontweight='bold', va='center', ha='right')
        ax.text(1200, y-40, 'users', color=GRAY, fontsize=8, va='center', ha='right')

    out = ASSETS / 'ctx_segmentation.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_segmentation.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# 3. A/B TESTING DASHBOARD
# ─────────────────────────────────────────────────────────────
def make_ab_testing():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off')

    # Header
    ax.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID))
    ax.text(20, H-26, 'Experiment & Optimization', color=WHITE, fontsize=13, fontweight='bold', va='center')
    ax.add_patch(FancyBboxPatch((W-200, H-44), 180, 34, boxstyle='round,pad=4', color=PURPLE))
    ax.text(W-110, H-27, '+ New Experiment', color=WHITE, fontsize=9, fontweight='bold', va='center', ha='center')

    # Active experiment card
    ax.add_patch(FancyBboxPatch((16, H-240), W-32, 174, boxstyle='round,pad=8', color=BG_CARD))
    ax.add_patch(patches.Rectangle((16, H-72), W-32, 6, color=GREEN))
    ax.add_patch(FancyBboxPatch((28, H-96), 80, 22, boxstyle='round,pad=2', color=GREEN+'44'))
    ax.text(68, H-85, '● RUNNING', color=GREEN, fontsize=8, va='center', ha='center', fontweight='bold')
    ax.text(125, H-85, 'Push Notification CTA Test — Upgrade Campaign', color=WHITE, fontsize=11, fontweight='bold', va='center')
    ax.text(125, H-108, 'Started Apr 15 · Day 6 of 14 · 43% traffic split', color=GRAY, fontsize=9, va='center')

    # Variant bars
    variants = [('Control (A)', 'Upgrade Now — Limited Time!', 18.3, 24200, GRAY),
                ('Variant B', 'Your exclusive offer expires tonight', 24.7, 32600, PURPLE),
                ('Variant C', 'Claim your 30% discount →', 21.1, 27900, CYAN)]
    for i, (label, msg, ctr, users, color) in enumerate(variants):
        y = H - 155 - i*42
        ax.text(28, y, label, color=color, fontsize=9, fontweight='bold', va='center')
        ax.text(140, y, f'"{msg}"', color=LIGHT, fontsize=8.5, va='center', style='italic')
        # Bar
        bar_w = ctr/30 * 300
        ax.add_patch(patches.Rectangle((780, y-10), 300, 20, color=BG_MID))
        ax.add_patch(patches.Rectangle((780, y-10), bar_w, 20, color=color, alpha=0.8))
        ax.text(786+bar_w+8, y, f'{ctr}% CTR', color=WHITE, fontsize=9, va='center', fontweight='bold' if i==1 else 'normal')
        ax.text(1200, y, f'{users:,}', color=GRAY, fontsize=9, va='center', ha='right')
        if i == 1:
            ax.add_patch(FancyBboxPatch((1205, y-12), 62, 22, boxstyle='round,pad=2', color=GREEN+'44'))
            ax.text(1236, y, '▲ Best', color=GREEN, fontsize=8, va='center', ha='center', fontweight='bold')

    # Statistics cards row
    stats = [('Statistical Significance', '94.2%', 'Need 95%+', ORANGE),
             ('Sample Size', '84,700', 'Target: 100K', PURPLE_L),
             ('Improvement', '+34.9%', 'vs Control', GREEN),
             ('Est. Completion', '3 days', 'Apr 24', CYAN)]
    y_s = 320
    for i, (label, val, sub, color) in enumerate(stats):
        x = 16 + i*316
        ax.add_patch(FancyBboxPatch((x, y_s), 298, 88, boxstyle='round,pad=6', color=BG_CARD))
        ax.add_patch(patches.Rectangle((x, y_s+82), 298, 6, color=color))
        ax.text(x+14, y_s+58, label, color=GRAY, fontsize=8.5, va='center')
        ax.text(x+14, y_s+28, val, color=WHITE, fontsize=20, fontweight='bold', va='center')
        ax.text(x+14, y_s+8, sub, color=color, fontsize=8, va='center')

    # Results timeline mini-chart
    ax_chart = fig.add_axes([0.02, 0.04, 0.96, 0.26])
    ax_chart.set_facecolor(BG_CARD)
    days_x = np.arange(1, 7)
    ctrl  = [16.1, 17.2, 17.8, 18.0, 18.1, 18.3]
    var_b = [17.5, 20.1, 21.8, 23.2, 24.1, 24.7]
    var_c = [16.8, 18.5, 19.4, 20.2, 20.8, 21.1]
    ax_chart.fill_between(days_x, ctrl, alpha=0.1, color=GRAY)
    ax_chart.plot(days_x, ctrl, 'o--', color=GRAY, linewidth=1.5, markersize=4, label='Control (A)')
    ax_chart.fill_between(days_x, var_b, alpha=0.15, color=PURPLE)
    ax_chart.plot(days_x, var_b, 'o-', color=PURPLE, linewidth=2, markersize=5, label='Variant B ★')
    ax_chart.fill_between(days_x, var_c, alpha=0.1, color=CYAN)
    ax_chart.plot(days_x, var_c, 'o--', color=CYAN, linewidth=1.5, markersize=4, label='Variant C')
    ax_chart.set_facecolor(BG_CARD)
    ax_chart.set_title('CTR by Day', color=WHITE, fontsize=9, fontweight='bold', pad=4)
    ax_chart.set_ylabel('CTR %', color=GRAY, fontsize=8)
    ax_chart.tick_params(colors=GRAY, labelsize=7)
    ax_chart.legend(loc='lower right', fontsize=8, labelcolor=LIGHT, framealpha=0.2, facecolor=BG_MID)
    ax_chart.grid(axis='y', color='#3D3D5E', linestyle='--', alpha=0.5)
    for spine in ax_chart.spines.values():
        spine.set_color('#3D3D5E')
    ax_chart.set_xticks(days_x)
    ax_chart.set_xticklabels([f'Day {d}' for d in days_x], color=GRAY, fontsize=7)

    out = ASSETS / 'ctx_ab.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_ab.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# 4. AI / ML DECISIONING ENGINE
# ─────────────────────────────────────────────────────────────
def make_ai():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off')

    # Header
    ax.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID))
    ax.text(20, H-26, '✦ CleverAI™ Decisioning Engine', color=WHITE, fontsize=13, fontweight='bold', va='center')
    ax.add_patch(FancyBboxPatch((W-170, H-44), 150, 32, boxstyle='round,pad=4', color=PURPLE+'44'))
    ax.text(W-95, H-28, 'AI-Powered ✦', color=PURPLE_L, fontsize=9, va='center', ha='center')

    # Prediction Score card
    ax.add_patch(FancyBboxPatch((16, H-240), 380, 174, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(30, H-80, 'User Predictions', color=WHITE, fontsize=11, fontweight='bold')
    preds = [('Churn Risk (7d)', 73, ORANGE), ('Purchase Intent', 61, GREEN), ('Upgrade Probability', 48, PURPLE_L)]
    for i, (label, pct, color) in enumerate(preds):
        y = H - 118 - i*42
        ax.text(30, y, label, color=LIGHT, fontsize=9, va='center')
        ax.add_patch(patches.Rectangle((210, y-10), 160, 18, color=BG_MID))
        ax.add_patch(patches.Rectangle((210, y-10), pct/100*160, 18, color=color, alpha=0.8))
        ax.text(382, y, f'{pct}%', color=color, fontsize=9, fontweight='bold', va='center')

    # STO card
    ax.add_patch(FancyBboxPatch((410, H-240), 860, 174, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(424, H-80, 'Send-Time Optimization (STO) — Per-User Best Delivery Window', color=WHITE, fontsize=10, fontweight='bold')
    hours = np.arange(0, 24)
    np.random.seed(7)
    dist = np.zeros(24)
    dist[7:9] += [0.5, 0.8]; dist[12:14] += [0.7, 0.6]; dist[19:22] += [0.9, 1.0, 0.75]
    dist += np.random.uniform(0, 0.2, 24)
    dist = dist / dist.max()
    ax_sto = fig.add_axes([0.335, 0.56, 0.64, 0.25])
    ax_sto.set_facecolor(BG_CARD)
    bars = ax_sto.bar(hours, dist, color=PURPLE, alpha=0.6, width=0.8)
    for b, d in zip(bars, dist):
        if d > 0.85:
            b.set_color(GREEN); b.set_alpha(1.0)
    ax_sto.set_facecolor(BG_CARD)
    ax_sto.set_xlim(-0.5, 23.5)
    ax_sto.tick_params(colors=GRAY, labelsize=7)
    ax_sto.set_xticks([0,6,12,18,23])
    ax_sto.set_xticklabels(['12AM','6AM','12PM','6PM','11PM'], color=GRAY, fontsize=7)
    ax_sto.set_title('Optimal Delivery Hours Distribution', color=LIGHT, fontsize=8, pad=3)
    ax_sto.grid(axis='y', color='#3D3D5E', linestyle='--', alpha=0.4)
    for spine in ax_sto.spines.values(): spine.set_color('#3D3D5E')

    # Dynamic Content & Recommendation
    ax.add_patch(FancyBboxPatch((16, 60), 600, 270, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(30, 308, 'Dynamic Content Personalization', color=WHITE, fontsize=10, fontweight='bold')
    recs = [('User #K-2847', 'Premium Plan', '92% match', GREEN),
            ('User #K-5591', 'Insurance Add-on', '87% match', PURPLE_L),
            ('User #K-1203', 'Savings Account', '79% match', CYAN),
            ('User #K-8834', 'Re-engagement Offer', '71% match', ORANGE)]
    for i, (uid, prod, score, color) in enumerate(recs):
        y = 268 - i*52
        ax.add_patch(FancyBboxPatch((26, y-36), 578, 44, boxstyle='round,pad=3', color=BG_MID))
        ax.text(40, y-14, uid, color=GRAY, fontsize=8.5, va='center')
        ax.text(180, y-14, prod, color=WHITE, fontsize=9, fontweight='bold', va='center')
        ax.add_patch(FancyBboxPatch((430, y-28), 100, 22, boxstyle='round,pad=2', color=color+'33'))
        ax.text(480, y-17, score, color=color, fontsize=8.5, va='center', ha='center', fontweight='bold')

    # Model accuracy gauge
    ax.add_patch(FancyBboxPatch((632, 60), 630, 270, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(646, 308, 'Model Performance', color=WHITE, fontsize=10, fontweight='bold')
    models = [('Churn Prediction', '91.3%', '↑ 2.1%', GREEN),
              ('Purchase Forecast', '87.6%', '↑ 1.4%', GREEN),
              ('LTV Prediction', '84.2%', '↑ 3.7%', GREEN),
              ('Next Best Action', '79.8%', '→ 0.2%', GRAY)]
    for i, (mname, acc, delta, color) in enumerate(models):
        y = 262 - i*55
        ax.add_patch(FancyBboxPatch((642, y-38), 610, 46, boxstyle='round,pad=3', color=BG_MID))
        ax.text(656, y-15, mname, color=LIGHT, fontsize=9, va='center')
        ax.text(900, y-15, acc, color=WHITE, fontsize=14, fontweight='bold', va='center', ha='center')
        ax.text(1080, y-15, delta, color=color, fontsize=10, fontweight='bold', va='center', ha='right')

    out = ASSETS / 'ctx_ai.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_ai.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# 5. PRODUCT OVERVIEW (소개 슬라이드)
# ─────────────────────────────────────────────────────────────
def make_product_overview():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID))
    ax.text(20, H-26, 'CleverTap Platform Overview', color=WHITE, fontsize=13, fontweight='bold', va='center')

    # Central platform diagram
    cx, cy = 640, 360
    # Core circle
    core = plt.Circle((cx, cy), 70, color=PURPLE, zorder=5)
    ax.add_patch(core)
    ax.text(cx, cy+12, 'CleverTap', color=WHITE, fontsize=10, fontweight='bold', ha='center', va='center', zorder=6)
    ax.text(cx, cy-10, 'Platform', color=PURPLE_L, fontsize=8.5, ha='center', va='center', zorder=6)

    # Orbiting features
    features = [
        ('Analytics', 0),     ('Segmentation', 45),   ('Campaigns', 90),
        ('AI/ML', 135),       ('A/B Test', 180),       ('Journeys', 225),
        ('Push/SMS', 270),    ('Reporting', 315),
    ]
    import math
    radius = 200
    for label, angle_deg in features:
        angle = math.radians(angle_deg)
        fx = cx + radius * math.cos(angle)
        fy = cy + radius * math.sin(angle)
        # Connection line
        ax.plot([cx, fx], [cy, fy], color=PURPLE_L, alpha=0.3, linewidth=1, zorder=2)
        # Node
        ax.add_patch(plt.Circle((fx, fy), 38, color=BG_CARD, zorder=3))
        ax.add_patch(plt.Circle((fx, fy), 38, fill=False, color=PURPLE, linewidth=1.5, zorder=4))
        ax.text(fx, fy, label, color=WHITE, fontsize=8, ha='center', va='center', fontweight='bold', zorder=5)

    # Stats
    stats = [('10,000+', 'Customers'), ('100+', 'Countries'), ('12T+', 'Events/month'), ('600+', 'Team')]
    for i, (v, l) in enumerate(stats):
        x = 50 + i*300
        ax.add_patch(FancyBboxPatch((x, 30), 240, 80, boxstyle='round,pad=6', color=BG_CARD))
        ax.add_patch(patches.Rectangle((x, 104), 240, 6, color=PURPLE))
        ax.text(x+120, 80, v, color=WHITE, fontsize=20, fontweight='bold', ha='center', va='center')
        ax.text(x+120, 52, l, color=GRAY, fontsize=9, ha='center', va='center')

    out = ASSETS / 'ctx_intro.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_intro.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# 6. ENGAGEMENT / MULTICHANNEL CAMPAIGN BUILDER
# ─────────────────────────────────────────────────────────────
def make_engagement():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID))
    ax.text(20, H-26, 'Campaign Manager — Omnichannel Engagement', color=WHITE, fontsize=13, fontweight='bold', va='center')
    ax.add_patch(FancyBboxPatch((W-190, H-44), 170, 32, boxstyle='round,pad=4', color=PURPLE))
    ax.text(W-105, H-28, '+ Create Campaign', color=WHITE, fontsize=9, fontweight='bold', va='center', ha='center')

    # Campaign list
    campaigns = [
        ('Onboarding Day 1', 'Push Notification', 'Active', '94.2K', '38.4%', '12.1%', GREEN, PURPLE),
        ('Cart Recovery — KR', 'Email + Push', 'Active', '23.7K', '41.2%', '18.3%', GREEN, ORANGE),
        ('Win-back 30d', 'SMS + InApp', 'Active', '67.1K', '19.8%', '7.4%', GREEN, CYAN),
        ('Premium Upsell', 'Push + Email', 'Scheduled', '—', '—', '—', PURPLE_L, PURPLE_L),
        ('KYC Completion', 'Push Notification', 'Draft', '—', '—', '—', GRAY, GRAY),
    ]
    # Table header
    y_h = H - 86
    ax.add_patch(patches.Rectangle((16, y_h-28), W-32, 28, color=BG_MID))
    for txt, x in [('Campaign', 30), ('Channel', 300), ('Status', 470),
                    ('Sent', 580), ('Open Rate', 700), ('CTR', 840)]:
        ax.text(x, y_h-14, txt, color=GRAY, fontsize=8.5, va='center', fontweight='bold')

    for i, (name, channel, status, sent, openr, ctr, sc, cc) in enumerate(campaigns):
        y = y_h - 62 - i*72
        ax.add_patch(FancyBboxPatch((16, y-44), W-32, 60, boxstyle='round,pad=3', color=BG_CARD))
        ax.add_patch(patches.Rectangle((16, y-44), 4, 60, color=cc))
        ax.text(30, y-14, name, color=WHITE, fontsize=10, fontweight='bold', va='center')
        ax.add_patch(FancyBboxPatch((30, y-40), 8*len(channel)+10, 22, boxstyle='round,pad=2', color=BG_MID))
        ax.text(30+4*len(channel)+5, y-29, channel, color=LIGHT, fontsize=8, va='center', ha='center')
        ax.add_patch(FancyBboxPatch((470, y-30), 72, 22, boxstyle='round,pad=2', color=sc+'33'))
        ax.text(506, y-19, status, color=sc, fontsize=8, va='center', ha='center', fontweight='bold')
        ax.text(580, y-14, sent, color=WHITE, fontsize=10, va='center')
        ax.text(700, y-14, openr, color=GREEN if openr != '—' else GRAY, fontsize=10, va='center', fontweight='bold' if openr != '—' else 'normal')
        ax.text(840, y-14, ctr, color=PURPLE_L if ctr != '—' else GRAY, fontsize=10, va='center', fontweight='bold' if ctr != '—' else 'normal')

    # Right sidebar: Channel stats
    ax.add_patch(FancyBboxPatch((W-310, H-480), 290, 400, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(W-296, H-100, 'Channel Performance', color=WHITE, fontsize=10, fontweight='bold')
    channels_d = [('Push Notification', 68, PURPLE), ('Email', 45, ORANGE),
                  ('In-App', 52, CYAN), ('SMS', 31, GREEN), ('WhatsApp', 22, '#25D366')]
    for i, (ch, pct, color) in enumerate(channels_d):
        y = H - 138 - i*60
        ax.text(W-296, y, ch, color=LIGHT, fontsize=8.5, va='center')
        ax.add_patch(patches.Rectangle((W-296, y-24), 260, 16, color=BG_MID))
        ax.add_patch(patches.Rectangle((W-296, y-24), pct/100*260, 16, color=color, alpha=0.8))
        ax.text(W-26, y-16, f'{pct}%', color=color, fontsize=8, va='center', ha='right', fontweight='bold')

    out = ASSETS / 'ctx_engagement.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_engagement.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# 7. ARCHITECTURE OVERVIEW (Journey Orchestration)
# ─────────────────────────────────────────────────────────────
def make_architecture():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID))
    ax.text(20, H-26, 'Journey Orchestration — Workflow Builder', color=WHITE, fontsize=13, fontweight='bold', va='center')

    # Journey flow nodes
    nodes = [
        (100, 360, 'TRIGGER\nApp Install', PURPLE),
        (280, 460, 'WAIT\n24 hours', BG_CARD),
        (280, 260, 'CHECK\nProfile', BG_CARD),
        (460, 530, 'SEND\nPush', GREEN),
        (460, 390, 'SEND\nEmail', ORANGE),
        (460, 230, 'SEND\nIn-App', CYAN),
        (640, 530, 'CHECK\nOpened?', BG_CARD),
        (640, 390, 'CHECK\nClicked?', BG_CARD),
        (820, 530, 'SEND\nSMS', '#25D366'),
        (820, 390, 'GOAL\nConverted', GREEN),
        (820, 250, 'WAIT\n3 days', BG_CARD),
    ]
    # Draw connections first
    connections = [
        (0,1),(0,2),(1,3),(1,4),(2,5),(3,6),(4,7),
        (6,8),(7,9),(5,10)
    ]
    for a_idx, b_idx in connections:
        x1, y1 = nodes[a_idx][0]+55, nodes[a_idx][1]
        x2, y2 = nodes[b_idx][0], nodes[b_idx][1]
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=PURPLE_L, lw=1.5), zorder=2)

    for (x, y, label, color) in nodes:
        is_trigger = 'TRIGGER' in label
        is_goal = 'GOAL' in label
        ax.add_patch(FancyBboxPatch((x-50, y-30), 110, 60,
                                     boxstyle='round,pad=6',
                                     color=color if color not in [BG_CARD] else BG_CARD,
                                     zorder=3,
                                     linewidth=2 if is_goal else 0,
                                     edgecolor=GREEN if is_goal else 'none'))
        for j, line in enumerate(label.split('\n')):
            lcolor = GRAY if 'WAIT' in label or 'CHECK' in label else WHITE
            fw = 'bold' if j == 0 else 'normal'
            fsz = 7 if j == 0 else 9
            ax.text(x+5, y+8-j*16, line, color=WHITE if color != BG_CARD else (PURPLE if j==0 else LIGHT),
                    fontsize=fsz, va='center', ha='center', fontweight=fw, zorder=4)

    # Stats strip
    ax.add_patch(patches.Rectangle((0, 0), W, 80, color=BG_MID))
    journey_stats = [('Active Journeys', '47'), ('Users in Journey', '284K'),
                     ('Completion Rate', '34.2%'), ('Avg Duration', '8.3 days'),
                     ('Revenue Attributed', '₩2.4B')]
    for i, (l, v) in enumerate(journey_stats):
        x = 80 + i*250
        ax.text(x, 52, v, color=WHITE, fontsize=16, fontweight='bold', ha='center', va='center')
        ax.text(x, 24, l, color=GRAY, fontsize=8.5, ha='center', va='center')

    out = ASSETS / 'ctx_architecture.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_architecture.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# 8. CUSTOMERS / GLOBAL LOGOS
# ─────────────────────────────────────────────────────────────
def make_customers():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID))
    ax.text(640, H-26, '10,000+ Global Brands Trust CleverTap', color=WHITE,
            fontsize=14, fontweight='bold', va='center', ha='center')

    # Customer name badges (representative sample)
    custs = [
        ('Jio', 'Telecom', PURPLE), ('Swiggy', 'Food Tech', ORANGE), ('PhonePe', 'FinTech', GREEN),
        ('Axis Bank', 'Banking', CYAN), ('Hotstar', 'Media', '#E31837'), ('Dream11', 'Gaming', GREEN),
        ('Air Asia', 'Travel', '#FF0000'), ('SonyLIV', 'OTT', '#003087'), ('MakeMyTrip', 'Travel', '#E03928'),
        ('Freecharge', 'FinTech', PURPLE_L), ('Ola', 'Mobility', '#1D1D1D'), ('Zomato', 'Food', '#E23744'),
    ]
    cols, rows = 4, 3
    for i, (name, industry, color) in enumerate(custs):
        col = i % cols; row = i // cols
        x = 40 + col * 305; y = H - 120 - row * 170
        ax.add_patch(FancyBboxPatch((x, y-100), 275, 110, boxstyle='round,pad=8', color=BG_CARD))
        ax.add_patch(patches.Rectangle((x, y+4), 275, 6, color=color))
        # Company initial circle
        ax.add_patch(plt.Circle((x+50, y-42), 30, color=color, alpha=0.2))
        ax.text(x+50, y-42, name[0], color=color, fontsize=20, fontweight='bold', ha='center', va='center')
        ax.text(x+90, y-30, name, color=WHITE, fontsize=13, fontweight='bold', va='center')
        ax.add_patch(FancyBboxPatch((x+90, y-62), 6*len(industry)+10, 20, boxstyle='round,pad=2', color=color+'33'))
        ax.text(x+90+3*len(industry)+5, y-52, industry, color=color, fontsize=8, va='center', ha='center')

    # Bottom counter
    ax.add_patch(patches.Rectangle((0, 0), W, 70, color=BG_MID))
    for i, (v, l) in enumerate([('10,000+', '글로벌 앱'), ('100+', '서비스 국가'), ('12T+', '월간 이벤트')]):
        x = 200 + i*400
        ax.text(x, 44, v, color=PURPLE_L, fontsize=22, fontweight='bold', ha='center', va='center')
        ax.text(x, 18, l, color=GRAY, fontsize=10, ha='center', va='center')

    out = ASSETS / 'ctx_customers.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_customers.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# 9. FINTECH USE CASE
# ─────────────────────────────────────────────────────────────
def make_fintech():
    fig = plt.figure(figsize=(W/DPI, H/DPI), dpi=DPI)
    fig.patch.set_facecolor(BG_DARK)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off')

    ax.add_patch(patches.Rectangle((0, H-52), W, 52, color=BG_MID))
    ax.text(20, H-26, 'FinTech Journey — Mobile Banking Engagement', color=WHITE, fontsize=13, fontweight='bold', va='center')

    # Funnel: Onboarding flow
    ax.add_patch(FancyBboxPatch((16, H-480), 560, 412, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(30, H-80, 'Onboarding Conversion Funnel', color=WHITE, fontsize=11, fontweight='bold')

    stages = [
        ('App Install', 100000, '#100%', PURPLE),
        ('Registration', 78000, '78%', PURPLE_L),
        ('KYC Started', 52000, '52%', CYAN),
        ('KYC Complete', 41000, '41%', ORANGE),
        ('First Transaction', 29000, '29%', GREEN),
    ]
    for i, (stage, count, pct, color) in enumerate(stages):
        y = H - 132 - i*68
        w = count/100000 * 480
        ax.add_patch(FancyBboxPatch((40, y-26), w, 52, boxstyle='round,pad=4', color=color, alpha=0.7, zorder=2))
        ax.text(48, y, stage, color=WHITE, fontsize=9, fontweight='bold', va='center', zorder=3)
        ax.text(48+w-10, y-8, f'{count//1000}K', color=WHITE, fontsize=12, fontweight='bold', va='center', ha='right', zorder=3)
        ax.text(48+w-10, y+10, pct, color=WHITE, fontsize=9, va='center', ha='right', zorder=3)

    # Right panel: KPI cards
    kpis = [
        ('신규 가입 전환율', '40%', '↑ vs industry avg 28%', GREEN),
        ('KYC 완료율', '28%', '↑ from 19% (CleverTap before)', GREEN),
        ('온보딩 ROI', '3.2x', 'vs manual outreach', PURPLE_L),
        ('이탈 방지율', '65%', 'of at-risk users retained', ORANGE),
    ]
    ax.add_patch(FancyBboxPatch((600, H-480), 664, 200, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(614, H-80, 'FinTech Impact Metrics', color=WHITE, fontsize=11, fontweight='bold')
    for i, (label, val, note, color) in enumerate(kpis[:2]):
        x = 614 + (i%2)*320; y = H-140 - (i//2)*120
        ax.add_patch(FancyBboxPatch((x, y-90), 295, 100, boxstyle='round,pad=6', color=BG_MID))
        ax.add_patch(patches.Rectangle((x, y+4), 295, 6, color=color))
        ax.text(x+14, y-20, label, color=GRAY, fontsize=8.5, va='center')
        ax.text(x+14, y-55, val, color=color, fontsize=28, fontweight='bold', va='center')
        ax.text(x+14, y-78, note, color=GRAY, fontsize=7.5, va='center')

    for i, (label, val, note, color) in enumerate(kpis[2:]):
        x = 614 + (i%2)*320; y = H-260 - (i//2)*120
        ax.add_patch(FancyBboxPatch((x, y-90), 295, 100, boxstyle='round,pad=6', color=BG_MID))
        ax.add_patch(patches.Rectangle((x, y+4), 295, 6, color=color))
        ax.text(x+14, y-20, label, color=GRAY, fontsize=8.5, va='center')
        ax.text(x+14, y-55, val, color=color, fontsize=28, fontweight='bold', va='center')
        ax.text(x+14, y-78, note, color=GRAY, fontsize=7.5, va='center')

    # Use case timeline
    ax.add_patch(FancyBboxPatch((600, H-660), 664, 160, boxstyle='round,pad=8', color=BG_CARD))
    ax.text(614, H-500, 'Automated Lifecycle Campaigns', color=WHITE, fontsize=10, fontweight='bold')
    use_cases = [('Day 1', '환영 메시지 + 앱 투어', PURPLE), ('Day 3', 'KYC 독려 푸시', ORANGE),
                 ('Day 7', '첫 거래 인센티브', GREEN), ('Day 30', '이탈 방지 리타겟팅', CYAN)]
    ax.add_patch(patches.Rectangle((620, H-568), 636, 3, color=PURPLE, alpha=0.4))
    for i, (day, action, color) in enumerate(use_cases):
        x = 630 + i*155
        ax.add_patch(plt.Circle((x, H-566), 10, color=color, zorder=4))
        ax.text(x, H-590, day, color=color, fontsize=8, ha='center', va='center', fontweight='bold')
        ax.text(x, H-612, action, color=LIGHT, fontsize=7.5, ha='center', va='center')

    # Bottom stats
    ax.add_patch(patches.Rectangle((0, 0), W, 80, color=BG_MID))
    for i, (v, l) in enumerate([('40% ↑', '신규 가입'), ('28% ↑', 'KYC 완료'), ('3.2x', 'ROI'), ('65%', '이탈 방지')]):
        x = 160 + i*320
        ax.text(x, 48, v, color=GREEN, fontsize=18, fontweight='bold', ha='center', va='center')
        ax.text(x, 22, l, color=GRAY, fontsize=9, ha='center', va='center')

    out = ASSETS / 'ctx_fintech.png'
    plt.savefig(str(out), dpi=DPI, bbox_inches='tight', facecolor=BG_DARK, pad_inches=0)
    plt.close()
    print(f'[OK] ctx_fintech.png ({out.stat().st_size//1024}KB)')
    return str(out)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    np.random.seed(42)
    print("=== CleverTap 슬라이드 UI 이미지 생성 시작 ===\n")
    make_product_overview()
    make_analytics()
    make_segmentation()
    make_engagement()
    make_ai()
    make_ab_testing()
    make_architecture()
    make_customers()
    make_fintech()
    print("\n=== 전체 완료 ===")
    for f in sorted(ASSETS.glob("ctx_*.png")):
        print(f"  {f.name}: {f.stat().st_size//1024}KB")
