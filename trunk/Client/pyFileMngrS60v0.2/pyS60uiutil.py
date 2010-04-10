#= pyS60uiutil.py - a collection of miscellaneous UI dialogs and utility
#=                  functions for PyS60.
#= Copyright (C) 2005 - 2006 Lasse Huovinen
#=
#= This library is free software; you can redistribute it and/or
#= modify it under the terms of the GNU Lesser General Public
#= License as published by the Free Software Foundation; either
#= version 2.1 of the License, or (at your option) any later version.
#=
#= This library is distributed in the hope that it will be useful,
#= but WITHOUT ANY WARRANTY; without even the implied warranty of
#= MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#= Lesser General Public License for more details.
#=
#= You should have received a copy of the GNU Lesser General Public
#= License along with this library; if not, write to the Free Software
#= Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import os
import appuifw
import e32
import dir_iter

from key_codes import \
     EKeyLeftArrow, EKeyRightArrow, EKeyUpArrow, EKeyDownArrow, EKeyDevice3, \
     EKey0, EKey2, EKey5, EKey8

#=
#= The current version number of the pyS60uiutil module.
#=
version = (0,4,0)

def version_compatibility(required_version):
    """
    Check if the version of the pyEditS60 module is older than required by
    the application utilizing the module. Only the first two most significant
    numbers are checked. The last number only indicates the bug fix level and
    thus compatibility is not an issue.
    """
    if (required_version[0] < version[0]):
        return True
    if (required_version[0] == version[0]):
        if (required_version[1] <= version[1]):
            return True
        else:
            return False
    else:
        return False

#=
#= Functions to save and restore application GUI data.
#=
def save_current_app_info():
    """
    Save the current application GUI data.
    """
    app_info = []
    app_info.append(appuifw.app.title)
    app_info.append(appuifw.app.body)
    app_info.append(appuifw.app.menu)
    app_info.append(appuifw.app.exit_key_handler)
    app_info.append(appuifw.app.screen)
    #= The ones above seem to be present always but
    #= the appuifw.app.t is sometimes missing.
    try:
        app_info.append(appuifw.app.t)
    except AttributeError:
        app_info.append(None)
    return app_info

def restore_app_info(app_info):
    """
    Restore the saved application GUI data.
    """
    appuifw.app.title            = app_info[0]
    appuifw.app.body             = app_info[1]
    appuifw.app.menu             = app_info[2]
    appuifw.app.exit_key_handler = app_info[3]
    appuifw.app.screen           = app_info[4]
    appuifw.app.t                = app_info[5]

