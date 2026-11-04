# ============================================================
# Power BI Python visual — PAGE 2: Details
# صفحة 2: التفاصيل — Ames, Iowa Housing Price Analytics
# ------------------------------------------------------------
# HOW TO USE / طريقة الاستخدام:
#  1) Get Data → load data/ames_housing.csv (نفس الجدول)
#  2) Insert → Python visual (صفحة جديدة اسمها "Details")
#  3) Drag these EXACT 4 columns into the visual's Values well /
#     اسحب هذه الأعمدة الأربعة بالضبط إلى خانة Values:
#        - SalePrice
#        - Neighborhood
#        - YearBuilt
#        - OverallQual
#  4) Paste this entire script / الصق هذا السكربت كاملاً
#
# Uses ONLY the `dataset` DataFrame injected by Power BI.
# No file loading, no plt.show() — Power BI renders the figure.
# Design: deep navy + gold on warm paper.
# ============================================================
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED = ["SalePrice", "Neighborhood", "YearBuilt", "OverallQual"]
missing = [c for c in REQUIRED if c not in dataset.columns]
if missing:
    raise ValueError("Missing columns — drag into Values: " + ", ".join(missing))

df = dataset.dropna(subset=REQUIRED).copy()
df["Decade"] = (df["YearBuilt"] // 10 * 10).astype(int)
BG, GOLD, NAVY, SLATE = "#FAF9F6", "#C9A227", "#1B2A4A", "#4A5568"

fig = plt.figure(figsize=(13, 8), facecolor=BG)
gs = fig.add_gridspec(2, 2, hspace=0.5, wspace=0.35, left=0.08, right=0.95, top=0.88, bottom=0.1)
fig.text(0.08, 0.95, "DETAILS  •  AMES HOUSING", fontsize=11, color=GOLD, weight="bold", va="center")

def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#D8D2C4")
    ax.grid(axis="y", alpha=0.25, linestyle="--"); ax.tick_params(colors=SLATE, labelsize=9)

ax = fig.add_subplot(gs[0, :]); style(ax)
med = df.groupby("Neighborhood")["SalePrice"].median().sort_values(ascending=False).head(10).sort_values()
bars = ax.barh(med.index, med.values, color=NAVY, height=0.62)
bars[-1].set_color(GOLD); bars[-1].set_edgecolor(NAVY)
ax.set_title("Top 10 neighborhoods by median price", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=8)
ax.set_xlabel("Median sale price (USD)", color=SLATE)
for i, v in enumerate(med.values):
    ax.text(v + 2500, i, f"${v:,.0f}", va="center", fontsize=8.5, color=SLATE)

ax = fig.add_subplot(gs[1, 0]); style(ax)
med_d = df.groupby("Decade")["SalePrice"].median().sort_index()
ax.bar(med_d.index.astype(str), med_d.values, color=GOLD, edgecolor=NAVY, linewidth=0.8)
ax.set_title("Median price by decade built", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=8)
ax.set_ylabel("Median price (USD)", color=SLATE)
plt.setp(ax.get_xticklabels(), rotation=35, ha="right", fontsize=8)

ax = fig.add_subplot(gs[1, 1]); style(ax)
order = sorted(df["OverallQual"].unique())
ax.boxplot([df.loc[df["OverallQual"] == q, "SalePrice"] for q in order], labels=order, patch_artist=True,
           boxprops=dict(facecolor="#F6E7B4", color=NAVY), medianprops=dict(color=NAVY, lw=1.5))
ax.set_title("Price by overall quality", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=8)
ax.set_xlabel("Overall quality", color=SLATE); ax.set_ylabel("Sale price (USD)", color=SLATE)
