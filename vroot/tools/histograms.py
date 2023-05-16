from typing import Tuple, Optional

from pathlib import Path
from vroot.hparams_mixin import HyperparametersMixin
from omegaconf import DictConfig, OmegaConf

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

class Histograms:
    def __init__(self, config: DictConfig) -> None:
        self._histograms = []
        self.parse_config(config)

    def parse_config(self, config: DictConfig) -> None:
        """Parse the config"""

        if "histograms" not in config:
            raise ValueError("No histograms found in the config!")

        for hist_cfg in config.histograms:
            cfg = config.copy()
            OmegaConf.set_struct(cfg, False)
            cfg.update(hist_cfg)
            if "histo_dir" in config:
                cfg.histname = str(Path(config.histo_dir, cfg.histname))
            histo = HistogramOptions(**cfg)

            self._histograms.append(histo)

    def __iadd__(self, other):
        self._histograms.extend(other._histograms)
        return self