#=
#= Directory browser
#=
class dirBrowser:
    """
    Browse the S60 phone directory structure interactively using joystick and
    select a file and/or directory. The user may also define an options
    menu with callback functions.
    Joystick events:
      up    - move up one item in the current listing
      down  - move down one item in the current listing
      left  - go to the parent directory
      right - open currently highlighted item if it is directory
    Keyboard events:
      0 - go to the root directory
      2 - go to top of the current listing
      5 - go to middle of the current listing
      8 - go to bottom of the current listing
    """
    def __init__(self, title='Select', menu=None, screen='normal'):
        self.my_title = unicode(title)
        self.script_lock = e32.Ao_lock()
        self.dir_stack = []
        self.current_dir = dir_iter.Directory_iter(e32.drive_list())
        self.entries = [] #= List of entries in current directory. Used to
                          #= speed up listing as list_repr() reads everything
                          #= from the disk which seems to be slow.
        self.current_index = 0
        self.dir_empty = False
        self.selection = None
        self.user_menu = menu
        self.screen_mode = screen
        self.selection_going_on = False

    def change_ui_defs(self, immediate_activation=True,
                       title=None, menu=None, screen=None):
        """
        Initially defined UI parameters may be changed through this method.
        They may be activated immediately (provided that browsing is going on)
        or for the next selection round.
        """
        if not title == None:
            self.my_title = unicode(title)
        if not menu == None:
            self.user_menu = menu
        if not screen == None:
            self.screen_mode = screen
        if self.selection_going_on and immediate_activation:
            if not title  == None: appuifw.app.title = self.my_title
            if not menu   == None: appuifw.app.menu = self.user_menu
            if not screen == None: appuifw.app.screen = self.screen_mode

    def reveal_current_location(self):
        """
        Returns the current directory and selected directory item provided
        that file browsing is currently active, otherwise None is returned.
        """
        if self.selection_going_on == True:
            if self.current_dir.at_root: return ('', '')
            if self.dir_empty == False:
                return os.path.split(self.current_dir.entry\
                                     (self.lbox.current()))
            else: return (self.current_dir.name(), '')
        else: return None
        
    def release_select(self):
        """
        If there's an active selection going on it can be released using
        method.
        """
        self.__exit_key_handler()
        
    def select(self, default_path=None, reset_index=False,
               refresh_listing=True, temp_title=None):
        """
        The selection will return a tuple containing the selected directory
        file item. The selected file item may also be a directory and
        either part may be empty.

        If the user does not select anything (presses the exit key)
        the return value will be None.

        If the default_path is not given the path from the previous selection
        will be used. In this case the last selected item in the listing will
        be set active unless the user wishes differently (reset_index).
        The content of the directory will be re-read but for the speed
        optimization purposes this is optional (refresh_listing).

        The argument temp_title defines the title for a particular selection
        round.
        """
        #print 'select(' + str(default_path) + ',' + str(reset_index) + ',' +\
        #     str(refresh_listing) + ')'
        
        self.__selecting(temp_title)
        if (not default_path == None) or (self.entries == []):
            #= If default path is given or the entries list is empty then lets
            #= refresh the directory content no matter what the user wishes
            #= to do.
            refresh_listing = True
            self.current_index = 0
            self.dir_stack = []
            self.current_dir = dir_iter.Directory_iter(e32.drive_list())
            self.dir_empty = False
        else:
            if reset_index: self.current_index = 0

        #print 'dp: ' + str(default_path) + ' ix: ' + str(self.current_index)
        
        if refresh_listing:
            self.__open_default_directory(default_path)

        self.lbox = appuifw.Listbox(self.entries, self.__process_user_evt)
        self.lbox.set_list(self.entries, self.current_index)
        self.lbox.bind(EKeyLeftArrow, lambda: self.__process_user_evt('back'))
        self.lbox.bind(EKeyRightArrow, lambda: self.__process_user_evt('next'))
        self.lbox.bind(EKey0, lambda: self.__process_user_evt('rootdir'))
        self.lbox.bind(EKey2, lambda: self.__process_user_evt('top'))
        self.lbox.bind(EKey5, lambda: self.__process_user_evt('middle'))
        self.lbox.bind(EKey8, lambda: self.__process_user_evt('bottom'))
        appuifw.app.body = self.lbox
        
        self.script_lock.wait()
        self.__selected()
        return self.selection

    def __process_user_evt(self, dir=None):
        if self.dir_empty: index = 0
        else: index = self.lbox.current()

        if dir == None:
            #= The user has made up her mind...
            #= Note: if at the root level, return tuple of empty strings
            focused_item = 0
            if self.current_dir.at_root:
                self.selection = ('', '')
            else:
                if self.dir_empty == False:
                    self.selection = \
                                   os.path.split(self.current_dir.entry(index))
                else:
                    self.selection = (self.current_dir.name(), '')
            #= Save dir index for the next selection
            self.current_index = index
            self.script_lock.signal()
            return

        elif dir == 'back':
            #= Go to the parent directory unless already in the root directory.
            if not self.current_dir.at_root:
                focused_item = self.dir_stack.pop()
                self.current_dir.pop()
            else:
                focused_item = index
            self.__read_dir_content()

        elif dir == 'next':
            #= Go to the focused sub-directory provided it's a directory.
            if self.current_dir.at_root:
                self.dir_stack.append(index)
                self.current_dir.add(index)
            elif self.dir_empty: #= No effect
                return
            elif os.path.isdir(self.current_dir.entry(index)):
                self.dir_stack.append(index)
                self.current_dir.add(index)
            else: #= Item not a directory -> no effect
                return
            focused_item = 0
            self.__read_dir_content()

        elif dir == 'top':    focused_item = 0
        elif dir == 'middle': focused_item = len(self.entries) / 2
        elif dir == 'bottom': focused_item = len(self.entries) - 1
        elif dir == 'rootdir':
            self.dir_stack = []
            self.current_dir = dir_iter.Directory_iter(e32.drive_list())
            self.__read_dir_content()
            focused_item = 0
        else: #= Would be a bug
            self.__internal_bug_handler('C')
            return
        self.lbox.set_list(self.entries, focused_item)

    def __read_dir_content(self):
        """
        Reads content of current directory and checks its emptiness.
        """
        self.entries = self.current_dir.list_repr()
        if self.entries == []:
            self.entries.insert(0, (u'<empty>', u''))
            self.dir_empty = True
        else:
            self.dir_empty = False
            if len(self.entries) <= self.current_index:
                self.current_index = len(self.entries) - 1
        
    def __open_default_directory(self, dir=None):
        """
        Parse and set the default directory. If the default directory is not
        given, it does not exist, or there are problems parsing the given
        path then default to the drive selection.
        """
        if dir == None:
            self.__read_dir_content()
            #print 'retA'
            return
        dir = os.path.normpath(dir)
        if not os.path.isdir(dir):
            #= Should raise an exception!
            raise ValueError, 'Given default path not a directory'
            #print 'ERROR: Given default path not a directory'
            #print 'retB'
            return
        drv, path = os.path.splitdrive(dir)
        #print 'dir ' + str(dir) + ' -> '
        #print 'drv ' + str(drv)
        #print 'path ' + str(path)

        self.__read_dir_content()
        index = self.__get_index(drv)
        if index == None: #= Would be a bug!
            self.__internal_bug_handler('A')
            return 
        self.dir_stack.append(index)
        self.current_dir.add(index)
        self.__read_dir_content()

        for item in path.split('\\'):
            if item == u'': continue
            index = self.__get_index(u'['+item+u']')
            if index == None: #= Would be a bug!
                self.__internal_bug_handler('B')
                return 
            self.dir_stack.append(index)
            self.current_dir.add(index)
            self.__read_dir_content()
        #print 'retE'
        return
    
    def __get_index(self, item):
        """
        Find the directory list index of a file or directory name in
        the current directory.
        """
        index = 0
        for entry in self.entries:
            if entry[0] == item: return index
            index += 1
        return None

    def __exit_key_handler(self):
        #= Save the last index for the next selection
        self.selection_going_on = False
        self.current_index = self.lbox.current()
        self.script_lock.signal()
        
    def __selecting(self, temp_title=None):
        """
        Save the GUI parameters of the 'parent program' and set the new ones.
        """
        self.old_app = save_current_app_info()

        self.selection_going_on = True
        if temp_title == None:
            appuifw.app.title = self.my_title
        else:
            appuifw.app.title = unicode(temp_title)
        appuifw.app.screen = self.screen_mode
        if self.user_menu == None:
            appuifw.app.menu = []
        else:
            appuifw.app.menu = self.user_menu
        appuifw.app.exit_key_handler = self.__exit_key_handler
        self.selection = None #= For new selection
        
    def __selected(self):
        """
        Restore the GUI parameters of the 'parent program'.
        """
        self.selection_going_on = False
        restore_app_info(self.old_app)
        self.lbox = None


    def __internal_bug_handler(self, place):
        """
        Reports an internal bug in directory list handling and tries to
        take actions such that normal operation could continue.
        """
        print 'Internal bug encountered at ' + str(place) + \
              '. Setting default directory to root.'
        self.dir_stack = []
        self.current_dir = dir_iter.Directory_iter(e32.drive_list())
        self.__read_dir_content()

