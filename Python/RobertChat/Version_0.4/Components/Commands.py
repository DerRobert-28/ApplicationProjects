##
##	==== IMPORTS ====
##

from .Command							import *;
from .Language							import *;
from .Constants.ApplicationConstants	import *;
from .Constants.GeneralConstants		import *;
from .Constants.JsonConstants			import *;
from .Tools								import *;
from os									import makedirs, path;
from random								import randint;

##
##	==== LOCAL VARIABLES ====
##

__answers:		list[str]		= [];
__commandList:	list[Command]	= [];
__isRunning:	bool			= True;
__language:		Language		= Language();

##
##	==== DATA TYPES ====
##

type __commandTuple = tuple[str, HelpType, CommandFunction];

##
##	==== GLOBAL FUNCTIONS ====
##

def AddAnswer(text: str) -> None:
	global __answers;
	__answers.append(text);
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
	index: int = randint(1, len(__answers));
	return __answers[index - 1];

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
		with open(GetSaveFile(), ForAppend()) as file:
			file.writelines(NewLine(answer) for answer in __answers);
		OutputPrompt(__language.getValue(JsonSuccessAppend()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __debugHistory() -> None:
	global __answers;
	for answer in __answers:
		OutputPrompt(answer);
	print();
	return;

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
	("x", (JsonHelpQuit(), ApplicationName()), __quitApplication)
];

def __hasFormat(helptext: HelpType) -> bool:
	return isinstance(helptext, tuple);

def __loadFile() -> None:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile()):
			with open(GetSaveFile(), ForInput()) as file:
				__answers = [Trim(answer) for answer in file];
			OutputPrompt(__language.getValue(JsonSuccessLoad()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __mergeFile() -> None:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		if path.isfile(GetSaveFile()):
			with open(GetSaveFile(), ForInput()) as file:
				__answers.extend(Trim(answer) for answer in file);
			OutputPrompt(__language.getValue(JsonSuccessMerge()), True);
		else:
			OutputPrompt(__language.getValue(JsonInfoNoHistory()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __quitApplication() -> None:
	global __isRunning;
	__isRunning = False;
	return;

def __saveFile() -> None:
	global __answers;
	try:
		makedirs(GetSavePath(), exist_ok = True);
		with open(GetSaveFile(), ForOutput()) as file:
			file.writelines(NewLine(answer) for answer in __answers);
		OutputPrompt(__language.getValue(JsonSuccessSave()), True);
	except Exception as exception:
		DebugErrorCode(exception);
	return;

def __showVersion() -> None:
	OutputPrompt(ApplicationLine(), True);
	return;
