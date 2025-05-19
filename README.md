# root_plot_utils
Plotting macros based on ROOT

## Create the environment
I use [nix.dev](https://nix.dev/) to create a reproduciable development environment and use [poetry 2.1](https://python-poetry.org/docs/) to manage python virtual environment.

```bash
poetry install
eval $(poetry env activate)
source `root-config --bindir`/thisroot.sh
```
or `poetry run which python`.

## Run the example

### Plot histograms from a root file
```bash
python scripts/run_vroot.py task_name=gnn_tracking task=plot_histograms histograms=rel24_idpvm_efficiencies task.filehandle.path=data/physval.v4.root
```
### Compare histograms from two root files
```bash
python scripts/run_vroot.py task_name=ckf_vs_gnn task=compare_two_files histograms=idpvm_efficiencies
```
or compare them with ratio panel
```bash
python scripts/run_vroot.py task_name=ckf_vs_gnn task=compare_two_files task.with_ratio=true canvas=with_ratio histograms=idpvm_resolution
```

To run all histograms
```bash
python scripts/run_vroot.py -m task_name=ckf_vs_gnn task=compare_two_files task.with_ratio=true canvas=with_ratio
```
or to run all histograms in release 24:
```bash
python scripts/run_vroot.py -m task_name=athena_chain task=plot_histograms task.filehandle.path=physval_debug.root  "histograms=glob(rel24_idpvm*)"
```