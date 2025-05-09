# FastFrames tutorial: ATLAS Top Workshop 2025

This tutorial will guide you through the setup of a `FastFrames` module to analyse the datasets previously produced in the `TopCPToolkit` tutorial.

We will adopt the following conventions:

- when some code is intended to be run on your terminal, you will see it on a red box,

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);">This should be run on your terminal...:</strong>

```bash
echo "Hello world!"
```
</div>

- when we refer to code that needs to be modified inside a specific file, it will highlighted in green. The corresponding file name will be at the top of the code.

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);">This code should go into Hello.cpp:</strong>

```cpp
# Hello.cpp

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```
</div>

- Exercises will be highlighted in yellow:

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise</h4>
</div>

- Finally, links to more detailed content will be in blue and notes will be in purple.

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>
</div>

## 0.0 Install

First, we will install `FastFrames`.

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

We assume that you are running this tutorial inside an <code>lxplus</code> machine, located at <code>/eos/user/your_username_first_letter/your_username</code>.

</div>

Setup the environment and download the code:
<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Clone the tutorial repository Create a directory to store your work
git clone --branch part-one ssh://git@gitlab.cern.ch:7999/dbaronmo/fftutorialtopws2025.git FFTutorial --recurse-submodules
cd FFTutorial


# Setup environment
setupATLAS --quiet && lsetup git && asetup StatAnalysis,0.5.3

```
</div>

Let's now compile and install FastFrames:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Configure, compile, install
cmake -S fastframes -B build_ff -DCMAKE_INSTALL_PREFIX=install_ff
cmake --build build_ff -j4 --target install

# Setup environment
source build_ff/setup.sh

```
</div>

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

To see installation instructions for different platforms and extendend details click <a href="https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/#how-to-checkout-and-compile-the-code" target="_blank">here</a>

</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

Once FF is compiled and installed you only need to re-load your environment.
```bash
setupATLAS --quiet && lsetup git && asetup StatAnalysis,0.5.3
source build_ff/setup.sh
```
</div>

## 0.1 Clean the input data and create the metadata

Before doing any analysis, we first need to handle the cases where in the `TopCPToolkit` workflow no events passed the selections. In those cases, `TopCPToolkit` will produce files without any trees (this can happen for background samples or real collision data where our signature is not present). To clean our datasets we use the `merge_empty_grid_files` script:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Clean input files
python3 python/merge_empty_grid_files.py --root_files_folder /eos/atlas/atlascerngroupdisk/phys-top/Top_Group_Tutorials/Tutorial_2025/FastFrames/

```
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

The previous step has already been taken care for you. You are not meant to run it. You will not have permissions to write to the tutorial input files location.
</div>

FastFrames also needs to read from a database that specifies the type of sample, file locations, sum of weights, etc. The code provides the `produce_metadata_files.py` script for this purpose. Let's use it:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Produce the input files metadata
cd fastframes
python3 python/produce_metadata_files.py --root_files_folder /eos/atlas/atlascerngroupdisk/phys-top/Top_Group_Tutorials/Tutorial_2025/FastFrames/ --output_path ../metadata/

```
</div>

This creates a directory called `metadata` one level up in the directory hierarchy. This directory contains two files: `filelist.txt` and `sum_of_weights.txt`.

## 1.0 Run FastFrames:

To run the framework the application entry point is the python script `FastFrames.py`. One can look at the supported options by doing:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Get running options for FastFrames
python3 python/FastFrames.py -h

```
</div>

The most important variables that define the run are:
- `-c` The master configuration file. We will talk about this next.
- `--step` This option allows you to specify if you want to create histograms or n-tuples.
-  `--samples` Allows you to run just over certain samples.

### 1.1 The `.yaml` configuration file:

FastFrames uses a configuration file to define the running job. For this tutorial the configuration file is called `ttZconfig.yaml`. This file is divided by blocks. The `general` block looks like this:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
  debug_level: INFO # Logger level
  input_filelist_path: "../metadata/filelist.txt" # Path to the metadata relative to fastframes directory
  input_sumweights_path: "../metadata/sum_of_weights.txt" # Path to the metadata relative to fastframes directory
  output_path_histograms: "../output_histograms/" # Path to the output histograms relative to fastframes directory
  output_path_ntuples: "../output_ntuples/" # Path to the output ntuples relative to fastframes directory
  default_sumweights: "NOSYS" # Default sum of weights for the samples. This is used to calculate the scaling to the luminosity.
  default_event_weights: "weight_mc_NOSYS * weight_pileup_NOSYS * globalTriggerEffSF_NOSYS * weight_leptonSF_tight_NOSYS * weight_jvt_effSF_NOSYS  * weight_ftag_effSF_GN2v01_Continuous_NOSYS"
  default_reco_tree_name: "reco" # Name of the reco tree in the input files.
  xsection_files: # Location of the cross-section, k-factor, filter-efficiency medatada split per campaign.
    - files: ["/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PMGTools/PMGxsecDB_mc23.txt"]
      campaigns: ["mc23a", "mc23d", "mc23e"]
  luminosity: # Luminosity for the different campaigns.
    mc23a: 29049.3
    mc23d: 27239.9
  automatic_systematics: False # Run over all systematics found in the input files.
  nominal_only: True # Run with/without systematics.
  number_of_cpus: 4 # CPU cores to use for the analysis.
  use_region_subfolders: True # Save the histograms in subfolders per region.
```
</div>

When you run the code you need to point to this configuration file:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Run over ttll sample:
python3 python/FastFrames.py -c ../ttZconfig.yaml --step h --samples ttll

# or run over all samples:
python3 python/FastFrames.py -c ../ttZconfig.yaml --step h
```
</div>

This will create `ttll.root` file under the `output_histograms` directory. If you inspect the output file, you will see the following structure:

<img src="../image1.png" alt="Architecture" width="600"/>

This structure corresponds to what is specified under the `regions` and `variables` blocks in the `ttZconfig.yaml` file:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

regions: # All the regions (defined by a selection criteria) to be used in the analysis.
  - name: all_loose_muon # This postfix will be appended to every variable.
    selection: "ROOT::VecOps::Sum(mu_select_loose_NOSYS) == mu_select_loose_NOSYS.size()" # Selection string, needs to be valid C++ syntax.
    variables: &common_variables # Here you list the variables. Note the usage of the anchor (&). This allows you to reuse the same variables in other regions.
      - name: "mu_pt" # Name of the variable. This will result in 'mu_pt_all_loose_muon'.
        title: "Muon p_{T} [GeV]; p_{T} [GeV]; Events"
        definition: "mu_pt_NOSYS"
        binning:
          min: 0
          max: 200000
          number_of_bins: 10

  - name: all_tight_muon # Another region with a different selection.
    selection: "ROOT::VecOps::Sum(mu_select_tight_NOSYS) == mu_select_tight_NOSYS.size()"
    variables: *common_variables # Reuse the common variables defined above.

```
</div>

If you instead run over all systematics present in the input files with:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
  automatic_systematics: True
  nominal_only: False # Run with/without systematics.
```
</div>

you will instead see the following output structure (in addition to the increased run time):

<img src="../image2.png" alt="Architecture" width="600"/>

Finally, in the `samples` block you define the list of MC/Data samples used in the analysis:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

samples: # All the samples to be used in the analysis.
  - name: "data" # Name given to the sample.
    dsids: [0] # For data, this is always 0.
    campaigns: ["2022"] # The corresponding campaing or campaigns.
    simulation_type: "data" # Type of simulation.

  - name: "ttll" # Another sample.
    dsids: [522028, 522032] # List of DSIDs for the sample.
    campaigns: ["mc23a"]
    simulation_type: "fullsim" # For MC samples we have a different simulation type.
```
</div>

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

A comprehensive list of options that can be used to steer FastFrames can be found <a href="https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/config/">here.</a>
</div>

### 1.2 Changing the configuration file:

One can use the configuration file to add new variables without having to write C++ code. However, we will see that for more complicated analyses writing code provides greater flexibility. This is explained in `Sec. 2.0`.

#### 1.2.1 Adding more regions, defining new variables and adding more histograms:

To add a new variable one can use the `define_custom_columns` option:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
  define_custom_columns: # You can define new variables here. Use valid C++ syntax.
      - name: "nMuons_NOSYS" # Count the number of muons with a pT > 7 GeV and which pass the tight selection.
        definition: "mu_pt_NOSYS[mu_pt_NOSYS >= 7000 && mu_select_tight_NOSYS==true].size()"
```
</div>

One can then proceed to add a histogram for this variable in one of the existing regions:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

regions: # All the regions (defined by a selection criteria) to be used in the analysis.
  - name: all_loose_muon # This postfix will be appended to every variable.
    selection: "ROOT::VecOps::Sum(mu_select_loose_NOSYS) == mu_select_loose_NOSYS.size()" # Selection string, needs to be valid C++ syntax.
    variables: &common_variables # Here you list the variables. Note the usage of the anchor (&). This allows you to reuse the same variables in other regions.
      - name: mu_pt # Name of the variable. This will result in 'mu_pt_all_loose_muon'.
        title: "Muon p_{T} [GeV]; p_{T} [GeV]; Events"
        definition: mu_pt_NOSYS
        binning:
          min: 0
          max: 200000
          number_of_bins: 100
      - name: "n_muons" # New variable here!
        type: unsigned long
        title : "Number of Muons ; nMuons ; Events"
        definition: nMuons_NOSYS
        binning:
          min: -0.5
          max: 7.5
          number_of_bins: 8
```
</div>

