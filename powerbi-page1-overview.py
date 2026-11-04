# ============================================================
# Power BI Python visual — PAGE 1: Overview
# صفحة 1: نظرة عامة — Ames, Iowa Housing Price Analytics
# ------------------------------------------------------------
# HOW TO USE / طريقة الاستخدام:
#  1) Get Data → load data/ames_housing.csv
#  2) Insert → Python visual (صفحة جديدة اسمها "Overview")
#  3) Drag these EXACT 3 columns into the visual's Values well /
#     اسحب هذه الأعمدة الثلاثة بالضبط إلى خانة Values:
#        - SalePrice
#        - GrLivArea
#        - OverallQual
#  4) Paste this entire script / الصق هذا السكربت كاملاً
#
# Uses ONLY the `dataset` DataFrame injected by Power BI.
# No file loading, no plt.show() — Power BI renders the figure.
# Design: deep navy + gold on warm paper.
# ============================================================
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd

REQUIRED = ["SalePrice", "GrLivArea", "OverallQual"]
missing = [c for c in REQUIRED if c not in dataset.columns]
if missing:
    raise ValueError("Missing columns — drag into Values: " + ", ".join(missing))

df = dataset.dropna(subset=REQUIRED).copy()
BG, CARD, GOLD, NAVY, SLATE = "#FAF9F6", "#1B2A4A", "#C9A227", "#1B2A4A", "#4A5568"

fig = plt.figure(figsize=(13, 8), facecolor=BG)
gs = fig.add_gridspec(3, 2, height_ratios=[0.6, 1, 1], hspace=0.5, wspace=0.3,
                      left=0.07, right=0.95, top=0.88, bottom=0.08)
fig.text(0.07, 0.95, "OVERVIEW  •  AMES HOUSING", fontsize=11, color=GOLD, weight="bold", va="center")

def kpi_card(pos, label, value):
    ax = fig.add_subplot(pos); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.01, 0.04), 0.98, 0.92, boxstyle="round,pad=0.015,rounding_size=0.09",
                                facecolor=CARD, edgecolor=GOLD, linewidth=1.2, transform=ax.transAxes))
    ax.text(0.5, 0.60, value, ha="center", va="center", fontsize=18, fontweight="bold",
            color=GOLD, transform=ax.transAxes)
    ax.text(0.5, 0.30, label, ha="center", va="center", fontsize=9, weight="bold",
            color="white", transform=ax.transAxes)

def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#D8D2C4")
    ax.grid(axis="y", alpha=0.25, linestyle="--"); ax.tick_params(colors=SLATE, labelsize=9)

kpi_card(gs[0, 0], "MEDIAN SALE PRICE", f"${df['SalePrice'].median():,.0f}")
kpi_card(gs[0, 1], "TRANSACTIONS", f"{len(df):,}")

ax = fig.add_subplot(gs[1, :]); style(ax)
ax.hist(df["SalePrice"], bins=42, color=NAVY, edgecolor="white", linewidth=0.4)
ax.axvline(df["SalePrice"].median(), color=GOLD, lw=2.5, label=f"Median ${df['SalePrice'].median():,.0f}")
ax.set_title("Sale price distribution", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=8)
ax.set_xlabel("Sale price (USD)", color=SLATE); ax.legend(fontsize=9, frameon=False)

ax = fig.add_subplot(gs[2, :]); style(ax)
sc = ax.scatter(df["GrLivArea"], df["SalePrice"], c=df["OverallQual"], cmap="YlOrBr",
                alpha=0.55, s=14, edgecolors="none")
ax.set_title("Living area vs sale price", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=8)
ax.set_xlabel("Living area (sqft)", color=SLATE); ax.set_ylabel("Sale price (USD)", color=SLATE)
plt.colorbar(sc, ax=ax, shrink=0.85, label="Overall quality")
ax.text(0.04, 0.94, f"r = {df['GrLivArea'].corr(df['SalePrice']):.2f}", transform=ax.transAxes,
        fontsize=10, color=NAVY, weight="bold",
        bbox=dict(facecolor="white", alpha=0.85, edgecolor="#EDE8DC", boxstyle="round,pad=0.3"))
