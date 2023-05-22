import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

from omegaconf import DictConfig, OmegaConf

track_parameter_names = ["d0", "z0", "qoverp", "pt", "z0sin", "theta", "phi"]
OmegaConf.register_new_resolver("ex_tp",
                                lambda x: [x + y for y in track_parameter_names])
OmegaConf.register_new_resolver("ex_tp_vals",
                                lambda x: [x for _ in range(len(track_parameter_names))])

OmegaConf.register_new_resolver("ex_ctp",
                                lambda x, ys: [x + y.strip() for y in ys.split(",")])
OmegaConf.register_new_resolver("gen_list",
                                lambda x, y: [x] * y)

OmegaConf.register_new_resolver("eval", eval)

import hydra

@hydra.main(version_base=None, config_path=root / "configs", config_name="run_task.yaml")
def my_app(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))
    print(cfg.histograms.histograms[0].histname)
    print(cfg.histograms.histograms[0].ratio_ylim)
    print(cfg.histograms.histograms[1].histname)
    print(cfg.histograms.histograms[1].ratio_ylim)

if __name__ == "__main__":
    my_app()
