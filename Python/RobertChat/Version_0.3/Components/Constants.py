from typing import Final;
from os		import path;

##
##	==== GENERAL CONSTANTS ====
##

EMPTY:			Final[str]	= "";
FOR_APPEND:		Final[str]	= "a";
FOR_INPUT:		Final[str]	= "r";
FOR_OUTPUT:		Final[str]	= "w";
INPUT_PROMPT:	Final[str]	= "YOU>";
LINE_NUMBER:	Final[str]	= "tb_lineno";
NEWLINE:		Final[str]	= "\n";
NULL:			Final[int]	= 0;
OUTPUT_PROMPT:	Final[str]	= "BOT:";
VERSION:		Final[str]	= "0.4";

##
##	==== APPLICATION CONSTANTS ====
##

APPLICATION:		Final[str]	= "RobertChat";
APPLICATION_LINE:	Final[str]	= f"{APPLICATION} - Version: {VERSION}";
SAVE_PATH:			Final[str]	= path.expandvars(f"%appdata%/{APPLICATION}");
SAVE_FILE:			Final[str]	= "answers.txt";
UNDER_LINE: 		Final[str]	= "-" * len(APPLICATION_LINE);
