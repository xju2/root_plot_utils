import warnings
from pathlib import Path

import numpy as np
import ROOT

from vroot.hparams_mixin import HyperparametersMixin
from vroot.tools.histograms import HistogramOptions
from vroot.utils import get_pylogger

logger = get_pylogger(__name__)


def convert_TEfficiency_to_TGraphAsymmErrors(hist: ROOT.TEfficiency) -> ROOT.TGraphAsymmErrors:
    t_eff_total = hist.GetCopyTotalHisto()
    n_bins_x = t_eff_total.GetNbinsX()

    # use Clopper-Pearson interval, which is the default for TEfficiency
    # need to loop through values to get only y-errors
    bins = np.empty(n_bins_x)
    vals = np.empty(n_bins_x)
    xErr = np.zeros(n_bins_x)
    yErrUp = np.empty(n_bins_x)
    yErrLo = np.empty(n_bins_x)

    for i in range(1, n_bins_x + 1):
        bins[i - 1] = t_eff_total.GetBinCenter(i)
        vals[i - 1] = hist.GetEfficiency(i)
        yErrUp[i - 1] = hist.GetEfficiencyErrorUp(i)
        yErrLo[i - 1] = hist.GetEfficiencyErrorLow(i)

    graph = ROOT.TGraphAsymmErrors(n_bins_x, bins, vals, xErr, xErr, yErrLo, yErrUp)

    return graph


class TH1FileHandle(HyperparametersMixin):
    def __init__(self, path: str, name: str, is_data: bool):
        super().__init__()
        self.save_hyperparameters()

        self.file_handle = ROOT.TFile.Open(self.hparams.path)
        if self.file_handle is None:
            raise RuntimeError(f"Cannot open file {self.hparams.path}")
        logger.info(f"Open {self.hparams.name} from {self.hparams.path}")

    def __str__(self) -> str:
        return f"TH1FileHandle: name={self.hparams.name}, path={self.hparams.path}"

    def __repr__(self) -> str:
        return super().__repr__() + f"({self.hparams.name})"

    def read(self, histogram: HistogramOptions) -> ROOT.TH1:
        th1 = self.read_by_name(histogram.name)
        th1_type = type(th1)
        hist = th1
        hist_copy = None

        if th1_type is ROOT.TEfficiency:
            hist = convert_TEfficiency_to_TGraphAsymmErrors(th1)
            hist.SetName(Path(histogram.name).name)
        elif th1_type is ROOT.TProfile:
            hist = th1.ProjectionX()

        histogram(hist)
        hist.SetLineWidth(2)
        if th1_type is ROOT.TEfficiency:
            hist_copy = th1.GetCopyPassedHisto()
            hist_copy.Divide(th1.GetCopyPassedHisto(), th1.GetCopyTotalHisto(), 1.0, 1.0, "B")
            hist_copy.SetLineWidth(2)
            histogram(hist_copy)
        else:
            hist_copy = hist.Clone(hist.GetName() + "_copy")
        return hist, hist_copy

    def read_by_name(self, histname: str) -> ROOT.TH1:
        th1 = self.file_handle.Get(histname)
        if th1 is None or type(th1) is ROOT.TObject:
            raise RuntimeError(
                f"Cannot find histogram {histname} in file {self.file_handle.GetName()}"
            )
        th1.SetDirectory(0)
        if type(th1) is ROOT.TH2 or type(th1) is ROOT.TH3:
            warnings.warn("2D/3D histogram is not supported yet", RuntimeWarning, stacklevel=2)

        return th1

    def get_all_histogram_names(self) -> list[str]:
        all_objects = {}

        def read_directory(directory):
            directory.cd()
            for key in directory.GetListOfKeys():
                obj = key.ReadObj()
                if isinstance(obj, ROOT.TDirectory):
                    read_directory(obj)
                else:
                    class_name = obj.ClassName()
                    if class_name not in all_objects:
                        all_objects[class_name] = []

                    name = Path(key.GetMotherDir().GetPath()) / obj.GetName()
                    name = str(name).split(":")[-1]
                    all_objects[class_name].append(name)

        read_directory(self.file_handle)

        # summarize the file contents
        all_names = []
        for class_name, names in all_objects.items():
            logger.info(f"Found {len(names)} {class_name} objects")
            if class_name != "TTree":
                all_names.extend(names)

        return all_names
