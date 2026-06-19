#!/usr/bin/env python3
"""Gera tabela LaTeX do cutflow para os três samples em output_histograms_muons_medium/."""

import os
import ROOT

ROOT.gROOT.SetBatch(True)

INPUT_DIR = "output_histograms_muons_medium"
HIST_NAME = "Cutflow_CutFlow_mumu_medium_ttbar"
OUTPUT_TEX = "Plots/cutflow_mumu_medium_table.tex"

SAMPLES = {
    "data.root":     ("Data",                    False),  # (label, is_mc)
    "ttHijing.root": (r"$t\bar{t}$ HIJING",      True),
    "zmumu.root":    (r"$Z \to \mu\mu$ HIJING",  True),
}

# ── ler todos os cutflows ────────────────────────────────────────────────────
results = {}
labels  = None

for fname, (sample_label, is_mc) in SAMPLES.items():
    f = ROOT.TFile(os.path.join(INPUT_DIR, fname))
    h = f.Get(HIST_NAME)
    h.SetDirectory(0)
    f.Close()

    n = h.GetNbinsX()
    if labels is None:
        labels = [h.GetXaxis().GetBinLabel(i).replace("CF_Pass_", "").replace("_", r"\_")
                  for i in range(1, n + 1)]

    results[fname] = {
        "label":  sample_label,
        "is_mc":  is_mc,
        "counts": [h.GetBinContent(i) for i in range(1, n + 1)],
    }

# ── montar tabela LaTeX ──────────────────────────────────────────────────────
col_labels = [v["label"] for v in results.values()]
ncols = len(col_labels)

lines = []
lines.append(r"\begin{table}[htbp]")
lines.append(r"  \centering")
lines.append(r"  \caption{Cutflow for the $t\bar{t} \to \mu\mu$ selection (Medium WP).}")
lines.append(r"  \label{tab:cutflow_mumu_medium}")
lines.append(r"  \begin{tabular}{l" + "r" * ncols + "}")
lines.append(r"    \toprule")

# cabeçalho
header = "    Selection cut & " + " & ".join(col_labels) + r" \\"
lines.append(header)
lines.append(r"    \midrule")

# linhas de cortes
sample_list = list(results.values())
for i, cut in enumerate(labels):
    row_vals = []
    for s in sample_list:
        val = s["counts"][i]
        if s["is_mc"]:
            row_vals.append(f"{val:.1f}")
        else:
            row_vals.append(f"{int(val):,}".replace(",", r"\,"))
    row = f"    {cut} & " + " & ".join(row_vals) + r" \\"
    lines.append(row)

lines.append(r"    \bottomrule")
lines.append(r"  \end{tabular}")
lines.append(r"\end{table}")

tex = "\n".join(lines)

# ── salvar ───────────────────────────────────────────────────────────────────
os.makedirs("Plots", exist_ok=True)
with open(OUTPUT_TEX, "w") as out:
    out.write(tex + "\n")

print(f"Salvo em: {OUTPUT_TEX}")
print()
print(tex)
