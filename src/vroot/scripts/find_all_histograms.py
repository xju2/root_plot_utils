import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

from pathlib import Path

import ROOT


def main():
    fname = root / "data/MyPhysVal_CKF.root"
    # list all histograms in the ROOT file
    # and print their names
    # if the object is a directory, change directory
    # to that directory and list all histograms in that directory
    # perform this recursively.
    f = ROOT.TFile(str(fname), "READ")

    all_histograms = []
    all_object_types = []
    all_objects = {}

    def read_directory(directory):
        directory.cd()
        for key in directory.GetListOfKeys():
            obj = key.ReadObj()
            if isinstance(obj, ROOT.TDirectory):
                read_directory(obj)
            else:
                class_name = obj.ClassName()
                if class_name not in all_objects:
                    all_objects[class_name] = []
                all_objects[class_name].append(obj)
                all_object_types.append(obj.ClassName())
                all_histograms.append(Path(key.GetMotherDir().GetPath()) / obj.GetName())

    read_directory(f)

    print(len(all_histograms))
    # print(all_histograms[:10], all_histograms[-10:])
    print(set(all_object_types))
    for key, value in all_objects.items():
        print(key, len(value))

if __name__ == "__main__":
    main()
