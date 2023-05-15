from omegaconf import DictConfig
import ROOT

class Canvas:
    def __init__(self, config: DictConfig) -> None:
        self.config = config

    def create(self, name) -> None:
        canvas = ROOT.TCanvas(name, name, self.config.size.width, self.config.size.height)
        if self.config.with_ratio_panel:
            pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1)
            pad1.SetBottomMargin(0)
            pad1.Draw()
            canvas.cd()
            pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, 0.3)
            pad2.SetTopMargin(0)
            pad2.SetBottomMargin(0.5)
            pad2.Draw()
            return canvas, pad1, pad2
        else:
            return canvas, None, None

    def add_legend(self):
        x = self.config.legend.x
        y = self.config.legend.y
        width = self.config.legend.width
        height = self.config.legend.height
        tsize = self.config.legend.text_size

        legend = ROOT.TLegend(x, y, x + width, y + height)
        legend.SetTextSize(tsize)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        return legend

    def add_atlas_label(self):
        text = self.config.atlas_label.get("text", "ATLAS Internal")
        x = self.config.atlas_label.x
        y = self.config.atlas_label.y
        tsize = self.config.atlas_label.text_size
        color = self.config.atlas_label.color

        label = ROOT.TLatex()
        label.SetNDC()
        label.SetTextFont(72)
        label.SetTextColor(color)
        label.SetTextSize(tsize)
        label.DrawLatex(x, y, "ATLAS")
        if text is not None:
            delx = 0.115 * 696 * ROOT.gPad.GetWh() / (472 * ROOT.gPad.GetWw()) * 0.75 * (tsize / 0.05)
            p = ROOT.TLatex()
            p.SetNDC()
            p.SetTextFont(42)
            p.SetTextSize(tsize)
            p.SetTextColor(color)
            p.DrawLatex(x + delx, y, text)

    def add_other_label(self):
        x = self.config.other_label.x
        y = self.config.other_label.y
        tsize = self.config.other_label.text_size
        color = self.config.other_label.color
        text = self.config.other_label.text

        label = ROOT.TLatex()
        label.SetNDC()
        label.SetTextFont(42)
        label.SetTextColor(color)
        label.SetTextSize(tsize)
        label.DrawLatex(x, y, text)
