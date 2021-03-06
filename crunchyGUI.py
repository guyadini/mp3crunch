#$Id: sample.py,v 1.2 2004/03/17 04:29:31 mandava Exp $

#This sample program is written as a class. The constructor(the ___init__
#method) is called with a parent widget, to which it adds a
#number of child widgets. The constructor starts by creating a Frame widget.
#A frame is a simple container, and is in this case used to hold the
#button and entry widgets.

MAX_WIDTH=140


from Tkinter import *
import tkFileDialog
import os
from crunch import *

#FIXME - pass to bottom, after passing this as a parameter
root = Tk()
root.title('MP3Crunch!')


def printToOutBox(msg,outBox, tagName=None):
    outBox['state'] = 'normal'
    if tagName: outBox.insert(END, msg+'\n',tagName)
    else: outBox.insert(END, msg+'\n')
    newWidth=max(outBox['width'],len(msg)+5)
    outBox['width']=min(MAX_WIDTH,newWidth)
    outBox['state'] = 'disabled'
    #FIXME - don't use a global parameter
    root.update_idletasks()



class App:
    def __init__(self,parent):

        parent.grid()
        parent.resizable(True,False)
        def keyPressEvent(event):
            self.setDir()

        self.dirName =StringVar()
        self.entry = Entry(parent,textvariable=self.dirName)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind('<Return>',keyPressEvent)


        self.browseButton= Button(parent,text='Browse',command=self.setDir)
        self.browseButton.grid(column=1,row=0,sticky='EW')


        self.fixTagsButton = Button(parent, text='Fix Tags',command=self.fixTags)
        self.fixTagsButton.grid(column=1,row=1,sticky='EW')

        self.dryRunVar = IntVar()
        self.dryRunVar.set(1)
        self.dryRunButton = Checkbutton(parent,text='Dry-run only',
            variable= self.dryRunVar)
        self.dryRunButton.grid(column=0,row=1,sticky='EW')


        self.outBox= Text(parent,)
        self.outBox.grid(column=0,row=2,sticky='NS',columnspan=2)
        self.outBox.tag_config("err", background="yellow", foreground="red")
        self.outBox.tag_config("convert", foreground="blue")
        self.outBox.tag_config("dir", foreground="green")

        self.outBox.insert(END, 'Uncheck dry-run to perform actual tag crunching\n' )
        self.outBox['state']='disabled'

        scrollbar = Scrollbar(parent)
        scrollbar.grid(row=2,column=3,sticky='NS' )

        # attach listbox to scrollbar
        self.outBox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.outBox.yview)

    def setDir(self):
        dirName = tkFileDialog.askdirectory(initialdir=self.dirName.get())
        if os.name=='nt': dirName = dirName.replace('/','\\')
        self.entry.config(width=len(dirName)+5)
        self.dirName.set(dirName)


    def fixTags(self):
        self.outBox['state'] = 'normal'
        self.outBox.delete(0.0,END)
        self.outBox['state'] = 'disabled'
        paramDict={'convertTags' : self.dryRunVar.get()==0, 'print' : True,
         'outputFunc' : printToOutBox, 'printParams' : [self.outBox]}
        crunchRoot(self.entry.get(),paramDict)



app = App(root)

root.mainloop()
