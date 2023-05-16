import warnings

from vroot.tools.plot_options import HistogramOptions
from vroot.hparams_mixin import HyperparametersMixin
from vroot.utils import get_pylogger

import ROOT
logger = get_pylogger(__name__)


class TH1FileHandle(HyperparametersMixin):
    def __init__(self,
                 path: str,
                 name: str,
                 is_data: bool):
        super().__init__()
        self.save_hyperparameters()

        self.file_handle = ROOT.TFile.Open(self.hparams.path)
        if self.file_handle is None:
            raise RuntimeError(f"Cannot open file {self.hparams.path}")
        else:
            logger.info(f"Open {self.hparams.name} from {self.hparams.path}")

    def __str__(self) -> str:
        return f"TH1FileHandle: name={self.hparams.name}, path={self.hparams.path}"

    def __repr__(self) -> str:
        return super().__repr__() + f"({self.hparams.name})"

    def read(self, hist_options: HistogramOptions) -> ROOT.TH1:
        """Read histogram from file and apply options"""

        th1 = self.read_by_name(hist_options.histname)

        if hist_options.xlabel is not None:
            th1.GetXaxis().SetTitle(hist_options.xlabel)

        if hist_options.xlim is not None:
            th1.GetXaxis().SetRangeUser(*hist_options.xlim)

        if hist_options.ylabel is not None:
            th1.GetYaxis().SetTitle(hist_options.ylabel)

        if hist_options.ylim is not None:
            th1.GetYaxis().SetRangeUser(*hist_options.ylim)

        if hist_options.rebin is not None and hist_options.rebin > 1:
            th1.Rebin(hist_options.rebin)

        return th1

    def read_by_name(self, histname: str) -> ROOT.TH1:
        th1 = self.file_handle.Get(histname)
        if th1 is None:
            raise RuntimeError(f"Cannot find histogram {histname} in file {self.file_handle.GetName()}")
        th1.SetDirectory(0)
        if th1.isinstance(ROOT.TH2) or th1.isinstance(ROOT.TH3):
            warnings.warn("2D/3D histogram is not supported yet", RuntimeWarning)
        return th1
