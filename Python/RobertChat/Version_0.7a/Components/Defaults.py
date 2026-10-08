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
		self.__value[JsonDebugError()] = "Error in module '{}' in line {}: {}";
		self.__value[JsonErrorAppend()] = "Answers could not be appended! :-(";
		self.__value[JsonErrorCommand()] = "Unknown command or a typo.";
		self.__value[JsonErrorLoad()] = "Answers could not be loaded! :-(";
		self.__value[JsonErrorMerge()] = "Answers could not be merged! :-(";
		self.__value[JsonErrorSave()] = "Answers could not be saved! :-(";
		self.__value[JsonHelpAppend()] = "Append current answers to saved answers.";
		self.__value[JsonHelpAvailable()] = "Available commands:";
		self.__value[JsonHelpBad()] = "Mark as bad answer.";
		self.__value[JsonHelpGood()] = "Mark as good answer.";
		self.__value[JsonHelpHelp()] = "Show {} help.";
		self.__value[JsonHelpList()] = "List conversation answers ('all'/'count'/'diff'/'total').";
		self.__value[JsonHelpLoad()] = "Load saved answers. Current answers will get lost!";
		self.__value[JsonHelpMerge()] = "Merge saved answers into current conversation.";
		self.__value[JsonHelpNew()] = "Start new conversation.";
		self.__value[JsonHelpQuit()] = "Quit {}.";
		self.__value[JsonHelpReset()] = "Reset all answer probabilities to equal.";
		self.__value[JsonHelpSave()] = "Save current answers. Previous answers will be overwritten!";
		self.__value[JsonHelpVersion()] = "Show current {} version.";
		self.__value[JsonHintCountAll()] = "{} answers altogether.";
		self.__value[JsonHintCountDiff()] = "{} different answers.";
		self.__value[JsonHintEnjoy()] = "Enjoy!";
		self.__value[JsonHintFullscreen()] = "Hit [ALT+ENTER] to switch between fullscreen and window.";
		self.__value[JsonHintGreeting()] = "Just type something and hit ENTER to chat with me.";
		self.__value[JsonHintVersion()] = "Version";
		self.__value[JsonInfoFeedback()] = "Thanks for your feedback.";
		self.__value[JsonInfoNoHistory()] = "No saved answers found! :-(";
		self.__value[JsonInfoNothing()] = "You did not talk to me, yet.";
		self.__value[JsonPromptChat()] = "BOT";
		self.__value[JsonPromptUser()] = "YOU";
		self.__value[JsonSuccessAppend()] = "Appending answers was successful! :-)";
		self.__value[JsonSuccessLoad()] = "Loading answers was successful! :-)";
		self.__value[JsonSuccessMerge()] = "Merging answers was successful! :-)";
		self.__value[JsonSuccessReset()] = "Resetting answer possibilities was successful! :-)";
		self.__value[JsonSuccessSave()] = "Saving answers was successful! :-)";
		self.__value[JsonUnknownStatus()] = "Unknown status.";
		return;

	def getValue(self: Defaults, key: str) -> str:
		return self.__value.get(key, EmptyString());
