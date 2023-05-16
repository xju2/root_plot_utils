from vroot.task.base import TaskBase
from vroot.utils import get_pylogger
from vroot.tools.reader import TH1FileHandle
from vroot.tools.plot_options import PlotOptions

import ROOT
# from vroot.tools.ploter import Plotter
# from vroot.tools.histograms import Histograms
logger = get_pylogger(__name__)

class CompareTwoIdentidicalFiles(TaskBase):
    def __init__(self,
                 reference_file: TH1FileHandle,
                 comparator_file: TH1FileHandle,
                 with_ratio: bool = True,
                 name: str = "CompareTwoIdentidicalFiles",
                 **kwargs) -> None:
        super().__init__()
        self.save_hyperparameters(ignore=["reference_file", "comparator_file"])
        self.ref_file = reference_file
        self.comparator_file = comparator_file
        # self.plotter = Plotter()

    def run(self) -> None:
        print(self.ref_file)
        print(self.comparator_file)
        print(self.histograms)

        with_ratio = self.hparams.with_ratio
        for histogram in self.histograms:
            hist_ref = self.ref_file.read(histogram)
            hist_comparator = self.comparator_file.read(histogram)
            canvas, pad1, pad2 = self.canvas.create("canvas", with_ratio)
            if with_ratio:
                pass
            else:
                hist_ref.Draw("hist")
                hist_comparator.Draw("hist same")

