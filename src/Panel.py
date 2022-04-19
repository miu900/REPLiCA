import tkinter as tk
from tkinter import scrolledtext
from tkinter.constants import END


class REPLICA:
    def __init__(self, bun):
        self.root = tk.Tk()
        self.bun = '************************\n'+bun+'\n************************'
        self.cursor = '0.0'
        self.setupUI()
    
    def setupUI(self):
        self.root.title('Replica')
        self.root.geometry('1200x600')
        self.kw_src_label = tk.Label(self.root, text='检索关键字')
        self.kw_tar_label = tk.Label(self.root, text='目标关键字')
        self.bun_bar_label = tk.Label(self.root, text='正文')
        self.rp_srcF_label = tk.Label(self.root, text='被替换词（前向组词）')
        self.rp_tarF_label = tk.Label(self.root, text='替换目标词（前向组词）')
        self.rp_srcB_label = tk.Label(self.root, text='被替换词（后向组词）')
        self.rp_tarB_label = tk.Label(self.root, text='替换目标词（后向组词）')
        self.kw_src_label.place(x=50, y=30)
        self.kw_tar_label.place(x=50, y=80)
        self.rp_srcB_label.place(x=800, y=30)
        self.rp_tarB_label.place(x=800, y=80)
        self.rp_srcF_label.place(x=1000, y=30)
        self.rp_tarF_label.place(x=1000, y=80)
        self.bun_bar_label.place(x=300, y=30)
        self.kw_src = tk.Entry(self.root)
        self.kw_tar = tk.Entry(self.root)
        self.rp_srcB = tk.Entry(self.root)
        self.rp_tarB = tk.Entry(self.root)
        self.rp_srcF = tk.Entry(self.root)
        self.rp_tarF = tk.Entry(self.root)
        self.kw_src.place(x=50, y=50)
        self.kw_tar.place(x=50, y=100)
        self.rp_srcB.place(x=800, y=50)
        self.rp_tarB.place(x=800, y=100)
        self.rp_srcF.place(x=1000, y=50)
        self.rp_tarF.place(x=1000, y=100)
        self.bun_bar = scrolledtext.ScrolledText(self.root, width=60, height=32, wrap="none")
        self.bun_bar.insert(0.0, self.bun)
        self.bun_bar.place(x=280, y=50)
        self.forced_rp = tk.Button(self.root, text='简单替换', command=lambda: self.ForcedReplace())
        self.forced_rp.place(x=50, y=300)
        self.search = tk.Button(self.root, text='顺序查找', command=lambda: self.StepForward())
        self.search.place(x=50, y=150)
        self.allF = tk.Button(self.root, text='全部替换（前向组词）', command=lambda: self.FReplace())
        self.allB = tk.Button(self.root, text='全部替换（后向组词）', command=lambda: self.BReplace())
        self.allB.place(x=800, y=200)
        self.allF.place(x=1000, y=200)
        self.export = tk.Button(self.root, text='导出', command=lambda: self.Export())
        self.export.place(x=1000, y=400)
        self.messagebox = tk.Text(self.root, width=20, height=3)
        self.messagebox.place(x=50, y=250)
    
    def ForcedReplace(self):
        self.bun = self.bun_bar.get(0.0, END)
        self.bun = self.bun.replace(self.kw_src.get(), self.kw_tar.get())
        self.bun_bar.delete(1.0, END)
        self.bun_bar.insert(1.0, self.bun[:-1])
    
    def MessageShow(self, content):
        self.messagebox.delete(1.0, END)
        self.messagebox.insert(1.0, content)
        
    def Export(self):
        StringOut = self.bun_bar.get(0.0, END)
        h = open("./output.txt", 'w', encoding='UTF-8')
        h.write(StringOut)
    
    def FReplace(self):
        self.bun = self.bun_bar.get(0.0, END)
        self.bun = self.bun.replace(self.rp_srcF.get(), self.rp_tarF.get())
        self.bun_bar.delete(1.0, END)
        self.bun_bar.insert(1.0, self.bun[:-1])
        self.bun_bar.see(index=self.cursor)
        
    def BReplace(self):
        self.bun = self.bun_bar.get(0.0, END)
        self.bun = self.bun.replace(self.rp_srcB.get(), self.rp_tarB.get())
        self.bun_bar.delete(1.0, END)
        self.bun_bar.insert(1.0, self.bun[:-1])
        self.bun_bar.see(index=self.cursor)

    def StepForward(self):
        pattern = self.kw_src.get()
        target = self.kw_tar.get()
        if len(pattern) < 1:
            self.MessageShow("被检索关键字不能为空.")
        else:
            flag = 1
            while 1:
                anchor = self.bun_bar.search(pattern, index=self.cursor, stopindex=END)
                if not anchor and flag == 1:
                    flag = 0
                    self.cursor = '1.0'
                    self.bun_bar.see(index=self.cursor)
                    self.MessageShow("已遍历，回到初始位置.")
                elif not anchor and flag == 0:
                    self.MessageShow("检索不到关键字.")
                    self.rp_srcF.delete(0, END)
                    self.rp_srcB.delete(0, END)
                    self.rp_tarF.delete(0, END)
                    self.rp_tarB.delete(0, END)
                    break
                else:
                    F_start_pos = anchor
                    F_end_pos = anchor + '+' + str(len(pattern) + 1) + 'c'
                    B_start_pos = anchor + '-1c'
                    B_end_pos = anchor + '+' + str(len(pattern)) + 'c'
                    self.cursor = anchor + '+1c'
                    self.rp_srcF.delete(0, END)
                    self.rp_srcB.delete(0, END)
                    self.rp_tarF.delete(0, END)
                    self.rp_tarB.delete(0, END)
                    self.rp_srcF.insert(0, self.bun_bar.get(F_start_pos, F_end_pos))
                    self.rp_srcB.insert(0, self.bun_bar.get(B_start_pos, B_end_pos))
                    self.rp_tarF.insert(0, self.rp_srcF.get().replace(pattern, target))
                    self.rp_tarB.insert(0, self.rp_srcB.get().replace(pattern, target))
                    self.bun_bar.tag_delete('tag1')
                    self.bun_bar.tag_add('tag1', F_start_pos, B_end_pos)
                    self.bun_bar.tag_config('tag1', background='yellow')
                    self.bun_bar.see(index=self.cursor)
                    # Not practical self.bun_bar.yview_moveto(self.kw_src.get())
                    break


if __name__ == '__main__':
    in_text = open('input.txt','r',encoding='UTF-8').read()
    Replica = REPLICA(in_text)
    Replica.root.mainloop()
