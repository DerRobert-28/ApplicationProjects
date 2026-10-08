##
##	==== IMPORTS ====
##

from random	import randint, seed;
from sys	import exit as sys_exit;
from time	import time;
from types	import TracebackType;
from typing	import Final;

##
##	==== STRING CONSTANTS ====
##

EMPTY:			Final[str]			= "";
INPUT_PROMPT:	Final[str]			= "YOU: ";
LINE_NUMBER:	Final[str]			= "tb_lineno";
NEWLINE:		Final[str]			= "\n";
NULL:			Final[int]			= 0;
OUTPUT_PROMPT:	Final[str]			= "BOT: ";
TRIM:			Final[str]			= "\0\a\b\f\n\r\t\v\x20";
VERSION:		Final[str]			= "0.0";

##
##	==== LOGO CONSTANTS ====
##

APPLICATION_LINE:	Final[str]	= f"PyChatBot - Version: {VERSION}";
UNDER_LINE: 		Final[str]	= "-" * len(APPLICATION_LINE);

##
##	==== COMMAND CONSTANTS ====
##

EXIT_CMD:	Final[str] = "/x";
HELP_CMD:	Final[str] = "/h";
QUEST_CMD:	Final[str] = "/?";
QUIT_CMD:	Final[str] = "/q";

##
##	==== FUNCTION DEBUGERRORCODE() ====
##

def debugErrorCode(exception: Exception) -> int:
	result: int = getErrorCode(exception);
	print(f"{NEWLINE}Error in source line: {result}.");
	print("Press ENTER to continue ...");
	input();
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
	print("Hit ALT+ENTER to switch between fullscreen and window.");
	print();
	print(f"Enter {EXIT_CMD} or {QUIT_CMD} to quit the programme.");
	print(f"Enter {HELP_CMD} or {QUEST_CMD} for help.");
	print();
	return;

##
##	==== FUNCTION MAIN() ====
##

def main() -> int:
	answer: str = EMPTY;
	answers: list[str] = [];
	command: str = EMPTY;
	exitCode: int = NULL;
	index: int = NULL;
	isRunning: bool = True;

	try:
		seed(milliTimer());
		showLogo();
		help();
		print(f"Enjoy!{NEWLINE * 2}");

		while isRunning:
			answer = input(INPUT_PROMPT);
			answer = answer.strip(TRIM);
			command = answer.lower();

			if command.startswith(EXIT_CMD):
				isRunning = False;
			elif command.startswith(HELP_CMD):
				help();
			elif command.startswith(QUEST_CMD):
				help();
			elif command.startswith(QUIT_CMD):
				isRunning = False;
			elif answer:
				answers.append(answer);
				index = randint(1, len(answers));
				print(f"{OUTPUT_PROMPT}{answers[index - 1]}{NEWLINE}");

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
