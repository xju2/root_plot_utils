from vroot.hparams_mixin import HyperparametersMixin
from omegaconf import DictConfig

class TaskHooks:
    def add_canvas(self, canvas_config: DictConfig) -> None:
        """Add canvas to the task"""

    def add_histograms(self, histogram_config: DictConfig) -> None:
        """Add histograms to the task"""

    def run(self) -> None:
        """Run the task"""


class TaskBase(TaskHooks, HyperparametersMixin):
    def __init__(self) -> None:
        super().__init__()
