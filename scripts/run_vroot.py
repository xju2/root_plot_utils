import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

import logging
from pathlib import Path

import hydra
from omegaconf import DictConfig, OmegaConf

def resolve_if(condition, true_value, false_value):
    return true_value if condition else false_value

OmegaConf.register_new_resolver("if", resolve_if)

track_parameter_names = ["d0", "z0", "qoverp", "pt", "z0sin", "theta", "phi"]
OmegaConf.register_new_resolver("ex_tp",
                                lambda x: [x + "_" + y for y in track_parameter_names])
OmegaConf.register_new_resolver("ex_tp_vals",
                                lambda x: [x for _ in range(len(track_parameter_names))])

OmegaConf.register_new_resolver("ex_ctp",
                                lambda x, ys: [x + "_" + y.strip() for y in ys.split(",")])
OmegaConf.register_new_resolver("gen_list",
                                lambda x, y: [x] * y)

OmegaConf.register_new_resolver("eval", eval)

# from vroot.task.base import TaskBase
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
    canvas = hydra.utils.instantiate(cfg.canvas)
    task.set_canvas(canvas)

    # histograms
    task.add_histograms(cfg.histograms)

    task.run()


@hydra.main(config_path=root / "configs", config_name="run_task.yaml", version_base="1.2")
def main(cfg: DictConfig) -> None:
    # print(OmegaConf.to_yaml(cfg))
    main_function(cfg)

if __name__ == "__main__":
    main()
