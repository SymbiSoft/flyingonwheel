#
# fileselector.py
#
# an utility for selecting a file in Series 60, inspired by the filebrowser in Nokia examples
#
# Usage:
#   import fileselector
#   path = fileselector.fileselector()
#
# or to give a default:
#   path = fileselector.fileselector("e:/images/default.jpg")  
#      
# (c) Markku Hänninen (hmm@iki.fi)
#

import sys, os
import appuifw
import e32
import time


class SelectorPath:
    def __init__(self, defaultpath = None):
        self.drivelist = e32.drive_list()
        self.dir = None
        self.file = None
        if defaultpath and os.path.exists(defaultpath):
            if os.path.isdir(defaultpath):
                self.dir = defaultpath
            else:
                (self.dir, self.file) = os.path.split(defaultpath)
    
    def pop(self):
        if not self.dir:
            return
        (newdir, self.file) = os.path.split(self.dir)
        if newdir != self.dir:
            self.dir = newdir
        else:
            self.file = os.path.splitdrive(self.dir)[0]
            self.dir = None
            
    def get(self, idx):
        if self.dir:
            ret =  os.path.join(self.dir, self.dirlist[idx-1])
        else:
            ret = self.dirlist[idx] + os.sep
        return ret
        
    def cd(self, idx):
        self.dir = self.get(idx)
        self.file = None

    def get_list(self):
        cur_idx = 0
        
        if not self.dir:
            entries = [((i, u"Drive")) for i in self.drivelist]
            self.dirlist = self.drivelist
        else:
            def item_format(dir, i):
                full_name = os.path.join(str(dir), i)
                time_field = time.strftime("%d.%m.%Y %H:%M",\
                               time.localtime(os.stat(full_name).st_mtime));
                info_field = time_field+"  "+str(os.stat(full_name).st_size)+"b"
                if os.path.isdir(full_name):
                    name_field = "["+i+"]"
                else:
                    name_field = i
                return (unicode(name_field), unicode(info_field))

            self.dirlist = os.listdir(self.dir)

            entries = [item_format(self.dir, item) for item in self.dirlist]
            
        if self.file:
            try:
                upperlist = [p.upper() for p in self.dirlist]
                cur_idx = upperlist.index(self.file.upper())
            except ValueError:
                pass

        if self.dir:
            entries.insert(0, (u"..", u""))
            cur_idx = cur_idx + 1 # for ".."
            
        return (entries, cur_idx)

    def getdir(self):
        return self.dir

    def __nonzero__(self):
        return self.dir != None


class Fileselector:
    def __init__(self, defaultpath = None):
        self.lock = e32.Ao_lock()
        self.path = SelectorPath(defaultpath)
        self.selected = None

    def run(self):
        from key_codes import EKeyLeftArrow
        (entries, focus) = self.path.get_list()
        self.lb = appuifw.Listbox(entries, self.lbox_observe)
        self.lb.bind(EKeyLeftArrow, lambda: self.lbox_observe(0))
        old_title = appuifw.app.title
        self.lb.set_list(entries, focus)

        self.refresh()
        self.lock.wait()
        appuifw.app.title = old_title
        appuifw.app.body = None
        self.lb = None
        self.lock = None
        return self.selected

    
    def refresh(self):
        appuifw.app.title = u"Select file"
        appuifw.app.menu = [(u"Select current", self.select_handler),
                            (u"New file", self.new_handler)]
        appuifw.app.exit_key_handler = self.exit_key_handler
        appuifw.app.body = self.lb

    def do_exit(self):
        self.exit_key_handler()

    def select_handler(self):
        index = self.lb.current()
        self.selected = self.path.get(index)
        self.lock.signal()

    def new_handler(self):
        data = appuifw.query(u"New file:", "text")
        self.selected = os.path.join(self.path.getdir(), data)
        self.lock.signal()

    def exit_key_handler(self):
        appuifw.app.exit_key_handler = None
        self.lock.signal()

    def lbox_observe(self, ind = None):
        if not ind == None:
            index = ind
        else:
            index = self.lb.current()

        if index == 0 and self.path:                              # ".." selected
            self.path.pop()
        else:
            selected = self.path.get(index)
            if os.path.isdir(selected):
                self.path.cd(index)
            else:
                i = appuifw.popup_menu([u"select"])
                if i == 0:
                    self.selected = selected
                    self.lock.signal()
                    return

        (entries, focus) = self.path.get_list()
        self.lb.set_list(entries, focus)
        

        

def fileselect(defaultpath = None):
    return Fileselector(defaultpath).run()
    

if __name__ == '__main__':
    selection = fileselect(u"e:/images/03122005027.jpg")
    appuifw.note(u"Selected %s" % selection, "info")

    
