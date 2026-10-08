##
##	==== IMPORTS ====
##

from Components.Language	import *;
from Constants				import *;
from ctypes					import Array, byref, c_uint, c_wchar, create_unicode_buffer, windll;
from os						import makedirs, system as System;
from pathlib				import Path;
from random					import seed;
from time					import time;
from types					import TracebackType;
from typing					import Final;

##
##	==== DATA TYPES ====
##

type ConfigType = dict[str, str];

##
##	==== LOCAL VARIABLES ====
##

__config: ConfigType	= {};
__language: Language	= Language();

##
##	==== GLOBAL FUNCTIONS ====
##

def DebugErrorCode(exception: Exception) -> int:
	errorMessage = __language.getValue(JsonDebugError());
	result: int = __getErrorCode(exception);
	file: str = __getModuleName(exception);
	print(exception);
	print(f"{errorMessage.format(file, result, exception)}\n");
	return result;

def GetConfig() -> ConfigType:
	global __config;
	return __config;

def SetConfig(key: str, value: str) -> None:
	global __config;
	__config[f"{key}"] = f"{value}";
	return;

def GetFolder(fileName: str = __file__) -> str:
	return str(Path(fileName).parent);

def GetSystemLanguage() -> str:
	buffer:			Array[c_wchar];
	bufferLen:		c_uint = c_uint();
	getLanguages:	Final = windll.kernel32.GetUserPreferredUILanguages;
	languageCount:	c_uint = c_uint();
	getLanguages(8, byref(languageCount), None, byref(bufferLen));
	buffer = create_unicode_buffer(bufferLen.value);
	getLanguages(8, byref(languageCount), byref(buffer), byref(bufferLen));
	languages = str(buffer[:]).strip("\0").split("\0");
	return LowerCase(languages[0][0:2]) if languages else "en";

def InputPrompt() -> str:
	prompt = __language.getValue(JsonPromptUser());
	return Trim(input(f"{prompt}>\x20"));

def IsFalsy(value: str) -> bool:
	return LowerCase(Trim(value)) in ["0", "no", "off", "false", "silent"];

def IsMain(name: str) -> bool:
	return "main" in LowerCase(Trim(name));

def IsTruthy(value: str) -> bool:
	return LowerCase(Trim(value)) in ["1", "on", "true", "verbose", "yes"];

def LowerCase(string: str) -> str:
	return string.lower();

def OutputPrompt(text: str, newline: bool = False) -> None:
	prompt = __language.getValue(JsonPromptChat());
	print(f"{prompt}: {text}");
	if newline: print();
	return;

def Randomize() -> None:
	seed(__milliTimer());
	return;

def ReadConfigFile() -> None:
	global __config;
	SetConfigDefaults();
	makedirs(GetSavePath(), exist_ok = True);
	with open(GetConfigFile(), ForAppend(), encoding=DefaultEncoding()): pass;
	with open(GetConfigFile(), ForInput(), encoding=DefaultEncoding()) as file:
		lines: list[str] = file.readlines();
	for line in lines:
		trimmed: str = Trim(LowerCase(line));
		if trimmed.startswith(";"): continue;
		if "=" not in trimmed: continue;
		iniLine = line.split("=", 1);
		key = Trim(iniLine[0]); value = Trim(iniLine[1]);
		__config[key] = value;
	return;

def SaveConfigFile() -> None:
	global __config;
	makedirs(GetSavePath(), exist_ok = True);
	with open(GetConfigFile(), ForOutput(), encoding=DefaultEncoding()) as file:
		for key, value in __config.items():
			configLine: str = f"{key}={value}\n";
			file.write(configLine)
	return;

def SetConfigDefaults() -> None:
	global __config;
	__config[ConfigAutoLoad()] = "false";
	__config[ConfigAutoSave()] = "false";
	__config[ConfigLanguage()] = GetSystemLanguage();
	return;

def SetToolsLanguage(language: Language) -> None:
	global __language;
	__language = language;
	return;

def ShowLogo() -> None:
	jsonHintVersion: str = __language.getValue(JsonHintVersion());
	applicationLine = ApplicationLine(jsonHintVersion);
	System(f"title {applicationLine}");
	print(UnderLine(applicationLine));
	print(applicationLine);
	print(f"{UnderLine(applicationLine)}\n");
	return;

def Trim(string: str) -> str:
	return string.strip("\0\a\b\f\n\r\t\v\x20");

##
##	==== LOCAL FUNCTIONS ====
##

def __getErrorCode(exception: Exception) -> int:
	tb: (TracebackType | None) = exception.__traceback__;
	while True:
		if tb is None: break;
		lineNumber: int = tb.tb_frame.f_code.co_firstlineno;
		if lineNumber: return lineNumber;
		tb = tb.tb_next;
	return 0;

def __getModuleName(exception: Exception) -> str:
	tb: (TracebackType | None) = exception.__traceback__;
	while True:
		if tb is None: break;
		filename: str = tb.tb_frame.f_code.co_filename;
		isPy: bool = filename.endswith(".py");
		isPyw: bool = filename.endswith(".pyw");
		isNoBracket: bool = not filename.startswith("<");
		if (isPy or isPyw) and isNoBracket: return filename;
		tb = tb.tb_next;
	return EmptyString();

def __milliTimer() -> int:
	return int(time() * 1000);
