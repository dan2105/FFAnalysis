# FFAnalysis

Analysis of $t\bar{t}$ production in heavy-ion collisions using the [FastFrames](https://gitlab.cern.ch/atlas-amglab/fastframes) framework, developed within the ATLAS experiment.

## Channels

| Config file | Channel |
|---|---|
| `ttmumu_wp_medium.yaml` | $t\bar{t} \to \mu\mu$ — Medium WP |
| `ttmumu_wp_loose.yaml` | $t\bar{t} \to \mu\mu$ — Loose WP |
| `ttee_wp_loose.yaml` | $t\bar{t} \to ee$ — Loose WP |
| `ttemu_wp_loose.yaml` | $t\bar{t} \to e\mu$ — Loose WP |
| `ttmujets_wp_loose.yaml` | $t\bar{t} \to \mu$+jets — Loose WP |

## Scripts

- `plot_cutflow_mumu.py` / `plot_cutflow_ee.py` — cutflow plots in ATLAS style
- `make_cutflow_table.py` / `make_cutflow_table_ee.py` — LaTeX cutflow tables
- `objects_selection.py` — object selection definitions

## Structure

```
FFAnalysis/
├── fastframes/              # FastFrames submodule
├── output_histograms_*/     # Generated histograms (not versioned)
├── Plots/                   # Generated plots (not versioned)
└── metadata/                # Filelists and sum-of-weights (not versioned)
```