#=
#= File viewer
#=
class fileViewer:
    """
    Show a long message on the screen. The message may be given as a
    parameter or it can be read from a file.
    """
    def __init__(self, title=None, font=None, color=None, joystick=False,
                 screen='normal'):
        if title: self.my_title = unicode(title)
        else:     self.my_title = None
        if font:  self.my_font  = unicode(font)
        else:     self.my_font  = None
        self.my_color = color
        self.script_lock = e32.Ao_lock()
        self.loaded_text = None
        self.use_joystick = joystick
        self.screen_mode = screen
        
    def __exit_key_handler(self):
        appuifw.app.exit_key_handler = None # Not needed
        self.script_lock.signal()

    def __set_new_gui(self):
        """
        Save the GUI parameters of the 'parent program' and set the new ones.
        """
        self.old_app = save_current_app_info()
        if self.my_title:
            appuifw.app.title = self.my_title
        appuifw.app.screen = self.screen_mode
        appuifw.app.t = appuifw.Text(u'')
        if self.use_joystick:
            self.stick = jumpTextCursorWithJoystick(appuifw.app.t)
        if self.my_font:
            appuifw.app.t.font = self.my_font
        if self.my_color:
            appuifw.app.t.color = self.my_color
        appuifw.app.body = appuifw.app.t
        appuifw.app.menu = []
        appuifw.app.exit_key_handler = self.__exit_key_handler

    def __read_file(self, file_name):
        mfile = file(file_name, 'r')
        msg = mfile.read()  # Note: reads everything!
        mfile.close()
        return msg.decode('iso-8859-1')

    def load(self, file_name=None):
        """
        Load the message to be viewed from a file.
        """
        if file_name == None: return
        fname = os.path.normpath(file_name)
        if not os.path.isfile(fname):
            # Should raise an exception!
            print 'ERROR: Given file ' + str(file_name) + ' not a regular file'
            return
        try:
            self.loaded_text = self.__read_file(fname)
            # The exception should be catched by the main app!!!
        except UnicodeError, detail:
            appuifw.note(u'Error while reading!\n' + unicode(detail),
                         'error')
        #except:
        #    appuifw.note(u'Error while reading!', 'error')

    def view(self, text=None):
        """
        View the content of the selected file or given text string.
        """
        if not text == None:
            # Message to be shown given as a parameter.
            txt = unicode(text)
        elif self.loaded_text == None:
            # No message to show.
            return
        else:
            # Message loaded from a file.
            txt = self.loaded_text
        self.__set_new_gui()
        appuifw.app.t.set(txt)
        appuifw.app.t.set_pos(0)
        self.script_lock.wait()
        restore_app_info(self.old_app)

