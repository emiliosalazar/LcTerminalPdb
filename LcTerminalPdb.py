import sys
import traceback
from IPython.terminal.debugger import TerminalPdb

class LcTerminalPdb(TerminalPdb):
    def default(self, line):
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

    # TerminalPdb doesn't directly call this function, so we can't import it
    # from there, and it's underscored, so it isn't immediately accessible from
    # TerminalPdb's parent Pdb. However, it's a simple function so I'm just
    # replicating it here.
    def _error_exc(self):
        exc_info = sys.exc_info()[:2]
        self.error(traceback.format_exception_only(*exc_info)[-1].strip())

def set_trace(frame=None):
    """
    Start debugging from `frame`.
    If frame is not specified, debugging starts from caller's frame.
    """
    debugLC().set_trace(frame or sys._getframe().f_back)