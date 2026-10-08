##
##	==== IMPORTS ====
##

from os import path;

##
##	==== CONSTANT FUNCTIONS ====
##

def ApplicationLine(versionHint: str) -> str:
	return f"{ApplicationName()} - {versionHint}: {GetVersion()}";

def ApplicationName() -> str:
	return "RobertChat";

def GetBackupFile_oldVersion06() -> str:
	return f"{GetSavePath()}answers.06";

def GetBackupFile_oldVersion041() -> str:
	return f"{GetSavePath()}answers.041";

def GetConfigFile() -> str:
	return f"{GetSavePath()}config.ini";

def GetSaveFile() -> str:
	return f"{GetSavePath()}answers.conv";

def GetSaveFile_oldVersion06() -> str:
	return f"{GetSavePath()}answers.dat";

def GetSaveFile_oldVersion041() -> str:
	return f"{GetSavePath()}answers.txt";

def GetSavePath() -> str:
	return path.expandvars(f"%appdata%/{ApplicationName()}{GetVersionPath()}");

def GetVersion() -> str:
	return "0.8";

def GetVersionPath() -> str:
	lastChar: str = GetVersion()[-1];
	if lastChar.isdigit(): return "/";
	return f"/{lastChar}/";

def UnderLine(applicationLine: str) -> str:
	return "-" * len(applicationLine);
