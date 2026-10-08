##
##	==== IMPORTS ====
##

from Constants.GeneralConstants import EmptyString;
from Constants.JsonConstants import *;

##
##	==== CLASSES ====
##

class Defaults:
	__value: dict[str, str] = {};

	def __init__(self: Defaults) -> None:
		self.__value = {
			JsonDebugError()		: "Error in module '{}' in line {}: {}",
			JsonErrorAppend()		: "Answers could not be appended! :-(",
			JsonErrorCommand()		: "Unknown command or a typo.",
			JsonErrorLoad()			: "Answers could not be loaded! :-(",
			JsonErrorMerge()		: "Answers could not be merged! :-(",
			JsonErrorSave()			: "Answers could not be saved! :-(",
			JsonHelpAppend()		: "Append current answers to saved answers.",
			JsonHelpAutoLoad()		: "Set automatic loading 'on' or 'off'.",
			JsonHelpAutoSave()		: "Set automatic saving 'on' or 'off'.",
			JsonHelpAvailable()		: "Available commands:",
			JsonHelpBad()			: "Mark as bad answer.",
			JsonHelpClear()			: "Clear screen content.",
			JsonHelpGood()			: "Mark as good answer.",
			JsonHelpHelp()			: "Show {} help.",
			JsonHelpLanguage()		: "Change user interface language ('de'/'en').",
			JsonHelpList()			: "List conversation answers ('all'/'count'/'diff'/'total').",
			JsonHelpLoad()			: "Load saved answers. Current answers will get lost!",
			JsonHelpMerge()			: "Merge saved answers into current conversation.",
			JsonHelpNew()			: "Start new conversation.",
			JsonHelpQuit()			: "Quit {}.",
			JsonHelpReset()			: "Reset all answer probabilities to equal.",
			JsonHelpSave()			: "Save current answers. Previous answers will be overwritten!",
			JsonHelpVersion()		: "Show current {} version.",
			JsonHintCountAll()		: "{} answers altogether.",
			JsonHintCountDiff()		: "{} different answers.",
			JsonHintEnjoy()			: "Enjoy!",
			JsonHintFullscreen()	: "Hit [ALT+ENTER] to switch between fullscreen and window.",
			JsonHintGreeting()		: "Just type something and hit ENTER to chat with me.",
			JsonHintLanguage()		: "Language has been changed.",
			JsonHintVersion()		: "Version",
			JsonInfoAutoLoadNo()	: "Automatic loading is off.",
			JsonInfoAutoLoadYes()	: "Automatic loading is on.",
			JsonInfoAutoSaveNo()	: "Automatic saving is off.",
			JsonInfoAutoSaveYes()	: "Automatic saving is on.",
			JsonInfoFeedback()		: "Thanks for your feedback.",
			JsonInfoLanguage()		: "User interface language is '{}'.",
			JsonInfoNoHistory()		: "No saved answers found! :-(",
			JsonInfoNothing()		: "You did not talk to me, yet.",
			JsonPromptChat()		: "BOT",
			JsonPromptUser()		: "YOU",
			JsonSuccessAppend()		: "Appending answers was successful! :-)",
			JsonSuccessLoad()		: "Loading answers was successful! :-)",
			JsonSuccessMerge()		: "Merging answers was successful! :-)",
			JsonSuccessReset()		: "Resetting answer possibilities was successful! :-)",
			JsonSuccessSave()		: "Saving answers was successful! :-)",
			JsonUnknownStatus()		: "Unknown status.",
		}
		return;

	def getValue(self: Defaults, key: str) -> str:
		return self.__value.get(key, EmptyString());
