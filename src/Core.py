import tkinter as tk


class Bun:
    def __init__(self, bun):
        self.bun = '********************************************************\n' + bun + '\n********************************************************'
        self.kw_src = ''
        self.kw_tar = ''
        self.message = ''
        self.length = 1
        self.history = ''
        self.cursor = 0
        self.neighbors = []
        self.rp_src = ''
        self.rp_tar = ''
    
    def SetLength(self, length):
        if length in [-2, -1, 0, 1, 2]:
            self.length = length
        else:
            self.Message("Length should be within [-2, 2]. ")
    
    def SetKeywordSrc(self, kw_src):
        self.kw_src = kw_src
    
    def SetKeywordTar(self, kw_tar):
        self.kw_tar = kw_tar
    
    def Message(self, message):
        self.message = message
    
    def StepForward(self):
        if len(self.kw_src) < 1:
            self.Message("Keyword Source cannot be empty. ")
        else:
            a = self.bun.find(self.kw_src, beg=self.cursor + 1)
            if a == -1:
                self.Message("Reach the end. ")
                self.cursor = 0
            else:
                self.cursor = a
                if self.length < 0:
                    self.rp_src = self.bun[self.cursor + self.length:self.cursor]
                    self.rp_tar = self.rp_src.replace(self.kw_src, self.kw_tar)
        self.CursorNeighbor()
    
    def CursorNeighbor(self):
        self.neighbors = self.bun[self.cursor - 50:self.cursor + 50]
    
    def Replace(self):
        self.bun.replace(self.rp_src, self.rp_tar)
        if self.cursor > len(self.bun):
            self.cursor = len(self.bun) - 10
    
    def Display(self):
        pass



