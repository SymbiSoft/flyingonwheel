
import e32
import appuifw
import dir_iter
import pyS60uiutil
import os
import os.path
import sys
import re
import socket

class pyFileManagerS60:
    """
    File Manager written in Python for S60 phones.
    Can be used as a standalone application or as a part of another program.
    """
    def __init__(self, title='pyFileManager for S60', my_real_full_name=None):
        self.my_title = unicode(title)
        if my_real_full_name == None:
            self.my_real_full_name = appuifw.app.full_name()
        else:
            self.my_real_full_name = my_real_full_name
        self.screen_size = 'normal'
            
        self.last_find = u'*.jpg'
        self.rexp = None
        self.matches = []
        self.nr_of_matches = 0
        
    #=
    #= Actions menu and corresponding callback functions.
    #=
    def __set_actions_menu(self):
        return [(u'Send',        self.__sendfile),
                (u'Open',        self.__open_with_app),
                (u'Rename',      self.__rename),
                (u'Copy',        self.__copy),
                (u'Move',        self.__move),
                (u'Create dir',  self.__create_dir),
                (u'Delete',      self.__delete),
                (u'Refresh dir', lambda x: None)]

    def __open_with_app(self, selection):
        """
        Opens a file with associated application. For example, JPEG image
        is shown with an image viewer application.
        
        If the file is a Python script it will be executed but the execution
        is not handled automatically by the system.
        """
        full_name = os.path.join(selection[0], selection[1])
        if not os.path.isfile(full_name):
            appuifw.note(u'Not a regular file!', 'error')
            return
        if os.path.splitext(selection[1])[1].lower() == '.py':
            execfile(full_name, globals())
            return
        # If the file is a text file (extension 'txt') and pyEdit has been
        # installed, the user prompted to select either pyEdit or the default
        # system text editor.
        #
        #if os.path.splitext(selection[1])[1].lower() == '.txt':
        #    execfile(full_name, globals())
        #    return
        # How to indicate the document to the pyEdit?
        #
        try:
            appuifw.Content_handler().open(full_name)
        except:
            type, value = sys.exc_info() [:2]
            appuifw.note(unicode(str(type)+'\n'+str(value)), 'error')

    def __ask_non_existing_file_name(self, path, file):
        """
        Prompts for a new file as long as the user types a file name
        that does not exist in the directory 'path' or cancels the operation.
        If the suggested file name 'file' does not exist no prompt is shown.
        """
        msg = u'File with the same name exists. Give a new name!'
        ok = False
        try:
            target = os.path.join(path, file)
            new_name = unicode(file)
            while ok == False:
                if os.path.exists(target):
                    new_name = appuifw.query(msg, 'text', new_name)
                    if new_name == None: return None
                    target = os.path.join(path, new_name)
                else: ok = True
            return target
        except:
            type, value = sys.exc_info() [:2]
            appuifw.note(unicode(str(type)+'\n'+str(value)), 'error')
            return None

    def __rename(self, selection):
        """
        Renames the file in the current directory.
        """
        source = os.path.join(selection[0], selection[1])
        new_name = appuifw.query(u'New name', 'text', unicode(selection[1]))
        target = self.__ask_non_existing_file_name(selection[0], new_name)
        if target == None:
            return        
        try:
            os.rename(source, target)
        except:
            type, value = sys.exc_info() [:2]
            appuifw.note(unicode(str(type)+'\n'+str(value)), 'error')

    def __move(self, source):
        """
        Moves a file from a directory to another directory or to the
        original directory with a new name.
        """
        if not self.screen_size == 'normal':
            #= Inform user in the case the title is not visible.
            appuifw.note(u'Select dest dir', 'info')
        target = self.fb.select(temp_title='Select dest dir')
        if target == None:
            return
        s = os.path.join(source[0], source[1])
        t = self.__ask_non_existing_file_name(target[0], source[1])
        if t == None:
            return
        try:
            os.rename(s, t)
        except:
            type, value = sys.exc_info() [:2]
            appuifw.note(unicode(str(type)+'\n'+str(value)), 'error')

    def __copy(self, source):
        """
        Copies a file from a directory to another directory or to the
        original directory with a new name.
        """
        if not os.path.isfile(os.path.join(source[0], source[1])):
            appuifw.note(u'Not a regular file! Cannot copy.', 'error')
            return
        if not self.screen_size == 'normal':
            #= Inform user in the case the title is not visible.
            appuifw.note(u'Select dest dir', 'info')
        target = self.fb.select(temp_title='Select dest dir')
        if target == None:
            return
        s = os.path.join(source[0], source[1])
        t = self.__ask_non_existing_file_name(target[0], source[1])
        if t == None:
            return
        try:
            e32.file_copy(t, s)
        except:
            type, value = sys.exc_info() [:2]
            appuifw.note(unicode(str(type)+'\n'+str(value)), 'error')

    def __create_dir(self, selection):
        """
        Creates a directory.
        """
        dir_name = appuifw.query(u'Directory name', 'text')
        if dir_name == None:
            return
        full_dir = os.path.join(selection[0], dir_name)
        try:
            os.mkdir(full_dir)
        except:
            type, value = sys.exc_info() [:2]
            appuifw.note(unicode(str(type)+'\n'+str(value)), 'error')

    def __delete(self, selection):
        """
        Removes regular files and directories.
        """
        full_name = os.path.join(selection[0], selection[1])
        q = unicode('Remove ' + full_name + '?')
        cnf = appuifw.query(q, 'query')
        if not cnf:
            return
        try:
            if os.path.isdir(full_name):
                os.rmdir(full_name)
            else:
                os.remove(full_name)
        except:
            type, value = sys.exc_info() [:2]
            appuifw.note(unicode(str(type)+'\n'+str(value)), 'error')

    def __readfile(self, selection):
        fname = os.path.join(selection[0], selection[1])
        mfile = file(fname, 'rb')
        mdata = mfile.read()
        mfile.close()
        return mdata

    def __sendfile(self, selection):
        """
        Send file via BlueTooth, FTP, or email.
        """
        comm_method = 'bluetooth'
        
        if comm_method == None: return                    
        elif comm_method == 'bluetooth':
            try:
                addr, serv = socket.bt_obex_discover()
                if addr == None or serv == None:
                    appuifw.note(u'BlueTooth Discovery Error', 'error')
                    return
                choises = serv.keys()
                choises.sort()
                lst = []
                for x in choises:
                    lst.append(unicode(str(x)+u' #'+str(serv[x])))
                choice = appuifw.popup_menu(lst)
                if choice == None: return
                target = (addr, serv[choises[choice]])
                fname = os.path.join(selection[0], selection[1])
                socket.bt_obex_send_file(target[0], target[1], unicode(fname))
            except socket.error, detail:
                err_msg = u'BlueTooth socket error: ' + unicode(detail)
                appuifw.note(err_msg, 'error')
                return
            appuifw.note(u'File sent', 'conf')

        elif comm_method == 'ftp':
            #
            # Not ready
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port = socket.getservbyname('ftp', 'tcp')
                addr = socket.gethostbyname('kosh.hut.fi')

                print str(addr)
                print str(port)

                s.connect((addr, port))
            except socket.error, detail:
                appuifw.note(u'Communication socket error!\n' + \
                             unicode(detail), 'error')
                return
            appuifw.note(u'File successfully sent', 'conf')
        elif comm_method == 'email':
            # to do
            pass

    #=
    #= Options menu and corresponding callback functions.
    #=
    def __set_options_menu(self):
        return [(u'Current path', self.__show_current_path),
                (u'Find',         self.__find),
                (u'Screen size',  self.__switch_screen),
                (u'Help',         self.__help),
                (u'About',        self.__about)]

    def __show_current_path(self):
        s = self.fb.reveal_current_location()
        if s == None:
            appuifw.note(u'No selection going on', 'error')
        if s == ('', ''):
            msg = '\\\n'
        else:
            s = os.path.split(s[0])
            msg = ''
            while s[1]:
                msg = s[1] + '\\\n' + msg
                s = os.path.split(s[0])
            msg = s[0] + '\n' + msg
        fv = pyS60uiutil.fileViewer('Current path')
        fv.view(msg)
        
    def __match_files(self, arg, dirname, names):
        for item in names:
            if self.rexp.match(item):
                self.matches.append(os.path.join(dirname,item))
                self.nr_of_matches += 1
                    
    def __find(self):
        expr = appuifw.query(u'Find what?', 'text', self.last_find)
        if expr == None: return
        self.last_find = expr
        expr = expr.replace('*', '.*')
        expr = expr.replace('?', '.?')
        self.rexp = re.compile(expr)
        self.matches = []
        self.nr_of_matches = 0
        current_dir = dir_iter.Directory_iter(e32.drive_list())
        entries = current_dir.list_repr()

        drive_selection_list = [u'From all drives']
        for drv in entries:
            drive_selection_list.append(u'From '+unicode(drv[0])+u' drive')
        selected_drv = appuifw.selection_list(drive_selection_list)
        if selected_drv == None: return

        if selected_drv == 0:
            # Scanning of all the drives selected.
            index = 0
            nr_of_drives_to_scan = len(entries)
        else:
            # Only one drive to scan. Probably not the most sophisticated
            # way to handle this situation but it works ;-)
            index = selected_drv - 1
            nr_of_drives_to_scan = index + 1
            
        while index < nr_of_drives_to_scan:
            appuifw.note(u'Scanning drive: ' + \
                         unicode(str(entries[index][0])) + \
                         u'  #' + \
                         unicode(str(index+1)) + \
                         u'/' + \
                         unicode(str(len(entries))),
                         'info')
            os.path.walk(entries[index][0],
                         self.__match_files,
                         None)
            index += 1

        # Show the results
        appuifw.note(u'Scanning completed!', 'info')
        scan_result = 'Number of matches: ' + str(self.nr_of_matches) + u'\n\n'
        for m in self.matches:
            scan_result += '* ' + os.path.normpath(m) + '\n'
        fv = pyS60uiutil.fileViewer('Scanning results', joystick=True)
        fv.view(scan_result)

    def __switch_screen(self):
        if (self.screen_size == 'normal'):
            self.screen_size = 'large'
        else:
            self.screen_size = 'normal'
        self.fb.change_ui_defs(screen=self.screen_size)

    def __help(self):
        my_dir = str(os.path.split(self.my_real_full_name)[0])
        fv = pyS60uiutil.fileViewer('Help on pyFileManager', joystick=True)
        fv.load(os.path.join(my_dir, 'pyfilemans60help.txt'))
        fv.view()

    def __about(self):
        my_dir = str(os.path.split(self.my_real_full_name)[0])
        fv = pyS60uiutil.fileViewer('About pyFileManager')
        fv.load(os.path.join(my_dir, 'pyfilemans60about.txt'))
        fv.view()

    #=
    #= The main functionality
    #=
    def execute(self):
        """
        Executes the pyFileManager object.
        """
        #= Check if the currently installed pyS60uiutil module version is
        #= compatible with this version of pyFileManager.
        if pyS60uiutil.version_compatibility((0,4)) == False:
            msg ='pyS60uiutil\nversion %d.%d.%d\ntoo old' % pyS60uiutil.version
            appuifw.note(unicode(msg), 'error')
            return

        old_app_gui_data = pyS60uiutil.save_current_app_info()
        appuifw.app.title = self.my_title

        appuifw.app.t = None
        appuifw.app.body = None
        appuifw.app.exit_key_handler = None

        actions_menu  = self.__set_actions_menu()
        actions_menul = []
        for i in actions_menu:
            actions_menul.append(i[0])

        self.fb = pyS60uiutil.dirBrowser('Select file',
                                        self.__set_options_menu())
        defpath = None
        refresh = False
        while 1:
            ix  = None
            #= Always use the previous path as a default path
            sel = self.fb.select(defpath, False, refresh)
            if sel == None: #= Means the user has pressed exit key
                break
            if sel[0] == '': #= At root level (drive list) -> no actions
                continue
            ix = appuifw.popup_menu(actions_menul)
            if not ix == None:
                func_name = (actions_menu[ix])[0]
                if sel[1] == '':
                    #= Check whether action is allowed in an empty directory
                    if not ((func_name == u'Create dir') or \
                            (func_name == u'Refresh dir')):
                        appuifw.note(u'Nothing selected', 'error')
                        refresh = False
                        continue
                ((actions_menu[ix])[1])(sel) #= Selected action executed here!
                if (func_name == u'Open') or (func_name == u'Send'):
                    #= After these actions it's not necessary to refresh the
                    #= directory listing since it's is likely up2date.
                    defpath = None
                    refresh = False
                if (func_name == u'Copy') or (func_name == u'Move'):
                    defpath = sel[0]
                    refresh = True
                else:
                    defpath = None
                    refresh = True
            else:
                # Action cancelled.
                pass
        pyS60uiutil.restore_app_info(old_app_gui_data)

#=
#= Used as a standalone application.
#=
if __name__ == '__main__':
    fm = pyFileManagerS60()
    fm.execute()
