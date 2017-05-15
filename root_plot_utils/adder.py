#!/usr/bin/env python
import ROOT

class adder(object):
    """
    Add line/text into canvas
    """
    def __init__(self):
        pass

    @staticmethod
    def add_text(x, y, color, text, size=0.05, font=42):
        l = ROOT.TLatex()
        l.SetTextSize(size)
        l.SetNDC()
        l.SetTextColor(color)
        l.SetTextFont(font)
        l.DrawLatex(x, y, text)

    @staticmethod
    def add_line(hist, y_val, color=1, style=2, option="x"):
        x_low = hist.GetBinLowEdge(hist.GetXaxis().GetFirst())
        x_hi = hist.GetBinLowEdge(hist.GetXaxis().GetLast()+1)
        y_low = hist.GetBinLowEdge(hist.GetYaxis().GetFirst())
        y_hi = hist.GetBinLowEdge(hist.GetYaxis().GetLast()+1)
        line = ROOT.TLine()
        line.SetLineColor(color)
        line.SetLineStyle(style)
        line.SetLineWidth(2)
        if option.lowercase() == "x":
            line.DrawLine(x_low, y_val, x_hi, y_val)
        else:
            line.DrawLine(y_val, y_low, y_val, y_hi)
