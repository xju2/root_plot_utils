"""Plot histograms from one file"""
from pathlib import Path
from vroot.task.base import TaskBase
from vroot.utils import get_pylogger
from vroot.tools.reader import TH1FileHandle


logger = get_pylogger(__name__)

class PlotHistogramsInOneFile(TaskBase):
    def __init__(self,
                 filehandle: TH1FileHandle,
                 outdir: str = ".",
                 name: str = "PlotoneFile",
                 **kwargs) -> None:
        super().__init__()
        self.save_hyperparameters(ignore=["filehandle"])
        self.file = filehandle

    def run(self) -> None:
        print(self.file)
        print(self.histograms)
        print(self.canvas)

        # check if canvas needs adjustment
        if "canvas" in self.histograms.config:
            self.canvas.update(self.histograms.config["canvas"])

        with_ratio = False
        for histogram in self.histograms:
            hist, hist_copy = self.file.read(histogram)

            # check if canvas needs adjustment for this histogram
            if "canvas" in histogram.hparams:
                canvas_cls = self.canvas.deepupdate(histogram.hparams.canvas)
            else:
                canvas_cls = self.canvas

            canvas, _, _ = canvas_cls.create(with_ratio)
            canvas.cd()
            hist_copy.SetLineColor(9000)
            hist.SetLineColor(9000)
            hist.SetMarkerSize(0)

            histname = Path(histogram.hparams.histname).name
            is_logy = histogram.hparams.is_logy
            if is_logy:
                canvas.SetLogy()

            hist_copy.Draw("hist")
            hist.Draw("EP")

            # add legend
            self.canvas.add_atlas_label(with_ratio)
            legend = self.canvas.create_legend()
            legend.AddEntry(hist_copy, self.file.hparams.name, "lep")
            legend.Draw()

            self.canvas.add_other_label()


            # write the canvas to file
            outname = histname
            if self.canvas.atlas_label.text is not None:
                outname += f"-{self.canvas.atlas_label.text}"
            outname += ".pdf"
            outname = Path(self.hparams.outdir) / outname
            canvas.SaveAs(str(outname))
