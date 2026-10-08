##
##	==== IMPORTS ====
##

from Constants.GeneralConstants	import DefaultEncoding, EmptyString, ForInput;
from Constants.JsonConstants	import *;
from .Defaults					import *;
from							json import load as JsonLoad;

##
##	==== CLASSES ====
##

class Language:
	__lang: dict[str, str] = {
		JsonDebugError()		: EmptyString(),
		JsonErrorAppend()		: EmptyString(),
		JsonErrorCommand()		: EmptyString(),
		JsonErrorLoad()			: EmptyString(),
		JsonErrorMerge()		: EmptyString(),
		JsonErrorSave()			: EmptyString(),
		JsonHelpAppend()		: EmptyString(),
		JsonHelpAvailable()		: EmptyString(),
		JsonHelpBad()			: EmptyString(),
		JsonHelpGood()			: EmptyString(),
		JsonHelpHelp()			: EmptyString(),
		JsonHelpList()			: EmptyString(),
		JsonHelpLoad()			: EmptyString(),
		JsonHelpMerge()			: EmptyString(),
		JsonHelpNew()			: EmptyString(),
		JsonHelpQuit()			: EmptyString(),
		JsonHelpReset()			: EmptyString(),
		JsonHelpSave()			: EmptyString(),
		JsonHelpVersion()		: EmptyString(),
		JsonHintCountAll()		: EmptyString(),
		JsonHintCountDiff()		: EmptyString(),
		JsonHintEnjoy()			: EmptyString(),
		JsonHintFullscreen()	: EmptyString(),
		JsonHintGreeting()		: EmptyString(),
		JsonHintVersion()		: EmptyString(),
		JsonInfoFeedback()		: EmptyString(),
		JsonInfoNoHistory()		: EmptyString(),
		JsonInfoNothing()		: EmptyString(),
		JsonPromptChat()		: EmptyString(),
		JsonPromptUser()		: EmptyString(),
		JsonSuccessAppend()		: EmptyString(),
		JsonSuccessLoad()		: EmptyString(),
		JsonSuccessMerge()		: EmptyString(),
		JsonSuccessReset()		: EmptyString(),
		JsonSuccessSave()		: EmptyString(),
		JsonUnknownStatus()		: EmptyString(),
	};
	__pwd: str = ".";

	def __init__(self: Language) -> None:
		for key in self.__lang:
			self.__lang[key] = key;
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
			defaults: Defaults = Defaults();
			for key in self.__lang:
				self.__lang[key] = defaults.getValue(key);
		return;
