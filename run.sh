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

# gnn4itkML "ZmumuPU200" "Z#rightarrow#mu#mu, <#mu> = 200, All" "primary"
# gnn4itkML "MuonPU0" "single muon, <#mu>=0, All" "primary"
#gnn4itkML "ttbar" "t#bar{t}, <#mu> = 200, All" "primary"

compare_gnn_with_gnn() {
  local sampleName="$1"
  local sampleLabel="$2"
  local IDPVM_MODE="primary"
  RUN_1_DIR_NAME="tracking_v1_maxHoles5"
  RUN_2_DIR_NAME="tracking"
  FILE_BASE_DIR="/global/cfs/cdirs/m3443/usr/xju/workflow/workarea"
  SAMPLE_DIR="${sampleName}/idpvm.gnn4itkML.${IDPVM_MODE}.triton.gnn4itkTriton.tracking.${sampleName}.root"

  run_vroot -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=${FILE_BASE_DIR}/$RUN_2_DIR_NAME/$SAMPLE_DIR \
  task.reference_file.name="Max 4 holes" \
  task.comparator_file.path=${FILE_BASE_DIR}/$RUN_1_DIR_NAME/$SAMPLE_DIR \
  task.comparator_file.name="Max 5 holes" \
  "histograms=glob(rel24_idpvm*)" \
  "canvas.other_label.text='#sqrt{s} = 14 TeV, ${sampleLabel}'" \
  canvas.otypes=png,pdf
}

compare_endcapEtaOLSP() {
  local sampleName="$1"
  local sampleLabel="$2"
  local IDPVM_MODE="primary"
  RUN_1_DIR_NAME="tracking_v2_maxHoles442_withEtaOverlapSPs"
  RUN_2_DIR_NAME="tracking"
  FILE_BASE_DIR="/global/cfs/cdirs/m3443/usr/xju/workflow/workarea"

  run_vroot -m \
  task_name=gnn4pixel task=compare_two_files \
  task.reference_file.path=${FILE_BASE_DIR}/$RUN_1_DIR_NAME/${sampleName}/idpvm.gnn4itkML.${IDPVM_MODE}.triton.gnn4itkTriton.tracking.${sampleName}.root \
  task.reference_file.name="with EndcapEtaOLSP" \
  task.comparator_file.path=${FILE_BASE_DIR}/$RUN_2_DIR_NAME/${sampleName}/idpvm.gnn4itkMLNoEndcapOLSP.${IDPVM_MODE}.triton.gnn4itkTriton.tracking.${sampleName}.root \
  task.comparator_file.name="w/o EndcapEtaOLSP" \
  "histograms=glob(rel24_idpvm*)" \
  "canvas.other_label.text='#sqrt{s} = 14 TeV, ${sampleLabel}'" \
  'canvas.otypes=png,pdf' \
  'canvas=with_ratio' \
  'task.with_ratio=true'
}
#compare_gnn_with_gnn "MuonPU0" "single muon, <#mu>=0, HS"
#compare_gnn_with_gnn "PionPU0" "single pion, <#mu>=0, HS"
# compare_gnn_with_gnn "ttbar" "t#bar{t}, <#mu> = 200, HS"

compare_endcapEtaOLSP "ttbar" "t#bar{t}, <#mu> = 200, HS"
compare_endcapEtaOLSP "PionPU0" "single pion, <#mu>=0, HS"
compare_endcapEtaOLSP "MuonPU0" "single muon, <#mu>=0, HS"
