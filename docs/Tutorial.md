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

- Finally, links to more detailed content will be in blue and notes will be in purple.

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>
</div>

<div style="background-color:rgb(255, 230, 254); border: 1px solid rgb(135, 33, 243); padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color:rgb(112, 13, 161); margin-top: 0;">Note:</h4>
</div>

### Install

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
git clone ssh://git@gitlab.cern.ch:7999/dbaronmo/fftutorialtopws2025.git FFTutorial --recurse-submodules
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
cmake --build build_ff -j10 --target install

# Setup environment
source build_ff/setup.sh

```
</div>
</div>

<div style="background-color: #e6f3ff; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0;">
<h4 style="color: #0d47a1; margin-top: 0;">More details...</h4>

To see installation instructions for different platforms and extendend details click [here](https://atlas-project-topreconstruction.web.cern.ch/fastframesdocumentation/#how-to-checkout-and-compile-the-code).
</div>

### Clean data and create metadata

Before doing any analysis, we first need to handle the cases where in the `TopCPToolkit` workflow no events passed the selections. In this case, `TopCPToolkit` will produce a file without any trees (this can happen for background samples or real collision data where our signature is not present). To clean our datasets we use the `merge_empty_grid_files` script:

<div style="background-color:rgb(255, 220, 220); padding: 15px; border-radius: 6px; border-left: 4px solid rgb(165, 19, 11);">
<strong style="color:rgb(195, 46, 12);"></strong>

```bash
# Clean input files
python3 python/merge_empty_grid_files.py --root_files_folder PLEASEMODIFYME

```
</div>
</div>

FastFrames needs to read a database where the type of sample, file locations, sum of weights, etc, are stored. The code provides the `produce_metadata_files.py` script for this purpose. Let's use it:

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