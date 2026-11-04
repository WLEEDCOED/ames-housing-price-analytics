# Ames, Iowa Housing Price Analytics — dashboard builder (real data)
# Design: deep navy + gold on warm paper. Run: python dashboard.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import numpy as np

BG, CARD, GOLD, NAVY, SLATE, SOFT = "#FAF9F6", "#1B2A4A", "#C9A227", "#1B2A4A", "#4A5568", "#EDE8DC"

df = pd.read_csv("data/ames_housing.csv")
df = df.drop(columns=["Id"], errors="ignore")
df["Decade"] = (df["YearBuilt"] // 10 * 10).astype(int)

fig = plt.figure(figsize=(16, 10), facecolor=BG)
gs = fig.add_gridspec(3, 4, height_ratios=[0.62, 1, 1.05], hspace=0.55, wspace=0.4,
                      left=0.055, right=0.965, top=0.88, bottom=0.07)

fig.text(0.055, 0.95, "AMES, IOWA  •  HOUSING PRICE ANALYTICS", fontsize=11, color=GOLD, weight="bold", va="center")
fig.text(0.055, 0.915, "Real home sales 2006–2010  •  1,460 transactions", fontsize=13, color=NAVY, va="center")

def kpi_card(pos, label, value):
    ax = fig.add_subplot(pos); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.01, 0.04), 0.98, 0.92, boxstyle="round,pad=0.015,rounding_size=0.09",
                                facecolor=CARD, edgecolor=GOLD, linewidth=1.2, transform=ax.transAxes))
    ax.text(0.5, 0.60, value, ha="center", va="center", fontsize=19, fontweight="bold",
            color=GOLD, transform=ax.transAxes)
    ax.text(0.5, 0.30, label, ha="center", va="center", fontsize=9.5, weight="bold",
            color="white", transform=ax.transAxes)

def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#D8D2C4")
    ax.grid(axis="y", alpha=0.25, linestyle="--")
    ax.tick_params(colors=SLATE, labelsize=9)

kpi_card(gs[0, 0], "MEDIAN SALE PRICE", f"${df['SalePrice'].median():,.0f}")
kpi_card(gs[0, 1], "MEAN SALE PRICE", f"${df['SalePrice'].mean():,.0f}")
kpi_card(gs[0, 2], "TRANSACTIONS", f"{len(df):,}")
kpi_card(gs[0, 3], "AVG PRICE / LIVING SQFT", f"${(df['SalePrice'] / df['GrLivArea']).mean():,.2f}")

# ---- Wide histogram + narrow decade bars ----
ax = fig.add_subplot(gs[1, 0:3]); style(ax)
ax.hist(df["SalePrice"], bins=42, color=NAVY, edgecolor="white", linewidth=0.4)
ax.axvline(df["SalePrice"].median(), color=GOLD, lw=2.5, label=f"Median ${df['SalePrice'].median():,.0f}")
ax.axvline(df["SalePrice"].mean(), color="#B3402A", ls="--", lw=2, label=f"Mean ${df['SalePrice'].mean():,.0f}")
ax.set_title("Sale price distribution  —  right-skewed (skew "
             f"{df['SalePrice'].skew():.2f})", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=10)
ax.set_xlabel("Sale price (USD)", color=SLATE); ax.legend(fontsize=8.5, frameon=False)

ax = fig.add_subplot(gs[1, 3]); style(ax)
med_d = df.groupby("Decade")["SalePrice"].median().sort_index()
ax.bar(med_d.index.astype(str), med_d.values, color=GOLD, edgecolor=NAVY, linewidth=0.8)
ax.set_title("Median by decade built", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=10)
ax.set_ylabel("Median price (USD)", color=SLATE)
plt.setp(ax.get_xticklabels(), rotation=35, ha="right", fontsize=8)

# ---- Scatter + neighborhoods ----
ax = fig.add_subplot(gs[2, 0:2]); style(ax)
sc = ax.scatter(df["GrLivArea"], df["SalePrice"], c=df["OverallQual"], cmap="YlOrBr",
                alpha=0.55, s=14, edgecolors="none")
ax.set_title("Living area vs sale price", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=10)
ax.set_xlabel("Living area (sqft)", color=SLATE); ax.set_ylabel("Sale price (USD)", color=SLATE)
cb = plt.colorbar(sc, ax=ax, shrink=0.85); cb.set_label("Overall quality", color=SLATE)
ax.text(0.04, 0.94, f"r = {df['GrLivArea'].corr(df['SalePrice']):.2f}", transform=ax.transAxes, fontsize=10,
        color=NAVY, weight="bold", bbox=dict(facecolor="white", alpha=0.85, edgecolor=SOFT, boxstyle="round,pad=0.3"))

ax = fig.add_subplot(gs[2, 2:4]); style(ax)
med = df.groupby("Neighborhood")["SalePrice"].median().sort_values(ascending=False).head(10).sort_values()
bars = ax.barh(med.index, med.values, color=NAVY, edgecolor="none", height=0.62)
bars[-1].set_color(GOLD); bars[-1].set_edgecolor(NAVY)
ax.set_title("Top 10 neighborhoods by median price", loc="left", fontsize=12, fontweight="bold", color=NAVY, pad=10)
ax.set_xlabel("Median sale price (USD)", color=SLATE)
for i, v in enumerate(med.values):
    ax.text(v + 2500, i, f"${v:,.0f}", va="center", fontsize=8.5, color=SLATE)
ax.tick_params(labelsize=8.5)

fig.text(0.5, 0.015, "Source: Ames Housing dataset (Dean De Cock, via Kaggle) — real sales, Ames, Iowa 2006–2010",
         ha="center", fontsize=8, color=SLATE)
fig.savefig("dashboard.png", dpi=100, facecolor=BG)
print("saved dashboard.png", df.shape)