#=
#= A dialog for font selection (does not work with PyS60 1.0.0)
#=
class fontSelectionDlg:
    """
    Let the user select a font amongst the fonts supported by the device.
    """
    def __init__(self, title=None, screen='normal'):
        if title: self.my_title = unicode(title)
        else:     self.my_title = u'Select font'
        self.script_lock = e32.Ao_lock()
        self.font = None
        self.screen_mode = screen

    def __show_font_test(self):
        font = appuifw.available_fonts()[self.lbox.current()]
        fv = fileViewer(None, font)
        fv.view(u'This text uses font ' + font)
        
    def __exit_key_handler(self):
        self.font = None
        appuifw.app.exit_key_handler = None # Not needed
        self.script_lock.signal()

    def __selection_handler(self):
        self.font = appuifw.available_fonts()[self.lbox.current()]
        appuifw.app.exit_key_handler = None # Not needed
        self.script_lock.signal()

    def select(self):
        """
        Dialog for font selection. The font name is returned as unicoded
        string. If no selection was made, None is returned.
        """
        self.old_app = save_current_app_info()
        appuifw.app.title = self.my_title
        appuifw.app.screen = self.screen_mode
        appuifw.app.exit_key_handler = self.__exit_key_handler
        appuifw.app.menu = [(u'Test', self.__show_font_test)]

        self.lbox = appuifw.Listbox(appuifw.available_fonts(),
                                    self.__selection_handler)
        appuifw.app.body = self.lbox
        self.script_lock.wait()
        restore_app_info(self.old_app)
        return self.font