Additionally, one can add a new region using this variable (notice how we use anchor expressions to re-use variables):

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

regions: # All the regions (defined by a selection criteria) to be used in the analysis.
  - name: 4mu
    selection: "nMuons_NOSYS == 4"
    variables: *common_variables # Reuse the common variables defined above.
```
</div>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 1</h4>

Add two variables: the number of tight electrons, and the number of jets passing the <code>jet_select_baselineJvt_NOSYS</code> selection.

Add two more regions: a four-electron region and a two-muon + two-electron region. Re-use the same variables.
</div>

<details>
<summary>Solution...</summary>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
  define_custom_columns:
    - name: nMuons_NOSYS
      definition: mu_pt_NOSYS[mu_pt_NOSYS >= 7000 && mu_select_tight_NOSYS==true].size()
    - name: nElectrons_NOSYS
      definition: el_pt_NOSYS[el_pt_NOSYS >= 7000 && el_select_tight_NOSYS==true].size()
    - name: nJets_NOSYS
      definition: jet_pt_NOSYS[jet_pt_NOSYS >= 25000 && jet_select_baselineJvt_NOSYS].size()

regions: # All the regions (defined by a selection criteria) to be used in the analysis.
  - name: all_loose_muon # This postfix will be appended to every variable.
    selection: "ROOT::VecOps::Sum(mu_select_loose_NOSYS) == mu_select_loose_NOSYS.size()" # Selection string, needs to be valid C++ syntax.
    variables: &common_variables # Here you list the variables. Note the usage of the anchor (&). This allows you to reuse the same variables in other regions.
      - name: mu_pt # Name of the variable. This will result in 'mu_pt_all_loose_muon'.
        title: "Muon p_{T} [GeV]; p_{T} [GeV]; Events"
        definition: mu_pt_NOSYS
        binning:
          min: 0
          max: 200000
          number_of_bins: 100
      - name: "n_muons"
        type: unsigned long
        title : "Number of Muons ; nMuons ; Events"
        definition: nMuons_NOSYS
        binning:
          min: -0.5
          max: 7.5
          number_of_bins: 8
      - name: "n_electrons"
        type: unsigned long
        title : "Number of Electrons ; nElectrons ; Events"
        definition: nElectrons_NOSYS
        binning:
          min: -0.5
          max: 7.5
          number_of_bins: 8
      - name: "n_jets"
        type: unsigned long
        title : "Number of Jets ; nJets ; Events"
        definition: nJets_NOSYS
        binning:
          min: -0.5
          max: 7.5
          number_of_bins: 8

  - name: all_tight_muon # Another region with a different selection.
    selection: "ROOT::VecOps::Sum(mu_select_tight_NOSYS) == mu_select_tight_NOSYS.size()"
    variables: *common_variables # Reuse the common variables defined above.

  - name: 4mu
    selection: "nMuons_NOSYS == 4"
    variables: *common_variables # Reuse the common variables defined above.

  - name: 4e
    selection: "nElectrons_NOSYS == 4"
    variables: *common_variables

  - name: 2e2mu
    selection: "nElectrons_NOSYS == 2 && nMuons_NOSYS == 2"
    variables: *common_variables

```
</div>


</details>

#### 1.2.2 Producing ntuples (for example to use as input for ML training):

FastFrames allows you to produce ntuples instead of histograms by specifying the `--step` option as `n` when running the framework. This is useful for creating datasets that can be used for machine learning, further slimming your ntuples or augmenting them.

To produce ntuples, ensure that the `output_path_ntuples` is correctly defined in the `general` block of your configuration file:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
  output_path_ntuples: "../output_ntuples/" # Path to the output ntuples relative to fastframes directory
```
</div>

Then, run the framework with the following command:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Produce ntuples
python3 python/FastFrames.py -c ../ttZconfig.yaml --step n --samples ttll
```
</div>

This will create ntuple root files in the directory specified by `output_path_ntuples`. The file will contain what is specified in the `ntuples` block:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

ntuples: # Use this block to define the ntuples to be created.
  regions: # Only events passing the selection of one of the regions will be saved in the ntuple.
    - 4mu
    - 4e
    - 2e2mu
  #selection: "nJets_NOSYS == 3" # You can alternatively define a selection for the ntuples.
  branches: # These branches will be saved in the ntuple.
    - .*_pt_NOSYS # You can use regular expressions. This will select e, mu and jet pt.
    - jet_eta
    - jet_phi
    - mu_eta
    - mu_phi
    - el_eta
    - el_phi
```
</div>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 2</h4>

Store the pT of electrons, muons and jets in GeV.
</div>

<details>
<summary>Solution...</summary>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
  define_custom_columns: # You can define new variables here. Use valid C++ syntax.
    - name: mu_pt_gev_NOSYS
      definition: mu_pt_NOSYS/1000.0 # Convert to GeV.
    - name: el_pt_gev_NOSYS
      definition: el_pt_NOSYS/1000.0
    - name: jet_pt_gev_NOSYS
      definition: jet_pt_NOSYS/1000.0

ntuples: # Use this block to define the ntuples to be created.
  regions: # Only events passing the selection of one of the regions will be saved in the ntuple.
    - 4mu
    - 4e
    - 2e2mu
  #selection: "nJets_NOSYS == 3" # You can alternatively define a selection for the ntuples.
  branches: # These branches will be saved in the ntuple.
    #- .*_pt_NOSYS # You can use regular expressions. This will select e, mu and jet pt.
    - jet_eta
    - jet_phi
    - mu_eta
    - mu_phi
    - el_eta
    - el_phi
    - .*_pt_gev_NOSYS # This will select e, mu and jet pt in GeV.

```
</div>


</details>


<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

For additional information on how to configure and use ntuples, refer to the <a href="https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/config/#ntuples-block-settings">FastFrames documentation</a>.
</div>

## 2.0 Using a custom class in FastFrames:

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note: only if you completed the previous sections.</h4>

This is the starting point for the workshop tutotorial. If you have followed the previous sections, you need to clean the previous exercises. To do this:

```bash
# Take all files to the initial state. Run from FFTutorial/ level.
git restore .

# Checkout the starting point for the live tutorial.
git checkout part-two
git submodule update --init --recursive
```

Once you do this, you can skip and go to <code>Section 2.1.3</code>.
</div>

### 2.1 Install and configure:

First, we need to download the tutorial code, install `FastFrames` and install the custom class.

#### 2.1.1 Download tutorial code:

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

We assume that you are running this tutorial inside an <code>lxplus</code> machine, located at <code>/eos/user/your_username_first_letter/your_username</code>.
</div>

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Clone the tutorial repository Create a directory to store your work
git clone --branch part-two ssh://git@gitlab.cern.ch:7999/dbaronmo/fftutorialtopws2025.git FFTutorial --recurse-submodules
cd FFTutorial

# Setup environment
setupATLAS --quiet && lsetup git && asetup StatAnalysis,0.5.3
```
</div>

#### 2.1.2 Install FastFrames:

Let's compile and install FastFrames:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Configure, compile, install
cmake -S fastframes -B build_ff -DCMAKE_INSTALL_PREFIX=install_ff
cmake --build build_ff -j4 --target install

# Setup environment
source build_ff/setup.sh

```
</div>

#### 2.1.3 Install the custom class:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Configure, compile, install
cmake -S FastFramesCustomClassTemplate -B build_custom -DCMAKE_PREFIX_PATH=$PWD/install_ff -DCMAKE_INSTALL_PREFIX=install_custom
cmake --build build_custom -j4 --target install

# Setup environment
source build_custom/setup.sh

```
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note: reminder to build the metadata.</h4>

To be able to run FastFrames you need to build the samples metadata. This is explained in <code>Section 0.1</code>. You need to:

```bash
# Produce the input files metadata
cd fastframes
python3 python/produce_metadata_files.py --root_files_folder /eos/atlas/atlascerngroupdisk/phys-top/Top_Group_Tutorials/Tutorial_2025/FastFrames/ --output_path ../metadata/
```
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

Once FF and the custom class are compiled and installed you only need to re-load your environment.
```bash
setupATLAS --quiet && lsetup git && asetup StatAnalysis,0.5.3
source build_ff/setup.sh
source build_custom/setup.sh
```
</div>

### 2.2 Add new variables:

The main point of a custom class is to be able to make object manipulations thorugh C++ code. This gives more flexibiliy to the analyser. For example in `Section 1.2.1` we learnt how to count the number of muons with a pT >= 7 GeV and that pass the tight selection. However, to do the same for electrons and jets we ended up writing the same expressions again.

FastFrames can be extended with a "custom class" where we can write a single function and re-use it. The custom class [skeleton source code](https://gitlab.cern.ch/atlas-amglab/FastFramesCustomClassTemplate/-/blob/main/MyCustomFrame/MyCustomFrame.h?ref_type=heads) has methods that allow you to define variables for histograming, ntupling and only for the truth variables.

The basic structure of the custom class code is:
```
- FastFramesCustomClassTemplate/
  - MyCustomFrame/ -------- This is the name of the class.
    - MyCustomFrame.h ----- Header file where the class declarations live.
  - Root/ ----------------- Directory containing the class implementation.
    - MyCustomFrame.cc ---- This is where the variable definitions go!
