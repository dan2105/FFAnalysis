# FastFrames tutorial: ATLAS Top Workshop 2025 CHANGE PLEASEMODIFYME

This tutorial will guide you through the setup of a FastFrames module to analyse the datasets previously produced in the `TopCPToolkit` tutorial.

We will adopt the following conventions:

- when some code is intended to be run on your terminal, you will see it on a red box,

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);">This should be run on your terminal...:</strong>

```bash
echo "Hello world!"
```
</div>
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

We assume that you are running this tutorial inside an `lxplus` machine, located at `/eos/user/<your_username_first_letter>/<your_username>`.
</div>

Setup the environment and download the code:
<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Clone the tutorial repository Create a directory to store your work
git clone --branch PLEASEMODIFYME ssh://git@gitlab.cern.ch:7999/dbaronmo/fftutorialtopws2025.git FFTutorial --recurse-submodules
cd FFTutorial


# Setup environment
setupATLAS --quiet && lsetup git && asetup StatAnalysis,0.5.3

```
</div>
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
</div>

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

To see installation instructions for different platforms and extendend details click [here](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/#how-to-checkout-and-compile-the-code).
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

Before doing any analysis, we first need to handle the case where in the `TopCPToolkit` workflow no events passed the selections. In this case, `TopCPToolkit` will produce a file without any trees (this can happen for background samples or real collision data where our signature is not present). To clean our datasets we use the `merge_empty_grid_files` script:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Clean input files
python3 python/merge_empty_grid_files.py --root_files_folder PLEASEMODIFYME

```
</div>
</div>

FastFrames also needs to read from a database that specifies the type of sample, file locations, sum of weights, etc. The code provides the `produce_metadata_files.py` script for this purpose. Let's use it:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Produce the input files metadata
cd fastframes
python3 python/produce_metadata_files.py --root_files_folder PLEASEMODIFYME --output_path ../metadata/

```
</div>
</div>

This creates a directory called `metadata` one level up in the directory hierarchy. This directory contains two files: `filelist.txt` and `sum_of_weights.txt`.

## 1.0 Run FastFrames:

To run the framework the application entry point is the python script `FastFrames.py`. One can see the supported options by doing:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Get running options for FastFrames
python3 python/FastFrames -h

```
</div>
</div>

The most important variables to define the run are:
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
# Get running options for FastFrames
python3 python/FastFrames.py -c ../ttZconfig.yaml --step h --samples ttZnunu

```
</div>
</div>

This will create `ttZnunu.root` file under the `output_histograms` directory. If you inspect the output file, you will see the following structure:

<img src="image1.png" alt="Architecture" width="600"/>

This structure corresponds to what we specified for `regions` anad `variables` in the `ttZconfig.yaml` file:

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

you will see this output structure (in addition to the increased run time):

<img src="image2.png" alt="Architecture" width="600"/>

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

A comprehensive list of options that can be used to steer FastFrames can be found [here](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/config/).
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
      - name: nMuons_NOSYS # Count the number of muons with a pT > 7 GeV and which pass the tight selection.
        definition: mu_pt_NOSYS[mu_pt_NOSYS >= 7000 && mu_select_tight_NOSYS==true].size()
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
          min: 0
          max: 8
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

Add two variables: the number of tight electrons and the number of jets passing the `jet_select_baselineJvt_NOSYS` selection.
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
          min: 0
          max: 8
          number_of_bins: 8
      - name: "n_electrons"
        type: unsigned long
        title : "Number of Electrons ; nElectrons ; Events"
        definition: nElectrons_NOSYS
        binning:
          min: 0
          max: 8
          number_of_bins: 8
      - name: "n_jets"
        type: unsigned long
        title : "Number of Jets ; nJets ; Events"
        definition: nJets_NOSYS
        binning:
          min: 0
          max: 8
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
python3 python/FastFrames.py -c ../ttZconfig.yaml --step n --samples ttZnunu
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

For additional information on how to configure and use ntuples, refer to the [FastFrames documentation](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/config/#ntuples-block-settings).
</div>

## 2.0 Using a custom FastFrames class:

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note: only if you completed the previous sections.</h4>

This is the starting point for the workshop tutotorial. If you have followed the previous sections, you need to clean the previous exercises. To do this:

```bash
# Take all files to the initial state. Run from FFTutorial/ level.
git restore .

