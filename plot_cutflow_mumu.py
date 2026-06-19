#!/usr/bin/env python3
import os
import ROOT
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

ROOT.gROOT.SetBatch(True)

INPUT_FILE = "output_histograms_muons_medium/data.root"
HIST_NAME  = "Cutflow_CutFlow_mumu_medium_ttbar"
OUTPUT_PDF = "Plots/cutflow_mumu_medium.pdf"
OUTPUT_PNG = "Plots/cutflow_mumu_medium.png"

# ── ler histograma ──────────────────────────────────────────────────────────
f = ROOT.TFile(INPUT_FILE)
h = f.Get(HIST_NAME)
h.SetDirectory(0)
f.Close()

n      = h.GetNbinsX()
labels = [h.GetXaxis().GetBinLabel(i).replace("CF_Pass_", "") for i in range(1, n + 1)]
counts = [h.GetBinContent(i) for i in range(1, n + 1)]

# ── plot ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10,8))

bars = ax.bar(range(n), counts, color="#1f77b4", edgecolor="black", linewidth=0.8)

# valores acima das barras
for bar, val in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() * 1.02,
            f"{int(val):,}",
            ha="center", va="bottom", fontsize=9)

# eixos
#canvas
ax.set_title("Cut Flow - (Medium W.P.)", fontsize=14, fontweight="bold")
# frame
ax.set_frame_on(True)
ax.set_xticks(range(n))
ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=10)
ax.set_ylabel("Events", fontsize=12, fontweight="bold")
ax.set_xlabel("Selection cut", fontsize=12, fontweight="bold")
ax.set_ylim(0, max(counts) * 1.2)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# estilo ATLAS-like
for spine in ax.spines.values():
    spine.set_visible(True)
ax.tick_params(axis="both", direction="in", which="both")
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

# label ATLAS
ax.text(0.89, 0.97, "ATLAS", transform=ax.transAxes,
        fontsize=14, fontweight="bold", fontstyle="italic",
        ha="right", va="top")
ax.text(0.97, 0.97, "Internal", transform=ax.transAxes,
        fontsize=11, ha="right", va="top")
ax.text(0.17, 0.97, "Data", transform=ax.transAxes,
        fontsize=14, fontweight="bold", ha="right", va="top")
ax.text(0.68, 0.92, "$t\\bar{t} \\to \\mu\\mu b\\bar{b} \\nu \\bar{\\nu}$", transform=ax.transAxes,
        fontsize=20, ha="right", va="top")


fig.tight_layout()

os.makedirs("Plots", exist_ok=True)
fig.savefig(OUTPUT_PDF, dpi=150)
fig.savefig(OUTPUT_PNG, dpi=150)
print(f"Salvo em: {OUTPUT_PDF}  |  {OUTPUT_PNG}")