```

First, to use the custom class we need to add the `custom_frame_name` option to the general block.

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
  custom_frame_name: "MyCustomFrame" # Name of the custom class.
```
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

The name of the custom class can be changed using the provided <code>renameFiles.sh</code> script.
DO NOT do this for the tutorial!
</div>

Now, we can add the number of jets passing some selections via the custom code. To add a custom variable that is **Systematics dependent** we use the `MainFrame::systematicDefine` method. We need to pass:
- The `mainNode` parameter,
- the variable name (it needs to be postfixed by `_NOSYS`),
- the function that will define the variable,
- and the columns that the previous function uses as parameters.

For the number of jets case, the following code needs to be added to the `ROOT::RDF::RNode MyCustomFrame::defineVariables` method in `MyCustomFrame.cc`:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

// Jets
// Lambda function to define the number of jets above 25 GeV.
auto numberOfJets25 = [](const ROOT::VecOps::RVec<float>& ptV,
  const ROOT::VecOps::RVec<char>& selection) {
    return DefineHelpers::numberOfObjects(ptV, 25000, selection);
};

LOG(INFO) << "Adding variable: n_jets_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "n_jets_NOSYS",
                                        numberOfJets25,
                                        {"jet_pt_NOSYS", "jet_select_baselineJvt_NOSYS"});
```
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

Notice how we made use of the helper function to count the number of objects that FastFrames already provides in <code>DefineHelpers.h</code>. For more information please read the <a href="https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/helpers/">documentation here</a>.
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

If a variable is not systematic dependent, one can instead of using <code>mainNode = MainFrame::systematicDefine(mainNode, ...)</code> use <code>mainNode = mainNode.Define(..)</code>.

See the <a href="https://root.cern/doc/v628/classROOT_1_1RDF_1_1RInterface.html#a4698601205a55ac49279150d56fc904f"> documentation here</a>.
</div>

Now, one can add a region in the `config.yaml` file, use this variable for a selection and plot it.

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

regions:
  - name: 2jp
      selection: "n_jets_NOSYS >= 2"
      variables: &2j_variables # This allows you to reuse the same variables in other regions.
        - name: n_jet
          type: unsigned long
          title : "Number of Jets ; nJets ; Events"
          definition: n_jets_NOSYS
          binning:
            min: -0.5
            max: 7.5
            number_of_bins: 8
```
</div>

But first, we need to re-compile the custom class, this needs to be done everytime we add/change the source code:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Re-compile the custom class.
cmake --build build_custom -j4 --target install
```
</div>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 3</h4>

<p>Add a function to count the number of tight muons/electrons with pT &gt;= 7 GeV.</p>
<p>Add the <code>n_muons_NOSYS</code> and <code>n_electrons_NOSYS</code> variables inside <code>MyCustomFrame::defineVariables</code> using the previously created function.</p>
</div>

<details>
<summary>Solution...</summary>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

// Muons
  // Lambda function to define the number of leptons above 7 GeV.
  auto numberOfLeptons7 = [](const ROOT::VecOps::RVec<float>& ptV,
    const ROOT::VecOps::RVec<char>& selection) {
      return DefineHelpers::numberOfObjects(ptV, 7000, selection);
  };

  LOG(INFO) << "Adding variable: n_muons_NOSYS" << std::endl;
  mainNode = MainFrame::systematicDefine(mainNode,
                                         "n_muons_NOSYS",
                                         numberOfLeptons7,
                                         {"mu_pt_NOSYS", "mu_select_tight_NOSYS"});

  // Electrons
  LOG(INFO) << "Adding variable: n_electrons_NOSYS" << std::endl;
  mainNode = MainFrame::systematicDefine(mainNode,
                                         "n_electrons_NOSYS",
                                         numberOfLeptons7,
                                         {"el_pt_NOSYS", "el_select_tight_NOSYS"});
```
</div>

</details>

FastFrames can also assist with the creation of `TLorentzVector` (TLV) containers from the individual particles `pT`, `eta`, `phi`, `e` containers. You just need to add the following line to the general block:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
   create_tlorentz_vectors_for: ["jet", "el", "mu"] # Create TLorentzVectors for the specified objects.
```
</div>

Once this is done, one can create pT-sorted containers using `DefineHelpers::sortedPassedVector`. For jets this would look like:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

// Specify the type for the pT sorting functions
using sorted_particle_1sel = ROOT::VecOps::RVec<TLV>(*)(const ROOT::VecOps::RVec<TLV>&,const ROOT::VecOps::RVec<char>&);
// Jets
LOG(INFO) << "Adding variable: sorted_jet_TLV_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "sorted_jet_TLV_NOSYS",
                                        static_cast<sorted_particle_1sel>(DefineHelpers::sortedPassedVector),
                                        {"jet_TLV_NOSYS", "jet_select_baselineJvt_NOSYS"});
```
</div>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 4</h4>

<ul>
  <li>Make the previously described changes.</li>
  <li>Add also pT-sorted vectors for muons and electrons.</li>
  <li>Add a function for pT-sorted b-jets passing the 85% working point.</li>
</ul>
</div>

<details>
<summary>Solution...</summary>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

// Muons
LOG(INFO) << "Adding variable: sorted_mu_TLV_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "sorted_mu_TLV_NOSYS",
                                        static_cast<sorted_particle_1sel>(DefineHelpers::sortedPassedVector),
                                        {"mu_TLV_NOSYS", "mu_select_tight_NOSYS"});

// Electrons
LOG(INFO) << "Adding variable: sorted_el_TLV_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "sorted_el_TLV_NOSYS",
                                        static_cast<sorted_particle_1sel>(DefineHelpers::sortedPassedVector),
                                        {"el_TLV_NOSYS", "el_select_tight_NOSYS"});

// b-tagged jets.
using sorted_particle_2sel = ROOT::VecOps::RVec<TLV>(*)(const ROOT::VecOps::RVec<TLV>&,const ROOT::VecOps::RVec<char>&, const ROOT::VecOps::RVec<char>&);
LOG(INFO) << "Adding variable: sorted_bjet_TLV_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "sorted_bjet_TLV_NOSYS",
                                        static_cast<sorted_particle_2sel>(DefineHelpers::sortedPassedVector),
                                        {"jet_TLV_NOSYS", "jet_select_baselineJvt_NOSYS","jet_GN2v01_FixedCutBEff_85_select"});

```
</div>

</details>

Sometimes the functions that we use to define variables are not simple and they extend for more than a few lines. Writing long lambda functions in `MyCustomFrame.cc` can be confusing. In this part we show how functions can be defined in separated header/source files.

One can create two files: `Variables.h` and `Variables.cc` and include them in the custom class structure like:

```
- FastFramesCustomClassTemplate/
  - MyCustomFrame/ -------- This is the name of the class.
    - MyCustomFrame.h ----- Header file where the class declarations live.
    - Variables.h --------- Header file for the function declarations.
  - ROOT/ ----------------- Directory containing the class implementation.
    - MyCustomFrame.cc ---- This is where the variable definitions go!
    - Variables.cc -------- This is where the function definitions go.
```

A good template (it already includes an example function) for these files is:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// Variables.h

# pragma once

#include <string>
#include <vector>
#include "ROOT/RVec.hxx"
#include "Math/Vector4D.h"
#include <Math/VectorUtil.h>

using TLV = ROOT::Math::PtEtaPhiEVector;

namespace ttZ {
  /**
   * @brief Function to get the sum of the charges of the leptons.
   * @param chargeV Vector of charges of the leptons.
   * @return float Sum of the charges.
   */
  float sumOfCharges( const ROOT::VecOps::RVec<float>& chargeV);
}

// Variables.cc

#include "MyCustomFrame/Variables.h"
#include "FastFrames/DefineHelpers.h"

#include <string>
#include <vector>
#include "ROOT/RVec.hxx"
#include <Math/VectorUtil.h>

namespace ttZ {
  float sumOfCharges( const ROOT::VecOps::RVec<float>& chargeV) { return ROOT::VecOps::Sum(chargeV); }
}
```
</div>

At this point, if one wants to create a variable that holds the charges of leptons that pass a tight selection, have a pT >= 7 GeV and are pT-sorted, once can add:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// Variables.h

namespace ttZ {
  /**
   * @brief Function to get the pt-sorted vector of charges of the leptons that pass a selection.
   * And have a pT > 7 GeV.
   * @param chargeV Vector of charges of the leptons.
   * @param ptV Vector of pT of the leptons.
   * @param selection Vector of selection flags for the leptons.
   * @return ROOT::VecOps::RVec<float> Vector of charges of the leptons that pass the selection, sorted by pt.
   */
  ROOT::VecOps::RVec<float> sortedPassedChargeVector7(
      const ROOT::VecOps::RVec<float>& chargeV,
      const ROOT::VecOps::RVec<float>& ptV,
      const ROOT::VecOps::RVec<char>& selection);
}

// Variables.cc

namespace ttZ {
  ROOT::VecOps::RVec<float> sortedPassedChargeVector7(
      const ROOT::VecOps::RVec<float>& chargeV,
      const ROOT::VecOps::RVec<float>& ptV,
      const ROOT::VecOps::RVec<char>& selection){

      // Create a vector of decisions to test pT > 7 GeV.
      ROOT::VecOps::RVec<char> gt7 = ptV > 7000;

      // Get the pt-sorted indices of the leptons that pass the selection
      auto passedIndices = DefineHelpers::sortedPassedIndices(ptV, gt7 ,selection);
      // Create a vector to hold the sorted charges
      ROOT::VecOps::RVec<float> sortedCharges;

      // Loop over the passed indices and fill the sorted charges vector
      for (const auto& index : passedIndices) {
          sortedCharges.push_back(chargeV[index]);
      }

      return sortedCharges;
  }

