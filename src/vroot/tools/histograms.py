from __future__ import annotations

from pathlib import Path

import ROOT
from omegaconf import DictConfig, OmegaConf

from vroot.hparams_mixin import HyperparametersMixin
from vroot.utils import get_pylogger

log = get_pylogger(__name__)


class HistogramOptions(HyperparametersMixin):
    def __init__(
        self,
        histname: str,
        xlabel: str | None = None,
        xlim: tuple[float, float] | None = None,
        ylabel: str | None = None,
        ylim: tuple[float, float] | None = None,
        is_data: bool = False,
        is_logy: bool = False,
        rebin: int | None = None,
        ratio_ylim: tuple[float, float] | None = None,
        ratio_ylabel: str | None = None,
        density: bool = False,
        **kwargs,  # ignore other options
    ) -> None:
        super().__init__()
        self.save_hyperparameters()
        self.name = histname

    def __eq__(self, other) -> bool:
        return self.hparams.histname == other.hparams.histname

    def __gt__(self, other) -> bool:
        return self.hparams.histname >= other.hparams.histname

    def __str__(self) -> str:
        return "HistogramOptions:\n" + super().__str__()

    def __repr__(self) -> str:
        return str(self)

    def __call__(self, hist: ROOT.TH1) -> None:
        # decorate the TH1.
        if self.hparams.xlabel is not None:
            hist.GetXaxis().SetTitle(self.hparams.xlabel)

        if self.hparams.xlim is not None:
            hist.GetXaxis().SetRangeUser(*self.hparams.xlim)

        if self.hparams.ylabel is not None:
            hist.GetYaxis().SetTitle(self.hparams.ylabel)

        if self.hparams.ylim is not None:
            hist.GetYaxis().SetRangeUser(*self.hparams.ylim)

        if self.hparams.rebin is not None and self.hparams.rebin > 1 and isinstance(hist, ROOT.TH1):
            hist.Rebin(self.hparams.rebin)

        if self.hparams.density and isinstance(hist, ROOT.TH1):
            if hist.GetSumw2() is None:
                hist.Sumw2()

            hist.Scale(1.0 / (hist.Integral() + 1e-10))
            hist.GetYaxis().SetTitle("Density")

    def __hash__(self) -> int:
        return hash(self.name)


class Histograms:
    def __init__(self, config: DictConfig) -> None:
        self._histograms = []
        self.config = {key: value for key, value in config.items() if key != "histograms"}
        self.use_all = self.config.pop("use_all_histograms", False)
        if self.use_all:
            log.info("Using all histograms in the file")

        self.parse_config(config)

    def parse_config(self, config: DictConfig) -> None:
        if "histograms" not in config:
            if self.use_all:
                return
            raise ValueError("No histograms found in the config!")

        def create_histogram(in_config: OmegaConf) -> None:
            in_cfg = OmegaConf.merge(self.config, in_config)
            if "histo_dir" in config:
                in_cfg.histname = str(Path(config.histo_dir, in_cfg.histname))
            out_histo = HistogramOptions(**in_cfg)
            self._histograms.append(out_histo)

        for hist_cfg in config.histograms:
            histname = hist_cfg.histname

            if isinstance(histname, list):
                # multiple histograms per config
                # check all histograms have the same length
                if not all(len(histname) == len(value) for key, value in hist_cfg.items()):
                    # find the key with the wrong length
                    for key, value in hist_cfg.items():
                        if len(value) != len(histname):
                            raise ValueError(
                                f"Length of `{key}` "
                                "is not the same as histnames "
                                f"{histname[0]}, {len(histname)}"
                            )

                for idx in range(len(histname)):
                    cfg = OmegaConf.create({key: value[idx] for key, value in hist_cfg.items()})
                    create_histogram(cfg)

            elif isinstance(histname, str):
                # single histogram per config
                create_histogram(hist_cfg)

    def __iadd__(self, other):
        self._histograms.extend(other._histograms)
        return self

    def __iter__(self):
        return iter(self._histograms)

    def __len__(self):
        return len(self._histograms)

    def __getitem__(self, index):
        return self._histograms[index]

    def __str__(self) -> str:
        outstr = f"Total histograms: {len(self._histograms):,}\n"
        for hist in self._histograms:
            y_lim_info = (
                f"ylim({hist.hparams.ylim[0]}, {hist.hparams.ylim[1]})" if hist.hparams.ylim else ""
            )
            outstr += f"\t {hist.name} {y_lim_info}\n"
        return outstr

    def get_all_histograms(self, file_handle):
        """Get all histograms from the file."""
        histogram_names = file_handle.get_all_histogram_names()
        all_histograms = [HistogramOptions(histname=histname) for histname in histogram_names]
        if self._histograms:
            # merge the existing histogram configurations with the
            # default ones
            self.merge(all_histograms)
        else:
            self._histograms = all_histograms
        log.info(f"Read {len(self._histograms):,} histograms from the file")

    def merge(self, other):
        """Merge the histograms in `other` with the existing ones."""
        for hist in other:
            if hist not in self._histograms:
                self._histograms.append(hist)
                log.info(f"Added histogram: {hist.hparams.histname}")
