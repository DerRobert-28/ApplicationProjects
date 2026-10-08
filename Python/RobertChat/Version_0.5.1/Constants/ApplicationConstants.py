##
##	==== IMPORTS ====
##

from os				import path;
from warnings		import deprecated;

##
##	==== CONSTANT FUNCTIONS ====
##

def ApplicationLine(versionHint: str) -> str:
	return f"{ApplicationName()} - {versionHint}: {GetVersion()}";

def ApplicationName() -> str:
	return "RobertChat";

def GetBackupFile_oldVersion041() -> str:
	return f"{GetSavePath()}/answers.bak";

def GetSaveFile() -> str:
	return f"{GetSavePath()}/answers.dat";

def GetSaveFile_oldVersion041() -> str:
	return f"{GetSavePath()}/answers.txt";

def GetSavePath() -> str:
	return path.expandvars(f"%appdata%/{ApplicationName()}");

def GetVersion() -> str:
	return "0.5.1";

def UnderLine(applicationLine: str) -> str:
	return "-" * len(applicationLine);