  // MyCustomFrame.cc

  #include "MyCustomFrame/Variables.h"

  // Lepton charges
  LOG(INFO) << "Adding variable: sorted_mu_charge_NOSYS" << std::endl;
  mainNode = MainFrame::systematicDefine(mainNode,
                                         "sorted_mu_charge_NOSYS",
                                         ttZ::sortedPassedChargeVector7,
                                         {"mu_charge", "mu_pt_NOSYS", "mu_select_tight_NOSYS"});

  LOG(INFO) << "Adding variable: sorted_el_charge_NOSYS" << std::endl;
  mainNode = MainFrame::systematicDefine(mainNode,
                                         "sorted_el_charge_NOSYS",
                                         ttZ::sortedPassedChargeVector7,
                                         {"el_charge", "el_pt_NOSYS", "el_select_tight_NOSYS"});
}
```
</div>

Since we added header and source files, we not only need to re-compile our code but also run the `CMake` configuration again. To do this:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Re-configure and re-compile the custom class after adding header/source files.
cmake -S FastFramesCustomClassTemplate -B build_custom -DCMAKE_PREFIX_PATH=$PWD/install_ff -DCMAKE_INSTALL_PREFIX=install_custom
cmake --build build_custom -j4 --target install
```
</div>


<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 5</h4>

<ul>
  <li>Make the previously described changes.</li>
  <li>Add a function that classifies the events into regions. It must return a string which is one of the following options: <strong>4e</strong>, <strong>4mu</strong>, <strong>2e2mu</strong>, <strong>mu3e</strong>, <strong>e3mu</strong>, or <strong>other</strong>. The regions must satisfy:
    <ul>
      <li>n_electrons + n_muons = 4</li>
      <li>The sum of the charges must be zero</li>
      <li>The leading lepton must have a pT &gt;= 27 GeV</li>
    </ul>
  </li>
  <li>Add a function for pT-sorted b-jets passing the 85% working point.</li>
  <li>Add these different regions to the configuration. Add histograms for the number of muons, electrons, and b-jets in every region.</li>
  <li>Split further into regions with one b-tagged jet (1b) and two or more b-jets (2bp). For these regions, add the histograms with the pT of the leading and sub-leading b-jets.</li>
</ul>
</div>

<details>
<summary>Solution...</summary>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

// Define the region name
LOG(INFO) << "Adding variable: region_name_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "region_name_NOSYS",
                                        ttZ::regionName,
                                        {"n_muons_NOSYS", "n_electrons_NOSYS",
                                          "sorted_el_charge_NOSYS", "sorted_mu_charge_NOSYS",
                                          "sorted_el_TLV_NOSYS", "sorted_mu_TLV_NOSYS"});

// Number of b-jets with pT > 25 GeV
auto numberOfBJets25 = []( const ROOT::VecOps::RVec<TLV>& tlv){
    std::size_t nBJets = 0;
    for (const auto& jet : tlv) {
        if (jet.Pt() > 25000) nBJets++;
    }
    return nBJets;
};

LOG(INFO) << "Adding variable: n_bjets_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "n_bjets_NOSYS",
                                        numberOfBJets25,
                                        {"sorted_bjet_TLV_NOSYS"});

// Variables.h

/**
 * @brief Function to determine the region based on the sum of the charges,
 * the pT of the leading lepton, and the number of leptons of each type.
 * @param nMuons Number of muons.
 * @param nElectrons Number of electrons.
 * @param elChargeV Vector of charges of the electrons.
 * @param muChargeV Vector of charges of the muons.
 * @param elTLV Vector of TLorentzVectors of the electrons.
 * @param muTLV Vector of TLorentzVectors of the muons.
 * @return std::string Region name.
 */
std::string regionName(
    std::size_t nMuons,
    std::size_t nElectrons,
    const ROOT::VecOps::RVec<float>& elChargeV,
    const ROOT::VecOps::RVec<float>& muChargeV,
    const ROOT::VecOps::RVec<TLV>& elTLV,
    const ROOT::VecOps::RVec<TLV>& muTLV);

// Variables.cc

std::string regionName(
      std::size_t nMuons,
      std::size_t nElectrons,
      const ROOT::VecOps::RVec<float>& elChargeV,
      const ROOT::VecOps::RVec<float>& muChargeV,
      const ROOT::VecOps::RVec<TLV>& elTLV,
      const ROOT::VecOps::RVec<TLV>& muTLV) {

          // Get the sum of the charges of the leptons.
          float sumOfChargesEl = sumOfCharges(elChargeV);
          float sumOfChargesMu = sumOfCharges(muChargeV);
          float sumOfCharges = sumOfChargesEl + sumOfChargesMu;

          // Get the leading lepton pT.
          float leadingMuonPt = nMuons > 0 ? muTLV.at(0).Pt() : 0.0f;
          float leadingElectronPt = nElectrons > 0 ? elTLV.at(0).Pt() : 0.0f;
          float leadingLeptonPt = std::max(leadingMuonPt, leadingElectronPt);

          if (nMuons + nElectrons != 4 || sumOfCharges != 0.0f || leadingLeptonPt < 27000) return "other";
          if (nMuons == 2 && nElectrons == 2) {
              // In this case, we need to check that one Z pair can be formed.
              if (sumOfChargesEl != 0.0f) return "other";
              return "2e2mu";
          }
          if (nMuons == 4) return "4mu";
          if (nElectrons == 4) return "4e";
          if (nMuons == 1 && nElectrons == 3) return "mu3e";
          if (nMuons == 3 && nElectrons == 1) return "e3mu";
          return "other";
  }

```

```yaml
# ttZconfig.yaml

regions:
  - name: 4mu
    selection: region_name_NOSYS == std::string("4mu")
    variables: &custom_class_variables
      - *2j_variables # Reuse the common variables defined above.
      - name: n_mu
        type: unsigned long
        title : "Number of Muons ; nMuons ; Events"
        definition: n_muons_NOSYS
        binning:
          min: 0
          max: 8
          number_of_bins: 8
      - name: n_el
        type: unsigned long
        title : "Number of Electrons ; nElectrons ; Events"
        definition: n_electrons_NOSYS
        binning:
          min: 0
          max: 8
          number_of_bins: 8
      - name: n_bjet
        type: unsigned long
        title : "Number of b-jets ; nBJets ; Events"
        definition: n_bjets_NOSYS
        binning:
          min: 0
          max: 8
          number_of_bins: 8

  - name: 4e
    selection: region_name_NOSYS == std::string("4e")
    variables: *custom_class_variables

  - name: 2e2mu
    selection: region_name_NOSYS == std::string("2e2mu")
    variables: *custom_class_variables

  - name: mu3e
    selection: region_name_NOSYS == std::string("mu3e")
    variables: *custom_class_variables

  - name: e3mu
    selection: region_name_NOSYS == std::string("e3mu")
    variables: *custom_class_variables # Reuse the common variables defined above.

  - name: 4mu1b
    selection: region_name_NOSYS == std::string("4mu") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2
    variables: &1b_varibles
      - *custom_class_variables # Reuse the common variables defined above.
      - name: bjet0_pt
        title : "B-jet 0 p_{T} [GeV]; p_{T} [GeV]; Events"
        definition: "sorted_bjet_TLV_NOSYS.at(0).Pt()"
        type: double
        binning:
          min: 0
          max: 200000
          number_of_bins: 10

  - name: 4mu2bp
    selection: region_name_NOSYS == std::string("4mu") && n_bjets_NOSYS >= 2 && n_jets_NOSYS >= 2
    variables: &2b_varibles
      - *1b_varibles
      - name: bjet1_pt
        title : "B-jet 1 p_{T} [GeV]; p_{T} [GeV]; Events"
        definition: "sorted_bjet_TLV_NOSYS.at(1).Pt()"
        type: double
        binning:
          min: 0
          max: 200000
          number_of_bins: 10

  - name: 4e1b
    selection: region_name_NOSYS == std::string("4e") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2
    variables: *1b_varibles

  - name: 4e2bp
    selection: region_name_NOSYS == std::string("4e") && n_bjets_NOSYS >= 2 && n_jets_NOSYS >= 2
    variables: *2b_varibles

  - name: 2e2mu1b
    selection: region_name_NOSYS == std::string("2e2mu") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2
    variables: *1b_varibles

  - name: 2e2mu2bp
    selection: region_name_NOSYS == std::string("2e2mu") && n_bjets_NOSYS >= 2 && n_jets_NOSYS >= 2
    variables: *2b_varibles

  - name: mu3e1b
    selection: region_name_NOSYS == std::string("mu3e") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2
    variables: *1b_varibles

  - name: mu3e2bp
    selection: region_name_NOSYS == std::string("mu3e") && n_bjets_NOSYS >= 2 && n_jets_NOSYS >= 2
    variables: *2b_varibles

  - name: e3mu1b
    selection: region_name_NOSYS == std::string("e3mu") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2
    variables: *1b_varibles

  - name: e3mu2bp
    selection: region_name_NOSYS == std::string("e3mu") && n_bjets_NOSYS >= 2 && n_jets_NOSYS >= 2
    variables: *2b_varibles

