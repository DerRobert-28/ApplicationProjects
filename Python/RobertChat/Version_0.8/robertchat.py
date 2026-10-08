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
##	==== LOCAL VARIABLES ====
##

__config: ConfigType = {};

##
##	==== FUNCTIONS ====
##

def initialize() -> None:
	global __config;
	ReadConfigFile();
	__config = GetConfig();
	LANGUAGE.setFolder(GetFolder(__file__));
	LANGUAGE.loadLanguage(__config[ConfigLanguage()]);
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
	return;

def showIntroScreen() -> None:
	ShowLogo();
	ShowHelp();
	return;

def main() -> int:
	global __config;
	exitCode: int = 0;
	request: str = EmptyString();
	try:
		initialize();
		if IsTruthy(__config[ConfigAutoLoad()]):
			LoadFile("silent");
		showIntroScreen();
		LANGUAGE.printValue(JsonHintEnjoy(), 2);
		while IsRunning():
			request = InputPrompt();
			if not request: continue;
			if request.startswith("/"):
				ExecuteCommand(request);
				if MustReload(): initialize();
			else:
				answer: str = GetRandomAnswer() or request;
				AddAnswer(request);
				OutputPrompt(answer, True);
	except Exception as exception:
		exitCode = DebugErrorCode(exception);
	return exitCode;

##
##	==== MAIN ====
##

if IsMain(__name__):
	SysExit(main());
