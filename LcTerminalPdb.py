"""
LcTerminalPdb is a TerminalPdb class modification to better handle list
comprehensions when one lands in the debugger from a breakpoint

See README for info on how to use in code
"""
import sys
import traceback
from IPython.terminal.debugger import TerminalPdb

class LcTerminalPdb(TerminalPdb):
    # the default method is what runs code written to the prompt of the debugger
    def default(self, line):
        # most of this method directly copies the original one, but there's no
        # good way to add the NameError handling separately from the original
        # code
        if line[:1] == '!': line = line[1:]
        locals = self.curframe_locals
        globals = self.curframe.f_globals
        try:
            code = compile(line + '\n', '<stdin>', 'single')
            save_stdout = sys.stdout
            save_stdin = sys.stdin
            save_displayhook = sys.displayhook
            try:
                sys.stdin = self.stdin
                sys.stdout = self.stdout
                sys.displayhook = self.displayhook
                exec(code, globals, locals)
            except NameError:
                # NameError occurs when a list comprehension requires variables
                # to be bound in its closure, but isn't able to because of how
                # exec handles local variables; putting the variable in the
                # global dictionary works, and this code takes the sledgehammer
                # approach of assigning *all* locals to globals, so we don't
                # have to be picky about which variable exactly was needed
                try:
                    tempGlobal = globals.copy()
                    tempGlobal.update(locals)
                    exec(code, tempGlobal, locals)
                except:
                    raise
            finally:
                sys.stdout = save_stdout
                sys.stdin = save_stdin
                sys.displayhook = save_displayhook
        except:
            self._error_exc()

    # TerminalPdb doesn't directly call _error_exc, which was originally defined
    # in Pdb, so we can't import it from there, and it's underscored, so it
    # isn't immediately accessible from TerminalPdb's parent Pdb. However, it's
    # a simple function so I'm just replicating it here.
    def _error_exc(self):
        exc_info = sys.exc_info()[:2]
        self.error(traceback.format_exception_only(*exc_info)[-1].strip())

def set_trace(frame=None):
    """
    Start debugging from `frame`.
    If frame is not specified, debugging starts from caller's frame.
    """
    LcTerminalPdb().set_trace(frame or sys._getframe().f_back)