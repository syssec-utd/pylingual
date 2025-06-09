"""SCons.Scanner.RC

This module implements the dependency scanner for RC (Interface
Definition Language) files.

"""
__revision__ = 'src/engine/SCons/Scanner/RC.py bee7caf9defd6e108fc2998a2520ddb36a967691 2019-12-17 02:07:09 bdeegan'
import re
import SCons.Node.FS
import SCons.Scanner

def no_tlb(nodes):
    """
    Filter out .tlb files as they are binary and shouldn't be scanned
    """
    return [n for n in nodes if str(n)[-4:] != '.tlb']

def RCScan():
    """Return a prototype Scanner instance for scanning RC source files"""
    res_re = '^(?:\\s*#\\s*(?:include)|.*?\\s+(?:ICON|BITMAP|CURSOR|HTML|FONT|MESSAGETABLE|TYPELIB|REGISTRY|D3DFX)\\s*.*?)\\s*(<|"| )([^>"\\s]+)(?:[>"\\s])*$'
    resScanner = SCons.Scanner.ClassicCPP('ResourceScanner', '$RCSUFFIXES', 'CPPPATH', res_re, recursive=no_tlb)
    return resScanner