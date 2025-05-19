{pkgs, ...}: {
    channel = "unstable";
    # Use https://search.nixos.org/packages to find packages

    packages = [
      pkgs.poetry
      pkgs.root
      pkgs.git-lfs
    ];
    idx.extensions = [
        "ms-python.python"
        "charliermarsh.ruff"
    ];
}