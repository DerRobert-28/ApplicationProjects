##
##	==== IMPORTS ====
##

from os import path;

##
##	==== FUNCTIONS ====
##

def ApplicationLine()	-> str: return f"{ApplicationName()} - Version: {GetVersion()}";
def ApplicationName()	-> str: return "RobertChat";
def GetSaveFile()		-> str: return f"{GetSavePath()}/answers.txt";
def GetSavePath()		-> str: return path.expandvars(f"%appdata%/{ApplicationName()}");
def GetVersion()		-> str: return "0.4.1";
def UnderLine()			-> str: return "-" * len(ApplicationLine());
