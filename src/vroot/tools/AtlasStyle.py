from pathlib import Path

import ROOT

ROOT.gROOT.SetBatch(True)
mplBlue = ROOT.TColor(9000, 31 / 255, 119 / 255, 180 / 255, "mplBlue")  # noqa: N816
mplOrange = ROOT.TColor(9001, 1, 127 / 255, 14 / 255, "mplOrange")  # noqa: N816

script_dir = str(Path(__file__).resolve().parent)
ROOT.gROOT.LoadMacro(script_dir + "/AtlasStyle.C")
ROOT.SetAtlasStyle()
