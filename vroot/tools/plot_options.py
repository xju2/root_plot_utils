from typing import Tuple, Optional

from vroot.hparams_mixin import HyperparametersMixin

class HistogramOptions(HyperparametersMixin):
    def __init__(self,
                 histname: str,
                 xlabel: Optional[str] = None,
                 xlim: Optional[Tuple[float, float]] = None,
                 ylabel: Optional[str] = None,
                 ylim: Optional[Tuple[float, float]] = None,
                 is_data: bool = False,
                 rebin: Optional[int] = None,
                 **kwargs) -> None:
        super().__init__()
        self.save_hyperparameters()


class RatioOptions(HyperparametersMixin):
    def __init__(self,
                 ylabel: str,
                 ylim: Optional[Tuple[float, float]] = None,
                 **kwargs) -> None:
        super().__init__()
        self.save_hyperparameters()


class PlotOptions(HyperparametersMixin):
    def __init__(self,
                 add_ratio: bool,
                 ratio_options: Optional[RatioOptions] = None,
                 atlas_label: str = "ATLAS Internal",
                 exatra_text: Optional[str] = None,
                 **kwargs) -> None:
        super().__init__()
        self.save_hyperparameters(ignore=["ratio_options"])
