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
from typing							import Any, IO;

##
##	==== DATA TYPES ====
##

type CommandTuple	= tuple[str, HelpType, CommandFunction];
type DatType		= tuple[int, str];

##
##	==== LOCAL VARIABLES ====
##

__answers:		list[DatType]	= [];
__commandList:	list[Command]	= [];
__isRunning:	bool			= True;
__language:		Language		= Language();

##
##	==== GLOBAL FUNCTIONS ====
##

def AddAnswer(text: str) -> None:
	global __answers;
	for i in range(0, len(__answers)):
		data: DatType = __answers[i];
		if data[1] == text:
			__answers[i] = (data[0] + 1, data[1]);
			return;
	__answers.append((1, text));
	return;

def CouldExecuteCommand(request: str) -> bool:
	global __commandList;
	for command in __commandList:
		if command.canExecute(request):
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
		makedirs(GetSavePath(), exist_ok = True);
		with __open(GetSaveFile(), ForAppend()) as file:
			for answer in __answers: file.write(__formatAnswer(answer));
		OutputPrompt(__language.getValue(JsonSuccessAppend()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __backupAnsiFile_041() -> None:
	if not path.isfile(GetSaveFile_oldVersion041()): return;
	try:
		with open(GetSaveFile_oldVersion041(), ForInput()) as file:
			with __open(GetSaveFile(), ForAppend()) as appendFile:
				for line in file: appendFile.write(__formatLine(1, line));
		replace(GetSaveFile_oldVersion041(), GetBackupFile_oldVersion041());
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __backupFile_041() -> None:
	if not path.isfile(GetSaveFile_oldVersion041()): return;
	try:
		with __open(GetSaveFile_oldVersion041(), ForInput()) as file:
			with __open(GetSaveFile(), ForAppend()) as appendFile:
				for line in file: appendFile.write(__formatLine(1, line));
		replace(GetSaveFile_oldVersion041(), GetBackupFile_oldVersion041());
	except (UnicodeDecodeError, UnicodeEncodeError):
		__backupAnsiFile_041();
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __debugHistory() -> None:
	global __answers;
	for _, answer in __answers:
		OutputPrompt(answer);
	print();
	return;

def __formatAnswer(answer: DatType) -> str:
	return __formatLine(answer[0], answer[1]);

def __formatLine(count: int, answer: str) -> str:
	return f"{count},{Trim(answer)}\n";

def __getCommandTuples() -> list[CommandTuple]: return [
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
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		__backupFile_041();
		if path.isfile(GetSaveFile()):
			with __open(GetSaveFile(), ForInput()) as file:
				__answers = [__parseLine(answer) for answer in file];
			OutputPrompt(__language.getValue(JsonSuccessLoad()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
		__optimizeAnswers();
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __mergeFile() -> None:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		__backupFile_041();
		if path.isfile(GetSaveFile()):
			with __open(GetSaveFile(), ForInput()) as file:
				__answers.extend(__parseLine(answer) for answer in file);
			OutputPrompt(__language.getValue(JsonSuccessMerge()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
		__optimizeAnswers();
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __open(fileName: str, fileMode: str) -> IO[Any]:
	return open(fileName, fileMode, encoding = DefaultEncoding());

def __optimizeAnswers() -> None:
	global __answers;
	answers: list[DatType] = [];
	answerSet: set[str] = {answer for _, answer in __answers};
	for answer in answerSet:
		count: int = 0;
		for amount, current in __answers:
			if current == answer: count += amount;
		answers.append((count, answer));
	__answers = answers;
	return;

def __parseLine(line: str) -> DatType:
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
		makedirs(GetSavePath(), exist_ok = True);
		with __open(GetSaveFile(), ForOutput()) as file:
			for answer in __answers: file.write(__formatAnswer(answer));
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
