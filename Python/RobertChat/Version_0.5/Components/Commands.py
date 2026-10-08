##
##	==== IMPORTS ====
##

from .Command						import *;
from .Language						import *;
from .Tools							import *;
from Constants.ApplicationConstants	import *;
from Constants.GeneralConstants		import *;
from Constants.JsonConstants		import *;
from warnings						import deprecated;
from os								import makedirs, path;
from random							import randint;
from shutil							import copy as ShUtilCopy;
from typing							import Any, IO;

##
##	==== DATA TYPES ====
##

type __commandTuple	= tuple[str, HelpType, CommandFunction];
type __datType		= tuple[int, str];

##
##	==== LOCAL VARIABLES ====
##

__answers_newVersion50:		list[__datType]	= [];
__answers_oldVersion041:	list[str]		= [];
__commandList:				list[Command]	= [];
__isRunning:				bool			= True;
__language:					Language		= Language();

##
##	==== GLOBAL FUNCTIONS ====
##

@deprecated("It will be renamed to 'AddAnswer' in the future.")
def AddAnswer_newVersion50(text: str) -> None:
	global __answers_newVersion50;
	for i in range(0, len(__answers_newVersion50)):
		data: __datType = __answers_newVersion50[i];
		if data[1] == text:
			__answers_newVersion50[i] = (data[0] + 1, data[1]);
			return;
	__answers_newVersion50.append((1, text));
	return;

@deprecated("It will be removed in the future.")
def AddAnswer_oldVersion041(text: str) -> None:
	global __answers_oldVersion041;
	__answers_oldVersion041.append(text);
	return;

def CouldExecuteCommand(request: str) -> bool:
	global __commandList;
	request = LowerCase(request);
	for command in __commandList:
		shortcut: str = command.getShortcut();
		if request.startswith(shortcut):
			command.execute();
			return True;
	return False;

@deprecated("It will be renamed to 'GetRandomAnswer' in the future.")
def GetRandomAnswer_newVersion50() -> str:
	global __answers_newVersion50;
	count: int = 0;
	for amount, _ in __answers_newVersion50:
		count += amount;
	index: int = randint(1, count);
	count = 0;
	for amount, answer in __answers_newVersion50:
		count += amount;
		if count >= index:
			return answer;
	return EmptyString();

@deprecated("It will be removed in the future.")
def GetRandomAnswer_oldVersion041() -> str:
	index: int = randint(1, len(__answers_oldVersion041));
	return __answers_oldVersion041[index - 1];

def InitCommands():
	for shortcut, helptext, function in __getCommandTuples():
		__addCommand(shortcut, helptext, function);

def IsRunning() -> bool:
	global __isRunning;
	return __isRunning;

def ShowHelp() -> None:
	global __commandList, __language;
	command: Command;
	helptext: HelpType;
	shortcut: str;
	print();
	__language.printValue(JsonHintGreeting());
	__language.printValue(JsonHintFullscreen(), 1);
	__language.printValue(JsonHelpAvailable());

	for command in __commandList:
		shortcut = command.getShortcut();
		helptext = command.getHelpText();
		hasFormat: bool = __hasFormat(helptext);
		text: str = helptext[0] if hasFormat else str(helptext);
		output: str = __language.getValue(text);
		if hasFormat: output = output.format(*helptext[1:]);
		print(f"\t{shortcut}\t{output}");
	print();
	return;

def SetCommandsLanguage(language: Language) -> None:
	global __language;
	__language = language;
	return;

##
##	==== LOCAL FUNCTIONS ====
##

def __addCommand(letter: str, help: HelpType, function: CommandFunction) -> None:
	global __commandList;
	__commandList.append(Command(letter, help, function));
	return;