```

</div>

</details>

The last part of this section will show you how to add a custom histogram to your jobs. This is useful for example to track metadata: such as when was the code ran, who ran the code or attach a tag.

First, we will start defining some custom options that can be later read by our custom class. This is done in the general block, through the `custom_options` parameter:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

general:
   custom_options: # Use this to pass custom options to the custom class.
    metadata_histogram_name: metadata_ttZ
    run_tag: ttZ-v1
    runner: Diego
```
</div>

Now, we need to modify our `MyCustomFrame` class to:
- Add a new member to the classs to store the metadata (`std::unique_ptr<TH1F> m_metadata_histogram`).
- Add a new method (`MyCustomFrame::createMetadataHistogram`) to the class to:
  - read the data from `custom_options`,
  - create and configure the histogram.
- Modify `MyCustomFrame::init()` method (this is just called once in our job) to:
  - configure the histogram by calling `createMetadataHistogram()`,
  - save the histogram to the output via the FastFrames provided `MainFrame::addCustomHistogramsToOutput` method.

<details>
<summary>Clike here to see how this would look like...</summary>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.h

class MyCustomFrame : public MainFrame {
public:

  explicit MyCustomFrame() = default;

  virtual ~MyCustomFrame() = default;

  virtual void init() override final {MainFrame::init();
    // Configure the metadata histogram.
    this->createMetadataHistogram();

    // Save it to the output.
    // Get the internal histogram from the unique pointer.
    TH1F& histogram = *m_metadata_histogram;
    histogram.SetDirectory(0);
    this->addCustomHistogramsToOutput(histogram);
  }

  virtual ROOT::RDF::RNode defineVariables(ROOT::RDF::RNode mainNode,
                                           const std::shared_ptr<Sample>& sample,
                                           const UniqueSampleID& id) override final;

  virtual ROOT::RDF::RNode defineVariablesNtuple(ROOT::RDF::RNode mainNode,
                                                 const std::shared_ptr<Sample>& sample,
                                                 const UniqueSampleID& id) override final;

  virtual ROOT::RDF::RNode defineVariablesTruth(ROOT::RDF::RNode node,
                                                const std::string& truth,
                                                const std::shared_ptr<Sample>& sample,
                                                const UniqueSampleID& sampleID) override final;

  virtual ROOT::RDF::RNode defineVariablesNtupleTruth(ROOT::RDF::RNode node,
                                                      const std::string& treeName,
                                                      const std::shared_ptr<Sample>& sample,
                                                      const UniqueSampleID& sampleID) override final;

  void createMetadataHistogram() {
    // Get the custom options from the configuration.
    CustomOptions& options = m_config->customOptions();

    // Check if the histogram name is provided in the options.
    // If not, use a default name.
    std::string histogramName = "metadata_histogram_default";
    bool hasHistogramName = options.hasOption("metadata_histogram_name");
    if (hasHistogramName) {
      histogramName = options.getOption("metadata_histogram_name");
    } else {
      LOG(WARNING) << "No histogram name provided. Using default: " << histogramName << std::endl;
      LOG(WARNING) << "To provide a name for the histogram use the option: metadata_histogram_name ." << histogramName << std::endl;
    }

    // Create a map of the options.
    std::vector<std::pair<std::string,std::string>> settings_vector;
    for (const auto& key : options.getKeys()){
      if (key == "metadata_histogram_name") continue;
      settings_vector.emplace_back(key, options.getOption<std::string>(key));
    }

    // Create the histogram with the specified name and number of bins.
    m_metadata_histogram = std::make_unique<TH1F>(histogramName.c_str(), histogramName.c_str(), settings_vector.size(), 0, settings_vector.size());
    // Get the internal histogram from the unique pointer.
    TH1F& histogram = *m_metadata_histogram;
    for (size_t i = 0; i < settings_vector.size(); ++i) {
        const std::string label = settings_vector[i].first + " || " + settings_vector[i].second;
        histogram.GetXaxis()->SetBinLabel(i+1, label.c_str());
    }
  }
private:
  // Add one standalone histogram for metadata tracking.
  std::unique_ptr<TH1F> m_metadata_histogram;

  ClassDefOverride(MyCustomFrame, 1);

};
```
</div>

</details>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 6</h4>

Add the previously shown feature.
</div>

### 2.3 `truth` trees and variables:

When we want to interact with other trees different than `reco`, e.g. truth information stored in the `truth` or `particleLevel` trees, we need to add the `truth:` block for the relevant samples.

For example, to add histograms from the `truth` tree to our signal ttZ sample (`ttll`), we need to do:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

samples:
  - name: "ttll" # Another sample.
      dsids: [522024, 522028, 522032] # List of DSIDs for the sample.
      campaigns: ["mc23a"]
      simulation_type: "fullsim" # For MC samples we have a different simulation type.
      truth:
      - name: ttZ_partons
        truth_tree_name: "truth" # The name of the tree you want to inspect.
        event_weight: "weight_mc_NOSYS"
        pair_reco_and_truth_trees: True # This allows you to access the truth variables in the reco tree.
        variables: # Truth variables to be saved for the sample.
          - name: truth_b_pt
            title : "Truth B-jet p_{T} [GeV]; p_{T} [GeV]; Events"
            definition: "truth_b_TLV.Pt()"
            type: double
            binning:
              min: 0
              max: 200000
              number_of_bins: 10
          - name: truth_bbar_pt
            title : "Truth Bbar-jet p_{T} [GeV]; p_{T} [GeV]; Events"
            definition: "truth_bbar_TLV.Pt()"
            type: double
            binning:
              min: 0
              max: 200000
              number_of_bins: 10
```
</div>

This will add the `truth_b_pt` and `truth_bbar_pt` variables when running only over the the `ttll` sample. However, we first need to define the variables they depend on. These variables should be defined via the `MyCustomFrame::defineVariablesTruth` method.

Let's for instance define the TLVs for the b-jets coming from the t and tbar decays. This information is stored in the `truth` tree under the following variables:

```
Ttz_MC_b_afterFSR_from_t_eta                    Float_t         Dataset
Ttz_MC_b_afterFSR_from_t_m                      Float_t         Dataset
Ttz_MC_b_afterFSR_from_t_pdgId                  Int_t           Dataset
Ttz_MC_b_afterFSR_from_t_phi                    Float_t         Dataset
Ttz_MC_b_afterFSR_from_t_pt                     Float_t         Dataset
Ttz_MC_bbar_afterFSR_from_tbar_eta              Float_t         Dataset
Ttz_MC_bbar_afterFSR_from_tbar_m                Float_t         Dataset
Ttz_MC_bbar_afterFSR_from_tbar_pdgId            Int_t           Dataset
Ttz_MC_bbar_afterFSR_from_tbar_phi              Float_t         Dataset
Ttz_MC_bbar_afterFSR_from_tbar_pt               Float_t         Dataset
```

Since the variables needed to form the TLVs for the truth b/bar particles are **not** systematic-dependent, this is a good oportunity to use `Define` instead of `systematicDefine`. The code we need to add is:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

ROOT::RDF::RNode MyCustomFrame::defineVariablesTruth(ROOT::RDF::RNode node,
                                                     const std::string& /*sample*/,
                                                     const std::shared_ptr<Sample>& /*sample*/,
                                                     const UniqueSampleID& /*sampleID*/) {

  // Define the truth TLorentzVector for the b and bbar quarks
  LOG(INFO) << "Adding variable: truth_b_TLV" << std::endl;
  node = node.Define("truth_b_TLV",
                    ttZ::makeTruthTLV(5),
                    {"Ttz_MC_b_afterFSR_from_t_pt",
                    "Ttz_MC_b_afterFSR_from_t_eta",
                    "Ttz_MC_b_afterFSR_from_t_phi",
                    "Ttz_MC_b_afterFSR_from_t_m",
                    "Ttz_MC_b_afterFSR_from_t_pdgId"});

  LOG(INFO) << "Adding variable: truth_bbar_TLV" << std::endl;
  node = node.Define("truth_bbar_TLV",
                    ttZ::makeTruthTLV(-5),
                    {"Ttz_MC_bbar_afterFSR_from_tbar_pt",
                    "Ttz_MC_bbar_afterFSR_from_tbar_eta",
                    "Ttz_MC_bbar_afterFSR_from_tbar_phi",
                    "Ttz_MC_bbar_afterFSR_from_tbar_m",
                    "Ttz_MC_bbar_afterFSR_from_tbar_pdgId"});

  return node;
}

// Variables.h

/**
 * @brief Functor class to create a TLorentzVector for a truth particle that must have a given particle ID.
 * If the truth particle does not have the given ID, it returns a TLorentzVector with zero values.
 * @param particleID Particle ID of the truth particle.
 */
class makeTruthTLV {
  using TLV = ROOT::Math::PtEtaPhiMVector;
  public:
      makeTruthTLV(int particleID) : m_particleID(particleID) {}

      TLV operator() (float pt,
                  float eta,
                  float phi,
                  float m,
                  int pdgId) const {
          // Create a vector to hold the TLorentzVectors
          TLV tlv(0,0,0,0);

          // Check if the particle ID matches the given ID
          if (pdgId != m_particleID) return tlv;

          // If it matches, fill the TLorentzVector with the given values.
          tlv.SetCoordinates(pt, eta, phi, m);
          return tlv;
      }

