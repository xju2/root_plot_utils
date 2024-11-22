import logging
from pathlib import Path

import hydra
from omegaconf import DictConfig, OmegaConf

from vroot import utils
from vroot.utils import resolvers

resolvers.add_my_resolvers()


@utils.task_wrapper
def main_function(cfg: DictConfig) -> None:
    """Main function to invoke different tasks."""
    logging.basicConfig(
        filename=Path(cfg.paths.output_dir, "log.txt"), encoding="uft-8", level=logging.INFO
    )
    if not cfg.get("task"):
        raise ValueError("Task is not specified in the config file.")

    # Instantiate the task
    task = hydra.utils.instantiate(cfg.task)
    canvas = hydra.utils.instantiate(cfg.canvas)
    task.set_canvas(canvas)

    # histograms
    task.add_histograms(cfg.histograms)

    task.run()


@hydra.main(config_path="configs", config_name="run_task.yaml", version_base="1.2.0")
def main_module(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    main_function(cfg)


def main() -> None:
    import os
    import importlib.util

    spec = importlib.util.find_spec("vroot")
    os.environ["PROJECT_ROOT"] = str(Path(spec.origin).parent.parent.parent)
    main_module()


if __name__ == "__main__":
    main()
