##
##	==== IMPORTS ====
##

from Components	import *;
from Constants	import *;
from sys		import exit as SysExit;
from typing		import Final;

##
##	==== CONSTANTS ====
##

LANGUAGE: Final[Language] = Language();

##
##	==== FUNCTIONS ====
##

def initialize() -> None:
	LANGUAGE.setFolder(GetFolder(__file__));
	LANGUAGE.loadLanguage(GetSystemLanguage());
	##
	##	Share Language:
	##
	SetCommandsLanguage(LANGUAGE);
	SetToolsLanguage(LANGUAGE);
	##
	##	Initialize Components:
	##
	InitCommands();
	Randomize();
	ShowLogo();
	ShowHelp();
	return;

def main() -> int:
	exitCode: int = 0;
	request: str = EmptyString();
	try:
		initialize();
		LANGUAGE.printValue(JsonHintEnjoy(), 2);
		while IsRunning():
			request = InputPrompt();
			if not request: continue;
			if not CouldExecuteCommand(request):
				AddAnswer(request);
				OutputPrompt(GetRandomAnswer(), True);
	except Exception as exception:
		exitCode = DebugErrorCode(exception);
	return exitCode;

##
##	==== MAIN ====
##

if IsMain(__name__):
	SysExit(main());
