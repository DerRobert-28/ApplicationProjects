##
##	==== IMPORTS ====
##

from .Language							import *;
from Constants.ApplicationConstants		import ApplicationLine, UnderLine;
from Constants.GeneralConstants			import EmptyString;
from Constants.JsonConstants			import JsonDebugError;
from ctypes								import Array, byref, c_uint, c_wchar, create_unicode_buffer, windll;
from pathlib							import Path;
from random								import seed;
from time								import time;
from types								import TracebackType;
from typing								import Final;

##
##	==== LOCAL VARIABLES ====
##

__language: Language = Language();

##
##	==== GLOBAL FUNCTIONS ====
##

def DebugErrorCode(exception: Exception) -> int:
	result: int = __getErrorCode(exception);
	file: str = __getModuleName(exception);
	print(
		__language.getValue(
			JsonDebugError()
		).format(
			file,
			result,
			exception
		)
	);
	print();
	return result;

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

def IsMain(name: str) -> bool:
	return name == "__main__";

def LowerCase(string: str) -> str:
	return string.lower();

def NewLine(text: str, count: int = 1) -> str:
	newline: str = "\n" * count;
	return f"{text}{newline}";

def OutputPrompt(text: str, newline: bool = False) -> None:
	prompt = __language.getValue(JsonPromptChat());
	print(f"{prompt}: {text}");
	if newline: print();
	return;

def Trim(string: str) -> str:
	return string.strip("\0\a\b\f\n\r\t\v\x20");

def Randomize() -> None:
	seed(__milliTimer());
	return;

def SetToolsLanguage(language: Language) -> None:
	global __language;
	__language = language;
	return;

def ShowLogo() -> None:
	jsonHintVersion: str = __language.getValue(JsonHintVersion());
	applicationLine = ApplicationLine(jsonHintVersion);
	print(UnderLine(applicationLine));
	print(applicationLine);
	print(NewLine(UnderLine(applicationLine)));
	return;

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
