##
##	==== IMPORTS ====
##

from .Constants.GeneralConstants	import DefaultEncoding, EmptyString, ForInput;
from .Constants.JsonConstants		import *;
from .Defaults						import *;
from								json import load as JsonLoad;

##
##	==== CLASSES ====
##

class Language:
	__lang: dict[str, str] = {
		JsonDebugError(): EmptyString(),
		JsonHelpAppend(): EmptyString(),
		JsonHelpAvailable(): EmptyString(),
		JsonHelpHelp(): EmptyString(),
		JsonHelpList(): EmptyString(),
		JsonHelpLoad(): EmptyString(),
		JsonHelpMerge(): EmptyString(),
		JsonHelpQuit(): EmptyString(),
		JsonHelpSave(): EmptyString(),
		JsonHelpVersion(): EmptyString(),
		JsonHintEnjoy(): EmptyString(),
		JsonHintFullscreen(): EmptyString(),
		JsonHintGreeting(): EmptyString(),
		JsonInfoNoHistory(): EmptyString(),
		JsonSuccessAppend(): EmptyString(),
		JsonSuccessLoad(): EmptyString(),
		JsonSuccessMerge(): EmptyString(),
		JsonSuccessSave(): EmptyString(),
	};
	__pwd: str = ".";

	def __init__(self: Language) -> None:
		for __key in self.__lang:
			self.__lang[__key] = __key;
		return;

	def getValue(self: Language, key: str) -> str:
		return self.__lang.get(key, key);

	def printValue(self: Language, key: str, count: int = 0) -> None:
		newlines: str = "\n" * count;
		print(f"{self.getValue(key)}{newlines}");
		return;	

	def setFolder(self: Language, folder: str) -> None:
		self.__pwd = folder;

	def loadLanguage(self: Language, shortcut: str = "en") -> None:
		try:
			fileName = f"{self.__pwd}/Languages/lang{shortcut}.json";
			with open(fileName, ForInput(), encoding = DefaultEncoding()) as file:
				self.__lang = JsonLoad(file);
		except:
			__defaults: Defaults = Defaults();
			for __key in self.__lang:
				self.__lang[__key] = __defaults.getValue(__key);
		return;
