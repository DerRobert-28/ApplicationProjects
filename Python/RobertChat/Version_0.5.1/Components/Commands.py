##
##	==== IMPORTS ====
##

from .Command						import *;
from .Language						import *;
from .Tools							import *;
from Constants.ApplicationConstants	import *;
from Constants.GeneralConstants		import *;
from Constants.JsonConstants		import *;
from os								import makedirs, path, replace;
from random							import randint;
from shutil							import copy as ShUtilCopy;
from typing							import Any, IO;

##
##	==== DATA TYPES ====
##

type __commandTuple	= tuple[str, HelpType, CommandFunction];
type __datType		= tuple[int, str];
type __statusType	= str | Exception;

##
##	==== LOCAL VARIABLES ====
##

__answers:					list[__datType]	= [];
__answers_oldVersion041:	list[str]		= [];
__commandList:				list[Command]	= [];
__isRunning:				bool			= True;
__language:					Language		= Language();

##
##	==== GLOBAL FUNCTIONS ====
##

def AddAnswer(text: str) -> None:
	global __answers;
	for i in range(0, len(__answers)):
		data: __datType = __answers[i];
		if data[1] == text:
			__answers[i] = (data[0] + 1, data[1]);
			return;
	__answers.append((1, text));
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

def GetRandomAnswer() -> str:
	global __answers;
	count: int = 0;
	for amount, _ in __answers:
		count += amount;
	index: int = randint(1, count);
	count = 0;
	for amount, answer in __answers:
		count += amount;
		if count >= index:
			return answer;
	return EmptyString();

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

def __appendFile() -> None:
	global __answers;
	try:
		__backupFile_oldVersion041();
		makedirs(GetSavePath(), exist_ok = True);
		with __open(GetSaveFile(), ForAppend()) as file:
			file.writelines(NewLine(__formatLine(answer)) for answer in __answers);
		OutputPrompt(__language.getValue(JsonSuccessAppend()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __backupFile_oldVersion041() -> None:
	if path.isfile(GetSaveFile_oldVersion041()):
		replace(GetSaveFile_oldVersion041(), GetBackupFile_oldVersion041());
	return;

def __debugHistory() -> None:
	global __answers;
	for _, answer in __answers:
		OutputPrompt(answer);
	print();
	return;

def __formatLine(line: __datType) -> str:
	return f"{line[0]},{line[1]}";

def __getCommandTuples() -> list[__commandTuple]: return [
	("?", (JsonHelpHelp(), ApplicationName()), ShowHelp),
	("*", JsonHelpList(), __debugHistory),
	("a", JsonHelpAppend(), __appendFile),
	("h", (JsonHelpHelp(), ApplicationName()), ShowHelp),
	("l", JsonHelpLoad(), __loadFile),
	("m", JsonHelpMerge(), __mergeFile),
	("q", (JsonHelpQuit(), ApplicationName()), __quitApplication),
	("s", JsonHelpSave(), __saveFile),
	("v", (JsonHelpVersion(), ApplicationName()), __showVersion),
	("x", (JsonHelpQuit(), ApplicationName()), __quitApplication),
];

def __hasFormat(helptext: HelpType) -> bool:
	return isinstance(helptext, tuple);

def __loadFile() -> None:
	status1: __statusType = __loadFile_oldVersion041();
	status2: __statusType = __loadFile_newVersion50();
	if status1 is str:
		OutputPrompt(__language.getValue(status1), True);
	elif status2 is str:
		OutputPrompt(__language.getValue(status2), True);
	elif status1 is Exception:
		DebugErrorCode(status1);
	elif status2 is Exception:
		DebugErrorCode(status2);
	else:
		OutputPrompt(__language.getValue(JsonUnknownStatus()), True);
	__mergeAnswers();
	return;

def __loadFile_newVersion50() -> __statusType:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile()):
			with __open(GetSaveFile(), ForInput()) as file:
				__answers = [__parseLine(answer) for answer in file];
			return JsonSuccessLoad();
		else:
			return JsonInfoNoHistory();
	except Exception as exception:
		return exception;

def __loadFile_oldVersion041() -> __statusType:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile_oldVersion041()):
			with __open(GetSaveFile_oldVersion041(), ForInput()) as file:
				__answers_oldVersion041 = [Trim(answer) for answer in file];
			
			return JsonSuccessLoad();
		else:
			return JsonInfoNoHistory();
	except (UnicodeDecodeError, UnicodeEncodeError):
		return __loadFileAnsi_oldVersion041();
	except Exception as exception:
		return exception;