# Checkout the starting point for the live tutorial.
git checkout PLEASEMODIFYME
```

Once you do this, you can skip and go to `Section 2.1.3`.
</div>

### 2.1 Install and configure:

First, we need to download the tutorial code, install `FastFrames` and install the custom class.

#### 2.1.1 Download tutorial code:

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

We assume that you are running this tutorial inside an `lxplus` machine, located at `/eos/user/<your_username_first_letter>/<your_username>`.
</div>

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Clone the tutorial repository Create a directory to store your work
git clone --branch PLEASEMODIFYME ssh://git@gitlab.cern.ch:7999/dbaronmo/fftutorialtopws2025.git FFTutorial --recurse-submodules
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
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

Once FF and the custom class are compiled and installed you only need to re-load your environment.
```bash
setupATLAS --quiet && lsetup git && asetup StatAnalysis,0.5.3
source build_ff/setup.sh
source build_custom/setup.sh
```
</div>

### 2.2 Add new variables:

The main point of a custom class is to be able to make object manipulations thorugh C++ code. This gives more flexibiliy to the analyser. For example in `Section 1.2.1` we learnt how to count the number of muons with a pT >= 7 GeV and that pass the tight selection. However, to do the same for electrons and jets we have to write the same expressions again. 

FastFrames can be extended with a "custom class" where we can write a single function and re-use it. The custom class [skeleton source code](https://gitlab.cern.ch/atlas-amglab/FastFramesCustomClassTemplate/-/blob/main/MyCustomFrame/MyCustomFrame.h?ref_type=heads) has methods that allow us to define variables for histograming, ntupling and only for the truth variables.

The basic structure of the custom class code is:
- FastFramesCustomClassTemplate/
  - MyCustomFrame/ ------------ This is the name of the class.
    - MyCustomFrame.h ----- Header file where the class declarations live.
  - ROOT/ ------------------------ Directory containing the class implementation.
    - MyCustomFrame.cc ---- This is where the variable definitions go! 

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

The name of the custom class can be changed using the provided `renameFiles.sh`. 
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

Notice how we made use of the helper function to count the number of objects that FastFrames already provides in `DefineHelpers.h`. For more information please red the [documentation here](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/helpers/).
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>

If our variable is **not systematic dependent** we can instead of using
```
mainNode = MainFrame::systematicDefine(mainNode, ...)
```
use 
```
mainNode = mainNode.Define(..)
```
see the [documentation here](https://root.cern/doc/v628/classROOT_1_1RDF_1_1RInterface.html#a4698601205a55ac49279150d56fc904f).
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
            min: 0
            max: 8
            number_of_bins: 8
```
</div>