  private:
      int m_particleID;
};
```
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

This time instead of using a function to define our variable we used a "Functor class". This is an abstraction that provides a storage (in this case <code>m_particleID</code>) and an overloaded <code>()</code> operator. This allows for more flexibility since we can "pass" parameters to the function and this makes it more flexible.
</div>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 7</h4>

Implement the previously described changes.
</div>

### 2.4 Per-sample decisions and matching truth and reco trees:

Sometimes you need to define a specific variable just for a given sample. One can do this via the `sample` parameter in the `MyCustomFrame::defineVariables` method.

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

If we wanted even further control (e.g. at the MC campaign or DSID level) we can use the tools explained in the <a href="https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/latest/tutorial/#uniquesample-based-decision-in-the-custom-class"> documentation</a>.
</div>

For example, let's say that only for the signal sample we want to perform a DeltaR matching between the previously created `truth_b_TLV` and the reco-level b-tagged jets in the `sorted_bjet_TLV_NOSYS` container.

First, to match the `reco` and `truth` trees (by default this is done via the `[runNumber, eventNumber]` map) we use the `pair_reco_and_truth_trees: True` inside the `truth:` block. Once that is done we can access the truth tree variables inside `MyCustomFrame::defineVariables` method. The code will look like:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

// Inside MyCustomFrame::defineVariables()
if (sample->name() == "ttll") {
  // Define the truth TLorentzVector for the b and bbar quarks
  // Note that to acces the truth variables you need to use the `truth` prefix.
  LOG(INFO) << "Adding variable: recotruth_b_TLV" << std::endl;
  mainNode = mainNode.Define("recotruth_b_TLV",
                            ttZ::makeTruthTLV(5),
                            {"truth.Ttz_MC_b_afterFSR_from_t_pt",
                            "truth.Ttz_MC_b_afterFSR_from_t_eta",
                            "truth.Ttz_MC_b_afterFSR_from_t_phi",
                            "truth.Ttz_MC_b_afterFSR_from_t_m",
                            "truth.Ttz_MC_b_afterFSR_from_t_pdgId"});

  // Match the truth b-jet to one of the reco b-jets.
  LOG(INFO) << "Adding variable: index_matched_b_NOSYS" << std::endl;
  mainNode = MainFrame::systematicDefine(mainNode,
                                          "index_matched_b_NOSYS",
                                          ttZ::recoIndexTruthBJet,
                                          {"sorted_bjet_TLV_NOSYS", "recotruth_b_TLV"});

}

// Variables.h

/**
 * @brief Function to get the index of the reco tagged b-jet that matches the truth b-jet.
 * Returns -1 if no match is found.
 * @param recoBJets Vector of TLorentzVectors of the reco b-jets.
 * @param truthBJet TLorentzVector of the truth b-jet.
 * @return int Index of the reco b-jet that matches the truth b-jet.
 */
int recoIndexTruthBJet(const ROOT::VecOps::RVec<TLV>& recoBJets,
                    const ROOT::Math::PtEtaPhiMVector& truthBJet);

// Variables.cc

int recoIndexTruthBJet(const ROOT::VecOps::RVec<TLV>& recoBJets,
    const ROOT::Math::PtEtaPhiMVector& truthBJet) {

    // Check the inputs are not empty
    if (recoBJets.size() == 0 || truthBJet.Pt() == 0) {
    return -1;
    }

    // Initialize the index to -1 (no match)
    int index = -1;
    double maxDeltaR = 0.4;

    // Loop over the reco b-jets
    for (std::size_t i = 0; i < recoBJets.size(); ++i) {
    // Calculate the deltaR between the reco b-jet and the truth b-jet
    double deltaR = ROOT::Math::VectorUtil::DeltaR(recoBJets[i], truthBJet);
    // Check if the deltaR is less than the maximum allowed
    if (deltaR < maxDeltaR) {
    index = i;
    maxDeltaR = deltaR;
    }
    }

    return index;
}
```
</div>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

# Add this variable to the 4mu1b region.
- name: reco_index_truth_b
  title : "Reco index of truth B-jet; Reco index; Events"
  definition: "index_matched_b_NOSYS"
  type: int
  binning:
    min: -1.5
    max: 3.5
    number_of_bins: 5

# The previous variable also needs to be added to the excluded variables from other samples!
exclude_variables: &truth_excluded
  - reco_index_truth_b
