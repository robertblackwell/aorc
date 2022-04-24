import sys
import os
import curses
import subprocess
__version__ = "0.6.0"

# print(sys.path)

from simple_curses import *
from pyfiglet import Figlet

def aorc_banner():
    """
    This function returns an List[str] containing a 'banner' for the aorc app
    """
    def string_pad_both_ends(candidate, length):
        s = candidate
        while len(s) < length:
            s = s + " "
            if len(s) < length:
                s = " " + s
        return s
    def string_pad_right(candidate, length):
        s = candidate
        while len(s) < length:
            s = s + " "
        return s

    def fig_it(astr):
        c = Figlet(font="big")
        s = c.renderText(astr)
        lines = s.split('\n')
        return lines

    def longest_line(lines):
        max = 0
        for line in lines:
            len(line)
            max = len(line) if len(line) > max else max
        return max
    
    def pad_fig(lines):
        newlines = []
        length = longest_line(lines)
        for line in lines:
            newlines.append(string_pad_right(line, length))
        return newlines

    banner_lines = [
                "****************************************************",
                "*                      AORC                        *",
                "*                                                  *",
                "*    For issues with this script, please reach     *",
                "*              out to Fred TheCoder                *",
                "*                                                  *",
                "*             fred@the_coder.io                    *",
                "****************************************************",
    ]
    last_line = "****************************************************"
    aorc_v_line =  string_pad_both_ends("Aorc version v{}".format(__version__), len(last_line))
    sc_vline =    string_pad_both_ends("simple_curses version v{}".format(simple_curses_version()), len(last_line))
    banner_lines.append(aorc_v_line)
    banner_lines.append(sc_vline)
    figs = fig_it("AORC")
    good_figs = []
    for line in figs:
        good_figs.append(string_pad_both_ends(line, len(last_line)))
    
    good_figs.append(aorc_v_line)
    good_figs.append(sc_vline)
    return good_figs

