__author__ = 'nobit'

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
