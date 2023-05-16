import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path=root / "configs", config_name="run_task.yaml")
def my_app(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
