# root_plot_utils
Plotting macros based on ROOT

## install ROOT via conda
See the blog: https://iscinumpy.gitlab.io/post/root-conda/

```bash
conda install -c conda-forge root
```
To setup the environment, in Faraday, `conda-start tf2.7`.
## Run the example
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
```