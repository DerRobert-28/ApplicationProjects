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
		self.__value[JsonErrorAppend()] = "Conversation could not be saved! :-(";
		self.__value[JsonErrorLoad()] = "History could not be loaded! :-(";
		self.__value[JsonErrorMerge()] = "History could not be merged! :-(";
		self.__value[JsonErrorSave()] = "Conversation could not be saved! :-(";
		self.__value[JsonHelpAppend()] = "Append conversation to history.";
		self.__value[JsonHelpAvailable()] = "Available commands:";
		self.__value[JsonHelpHelp()] = "Show {} help.";
		self.__value[JsonHelpList()] = "List all conversation answers.";
		self.__value[JsonHelpLoad()] = "Load history (conversation will be overwritten).";
		self.__value[JsonHelpMerge()] = "Merge history into conversation.";
		self.__value[JsonHelpQuit()] = "Quit {}.";
		self.__value[JsonHelpSave()] = "Save conversation (history will be overwritten).";
		self.__value[JsonHelpVersion()] = "Show current {} version.";
		self.__value[JsonHintEnjoy()] = "Enjoy!";
		self.__value[JsonHintFullscreen()] = "Hit [ALT+ENTER] to switch between fullscreen and window.";
		self.__value[JsonHintGreeting()] = "Just type something and hit ENTER to chat with me.";
		self.__value[JsonHintVersion()] = "Version";
		self.__value[JsonInfoNoHistory()] = "No history found! :-(";
		self.__value[JsonPromptChat()] = "BOT";
		self.__value[JsonPromptUser()] = "YOU";
		self.__value[JsonSuccessAppend()] = "Appending conversation was successful! :-)";
		self.__value[JsonSuccessLoad()] = "Loading history was successful! :-)";
		self.__value[JsonSuccessMerge()] = "Merging history was successful! :-)";
		self.__value[JsonSuccessSave()] = "Saving conversation was successful! :-)";
		self.__value[JsonUnknownStatus()] = "Unknown status.";
		return;

	def getValue(self: Defaults, key: str) -> str:
		return self.__value.get(key, EmptyString());
