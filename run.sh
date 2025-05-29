#!/bin/bash


function gnn4pixel_with_AR() {

run_vroot -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=data/gnn4pixel/ckf.root \
  task.reference_file.name=main \
  task.comparator_file.path=data/gnn4pixel/gnn_v1.root \
  task.comparator_file.name="gnn4pixel w/ AR" \
  histograms=rel24_idpvm_efficiencies \
  "canvas.other_label.text='#sqrt{s} = 14 TeV, t#bar{t}, <#mu> = 200, HS'" \
  canvas.otypes="png"
}

function gnn4pixel_without_AR() {
run_vroot -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=data/gnn4pixel/ckf.root \
  task.reference_file.name=main \
  task.comparator_file.path=data/gnn4pixel/gnn_v2.root \
  task.comparator_file.name="gnn4pixel w/o AR" \
  "histograms=glob(rel24_idpvm*)" \
  "canvas.other_label.text='#sqrt{s} = 14 TeV, t#bar{t}, <#mu> = 200, HS'" \
  canvas.otypes=png,pdf
}

function gnn4ITk_ML_no_AR() {
run_vroot -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=data/gnn4pixel/ckf.root \
  task.reference_file.name=main \
  task.comparator_file.path=data/gnn4itk/end2end_ML.root \
  task.comparator_file.name="gnn4ITk w/o AR" \
  "histograms=glob(rel24_idpvm*)" \
  "canvas.other_label.text='#sqrt{s} = 14 TeV, t#bar{t}, <#mu> = 200, HS'" \
  canvas.otypes=png,pdf
}

gnn4itkML_ttbar() {
run_vroot -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=data/gnn4itk/paper2025data_v2.idpvm.ckf.ttbar.root \
  task.reference_file.name=main \
  task.comparator_file.path=data/gnn4itk/paper2025data_v3.idpvm.gnn4itkTriton.tracking.ttbar.root \
  task.comparator_file.name="GNN w/ Metric Learning" \
  "histograms=glob(rel24_idpvm*)" \
  "canvas.other_label.text='#sqrt{s} = 14 TeV, t#bar{t}, <#mu> = 200, All'" \
  canvas.otypes=png,pdf
}

gnn4itkML() {
  if [ $# -ne 3 ]; then
    echo "Usage: $0 <sampleName> <sampleLabel> <IDPVM_MODE>"
    exit 1
  fi
  local sampleName="$1"
  local sampleLabel="$2"
  local IDPVM_MODE="$3"
run_vroot -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=data/gnn4itk/idpvm.ckf.${IDPVM_MODE}.local.gnn4itkTriton.none.${sampleName}.root \
  task.reference_file.name=main \
  task.comparator_file.path=data/gnn4itk/idpvm.gnn4itkML.${IDPVM_MODE}.triton.gnn4itkTriton.tracking.${sampleName}.root \
  task.comparator_file.name="GNN w/ Metric Learning" \
  "histograms=glob(rel24_idpvm*)" \
  "canvas.other_label.text='#sqrt{s} = 14 TeV, ${sampleLabel}'" \
  canvas.otypes=png,pdf
}

# gnn4pixel_with_AR
# gnn4pixel_without_AR
# gnn4ITk_ML_no_AR

#gnn4itkML_ttbar

gnn4itkML "ZmumuPU200" "Z#rightarrow#mu#mu, <#mu> = 200, All" "primary"
# gnn4itkML "MuonPU0" "single muon, <#mu>=0, All" "primary"
#gnn4itkML "ttbar" "t#bar{t}, <#mu> = 200, All" "primary"
