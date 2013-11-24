__author__ = 'vytautas'


#!/usr/bin/env python
import wx
import socket
import threading
import time

myEVT_COUNT = wx.NewEventType()
EVT_COUNT = wx.PyEventBinder(myEVT_COUNT, 1)
#
myEVT_RECV = wx.NewEventType()
EVT_RECV = wx.PyEventBinder(myEVT_RECV, 1)

class CountEvent(wx.PyCommandEvent):
    """Evetn to singal that a count value is ready
    """
    def __init__(self, etype, eid, value=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the vlaue from the event.
        @return: the value of this event
        """
        return self._value

class Countingthread(threading.Thread):
    def __init__(self, parent, value):
        threading.Thread.__init__(self)
        self._parent = parent
        self._value = value

        self.HOST = '0.0.0.0'                 # Symbolic name meaning all available interfaces
        self.PORT = 50007              # Arbitrary non-privileged port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.bind((self.HOST, self.PORT))

        self.conntected = False
        self.running = True

    def run(self):
        while self.running:
            time.sleep(1)
            evt = CountEvent(myEVT_COUNT, -1, self._value)
            wx.PostEvent(self._parent, evt)

            if self.conntected == False:
                print "Init"
                self.s.setblocking(False)
                self.s.settimeout(0.001)

                try:
                    self.s.listen(1)
                    self.conn, self.addr = self.s.accept()
                    print 'Connected by', self.addr
                    self.conntected = True
                except socket.timeout:
                    pass

            else:
                try:
                    print "try read"
                    self.msg = self.conn.recv(1024)
                except socket.error as m1:
                    print m1
                    self.msg = None
                    pass
                if self.msg:
                    evt = CountEvent(myEVT_RECV, -1, self.msg)
                    wx.PostEvent(self._parent, evt)
                elif self.msg == '':
                    print "Client Disconnect"
                    self.conntected = False


    def stop(self):
        self.running = False


class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(750) # start timer after a delay

        self.lblname = wx.StaticText(self, label="Your name :",)
        self.lbl_runtimes = wx.StaticText(self, label="Run times")
        self._counter = wx.StaticText(self, label="0")
        self.cnt_1 = 0

        self.btnRun = wx.Button(self, label="Run")
        self.Bind(wx.EVT_BUTTON, self.OnRun, self.btnRun)
        self.MainSizer.Add(self.lblname, 0, wx.ALL, 5)
        self.MainSizer.Add(self.lbl_runtimes, 0, wx.ALL, 5)
        self.MainSizer.Add(self._counter, 0, wx.CENTER, 5)
        self.MainSizer.Add(self.btnRun, 0, wx.ALL, 5)




        self.SetSizer(self.MainSizer)




        self.Bind(EVT_COUNT, self.OnCount)
        self.Bind(EVT_RECV, self.OnRecv)
        self.Bind(wx.EVT_CLOSE, self.OnClose)



        self.Show(True)


    def OnRun(self, event):
        self.worker = Countingthread(self, 1)
        self.worker.start()

    def OnCount(self, event):
        val = int(self._counter.GetLabel()) + event.GetValue()
        self._counter.SetLabel(unicode(val))

    def OnRecv(self, event):
        print "RX", event.GetValue()
        self.lblname.SetLabel(event.GetValue())

    def on_timer(self, event):
        self.cnt_1 = self.cnt_1 + 1
        self.lbl_runtimes.Label = str(self.cnt_1)

    def OnClose(self, event):
        self.worker.stop()
        self.worker.join(10)

        self.Destroy()





app = wx.App(False)
frame = MyFrame(None, 'Small editor')
app.MainLoop()

