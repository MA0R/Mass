"""
Useful classes and methods for GUI with events, timers and threaded tasks.
"""
import threading
import wx
import random
import time

class DataGen(object):
    """ A class that generates pseudo-random data for
        display in the plot.  Taken from
        Eli Bendersky (eliben@gmail.com), Last modified: 31.07.2008
    """
    def __init__(self, init=109):
        self.data = self.init = init
        
    def next(self):
        self._recalc_data()
        return self.data
    
    def _recalc_data(self):
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8: 
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta

class SharedList(object):
    """
    This structure should work for something more complicated. Not necessary for
    just a list?
    """
    def __init__(self, item):
        self.lock = threading.Lock()
        self.item = item
        self.value = [] # this initialisation makes it a list
        
    def add_to_list(self,item): # this method is list specific
        self.lock.acquire()
        self.value.append(item)
        self.lock.release()
        
    def copy_list(self): # need a copy to avoid changes during plotting
        self.lock.acquire()
        a = self.value[:]
        self.lock.release()
        return a
        
    def reset_list(self):
        self.lock.acquire()
        self.value = []
        self.lock.release()

def EVT_RESULT(win, func, EVT):
    """Define Result Event."""
    win.Connect(-1, -1, EVT, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, EVT, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.EVT = EVT
        self.SetEventType(self.EVT)
        self.data = data
        
class RedirectText(object):
    """
    A thread-safe class for redirecting stdout/stderr.
    """
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl
        
    def write(self, string):
        wx.CallAfter(self.out.WriteText, string) #remove CallAfter for no threads.
