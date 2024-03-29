import ROOT
ROOT.gROOT.SetBatch(True)
mplBlue = ROOT.TColor(9000, 31 / 255, 119 / 255, 180 / 255, "mplBlue")
mplOrange = ROOT.TColor(9001, 1, 127 / 255, 14 / 255, "mplOrange")

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
ROOT.gROOT.LoadMacro(script_dir + "/AtlasStyle.C")
ROOT.SetAtlasStyle()