#=
#= A dialog for font color selection (does not work with PyS60 1.0.0)
#=
class fontColorSelectionDlg:
    """
    Let the user select the font color from predefined list or make custom
    selection. predef_colors may contain list of color names and their
    respective RGB values:
    predef_colors = [(u'color name 1', (r1, g1, b1)), \
                     (u'color name 2', (r2, g2, b2)), \
				 ... \
                     (u'color name N', (rN, gN, bN)), \
                     (u'Custom',       (r, g, b))]
    custom_index = N #= not N+1
    """
    def __init__(self, title=None, predef_colors=None, custom_index=None,
                 screen='normal'):
        if title: self.my_title = unicode(title)
        else:     self.my_title = u'Select font color'
        self.screen_mode = screen
        self.predef_colors = predef_colors
        self.custom_index = custom_index

        if self.predef_colors:
            self.color_menu = []
            for c in self.predef_colors:
                self.color_menu.append(c[0])
        else:
            self.color_menu = None
        self.initial_custom_color = None
        self.form  = None
        self.color = None
        self.script_lock = e32.Ao_lock()

    def __custom_show_font_test(self):
        if self.color == None:
            return
        fv = fileViewer(None, None, self.color)
        fv.view(u'This text uses font color ' + unicode(str(self.color)))

    def __custom_done(self):
        appuifw.app.exit_key_handler = None
        self.script_lock.signal()

    def __custom_selection_handler(self):
        ix = self.lbox.current()
        label = ['Red', 'Green', 'Blue'][ix] + ' component (0-255)'
        color_lst = []
        for i in range(3): color_lst.append(self.color[i]) 
        old_val = color_lst[ix]
        new_val = 0xffff
        #= The values of the RGB components must belong to range [0-255].
        while (not new_val == None) and ((new_val < 0) or (new_val > 255)):
            new_val = appuifw.query(unicode(label), 'number', old_val)
        if not new_val == None:
            color_lst[ix] = new_val
            self.color = (color_lst[0], color_lst[1], color_lst[2])
        self.__custom_set_rgb_list(ix)

    def __custom_set_rgb_list(self, curr_ix=None):
        color_menu = [(u'Red',   unicode(self.color[0])), \
                      (u'Green', unicode(self.color[1])), \
                      (u'Blue' , unicode(self.color[2])) ]
        if curr_ix:
            self.lbox.set_list(color_menu, curr_ix)
        else:
            self.lbox.set_list(color_menu)
        
    def __custom_selection(self):
        appuifw.app.menu = [(u'Test', self.__custom_show_font_test), \
                            (u'Done', self.__custom_done) ]
        
        if self.initial_custom_color:
            self.color = self.initial_custom_color
        elif self.predef_colors and self.custom_index:
            self.color = self.predef_colors[self.custom_index][1]
        else:
            #= If initial color is not provided then default to black.
            self.color = (0, 0, 0)
        
        self.lbox = appuifw.Listbox([(u'foo', u'bar')], \
                                     self.__custom_selection_handler)
        self.__custom_set_rgb_list()
        appuifw.app.body = self.lbox

    def __predef_show_font_test(self):
        ix = self.lbox.current()
        if ix == self.custom_index:
            return
        color = self.predef_colors[ix][1]
        fv = fileViewer(None, None, color)
        fv.view(u'This text uses font color ' + unicode(str(color)))
        
    def __predef_selection_handler(self):
        ix = self.lbox.current()
        if ix == self.custom_index:
            self.__custom_selection()
        else:
            self.color = self.predef_colors[ix][1]
            appuifw.app.exit_key_handler = None
            self.script_lock.signal()

    def __predef_selection(self):
        appuifw.app.menu = [(u'Test', self.__predef_show_font_test)]
        self.lbox = appuifw.Listbox(self.color_menu,
                                    self.__predef_selection_handler)
        appuifw.app.body = self.lbox

    def __exit_key_handler(self):
        self.color = None
        appuifw.app.exit_key_handler = None
        self.script_lock.signal()

    def select(self, custom_color_default=None):
        """
        Dialog for font color selection. The font color is returned as a
        tuple containing selected RGB values. If no selection was made,
        None is returned.
        """
        self.old_app = save_current_app_info()
        appuifw.app.title = self.my_title
        appuifw.app.screen = self.screen_mode
        appuifw.app.exit_key_handler = self.__exit_key_handler

        #= Update the initial custom color if so requested.
        if custom_color_default:
            self.initial_custom_color = custom_color_default

        if self.color_menu:
            #= Predefined menu given.
            self.__predef_selection()
        else:
            #= Go directly to custom color selection since no predefined
            #= menu defined.
            self.__custom_selection()

        self.script_lock.wait()
        restore_app_info(self.old_app)
        return self.color

