##
##	==== IMPORTS ====
##

from os		import makedirs, path;
from random	import randint, seed;
from sys	import exit as sys_exit;
from time	import time;
from types	import TracebackType;
from typing	import Final;

##
##	==== GENERAL CONSTANTS ====
##

EMPTY:			Final[str]	= "";
FOR_APPEND:		Final[str]	= "a";
FOR_INPUT:		Final[str]	= "r";
FOR_OUTPUT:		Final[str]	= "w";
PROGRESS:		Final[str]	= "chat history";
INPUT_PROMPT:	Final[str]	= "YOU>";
LINE_NUMBER:	Final[str]	= "tb_lineno";
NEWLINE:		Final[str]	= "\n";
NULL:			Final[int]	= 0;
OUTPUT_PROMPT:	Final[str]	= "BOT:";
TRIM:			Final[str]	= "\0\a\b\f\n\r\t\v\x20";
VERSION:		Final[str]	= "0.2";

##
##	==== APPLICATION CONSTANTS ====
##

APPLICATION_LINE:	Final[str]	= f"PyChatBot - Version: {VERSION}";
SAVE_PATH:			Final[str]	= path.expandvars("%appdata%/PyChatBot");
SAVE_FILE:			Final[str]	= "answers.txt";
UNDER_LINE: 		Final[str]	= "-" * len(APPLICATION_LINE);

##
##	==== COMMAND CONSTANTS ====
##

ADD_CMD:		Final[str]	= "/a";
EXIT_CMD:		Final[str]	= "/x";
HELP_CMD:		Final[str]	= "/h";
LOAD_CMD:		Final[str]	= "/l";
MERGE_CMD:		Final[str]	= "/m";
QUESTION_CMD:	Final[str]	= "/?";
QUIT_CMD:		Final[str]	= "/q";
SAVE_CMD:		Final[str]	= "/s";
VERSION_CMD:	Final[str]	= "/v";

##
##	==== GLOBAL VARIABLES ====
##

answers:	list[str] = [];
isRunning:	bool = True;

##
##	==== FUNCTION COULDEXECUTECOMMAND() ====
##

def couldExecuteCommand(command: str) -> bool:
	global answers, isRunning;

	try:
		command = command.strip(TRIM).lower();
		result: bool = True;
		#
		#	/a
		#
		if command.startswith(ADD_CMD):
			makedirs(SAVE_PATH, exist_ok = True);
			with open(f"{SAVE_PATH}/{SAVE_FILE}", FOR_APPEND) as file:
				file.writelines(f"{answer}{NEWLINE}" for answer in answers);
			print(f"{OUTPUT_PROMPT} Saving {PROGRESS} was successful :-){NEWLINE}")
		#
		#	/q or /x
		#
		elif command.startswith((EXIT_CMD, QUIT_CMD)):
			isRunning = False;
		#
		#	/h or /?
		#
		elif command.startswith((HELP_CMD, QUESTION_CMD)):
			help();
		#
		#	/l
		#
		elif command.startswith(LOAD_CMD):
			makedirs(SAVE_PATH, exist_ok = True);
			if path.isfile(f"{SAVE_PATH}/{SAVE_FILE}"):
				with open(f"{SAVE_PATH}/{SAVE_FILE}", FOR_INPUT) as file:
					answers = [answer.strip(TRIM) for answer in file];
				print(f"{OUTPUT_PROMPT} Loading {PROGRESS} was successful :-){NEWLINE}")
			else:
				print(f"{OUTPUT_PROMPT} No {PROGRESS} found :-({NEWLINE}")
		#
		#	/m
		#
		elif command.startswith(MERGE_CMD):
			makedirs(SAVE_PATH, exist_ok = True);
			if path.isfile(f"{SAVE_PATH}/{SAVE_FILE}"):
				with open(f"{SAVE_PATH}/{SAVE_FILE}", FOR_INPUT) as file:
					answers.extend(answer.strip(TRIM) for answer in file);
				print(f"{OUTPUT_PROMPT} Merging {PROGRESS} was successful :-){NEWLINE}")
			else:
				print(f"{OUTPUT_PROMPT} No {PROGRESS} found :-({NEWLINE}")
		#
		#	/s
		#
		elif command.startswith(SAVE_CMD):
			makedirs(SAVE_PATH, exist_ok = True);
			with open(f"{SAVE_PATH}/{SAVE_FILE}", FOR_OUTPUT) as file:
				file.writelines(f"{answer}{NEWLINE}" for answer in answers);
			print(f"{OUTPUT_PROMPT} Saving {PROGRESS} was successful :-){NEWLINE}")
		#
		#	/v
		#
		elif command.startswith(VERSION_CMD):
			print(f"{OUTPUT_PROMPT} {APPLICATION_LINE}{NEWLINE}");
		#
		#	unknown command:
		#
		else:
			result = False;

	except Exception as exception:
		debugErrorCode(exception);

	return result;

##
##	==== FUNCTION DEBUGERRORCODE() ====
##

def debugErrorCode(exception: Exception) -> int:
	result: int = getErrorCode(exception);
	print(f"{NEWLINE}Error in source line: {result}.");
	#print("Press ENTER to continue ...");
	#input();
	print();
	return result;

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
##	==== FUNCTION HELP() ====
##

def help() -> None:
	print(f"{NEWLINE}Type something and hit ENTER to talk to the chatbot.");
	print("Hit [ALT+ENTER] to switch between fullscreen and window.");
	print();
	print(f"Enter {LOAD_CMD} to load your {PROGRESS}.");
	print(f"Enter {SAVE_CMD} to save your {PROGRESS}.");
	print(f"Enter {ADD_CMD} to add your current chat to your {PROGRESS}.");
	print(f"Enter {MERGE_CMD} to add your {PROGRESS} to your current chat.");
	print(f"Enter {EXIT_CMD} or {QUIT_CMD} to quit the programme.");
	print(f"Enter {HELP_CMD} or {QUESTION_CMD} for help.");
	print();
	return;

##
##	==== FUNCTION MAIN() ====
##

def main() -> int:
	global answers, isRunning;

	answer: str = EMPTY;
	exitCode: int = NULL;
	index: int = NULL;

	try:
		seed(milliTimer());
		showLogo();
		help();
		print(f"Enjoy!{NEWLINE * 2}");

		while isRunning:
			answer = input(f"{INPUT_PROMPT}\x20");
			answer = answer.strip(TRIM);

			if couldExecuteCommand(answer):
				continue;

			if answer:
				answers.append(answer);
				index = randint(1, len(answers));
				print(f"{OUTPUT_PROMPT} {answers[index - 1]}{NEWLINE}");

	except Exception as exception:
		exitCode = debugErrorCode(exception);

	return exitCode;

##
##	==== FUNCTION MILLITIMER() ====
##

def milliTimer() -> int:
	return int(time() * 1000);

##
##	==== FUNCTION SHOWLOGO() ====
##

def showLogo() -> None:
	print(UNDER_LINE);
	print(APPLICATION_LINE);
	print(f"{UNDER_LINE}{NEWLINE}");
	return;

##
##	==== MAIN ====
##

if __name__ == "__main__":
	sys_exit(main());
