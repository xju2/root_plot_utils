from omegaconf import DictConfig

from vroot.hparams_mixin import HyperparametersMixin
from vroot.tools.canvas import Canvas
from vroot.tools.histograms import Histograms


class TaskHooks:

    def run(self) -> None:
        """Run the task."""


class TaskBase(TaskHooks, HyperparametersMixin):
    def __init__(self) -> None:
        super().__init__()
        self.canvas: Canvas = None
        self.histograms: Histograms = None

    def set_canvas(self, canvas: Canvas) -> None:
        """Add canvas to the task."""
        self.canvas = canvas

    def add_histograms(self, histo_config: DictConfig) -> None:
        """Add histograms to the task."""
        self.histograms = Histograms(histo_config)
