from __future__ import annotations

from pathlib import Path

import hydra
from omegaconf import DictConfig, OmegaConf

from vroot.utils import resolvers

resolvers.add_my_resolvers()


@hydra.main(config_path="configs", config_name="run_task.yaml", version_base="1.2.0")
def main_module(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    print(cfg.histograms.histograms[0].histname)
    print(cfg.histograms.histograms[1].histname)


def my_app() -> None:
    import importlib.util
    import os

    spec = importlib.util.find_spec("vroot")
    os.environ["PROJECT_ROOT"] = str(Path(spec.origin).parent.parent.parent)
    main_module()  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    my_app()
