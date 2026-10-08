##
##	==== IMPORTS ====
##

from .Tools	import LowerCase, Trim;
from typing	import Callable;

##
##	==== DATA TYPES ====
##

type CommandFunction	= Callable[[]];
type HelpType			= str | tuple[str, ...];

##
##	==== CLASSES ====
##

class Command:
	__function: CommandFunction;
	__helptext: HelpType;
	__shortcut: str;

	def __init__(
			self: Command,
			letter: str,
			helptext: HelpType,
			function: CommandFunction
		) -> None:
		#self.__shortcut = f"/{LowerCase(Trim(letter))}\x20"[:2];
		self.__shortcut = f"/{LowerCase(Trim(letter))}";
		self.__function = function;
		self.__helptext = helptext;
		return;

	def execute(self: Command) -> None:
		self.__function();
		return;

	def getHelpText(self: Command) -> HelpType:
		return self.__helptext;

	def getShortcut(self: Command) -> str:
		return self.__shortcut;

	def canExecute(self: Command, text: str) -> bool:
		shortcut: str = f"{self.getShortcut()}\x20";
		test: str = f"{LowerCase(Trim(text))}\x20";
		return test.startswith(shortcut);
