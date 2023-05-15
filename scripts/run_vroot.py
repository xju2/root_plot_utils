import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)
from typing import List
import logging
from pathlib import Path

import hydra
from omegaconf import DictConfig

from vroot.task.base import TaskBase
from vroot import utils

@utils.task_wrapper
def main_function(cfg: DictConfig) -> None:
    """Main function to invoke different tasks
    """

    logging.basicConfig(
        filename=Path(cfg.paths.output_dir, "log.txt"), encoding='uft-8', level=logging.INFO)
    if not cfg.get("task"):
        raise ValueError("Task is not specified in the config file.")

    # Instantiate the task
    task = hydra.utils.instantiate(cfg.task)
    task.add_canvas(cfg.canvas)

    # histograms
    histogram_config = cfg.histograms
    if histogram_config:
        task.add_histograms(histogram_config)
    else:
        logging.info("No histograms are added.")

    task.run()


@hydra.main(config_path=root / "configs", config_name="run_task.yaml", version_base="1.2")
def main(cfg: DictConfig) -> None:
    main_function(cfg)

if __name__ == "__main__":
    main()
