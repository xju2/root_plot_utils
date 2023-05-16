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