def __loadFileAnsi_oldVersion041() -> __statusType:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile_oldVersion041()):
			ShUtilCopy(GetSaveFile_oldVersion041(), f"{GetSaveFile_oldVersion041()}.bak")
			with open(GetSaveFile_oldVersion041(), ForInput()) as file:
				__answers_oldVersion041 = [Trim(answer) for answer in file];
			return JsonSuccessLoad();
		else:
			return JsonInfoNoHistory();
	except (UnicodeDecodeError, UnicodeEncodeError):
		return JsonErrorLoad();
	except Exception as exception:
		return exception;

def __mergeAnswers() -> None:
	global __answers;
	global __answers_oldVersion041;
	answers: list[__datType] = [*__answers];
	for answer in __answers_oldVersion041:
		answers.append((1, answer));
	__answers = answers;
	__optimizeAnswers();
	return;

def __mergeFile() -> None:
	__mergeFile_oldVersion041();
	__mergeFile_newVersion50();
	__mergeAnswers();


	status1: __statusType = __mergeFile_oldVersion041();
	status2: __statusType = __mergeFile_newVersion50();
	if status1 is str:
		OutputPrompt(__language.getValue(status1), True);
	elif status2 is str:
		OutputPrompt(__language.getValue(status2), True);
	elif status1 is Exception:
		DebugErrorCode(status1);
	elif status2 is Exception:
		DebugErrorCode(status2);
	else:
		OutputPrompt(__language.getValue(JsonUnknownStatus()), True);
	__mergeAnswers();
	return;

	return;

def __mergeFile_newVersion50() -> __statusType:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile()):
			with __open(GetSaveFile(), ForInput()) as file:
				__answers.extend(__parseLine(answer) for answer in file);
			return JsonSuccessMerge();
		else:
			return JsonInfoNoHistory();
	except Exception as exception:
		return exception;

def __mergeFile_oldVersion041() -> __statusType:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile_oldVersion041()):
			with __open(GetSaveFile_oldVersion041(), ForInput()) as file:
				__answers_oldVersion041.extend(Trim(answer) for answer in file);
			return JsonSuccessMerge();
		else:
			return JsonInfoNoHistory();
	except (UnicodeDecodeError, UnicodeEncodeError):
		OutputPrompt(__language.getValue(JsonErrorMerge()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __mergeFileAnsi_oldVersion041() -> __statusType:
	global __answers_oldVersion041;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile_oldVersion041()):
			ShUtilCopy(GetSaveFile_oldVersion041(), f"{GetSaveFile_oldVersion041()}.bak")
			with open(GetSaveFile_oldVersion041(), ForInput()) as file:
				__answers_oldVersion041.extend(Trim(answer) for answer in file);
			return JsonSuccessLoad();
		else:
			return JsonInfoNoHistory();
	except (UnicodeDecodeError, UnicodeEncodeError):
		return JsonErrorLoad();
	except Exception as exception:
		return exception;

def __open(fileName: str, fileMode: str) -> IO[Any]:
	return open(fileName, fileMode, encoding = DefaultEncoding());

def __optimizeAnswers() -> None:
	global __answers;
	answers: list[__datType] = [];
	answerSet: set[str] = {answer for _, answer in __answers};
	for answer in answerSet:
		count: int = 0;
		for amount, current in __answers:
			if current == answer: count += amount;
		answers.append((count, answer));
	__answers = answers;
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

def __saveFile() -> None:
	global __answers;
	try:
		__backupFile_oldVersion041();
		makedirs(GetSavePath(), exist_ok = True);
		with __open(GetSaveFile(), ForOutput()) as file:
			file.writelines(NewLine(__formatLine(answer)) for answer in __answers);
		OutputPrompt(__language.getValue(JsonSuccessSave()), True);
	except (UnicodeDecodeError, UnicodeEncodeError):
		OutputPrompt(__language.getValue(JsonErrorSave()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

"""
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
"""

def __showVersion() -> None:
	jsonHintVersion: str = __language.getValue(JsonHintVersion());
	applicationLine = ApplicationLine(jsonHintVersion);
	OutputPrompt(applicationLine, True);
	return;
