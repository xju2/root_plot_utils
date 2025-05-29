#!/bin/bash

download(){
	BASEDIR="/global/cfs/cdirs/m3443/usr/xju/workflow/workarea/tracking/"
	SAMPLE=$1
	IDPVM_MODE="primary"
	scp pl:${BASEDIR}/$SAMPLE/idpvm.ckf.${IDPVM_MODE}.local.gnn4itkTriton.none.$SAMPLE.root data/gnn4itk/
	scp pl:${BASEDIR}/$SAMPLE/idpvm.gnn4itkML.${IDPVM_MODE}.triton.gnn4itkTriton.tracking.$SAMPLE.root data/gnn4itk/
}

#download ttbar
# download MuonPU0
download ZmumuPU200
