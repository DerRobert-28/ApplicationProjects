##
##	==== IMPORTS ====
##

from .Tools						import LowerCase, Trim;
from Constants.GeneralConstants	import EmptyString;
from typing						import Callable;

##
##	==== DATA TYPES ====
##

type CommandFunction	= Callable[[str], None];
type HelpType			= str | tuple[str, ...];

##
##	==== CLASSES ====
##

class Command:
	__function: CommandFunction;
	__helptext: HelpType;
	__parameter: str;
	__shortcut: str;

	def __init__(
			self: Command,
			letter: str,
			helptext: HelpType,
			function: CommandFunction
		) -> None:
		self.__function = function;
		self.__helptext = helptext;
		self.__parameter = EmptyString();
		self.__shortcut = LowerCase(Trim(letter));
		return;

	def execute(self: Command) -> None:
		self.__function(self.__parameter);
		return;

	def getHelpText(self: Command) -> HelpType:
		return self.__helptext;

	def getShortcut(self: Command) -> str:
		return self.__shortcut;

	def canExecute(self: Command, text: str) -> bool:
		shortcut: str = self.getShortcut();
		cmdLine = f"{Trim(text)}\x20".split("\x20", 1);
		request: str = LowerCase(cmdLine[0]);
		self.__parameter = Trim(cmdLine[1]);
		return request == shortcut;
