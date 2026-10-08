from .Tools	import LCase, Trim;
from typing	import Callable;


class Command:

	__function: Callable[[]];
	__helptext: str;
	__shortcut: str;

	def __init__(
			self: Command,
			letter: str,
			helptext: str,
			function: Callable[[]]
		) -> None:
		self.__shortcut = f"/{LCase(Trim(letter))}\x20"[:2];
		self.__function = function;
		self.__helptext = helptext;
		return;

	def execute(self: Command) -> None:
		self.__function();
		return;

	def getHelpText(self: Command) -> str:
		return self.__helptext;

	def getShortcut(self: Command) -> str:
		return self.__shortcut;
