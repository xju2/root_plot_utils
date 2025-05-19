{pkgs, ...}: {
    channel = "unstable";
    # Use https://search.nixos.org/packages to find packages

    packages = [
      pkgs.poetry
      pkgs.root
    ];
    idx.extensions = [
        "ms-python.python"
    ];
}