We need to re-compile the custom class, this needs to be done everytime we add/change the source code:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Re-compile the custom class.
cmake --build build_custom -j4 --target install
```
</div>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 3</h4>

- Make the previously described changes.
- Add a function to count the number of tight muons/electrons with pT >= 7 GeV.
- Add the corresponding variables using the previous function.
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

Once this is done one can create pT-sorted containers using `DefineHelpers::sortedPassedVector`, for jets this would look like:

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

- Make the previously described changes.
- Add also pT-sorted vectors for muons and electrons.
- Add a function for pT-sorted b-jets passing the 85% working point.
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

- FastFramesCustomClassTemplate/
  - MyCustomFrame/ ------------ This is the name of the class.
    - MyCustomFrame.h ----- Header file where the class declarations live.
    - Variables.h ------- Header file for the function declarations.
  - ROOT/ ------------------------ Directory containing the class implementation.
    - MyCustomFrame.cc ---- This is where the variable definitions go!
    - Variables.cc ------- This is where the function definitions go.

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

- Make the previously described changes.
- Add a function classifies the events into regions, it must return a string:
  - n_electrons + n_muons = 4,
  - the sum of the charges must be zero.
  - the leading lepton must have a pT >= 27 GeV.
  - Classify in: 4mu, 4e, 2e2mu, mu3e, e3mu, and everything else is 'other'.
- Add a function for pT-sorted b-jets passing the 85% working point.
- Add these different regions to the configuration. Add histograms for the number of muons, electrons and b-jets in every region.
- Split further into regions with one b-tagged jet (1b) and two or more b-jets (2bp). For these regions add the histograms with the pT of the leading and sub-leading b-jets.
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
          number_of_bins: 100

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
          number_of_bins: 100

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
- Add a new method (`MyCustomFrame::createMetadataHistogram`)to the class to:
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
            definition: "truth_b_TLV_NOSYS.Pt()"
            type: double
            binning:
              min: 0
              max: 200000
              number_of_bins: 100
          - name: truth_bbar_pt
            title : "Truth Bbar-jet p_{T} [GeV]; p_{T} [GeV]; Events"
            definition: "truth_b_TLV_NOSYS.Pt()"
            type: double
            binning:
              min: 0
              max: 200000
              number_of_bins: 100
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

Since the variables needed to form the TLVs for the truth b/bar particles are **not** systematic-dependent, this is also a good oportunity to use `Define` instead of `systematicDefine`. The code we need to add is:

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

This time instead of using a function to define our variable we used a "Functor class". This is an abstraction that provides a storage (in this case `m_particleID`) and an overloaded `()` operator. This allows for more flexibility since we can "pass" parameters and to make our function more flexible.
</div>

Finally, since the `truth_b_pt` and `truth_bbar_pt` variables are only valid for our `ttll` sample, we want to exclude them from other samples. This is achieved via the `exclude_variables` option, let's put this under the samples we want to apply the skim:

<div style="background-color:rgb(227, 253, 237); padding: 15px; border-radius: 6px; margin-bottom: 15px; border-left: 4px solid rgb(8, 191, 41);">
<strong style="color:rgb(1, 142, 32);"></strong>

```yaml
# ttZconfig.yaml

# For example we do not want these variables in data.
samples: # All the samples to be used in the analysis.
  - name: "data" # Name given to the sample.
    dsids: [0] # For data, this is always 0.
    campaigns: ["2022"] # The corresponding campaing or campaigns.
    simulation_type: "data" # Type of simulation.
    exclude_variables: &truth_excluded
      - truth_b_pt
      - truth_bbar_pt
```
</div>

<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 7</h4>

Implement the previously described changes.
</div>

### 2.3 Per-sample decisions and matching truth and reco trees:

Sometimes you need to define a specific variable just for a given sample. One can do this via the `sample` parameter in the `MyCustomFrame::defineVariables` method.

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

If we wanted even further control (e.g. at the MC campaign or DSID level) we can use the tools explained in the [documentation](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/latest/tutorial/#uniquesample-based-decision-in-the-custom-class).
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
    min: -1
    max: 3
    number_of_bins: 4

# The previous variable also needs to be added to the excluded variables from other samples!
exclude_variables: &truth_excluded
  - truth_b_pt
  - truth_bbar_pt
  - reco_index_truth_b
```
</div>


<div style="background-color:rgb(247, 250, 192); border: 1px solid rgb(95, 76, 0); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(88, 93, 0); margin-top: 0;">Exercise 8</h4>

Implement the previously described changes.
</div>

- Implement the branch protection?

## 3.0 Machine learning:

Explain the ML inputs...

Exercise... define variables to create inputs.

Show Michal model and explain simple ONNX inference via config.

Show alternative way of doing this directly in the code.

## 4.0 Using distributed computing:

Show how to configure a condor run.
- Exercise, give some job specifications and ask for the command.


<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

You can find more information about the following topics in these links:

- [FastFrames documentation](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/).
- [TopCPToolkit documentation](https://topcptoolkit.docs.cern.ch).
- [FastFrames source code](https://gitlab.cern.ch/atlas-amglab/fastframes/).
- [FastFrames main tutorial](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/tutorial/).
- [FastFrames mattermost channel](https://mattermost.web.cern.ch/top-analysis/channels/histogramming-tool-rdataframe).

</div>