@deprecated("It will be renamed to '__appendFile' in the future.")
def __appendFile_newVersion50() -> None:
	global __answers_newVersion50;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		with __open(GetSaveFile(), ForAppend()) as file:
			file.writelines(NewLine(__formatLine(answer)) for answer in __answers_newVersion50);
		OutputPrompt(__language.getValue(JsonSuccessAppend()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

@deprecated("It will be removed in the future.")
def __appendFile_oldVersion041() -> None:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		with __open(GetSaveFile_oldVersion041(), ForAppend()) as file:
			file.writelines(NewLine(answer) for answer in __answers_oldVersion041);
		OutputPrompt(__language.getValue(JsonSuccessAppend()), True);
	except (UnicodeDecodeError, UnicodeEncodeError):
		OutputPrompt(__language.getValue(JsonErrorAppend()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

@deprecated("It will be renamed to '__debugHistory' in the future.")
def __debugHistory_newVersion50() -> None:
	global __answers_newVersion50;
	for _, answer in __answers_newVersion50:
		OutputPrompt(answer);
	print();
	return;

@deprecated("It will be removed in the future.")
def __debugHistory_oldVersion041() -> None:
	global __answers_oldVersion041;
	for answer in __answers_oldVersion041:
		OutputPrompt(answer);
	print();
	return;

def __formatLine(line: __datType) -> str:
	return f"{line[0]},{line[1]}";

def __getCommandTuples() -> list[__commandTuple]: return [
	("?", (JsonHelpHelp(), ApplicationName()), ShowHelp),
	("*", JsonHelpList(), __debugHistory_newVersion50),
	("a", JsonHelpAppend(), __appendFile_newVersion50),
	("h", (JsonHelpHelp(), ApplicationName()), ShowHelp),
	("l", JsonHelpLoad(), __loadFile),
	("m", JsonHelpMerge(), __mergeFile),
	("q", (JsonHelpQuit(), ApplicationName()), __quitApplication),
	("s", JsonHelpSave(), __saveFile_newVersion50),
	("v", (JsonHelpVersion(), ApplicationName()), __showVersion),
	("x", (JsonHelpQuit(), ApplicationName()), __quitApplication),
];

def __hasFormat(helptext: HelpType) -> bool:
	return isinstance(helptext, tuple);

@deprecated("Multiple versions support won't be available in the future.")
def __loadFile() -> None:
	__loadFile_oldVersion041();
	__loadFile_newVersion50();
	__mergeAnswers();
	return;

@deprecated("It will be renamed to '__loadFile' in the future.")
def __loadFile_newVersion50() -> None:
	global __answers_newVersion50;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile()):
			with __open(GetSaveFile(), ForInput()) as file:
				__answers_newVersion50 = [__parseLine(answer) for answer in file];
			OutputPrompt(__language.getValue(JsonSuccessLoad()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

@deprecated("It will be removed in the future.")
def __loadFile_oldVersion041() -> None:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile_oldVersion041()):
			with __open(GetSaveFile_oldVersion041(), ForInput()) as file:
				__answers_oldVersion041 = [Trim(answer) for answer in file];
			OutputPrompt(__language.getValue(JsonSuccessLoad()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
	except (UnicodeDecodeError, UnicodeEncodeError):
		__loadFileAnsi_oldVersion041();
	except Exception as exception:
		DebugErrorCode(exception);
	return;

@deprecated("It will be removed in the future.")
def __loadFileAnsi_oldVersion041() -> None:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile_oldVersion041()):
			ShUtilCopy(GetSaveFile_oldVersion041(), f"{GetSaveFile_oldVersion041()}.bak")
			with open(GetSaveFile_oldVersion041(), ForInput()) as file:
				__answers_oldVersion041 = [Trim(answer) for answer in file];
			OutputPrompt(__language.getValue(JsonSuccessLoad()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
	except (UnicodeDecodeError, UnicodeEncodeError):
		OutputPrompt(__language.getValue(JsonErrorLoad()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

@deprecated("It will be removed in the future.")
def __mergeAnswers() -> None:
	global __answers_newVersion50;
	global __answers_oldVersion041;
	answers: list[__datType] = [*__answers_newVersion50];
	for answer in __answers_oldVersion041:
		answers.append((1, answer));
	__answers_newVersion50 = answers;
	__optimizeAnswers();
	return;

@deprecated("Multiple versions support won't be available in the future.")
def __mergeFile() -> None:
	__mergeFile_oldVersion041();
	__mergeFile_newVersion50();
	__mergeAnswers();
	return;

@deprecated("It will be renamed to '__mergeFile' in the future.")
def __mergeFile_newVersion50() -> None:
	global __answers_newVersion50;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile()):
			with __open(GetSaveFile(), ForInput()) as file:
				__answers_newVersion50.extend(__parseLine(answer) for answer in file);
			OutputPrompt(__language.getValue(JsonSuccessMerge()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

@deprecated("It will be removed in the future.")
def __mergeFile_oldVersion041() -> None:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile_oldVersion041()):
			with __open(GetSaveFile_oldVersion041(), ForInput()) as file:
				__answers_oldVersion041.extend(Trim(answer) for answer in file);
			OutputPrompt(__language.getValue(JsonSuccessMerge()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
	except (UnicodeDecodeError, UnicodeEncodeError):
		OutputPrompt(__language.getValue(JsonErrorMerge()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __open(fileName: str, fileMode: str) -> IO[Any]:
	return open(fileName, fileMode, encoding = DefaultEncoding());

@deprecated("It will be removed in the future.")
def __optimizeAnswers() -> None:
	global __answers_newVersion50;
	answers: list[__datType] = [];
	answerSet: set[str] = {answer for _, answer in __answers_newVersion50};
	for answer in answerSet:
		count: int = 0;
		for amount, current in __answers_newVersion50:
			if current == answer: count += amount;
		answers.append((count, answer));
	__answers_newVersion50 = answers;
	return;

def __parseLine(line: str) -> __datType:
	answer: str = EmptyString();
	count: int = 1;
	countStr: str = "1";
	trimmed: str = Trim(line);
	datLine = trimmed.split(",", 1);
	if len(datLine) == 1:
		answer = datLine[0];
	if len(datLine) == 2:
		countStr = datLine[0];
		answer = datLine[1];
	if countStr.isdigit():
		count = int(countStr);
	else:
		answer = trimmed;
	count = max(count, 1);
	return count, answer;

def __quitApplication() -> None:
	global __isRunning;
	__isRunning = False;
	return;

@deprecated("It will be renamed to '__saveFile' in the future.")
def __saveFile_newVersion50() -> None:
	global __answers_newVersion50;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		with __open(GetSaveFile(), ForOutput()) as file:
			file.writelines(NewLine(__formatLine(answer)) for answer in __answers_newVersion50);
		OutputPrompt(__language.getValue(JsonSuccessSave()), True);
	except (UnicodeDecodeError, UnicodeEncodeError):
		OutputPrompt(__language.getValue(JsonErrorSave()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

@deprecated("It will be removed in the future.")
def __saveFile_oldVersion041() -> None:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		with __open(GetSaveFile_oldVersion041(), ForOutput()) as file:
			file.writelines(NewLine(answer) for answer in __answers_oldVersion041);
		OutputPrompt(__language.getValue(JsonSuccessSave()), True);
	except (UnicodeDecodeError, UnicodeEncodeError):
		OutputPrompt(__language.getValue(JsonErrorSave()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __showVersion() -> None:
	jsonHintVersion: str = __language.getValue(JsonHintVersion());
	applicationLine = ApplicationLine(jsonHintVersion);
	OutputPrompt(applicationLine, True);
	return;
