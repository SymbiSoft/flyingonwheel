#=
#= default.py for pyFileManagerS60
#=

#= Do not change. This id has been officially allocated from Symbian.
# SYMBIAN_UID=0x10279730

import sys
import os.path
import appuifw

if __name__ == '__main__':
    #=
    #= Run as a main program.
    #= Force importing from the local directory first.
    #=
    localpath = str(os.path.split(appuifw.app.full_name())[0])
    sys.path  = [localpath] + sys.path
    localpath = os.path.join(localpath, 'my')
    sys.path  = [localpath] + sys.path
    try:
        import pyFileManager
        fm = pyFileManager.pyFileManagerS60()
        fm.execute()
        sys.exit()
    except ImportError, detail:
        appuifw.note(u'pyFileMngr not properly installed - ' +
                     unicode(str(detail)), 'error')
else:
    #=
    #= Run from another script. The path of this script is passed
    #= in the variable __fmgrpath__ from the script executing
    #= this script.
    #=
    #= Force importing from the local directory first.
    #=
    try:
        globals()['__fmgrpath__']
        localpath = os.path.split(globals()['__fmgrpath__'])[0]
        sys.path  = [localpath] + sys.path

        import pyFileManager
        fmngr_full_name = globals()['__fmgrpath__']
        fm = pyFileManager.pyFileManagerS60(my_real_full_name=fmngr_full_name)
        fm.execute()
    except (AttributeError, TypeError), detail:
        #= Most likely__fmgrpath__ == None
        appuifw.note(u'pyFileMngr not properly installed - ' +
                     unicode(str(detail)), 'error')        
    except KeyError, detail:
        #= The executing script has not defined __fmgrpath__ 
        appuifw.note(u'pyFileMngr not properly installed - ' +
                     unicode(str(detail)), 'error')
    except ImportError, detail:
        appuifw.note(u'pyFileMngr not properly installed - ' +
                     unicode(str(detail)), 'error')
