##
##	==== IMPORTS ====
##

from os			import makedirs;
from random		import randint, seed;
from sys		import exit as sys_exit;
from time		import time;
from types		import TracebackType;
from typing		import Final;
from Components	import *;

##
##	==== GLOBAL VARIABLES ====
##

answers:		list[str] = [];
isRunning:		bool = True;
commandList:	list[Command] = [];

##
##	==== FUNCTION ADDCOMMAND() ====
##

def addCommand(letter: str, help: str, function: Callable[[]]) -> None:
	global commandList;
	commandList.append(Command(letter, help, function));
	return;

##
##	==== FUNCTION APPENDFILE() ====
##

def appendFile() -> None:
	global answers;
	try:
		makedirs(SAVE_PATH, exist_ok = True);
		with open(f"{SAVE_PATH}/{SAVE_FILE}", FOR_APPEND) as file:
			file.writelines(f"{answer}{NEWLINE}" for answer in answers);
		print(f"{OUTPUT_PROMPT} Saving conversation was successful :-){NEWLINE}")
	except Exception as exception:
		debugErrorCode(exception);
	return;

##
##	==== FUNCTION COULDEXECUTECOMMAND() ====
##

def couldExecuteCommand(request: str) -> bool:
	global commandList;
	request = LCase(Trim(request));
	for command in commandList:
		shortcut: str = command.getShortcut();
		if request.startswith(shortcut):
			command.execute();
			return True;
	return False;

##
##	==== FUNCTION DEBUGERRORCODE() ====
##

def debugErrorCode(exception: Exception) -> int:
	result: int = getErrorCode(exception);
	print(f"{NEWLINE}Error in source line: {result}.{NEWLINE}");
	return result;

##
##	==== FUNCTION DEBUGHISTORY() ====
##

def debugHistory() -> None:
	global answers;
	for answer in answers:
		print(f"{OUTPUT_PROMPT} {answer}");
	print();
	return;

##
##	==== FUNCTION GETERRORCODE() ====
##

def getErrorCode(exception: Exception) -> int:
	tb: (TracebackType | None) = exception.__traceback__;
	while True:
		if tb is None: break;
		if tb.tb_next is None: break;
		tb = tb.tb_next;
	return getattr(tb, LINE_NUMBER, NULL);

##
##	==== FUNCTION LOADFILE() ====
##

def loadFile() -> None:
	global answers;
	try:
		makedirs(SAVE_PATH, exist_ok = True);
		if path.isfile(f"{SAVE_PATH}/{SAVE_FILE}"):
			with open(f"{SAVE_PATH}/{SAVE_FILE}", FOR_INPUT) as file:
				answers = [Trim(answer) for answer in file];
			print(f"{OUTPUT_PROMPT} Loading history was successful :-){NEWLINE}");
		else:
			print(f"{OUTPUT_PROMPT} No history found :-({NEWLINE}");
	except Exception as exception:
		debugErrorCode(exception);
	return;

##
##	==== FUNCTION MAIN() ====
##

def main() -> int:
	global answers, commandList, isRunning;
	
	request: str = EMPTY;
	response: str = EMPTY;
	exitCode: int = NULL;
	index: int = NULL;

	addCommand("?", f"Show {APPLICATION} help.", showHelp);
	addCommand("*", f"List all conversation answers.", debugHistory);
	addCommand("a", f"Append conversation to history.", appendFile);
	addCommand("h", f"Show {APPLICATION} help.", showHelp);
	addCommand("l", f"Load history (conversation will be overwritten).", loadFile);
	addCommand("m", f"Merge history into conversation.", mergeFile);
	addCommand("q", f"Quit {APPLICATION}.", quitApplication);
	addCommand("s", f"Save conversation (history will be overwritten).", saveFile);
	addCommand("v", f"Show {APPLICATION} version.", showVersion);
	addCommand("x", f"Quit {APPLICATION}.", quitApplication);

	try:
		seed(milliTimer());
		showLogo();
		showHelp();
		print(f"Enjoy!{NEWLINE * 2}");

		while isRunning:
			request = Trim(input(f"{INPUT_PROMPT}\x20"));

			if couldExecuteCommand(request):
				continue;

			if request:
				answers.append(request);
				index		= randint(1, len(answers));
				response	= answers[index - 1];
				print(f"{OUTPUT_PROMPT} {response}{NEWLINE}");

	except Exception as exception:
		exitCode = debugErrorCode(exception);

	return exitCode;

##
##	==== FUNCTION MERGEFILE() ====
##

def mergeFile() -> None:
	global answers;
	try:
		makedirs(SAVE_PATH, exist_ok = True);
		if path.isfile(f"{SAVE_PATH}/{SAVE_FILE}"):
			with open(f"{SAVE_PATH}/{SAVE_FILE}", FOR_INPUT) as file:
				answers.extend(Trim(answer) for answer in file);
			print(f"{OUTPUT_PROMPT} Merging history was successful :-){NEWLINE}");
		else:
			print(f"{OUTPUT_PROMPT} No history found :-({NEWLINE}");
	except Exception as exception:
		debugErrorCode(exception);
	return;

##
##	==== FUNCTION MILLITIMER() ====
##

def milliTimer() -> int:
	return int(time() * 1000);

##
##	==== FUNCTION QUITAPPLICATION() ====
##

def quitApplication() -> None:
	global isRunning;
	isRunning = False;
	return;

##
##	==== FUNCTION SAVEFILE() ====
##

def saveFile() -> None:
	global answers;
	try:
		makedirs(SAVE_PATH, exist_ok = True);
		with open(f"{SAVE_PATH}/{SAVE_FILE}", FOR_OUTPUT) as file:
			file.writelines(f"{answer}{NEWLINE}" for answer in answers);
		print(f"{OUTPUT_PROMPT} Saving conversation was successful :-){NEWLINE}");
	except Exception as exception:
		debugErrorCode(exception);
	return;

##
##	==== FUNCTION SHOWHELP() ====
##

def showHelp() -> None:
	global commandList;

	command: Command;
	shortcut: str;
	helptext: str;

	print(f"{NEWLINE}Type something and hit ENTER to talk to the chatbot.");
	print("Hit [ALT+ENTER] to switch between fullscreen and window.");
	print(f"{NEWLINE}Available commands:");

	for command in commandList:
		shortcut = command.getShortcut();
		helptext = command.getHelpText();
		print(f"\t{shortcut}\t{helptext}");
	
	print();
	return;

##
##	==== FUNCTION SHOWLOGO() ====
##

def showLogo() -> None:
	print(UNDER_LINE);
	print(APPLICATION_LINE);
	print(f"{UNDER_LINE}{NEWLINE}");
	return;

##
##	==== FUNCTION SHOWVERSION() ====
##

def showVersion() -> None:
	print(f"{OUTPUT_PROMPT} {APPLICATION_LINE}{NEWLINE}");
	return;

##
##	==== MAIN ====
##

if __name__ == "__main__":
	sys_exit(main());