```
</div>


<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 8</h4>

Implement the previously described changes.
</div>

## 3.0 Machine learning:

In this part of the tutorial we will explain how machine learning (ML) models can be used in FastFrames. FastFrames offers two options:

- 1.0 Schedule the ML inference from the `ttZconfig.yaml` file.
- 2.0 Schedule the inference from the custom class by writting code.

 Method 1.0 applies for *simple enough* models. What is a simple enough model?
- Each input layer must accept a 1-D tensor (excluding the batch dimension) of type `float32`.
- The output layer that the user wants to access must produce a 1-D tensor (excluding the batch dimension) of type `float32`.

In other cases, you have to use method 2.0

For this tutorial we will implement a *simple enough* model. However, we will also show how method 2.0 is implemented for this same model.

The ML algorithm we will use has been trained to distinguish ttZ (signal) events from other physics processes (background). The inputs for the model are:

- Jet leading GN2v01 quantile score.
- Jet subleading GN2v01 quantile score.
- Invariant mass of the lepton pair which is considered to be from ttbar. The opposite sign, same flavor pair with `mll` closest to `mZ` is considered to come from the Z boson, the other two leptons are the ttbar pair.
- Missing transverse momentum.

The model outputs a score between zero and one. Two models are provided in the `onnxModels/` directory. One model is trained with even `eventNumber` events and the other with odd events.

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 9</h4>

Define the input variables and add them to the <strong>4mu1b</strong> region for the variables to be replicated in all the remaining regions.
</div>

<details>
<summary>Solution...</summary>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

// ttbar lepton pair invariant mass
LOG(INFO) << "Adding variable: ttbar_mass_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "ttbar_mass_NOSYS",
                                        ttZ::ttbarLeptonPairInvariantMass,
                                        {"region_name_NOSYS", "sorted_mu_TLV_NOSYS", "sorted_el_TLV_NOSYS",
                                        "sorted_mu_charge_NOSYS", "sorted_el_charge_NOSYS"});

// leading and subleading GN2 quantile scores.
// Step 1
// Lambda function to define the pt-sorted indices jets passing a pT >= 25 GeV selection,
// and the baseline JVT selection.
auto ptSortedGN2QuantileIndices = [](const ROOT::RVec<float>& pt,
  const ROOT::RVec<char>& selection1) {
    // Create a vector of decisions to test pT > 25 GeV.
    ROOT::RVec<char> gt25 = pt > 25000;
    // Do the logical AND with the selections
    auto selection = gt25 && selection1;
    return DefineHelpers::sortedPassedIndices(pt, selection);
};
LOG(INFO) << "Adding variable: ptsorted_jet25_indices_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "ptsorted_jet25_indices_NOSYS",
                                        ptSortedGN2QuantileIndices,
                                        {"jet_pt_NOSYS", "jet_select_baselineJvt_NOSYS"});

// Step 2
// Lambda function to extract the GN2 quantile scores of the jets with the previously defined indices.
auto GN2QuantileScores = [](const ROOT::RVec<int>& GN2Quantile,
  const ROOT::RVec<std::size_t>& indices) {
    return ROOT::VecOps::Take(GN2Quantile, indices);
};
LOG(INFO) << "Adding variable: GN2_quantile_scores_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "GN2_quantile_scores_NOSYS",
                                        GN2QuantileScores,
                                        {"jet_GN2v01_Continuous_quantile","ptsorted_jet25_indices_NOSYS"});

// Step 3
// Leading and subleading GN2 quantile scores
auto leadingGN2Quantile = [](const ROOT::RVec<int>& GN2QuantileScores) {
    // Check that the vector is not empty
    if (GN2QuantileScores.size() < 1) {
        return 1.0f;
    }
    return static_cast<float>(ROOT::VecOps::Max(GN2QuantileScores));
};
LOG(INFO) << "Adding variable: GN2_quantile_leading_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "GN2_quantile_leading_NOSYS",
                                        leadingGN2Quantile,
                                        {"GN2_quantile_scores_NOSYS"});

auto subleadingGN2Quantile = [](const ROOT::RVec<int>& GN2QuantileScores) {
    // Check that the vector has at least two elements
    if (GN2QuantileScores.size() < 2) {
        return 1.0f;
    }
    // Sort the scores
    ROOT::RVec<int> sortedScores = ROOT::VecOps::Sort(GN2QuantileScores);

    // Get the second largest score
    int subleadingScore = sortedScores.at(sortedScores.size() - 2);

    return static_cast<float>(subleadingScore);
};
LOG(INFO) << "Adding variable: GN2_quantile_subleading_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "GN2_quantile_subleading_NOSYS",
                                        subleadingGN2Quantile,
                                        {"GN2_quantile_scores_NOSYS"});

// Variables.h

/**
 * @brief Invariant mass of the ttbar lepton pair.
 * -1 if no pair is found.
 * @param regionName Name of the region.
 * @param muonTLV Vector of TLorentzVectors of the muons.
 * @param electronTLV Vector of TLorentzVectors of the electrons.
 * @param muonCharge Vector of charges of the muons.
 * @param electronCharge Vector of charges of the electrons.
 * @return float Invariant mass of the ttbar lepton pair.
 */
float ttbarLeptonPairInvariantMass(
    const std::string& regionName,
    const ROOT::VecOps::RVec<TLV>& muonTLV,
    const ROOT::VecOps::RVec<TLV>& electronTLV,
    const ROOT::VecOps::RVec<float>& muonCharge,
    const ROOT::VecOps::RVec<float>& electronCharge);

// Variables.cc

// Returns the indices from a list excluding the two given indices.
// Example: if the list is {0, 1, 2, 3} and the indices are 1 and 2,
// the function will return {0, 3}.
std::vector<int> getOtherIndices(int index1, int index2, std::size_t nLeptons) {

    // Check more than two leptons.
    if (nLeptons <= 2) {
        throw std::invalid_argument("There must be at least 3 leptons to get other indices");
    }

    // If any of the indices are -1, returns a vector of -1s.
    if (index1 == -1 || index2 == -1) {
        // Construct a vector with nLpeptons - 2 indices
        std::vector<int> indices;
        for (std::size_t i = 0; i < nLeptons-2; ++i) {
            indices.push_back(-1);
        }
        return indices;
    }

    // Form the vector of indices excluding the two given indices.
    std::vector<int> indices;
    for (std::size_t i = 0; i < nLeptons; ++i) {
        if (static_cast<int>(i) != index1 && static_cast<int>(i) != index2) {
            indices.push_back(i);
        }
    }
    return indices;
}

// Function to get the indices of the two leptons with an invariant mass closest to the Z boson mass.
std::vector<int> getClosestZPair(const ROOT::VecOps::RVec<TLV>& leptonTLV, const ROOT::VecOps::RVec<float>& leptonCharge){

    // Check that the inputs have the same size.
    if (leptonTLV.size() != leptonCharge.size()){
        throw std::invalid_argument("leptonTLV and leptonCharge must have the same size");
    }

    // Default values in case no pair is found.
    int Z1 = -1;
    int Z2 = -1;
    float mZ = 91000.0f; // Z boson mass in MeV.
    float minLLmass = 100*mZ; // Initialize to a large value.
    // Go pair by pair, check that is OS pair and calculate the invariant mass.
    // If the invariant mass is less than the current minimum, update the minimum and the indices.
    for (std::size_t i = 0; i < leptonTLV.size(); ++i) {
        for (std::size_t j = i + 1; j < leptonTLV.size(); ++j) {
            if (leptonCharge[i] * leptonCharge[j] > 0) continue;
            float llmass = ROOT::Math::VectorUtil::InvariantMass(leptonTLV[i], leptonTLV[j]);
            if (llmass < minLLmass) {
                minLLmass = llmass;
                Z1 = i;
                Z2 = j;
            }
        }
    }

    return {Z1, Z2};
}

// Function that given two indices, returns the invariant mass of the leptons at those indices.
float getMassPairByIndex(
    const ROOT::VecOps::RVec<TLV>& leptonTLV,
    const std::vector<int>& indices) {

        // Check that only two indices are given.
        if (indices.size() != 2) {
            throw std::invalid_argument("indices must have size 2");
        }
        // Check that the indices are valid.
        if (indices.at(0) == -1 || indices.at(1) == -1) {
            return 0.0f;
        }

        return ROOT::Math::VectorUtil::InvariantMass(leptonTLV[indices[0]], leptonTLV[indices[1]]);
    }

float ttbarLeptonPairInvariantMass(
    const std::string& regionName,
    const ROOT::VecOps::RVec<TLV>& muonTLV,
    const ROOT::VecOps::RVec<TLV>& electronTLV,
    const ROOT::VecOps::RVec<float>& muonCharge,
    const ROOT::VecOps::RVec<float>& electronCharge){

        // If region is other, return 0.0f
        if (regionName == "other") return 0.0f;

        // Check each region and calculate the invariant mass.
        // The workflow goes like this:
        // 1. Get the closest Z pair of leptons.
        // 2. Get the indices of the other two leptons.
        // 3. Get the invariant mass from those two indices.
        if (regionName == "4mu"){
            auto closestZPair = getClosestZPair(muonTLV, muonCharge);
            auto indices = getOtherIndices(closestZPair[0], closestZPair[1], 4);
            return getMassPairByIndex(muonTLV, indices);
        }
        if (regionName == "4e"){
            auto closestZPair = getClosestZPair(electronTLV, electronCharge);
            auto indices = getOtherIndices(closestZPair[0], closestZPair[1], 4);
            return getMassPairByIndex(electronTLV, indices);
        }
        if (regionName == "2e2mu"){
            float mZ = 91000.0f;
            auto mmMass = getMassPairByIndex(muonTLV, {0, 1});
            auto eeMass = getMassPairByIndex(electronTLV, {0, 1});
            bool mumuCloser = std::abs(mmMass - mZ) < std::abs(eeMass - mZ);
            return mumuCloser ? eeMass : mmMass;
        }
        if (regionName == "e3mu"){
            auto closestZPairMu = getClosestZPair(muonTLV, muonCharge);
            auto otherLeptonIndex = getOtherIndices(closestZPairMu[0], closestZPairMu[1], 3).at(0);
            if (otherLeptonIndex == -1) return 0.0f;
            return ROOT::Math::VectorUtil::InvariantMass(muonTLV[otherLeptonIndex], electronTLV[0]);
        }
        if (regionName == "mu3e"){
            auto closestZPairEl = getClosestZPair(electronTLV, electronCharge);
            auto otherLeptonIndex = getOtherIndices(closestZPairEl[0], closestZPairEl[1], 3).at(0);
            if (otherLeptonIndex == -1) return 0.0f;
            return ROOT::Math::VectorUtil::InvariantMass(electronTLV[otherLeptonIndex], muonTLV[0]);
        }
        return 0.0f;
    }

```

```yaml
# ttZconfig.yaml

regions:
  - name: 4mu1b
    selection: region_name_NOSYS == std::string("4mu") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2
    variables: &1b_varibles
      - *custom_class_variables # Reuse the common variables defined above.
      - name: bjet0_pt
        title : "B-jet 0 p_{T} [GeV]; p_{T} [GeV]; Events"
        definition: "sorted_bjet_TLV_NOSYS.at(0).Pt()"
        type: double
        binning:
          min: 0
          max: 200000
          number_of_bins: 10
      - name: reco_index_truth_b
        title : "Reco index of truth B-jet; Reco index; Events"
        definition: "index_matched_b_NOSYS"
        type: int
        binning:
          min: -1
          max: 3
          number_of_bins: 4
      - name: ttbar_mass
        title : "ttbar mass [GeV]; m_{tt} [GeV]; Events"
        definition: "ttbar_mass_NOSYS"
        type: float
        binning:
          min: 0
          max: 500000
          number_of_bins: 10
      - name: leading_GN2_quantile
        title : "Leading GN2 quantile; Leading GN2 quantile; Events"
        definition: "GN2_quantile_leading_NOSYS"
        type: float
        binning:
          min: 0
          max: 7
          number_of_bins: 7
      - name: subleading_GN2_quantile
        title : "Subleading GN2 quantile; Subleading GN2 quantile; Events"
        definition: "GN2_quantile_subleading_NOSYS"
        type: float
        binning:
          min: 0
          max: 7
          number_of_bins: 7
      - name: met_met
        title : "Missing ET [GeV]; E_{T}^{miss} [GeV]; Events"
        definition: "met_met_NOSYS"
        type: float
        binning:
          min: 0
          max: 300000
          number_of_bins: 15
```

</div>

</details>


With the input variables defined: `GN2_quantile_leading_NOSYS`, `GN2_quantile_subleading_NOSYS`, `ttbar_mass_NOSYS`, `met_met_NOSYS`, we can use the `simple_onnx_inference` block to configure the model inference.

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 10</h4>

Look at the FF ONNX documentation <a href="https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/latest/config/#simple_onnx_inference-block-settings">here</a> and write an appropriate <code>simple_onnx_inference</code> block. Add the model output variable to the <strong>4mu1b</strong> and the subsequent regions.
</div>

<details>
<summary>Solution...</summary>

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

simple_onnx_inference:
  - name: "ttZ_model" # Name of the model.
    model_paths: [ # Paths to the model files. You can use a list of paths.
      "../onnxModels/model_odd.onnx", # The expression deciding which model to use is:
      "../onnxModels/model_even.onnx" # eventNumber % 2 == 0 ? model_pos_0 : model_pos_1
    ]
    inputs:
      "input": ["GN2_quantile_leading_NOSYS", "GN2_quantile_subleading_NOSYS", "ttbar_mass_NOSYS", "met_met_NOSYS"]
    outputs:
      "output": ["ttZ_score_NOSYS"]

regions:
  - name: 4mu1b
      selection: region_name_NOSYS == std::string("4mu") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2
      variables: &1b_varibles
        - *custom_class_variables # Reuse the common variables defined above.
        - name: ttz_score
          title : "ttZ score; ttZ score; Events"
          definition: "ttZ_score_NOSYS"
          type: float
          binning:
            min: 0
            max: 1
            number_of_bins: 10