#=
#= Cursor jumping with joystick
#=
class jumpTextCursorWithJoystick:
    """
    Idea: once the user presses the joystick the callback functions to
    handle joystick movements are activated. The joystick movements are
    interpreted as follows:
    - up    -> go beginning of document
    - down  -> go end of document
    - left  -> go beginning of line
    - right -> go end of line (finds 'newline')
    - press -> back to normal operation
    It is enough to create this object. It will then work autonomously.
    """
    #= Note:  The joystick movements are passed to the underlying SW and this
    #=        must be taken in the account in the callback functions below!
    #=
    #= Note2: For some reason the callback functions __bol() and __eol()
    #=        are not called properly if the current cursor position is
    #=        either 'in the beginning of document' or 'in the end of
    #=        document'. How to fix this?    
    def __init__(self, text_type):
        """
        text_type is an instance of Text Type (editor UI control) of
        appuifw module.
        """
        self.tt = text_type
        self.tt.bind(EKeyDevice3, self.__set_movements)

    def clear(self):
        """
        Clear joystick bindings.
        """
        self.__reset_movements()
        self.tt.bind(EKeyDevice3, None)

    def resume(self):
        """
        Resume joystick bindings that were cleared using clear().
        """
        self.tt.bind(EKeyDevice3, self.__set_movements)

    def __bol(self):
        """
        Moves cursor to the beginning of the current line.
        """
        self.__reset_movements()
        #= Below, one must be added to the intended position since the
        #= underlying SW moves cursor one position left anyway.
        cpos = self.tt.get_pos()
        if cpos == 0:
            #= Already in the beginning of the very first line.
            self.tt.set_pos(cpos+1)
            return
        if cpos == self.tt.len():
            #= Already in the beginning of the very last line.
            #= FIX: See Note2 above.
            self.tt.set_pos(0)
            return
        cpos -= 1
        while cpos:
            c = self.tt.get(cpos, 1)
            if c == u'\u2029': break #= Newline ('paragraph separator') found.
            cpos -= 1
        if cpos: cpos += 1
        self.tt.set_pos(cpos+1)

    def __eol(self):
        """
        Moves cursor to the end of the current line.
        """
        self.__reset_movements()
        cpos = self.tt.get_pos()
        end  = self.tt.len()
        while cpos < end:
            c = self.tt.get(cpos, 1)
            if c == u'\u2029': break #= Newline ('paragraph separator') found.
            cpos += 1
        #= One must be reduced since the underlying SW will move the cursor
        #= one positiont to right.
        self.tt.set_pos(cpos-1)
    
    def __bod(self):
        """
        Moves the cursor to the beginning of the document.
        """
        self.__reset_movements()
        self.tt.set_pos(0)
    
    def __eod(self):
        """
        Moves the cursor to the end of the document.
        """
        self.__reset_movements()
        self.tt.set_pos(self.tt.len())

    def __set_movements(self):
        """
        Set the callback functions once the user has pressed the joystick.
        """
        self.tt.bind(EKeyLeftArrow,  self.__bol)
        self.tt.bind(EKeyRightArrow, self.__eol)
        self.tt.bind(EKeyUpArrow,    self.__bod)
        self.tt.bind(EKeyDownArrow,  self.__eod)
        self.tt.bind(EKeyDevice3,    self.__reset_movements)
    
    def __reset_movements(self):
        """
        Reset the callback functions. This is 'normal' operation, i.e.,
        the cursor is moved one position once joystick is turned.
        """
        self.tt.bind(EKeyLeftArrow,  None)
        self.tt.bind(EKeyRightArrow, None)
        self.tt.bind(EKeyUpArrow,    None)
        self.tt.bind(EKeyDownArrow,  None)
        self.tt.bind(EKeyDevice3,    self.__set_movements)

#= <skip_sa_test>
#= Stand-alone testing
#=
def _stand_alone_test_dirBrowser():
    fb = dirBrowser('Select a file or directory...')
    default_path = 'C:\\Nokia\\'
    loop_test=True
    while loop_test:
        try:
            #selection = fb.select(default_path, refresh_listing=False)
            selection = fb.select(None)
            #selection = fb.select(None, refresh_listing=False)
            #selection = fb.select(None, True, False)
            #selection = fb.select('C:\\notadir')
        except ValueError, detail:
            print '*** error: ' + str(detail)
            return
        if selection == None:
            print 'Nothing selected'
        else:
            print 'Selected path', str(selection[0])
            print 'Selected file', str(selection[1])
            default_path = selection[0]
        if not appuifw.query(u'Do another selection?', 'query'):
            loop_test = False

def _stand_alone_test_fontSelectionDlg():
    fs = fontSelectionDlg('Select your favorite font')
    font = fs.select()
    if font:
        print u'Selected font ' + font
    else:
        print u'No font selection made'

def _stand_alone_test_fontColorSelectionDlg():
    test_predef_menu = 0
    if test_predef_menu:
	predef_menu = [(u'Black',  (0,0,0)),   \
                       (u'Blue',   (0,0,255)), \
                       (u'Green',  (0,255,0)), \
                       (u'Red',    (255,0,0)), \
                       (u'Custom', (0,255,255))]
	custom_index = 4
    else:
	predef_menu = None
	custom_index = None

    fcs = fontColorSelectionDlg('Select your favorite font color', \
                                predef_menu, custom_index)
    color = fcs.select()
    if color:
        print u'Selected font color ' + unicode(str(color))
    else:
        print u'No font color selection made'

def _stand_alone_test_jumpTextCursorWithJoystick():
    fv = fileViewer('Test', None, None, True)
    fv.view('This is a fairly long text to be show on the screen.\n' + \
            'It should be divided at least on two different lines ' + \
            'in order to make it usable for this test.\n')

if __name__ == '__main__':
    # _stand_alone_test_dirBrowser()
    # _stand_alone_test_fontSelectionDlg()
    # _stand_alone_test_fontColorSelectionDlg()
    # _stand_alone_test_jumpTextCursorWithJoystick()
    pass
