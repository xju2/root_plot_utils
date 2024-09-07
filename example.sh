#!/bin/bash

scp pl:/pscratch/sd/x/xju/ITk/ForFinalPaper/run_athena/run/AllEvents/gnn/physval.root data/gnn4pixel/gnn_v1.root
scp pl:/pscratch/sd/x/xju/ITk/ForFinalPaper/run_athena/run/AllEvents/gnn/physval.noAR.50evts.root data/gnn4pixel/gnn_v2.root

scp pl:/pscratch/sd/x/xju/ITk/ForFinalPaper/run_athena/run/AllEvents/ckf/physval.root data/gnn4pixel/ckf.root

scp pl:/pscratch/sd/x/xju/ITk/ForFinalPaper/run_athena/run/AllEvents/end2end_ML/physval.root data/gnn4itk/end2end_ML.root


python scripts/run_vroot.py -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=data/gnn4pixel/ckf.root \
  task.reference_file.name=main \
  task.comparator_file.path=data/gnn4pixel/gnn_v2.root \
  task.comparator_file.name=gnn4pixel \
  histograms=rel24_idpvm_efficiencies,rel24_idpvm_resolution,rel24_idpvm_hits,rel24_idpvm_parameters

python scripts/run_vroot.py -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=data/gnn4pixel/ckf.root \
  task.reference_file.name=main \
  task.comparator_file.path=data/gnn4itk/end2end_ML.root \
  task.comparator_file.name=gnn4ITk \
  histograms=rel24_idpvm_efficiencies,rel24_idpvm_resolution,rel24_idpvm_hits,rel24_idpvm_parameters \
  "canvas.other_label.text='#sqrt{s} = 14 TeV, t#bar{t}, <#mu> = 200, HS'" \
  rel24_idpvm_parameters.density=True