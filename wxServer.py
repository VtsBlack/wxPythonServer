__author__ = 'norbit'


#!/usr/bin/env python
import wx
import wx.animate
import app
import threading
from app import EVT_COUNT, EVT_RECV, Countingthread


class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.panel = wx.Panel(self, -1)

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(750) # start timer after a delay

        self.lblname = wx.StaticText(self.panel, label="Your name :",)
        self.lbl_runtimes = wx.StaticText(self.panel, label="Run times")
        self._counter = wx.StaticText(self.panel, label="0")
        self.cnt_1 = 0

        self.btnRun = wx.Button(self.panel, label="Run")
        self.Bind(wx.EVT_BUTTON, self.OnRun, self.btnRun)
        self.MainSizer.Add(self.lblname, 0, wx.ALL, 5)
        self.MainSizer.Add(self.lbl_runtimes, 0, wx.ALL, 5)
        self.MainSizer.Add(self._counter, 0, wx.CENTER, 5)
        self.MainSizer.Add(self.btnRun, 0, wx.ALL, 5)

        #animation
        gif = wx.animate.GIFAnimationCtrl(self.panel, -1, "gear_gif.gif", pos=(50, 80))
        gif.GetPlayer().UseBackgroundColour(True)
        self.gif = gif


        self.panel.SetSizer(self.MainSizer)

        self.Bind(EVT_COUNT, self.OnCount)
        self.Bind(EVT_RECV, self.OnRecv)
        self.Bind(wx.EVT_CLOSE, self.OnClose)




        self.Show(True)


    def OnRun(self, event):
        self.worker = Countingthread(self, 1)
        self.worker.start()
        self.gif.Play()

    def OnCount(self, event):
        val = int(self._counter.GetLabel()) + event.GetValue()
        self._counter.SetLabel(unicode(val))

    def OnRecv(self, event):
        self.lblname.SetLabel(event.GetValue())

    def on_timer(self, event):
        self.cnt_1 = self.cnt_1 + 1
        self.lbl_runtimes.SetLabel(str(self.cnt_1))

    def OnClose(self, event):
        try:
            self.worker.stop()
            self.worker.join(10)
        except:
            pass

        self.Destroy()





app = wx.App(False)
frame = MyFrame(None, 'Server App 0.0')
app.MainLoop()