```

</div>

</details>

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

To find the name of the input and output tensors for a given ONNX model, you can use the <a href="https://netron.app"> Netron app</a>.
</div>


To finish with this section, we will show how to implement the ONNX model directly in the custom class without having to rely on the `simple_onnx_inference` block. First, we need to add to our custom class an object of type `ONNXWrapper`. The definition for this object can be found in the `FastFrames/ONNXWrapper.h` header file.

We add the object to the custom class and initialise it with our models:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.h

#include "FastFrames/ONNXWrapper.h"

class MyCustomFrame : public MainFrame {
public:
virtual void init() override final {MainFrame::init();
  // ML inference.
  m_onnx = std::make_unique<ONNXWrapper>("CustomClass_ttZ_model",std::vector<std::string>{"../onnxModels/model_odd.onnx", "../onnxModels/model_even.onnx"});
}

private:
// ML inference.
std::unique_ptr<ONNXWrapper> m_onnx;

};
```
</div>

Next, we need to define a new column that stores the output of running inference with the `m_onnx` object. We do it inside `MyCustomFrame::defineVariables` method.

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```cpp
// MyCustomFrame.cc

// This function is called for each event in the sample.
// It interacts with the ONNXWrapper class to perform inference.
// We need the input variables as paramerters to the function.
// We also need the pointer to the ONNXWrapper class.
auto MLInference = [this](float b1_quantile, float b2_quantile,
                          float ttbar_mass, float met, unsigned long long eventNumber) {

  // Prepare the inputs.
  ONNXWrapper::Inference infer = m_onnx->createInferenceInstance();
  std::vector<float> X = {b1_quantile, b2_quantile, ttbar_mass, met};
  std::vector<int64_t> shape = {1, static_cast<int64_t>(X.size())};
  infer.addInputs(X, shape);

  // Use the eventNumber % nModels to select the model to use for inference.
  unsigned int fold = m_onnx->getSessionIndex(eventNumber);

  // Run the inference.
  m_onnx->evaluate(infer, fold);

  // Extract the outputs.
  float* output = infer.getOutputs<float>("output");

  return *output;
};

LOG(INFO) << "Adding variable: ML_output_NOSYS" << std::endl;
mainNode = MainFrame::systematicDefine(mainNode,
                                        "ML_output_NOSYS",
                                        MLInference,
                                        {"GN2_quantile_leading_NOSYS", "GN2_quantile_subleading_NOSYS",
                                        "ttbar_mass_NOSYS", "met_met_NOSYS", "eventNumber"});
```
</div>

Notice how pass the `this` pointer to the function in order to have access to the `m_onnx` object. Additionally, we need to pass the `eventNumber` column since this will be used to define which model to apply to a certain event - this is done by checking the expression: `eventNumber % 2 = 0`.

Finally, we need to add the `ML_output_NOSYS` variable to one of our regions:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

regions:
  - name: 4mu1b
    selection: region_name_NOSYS == std::string("4mu") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2
    variables: &1b_varibles
      - *custom_class_variables # Reuse the common variables defined above.
      - name: ttz_score_onnx
        title : "ttZ score (ONNX); ttZ score (ONNX); Events"
        definition: "ML_output_NOSYS"
        type: float
        binning:
          min: 0
          max: 1
          number_of_bins: 100
```
</div>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 11</h4>

Implement the previously shown changes.
</div>

## 4.0 How to produce a TRExFitter configuration for plotting:

FastFrames can help with the creation of [TRExFitter](https://trexfitter-docs.web.cern.ch/trexfitter-docs/latest/) configurations. These files can be used to perform a fit or just plot our histograms. In this part of the tutorial we will show how to do the latter.

First, we create two additional regions in the configuration, these ones will be selected for plotting. In these two regions we add all the 4-lepton cases and separate by number of b-tagged jets. 

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

regions:
  - name: TREx4l1b
    selection: (region_name_NOSYS != std::string("other") && n_bjets_NOSYS == 1 && n_jets_NOSYS >= 2)
    variables: *1b_varibles

  - name: TREx4l2bp
    selection: (region_name_NOSYS != std::string("other") && n_bjets_NOSYS >= 2 && n_jets_NOSYS >= 2)
    variables: *2b_varibles
```
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

We cannot use many of the previously created regions with <code>TRExFitter</code> because their names start with a number, this is not supported. In part, we create the previous regions because of this and also to increase the number of events in the plots.
</div>


To create a configuration that can be run from `TRExFitter` we use the `produce_trexfitter_config.py` script. In this tutorial we will use the following parameters for the script:
- `-c` FastFrames configuration file.
- `-o` Output path and name for the generated configuration file.
- `--trex_settings` Path and name of an auxiliary configuration file where more TRExFitter-related options are defined.

The command that generates the `TRExFitter` configuration is:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Generate TRExFitter config. Run from fastframes/
python3 python/produce_trexfitter_config.py -c ../ttZconfig.yaml -o ../my_trex.config --trex_settings ../ttZ_trex_settings.yaml
```
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

The <code>produce_trexfitter_config.py</code> script does not support the <code>use_region_subfolders</code> option. You have to re-run the histogram production with the latter option set to <code>False</code> to be able to use the <code>TRExFitter</code> configuration generation.
</div>



Let's see how the `ttZ_trex_settings.yaml` configuration file looks like:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZ_trex_settings.yaml

selected_regions: ["TREx4l.*n_mu.*",
                  "TREx4l.*n_el.*",
                  "TREx4l.*n_jet.*",
                  "TREx4l.*n_bjet.*",
                  "TREx4l.*bjet0_pt.*",
                  "TREx4l.*bjet1_pt.*",
                  "TREx4l.*leading_GN2_quantile.*",
                  "TREx4l.*subleading_GN2_score.*",
                  "TREx4l.*met_met.*",
                  "TREx4l.*ttbar_mass.*",
                  "TREx4l.*ttz_score_onnx.*"] # This allows to filter which regions + variable pairs are used.

Job: # This corresponds to TREx settings.
  Label: ttZ
  CmeLabel: 13.6
  LumiLabel: 29.0

Fit: # This corresponds to TREx settings.
  FitType: "SPLUSB"
  FitRegion: "CRSR"
  POIAsimov: 1
  FitBlind: "True"

samples: # Sample settings. They need to match the ones defined in ttZconfig.yaml
    - name: "data"
      Color: 1
      Title: "Data"
      Type: "DATA"
    - name: "ttll"
      Color: 4 # You can define the sample colour, title and type.
      Title: "t#bar{t}Z"
      Type: "SIGNAL"
    - name: "tWZ"
      Color: 3
      Title: "tWZ"
      Type: "BACKGROUND"
    - name: "ZZ4ljj"
      Color: 2
      Title: "ZZ4ljj"
      Type: "BACKGROUND"
    - name: "ZZ4l"
      Color: 46
      Title: "ZZ4l"
      Type: "BACKGROUND"

Regions: # This block helps to overwrite options in specifc regions.
  - name: TREx4l.*
    Type: "VALIDATION" # For example this,
  - name: TREx4l.*ttz_score_onnx.*
    Type: "SIGNAL"
    Rebin: 10 # or this.
  - name: TREx4l.*bjet0_pt.*
    Type: "VALIDATION"
    Rebin: 10
  - name: TREx4l.*bjet1_pt.*
    Type: "VALIDATION"
    Rebin: 10
  - name: TREx4l.*met_met.*
    Type: "VALIDATION"
    Rebin: 12
  - name: TREx4l.*ttbar_mass.*
    Type: "VALIDATION"
    Rebin: 20

Systematics:
    - name: "Luminosity"
      Title: "Luminosity"
      Type: "OVERALL"
      OverallUp: 0.017
      OverallDown: -0.017
      Category: "Instrumental"

NormFactors: # We can attach normalisation factors to the samples.
    - name: "mu_signal"
      Title: "#mu(signal)"
      Nominal: 1
      Min: -100
      Max: 100
      Samples: "ttll"

    - name: "mu_bkg"
      Title: "#mu(bkg)"
      Nominal: 1
      Min: -100
      Max: 100
      Samples: "tWZ,ZZ4ljj,ZZ4l"
```

</div>

After the `produce_trexfitter_config.py` script is run, one will obtain a `my_trex.config` file which one can use to generate some plots. Let's create a separate folder (`Plots`) at the `FFTutorial` level to produce the plots:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Create Plots directory
mkdir Plots && cd Plots

# Run TRExFitter
trex-fitter -hwd ../my_trex.config
```
</div>

Now, you can inspect the `Plots/Plots/` directory and have a look at the produced histograms.

## Finished!

Congratulations for making it to the end of the tutorial!

If you want to see the full solution please do:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Get tutorial solution.
git clone --branch solution ssh://git@gitlab.cern.ch:7999/dbaronmo/fftutorialtopws2025.git FFTutorial --recurse-submodules

```
</div>


<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

<p>You can find more information about the following topics in these links:</p>
<ul>
  <li><a href="https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/">FastFrames documentation</a></li>
  <li><a href="https://topcptoolkit.docs.cern.ch">TopCPToolkit documentation</a></li>
  <li><a href="https://gitlab.cern.ch/atlas-amglab/fastframes/">FastFrames source code</a></li>
  <li><a href="https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/tutorial/">FastFrames main tutorial</a></li>
  <li><a href="https://mattermost.web.cern.ch/top-analysis/channels/histogramming-tool-rdataframe">FastFrames mattermost channel</a></li>
  <li><a href="https://batchdocs.web.cern.ch/tutorial/introduction.html">HTCondor ATLAS</a></li>
</ul>
</div>