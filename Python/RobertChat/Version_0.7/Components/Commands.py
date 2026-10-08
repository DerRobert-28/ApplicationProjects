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
##	==== CONSTANTS ====
##

__POSITIVE:	Final[int] = 2;
__NEUTRAL:	Final[int] = 1;
__NEGATIVE:	Final[int] = -(__POSITIVE + __NEUTRAL);

##
##	==== LOCAL VARIABLES ====
##

__answers:		list[DatType]	= [];
__commandList:	list[Command]	= [];
__isRunning:	bool			= True;
__language:		Language		= Language();
__lastIndex:	int				= -1;

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

def ExecuteCommand(request: str):
	global __commandList;
	if not request.startswith("/"): return;
	request = Trim(f"{request}\x20"[1:]);
	if not request: return;
	for command in __commandList:
		if command.canExecute(request):
			command.execute();
			return;
	OutputPrompt(__language.getValue(JsonErrorCommand()), True);
	return;

def GetRandomAnswer() -> str:
	global __answers, __lastIndex;
	count: int = 0;
	for amount, _ in __answers:
		count += amount;
	if count < 1: return EmptyString();
	randomIndex: int = randint(1, count);
	index: int = 0;
	count = 0;
	for amount, answer in __answers:
		count += amount;
		if count >= randomIndex:
			__lastIndex = index;
			__feedback(__NEUTRAL);
			return answer;
		index += 1;
	return EmptyString();

def InitCommands():
	for shortcut, helptext, function in __getCommandTuples():
		__addCommand(shortcut, helptext, function);

def IsRunning() -> bool:
	global __isRunning;
	return __isRunning;

def ShowHelp(_: str = EmptyString()) -> None:
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
		print(f"\t{shortcut:<16}{output}");
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

def __appendFile(_: str = EmptyString()) -> None:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		__backupFile_041();
		__backupFile_06();
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
			with __open(GetSaveFile_oldVersion06(), ForAppend()) as appendFile:
				for line in file: appendFile.write(__formatAnswerLine(1, line));
		replace(GetSaveFile_oldVersion041(), GetBackupFile_oldVersion041());
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __backupFile_041() -> None:
	if not path.isfile(GetSaveFile_oldVersion041()): return;
	try:
		with __open(GetSaveFile_oldVersion041(), ForInput()) as file:
			with __open(GetSaveFile_oldVersion06(), ForAppend()) as appendFile:
				for line in file: appendFile.write(__formatAnswerLine(1, line));
		replace(GetSaveFile_oldVersion041(), GetBackupFile_oldVersion041());
	except (UnicodeDecodeError, UnicodeEncodeError):
		__backupAnsiFile_041();
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __backupFile_06() -> None:
	if not path.isfile(GetSaveFile_oldVersion06()): return;
	try:
		with __open(GetSaveFile_oldVersion06(), ForInput()) as file:
			with __open(GetSaveFile(), ForAppend()) as appendFile:
				for answer in file: appendFile.write(__formatLine(answer));
		replace(GetSaveFile_oldVersion06(), GetBackupFile_oldVersion06());
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __badAnswer(_: str = EmptyString()) -> None:
	global __answers, __lastIndex;
	if __lastIndex < 0: return;
	if __lastIndex > len(__answers) - 1: return;
	__feedback(__NEGATIVE);
	OutputPrompt(__language.getValue(JsonInfoFeedback()), True);
	return;

def __feedback(points: int) -> None:
	global __answers, __lastIndex;
	if __lastIndex < 0: return;
	if __lastIndex > len(__answers) - 1: return;
	if points == 0: return;
	count, answer = __answers[__lastIndex];
	count += points;
	if count > 0:
		__answers[__lastIndex] = (count, answer);
	else:
		__answers.pop(__lastIndex);
		__lastIndex = -1;
	return;

def __formatAnswer(answer: DatType) -> str:
	return __formatAnswerLine(answer[0], answer[1]);

def __formatAnswerLine(count: int, answer: str) -> str:
	return f"{count},{Trim(answer)}\n";

def __formatLine(text: str) -> str:
	return f"{Trim(text)}\n";

def __getCommandTuples() -> list[CommandTuple]: return [
	("append", JsonHelpAppend(), __appendFile),
	("bad", JsonHelpBad(), __badAnswer),
	("exit", (JsonHelpQuit(), ApplicationName()), __quitApplication),
	("good", JsonHelpGood(), __goodAnswer),
	("help", (JsonHelpHelp(), ApplicationName()), ShowHelp),
	("list", JsonHelpList(), __listAnswers),
	("load", JsonHelpLoad(), __loadFile),
	("merge", JsonHelpMerge(), __mergeFile),
	("new", JsonHelpNew(), __newFile),
	("quit", (JsonHelpQuit(), ApplicationName()), __quitApplication),
	("reset", JsonHelpReset(), __resetWeights),
	("save", JsonHelpSave(), __saveFile),
	("version", (JsonHelpVersion(), ApplicationName()), __showVersion),
];

def __goodAnswer(_: str = EmptyString()) -> None:
	global __answers, __lastIndex;
	if __lastIndex < 0: return;
	if __lastIndex > len(__answers) - 1: return;
	__feedback(__POSITIVE);
	OutputPrompt(__language.getValue(JsonInfoFeedback()), True);
	return;

def __hasFormat(helptext: HelpType) -> bool:
	return isinstance(helptext, tuple);

def __listAnswers(param: str = EmptyString()) -> None:
	global __answers;
	if LowerCase(param) == "all":
		if __answers:
			for count, answer in __answers:
				OutputPrompt(f"[{count}] {answer}");
		else:
			OutputPrompt(__language.getValue(JsonInfoNothing()));
	elif LowerCase(param) in ["count-all", "total"]:
		count: int = 0;
		for amount, _ in __answers:
			count += amount;
		msg: str = __language.getValue(JsonHintCountAll())
		OutputPrompt(msg.format(count));
	elif LowerCase(param) in ["count", "diff"]:
		count: int = len(__answers);
		msg: str = __language.getValue(JsonHintCountDiff())
		OutputPrompt(msg.format(count));
	else:
		if __answers:
			for _, answer in __answers:
				OutputPrompt(answer);
		else:
			OutputPrompt(__language.getValue(JsonInfoNothing()));
	print();
	return;

def __loadFile(_: str = EmptyString()) -> None:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		__backupFile_041();
		__backupFile_06();
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

def __mergeFile(_: str = EmptyString()) -> None:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		__backupFile_041();
		__backupFile_06();
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

def __newFile(_: str = EmptyString()) -> None:
	global __answers;
	__answers = [];
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

def __quitApplication(_: str = EmptyString()) -> None:
	global __isRunning;
	__isRunning = False;
	return;

def __resetWeights(_: str = EmptyString()) -> None:
	global __answers;
	__optimizeAnswers();
	for i in range(0, len(__answers)):
		answer: DatType = __answers[i];
		__answers[i] = (1, answer[1]);
	OutputPrompt(__language.getValue(JsonSuccessReset()), True);
	return;

def __saveFile(_: str = EmptyString()) -> None:
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

def __showVersion(_: str = EmptyString()) -> None:
	jsonHintVersion: str = __language.getValue(JsonHintVersion());
	applicationLine = ApplicationLine(jsonHintVersion);
	OutputPrompt(applicationLine, True);
	return;
