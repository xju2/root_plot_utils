from array import array

import ROOT


def create_graph(name: str, x: list[float], y: list[float]) -> ROOT.TGraph:
    """Create a ROOT TGraph object.

    Parameters
    ----------
    name: str
        The name of the graph.
    x: list[float]
        A list of x-values.
    y: list[float]
        A list of y-values.

    Returns
    -------
    ROOT.TGraph
        The graph object.

    """
    gr = ROOT.TGraph(len(x), array("f", x), array("f", y))
    gr.SetName(name)
    return gr


def graph_error(
    name: str, x: list[float], xe: list[float], y: list[float], ye: list[float]
) -> ROOT.TGraphErrors:
    """Create a ROOT TGraphErrors object with symmetric errors.

    Parameters
    ----------
    name: str
        The name of the graph.
    x: list[float]
        A list of x-values.
    xe: list[float]
        A list of x-error values.
    y: list[float]
        A list of y-values.
    ye: list[float]
        A list of y-error values.

    Returns
    -------
    ROOT.TGraphErrors
        The graph object with errors.

    """
    gr = ROOT.TGraphErrors(len(x), array("f", x), array("f", xe), array("f", y), array("f", ye))
    gr.SetName(name)
    return gr


def unequal_bin_hist(hist_name: str, bin_list: list[float]) -> ROOT.TH1F:
    """Create a ROOT TH1F histogram with unequal bin widths.

    Parameters
    ----------
    hist_name : str
        The name of the histogram.
    bin_list : list of float
        A list of bin edges.

    Returns
    -------
    ROOT.TH1F
        The histogram object with unequal bin widths.
    """
    nbins = len(bin_list) - 1
    h1 = ROOT.TH1F(hist_name, hist_name, nbins, array("f", bin_list))
    return h1
