import json
import os

from errbot import BotPlugin, botcmd

from config import BOT_DATA_DIR


# NB: This will produce an error on Windows systems if the BOT_DATA_DIR is something like C:\Users\...
# Due to the fact that \Us is invalid unicode
class Diplomat(BotPlugin):
    """Diplomat plugin for Luvbot"""

    def __init__(self):
        self.diplomat = {}

    def activate(self):
        """
        Triggers on plugin activation
        """
        self.log.info('Activating Diplomat Plugin')
        super(Diplomat, self).activate()

        if "diplomat" not in self:
            self.diplomat = {}

        self.log.info("Loading character database.")
        with open(BOT_DATA_DIR + os.sep + "standings.json", 'r') as infile:
            # read in each file json entry
            # create new value in associative array s.t.
            # diplomat['character_name'] = [tag1, ..., tagn]
            self.diplomat = json.load(infile)

            # self.log.info('Loaded character database successfully.')

    def deactivate(self):
        self.diplomat_save()
        super(Diplomat, self).deactivate()

    @botcmd
    def diplomat_isred(self, message, args):
        # Check to determine if the character name passed to the function is red
        # If it exists in the player_list, return
        self.log.debug("Checking diplomat for name: " + args)
        response = ""
        args = args.lower()
        if args is "":
            response = "Please include a name of a character to check."
        elif args not in self.diplomat:
            response = args + " does not exist in Diplomat."
        else:
            response = args + "\nStanding: " + str(self.diplomat[args]['standing']) + \
                       "\nTags: " + ', '.join(self.diplomat[args]['tags'])
        return response

    @botcmd
    def diplomat_addtag(self, message, args):
        # Adds a tag to a character if it exists in the red list
        # If character does not exist in red list, does nothing
        self.log.info("Attempting to add tag: " + message.body)
        response = ""
        args = args.lower().strip()
        if args is "":
            response = "Please include a tag and character name" + \
                       "\nProper syntax is !diplomat addtag <tag> <name>"
        else:
            first_space_index = args.find(" ")
            if first_space_index == -1:
                name = ""
                tag = args
            else:
                tag = args[0:args.find(" ")].strip()
                # self.log.debug("Tag: " + tag)
                name = args[args.find(" "):len(args)].strip()
                # self.log.debug("Character: " + name)
            if name is "":
                response = "Please include a name of a character to check." + \
                           "\nProper syntax is !diplomat addtag <tag> <name>"
            elif name not in self.diplomat:
                response = "Character " + name + " does not exist in Diplomat."
            else:
                self.diplomat[name]['tags'].append(tag)
                response = "Added tag '" + tag + "' to character '" + name + "'"
                self.diplomat_save()
        return response

    @botcmd
    def diplomat_remtag(self, message, args):
        self.log.info("Attempting to remove tag: " + message.body)
        response = ""
        args = args.lower().strip()
        if args is "":
            response = "Please include a tag and character name" + \
                       "\nProper syntax is !diplomat remtag <tag> <name>"
        else:
            first_space_index = args.find(" ")
            if first_space_index == -1:
                name = ""
                tag = args
            else:
                tag = args[0:args.find(" ")].strip()
                # self.log.debug("Tag: " + tag)
                name = args[args.find(" "):len(args)].strip()
                # self.log.debug("Character: " + name)
            if name is "":
                response = "Please include a name of a character to remove a tag from." + \
                           "\nProper syntax is !diplomat remtag <tag> <name>"
            elif name not in self.diplomat:
                response = "Character " + name + " does not exist in Diplomat."
            else:
                if tag in self.diplomat[name]['tags']:
                    self.diplomat[name]['tags'].remove(tag)
                    response = "Removed tag '" + tag + "' from character '" + name + "'"
                    self.diplomat_save()
                else:
                    response = "Tag '" + tag + "' does not exist for character '" + name + "'"
        return response

    @botcmd
    def diplomat_remchar(self, message, args):
        response = ""
        args = args.lower().strip()
        if args is "":
            response = "Please include the name of a character to remove from Diplomat." + \
                       "\nProper syntax is !diplomat remchar <name>"
        elif args not in self.diplomat:
            response = args + " does not exist in Diplomat."
        else:
            del self.diplomat[args]
            response = "Removed character '" + args + "' from Diplomat."
            self.diplomat_save()
        return response

    @botcmd
    def diplomat_addchar(self, message, args):
        self.log.debug("Adding character to Diplomat with message body: " + args)

        # Initialize blank response
        response = ""

        # Convert message body to lower case and strip whitespace from edges
        args = args.lower().strip()

        # Check to see if arg string is empty; if so, return error message with proper syntax
        if args == "":
            response = "Please include a standing, tag and character name to add to Diplomat." + \
                       "\nProper syntax is !diplomat addchar <standing> <tag> <name>"
        else:
            # arg string is not empty, parse standing from args

            # There are no spaces in input string; we are short input
            if args.find(" ") == -1:
                standing = args
            # There's a whitespace character within the arg string, we can assume we have at least 2 arguments
            else:
                # Grad the standing by taking the substring of [0...i] where i is first whitespace index
                # Trim an remaining whitespace
                standing = args[0:args.find(" ")].strip()

                # Trim standing from arg string
            args = args[args.find(standing) + len(standing):].strip()

            self.log.debug("standing is: " + standing)
            self.log.debug("args is: " + args)

            # Check to see if standing represents a valid float
            # If not valid float, return error message indicating correct syntax for standing
            if not self.is_standing(standing):
                response = "Please include the standing as a valid numeric (-10.0 ... 10.0)" + \
                           "\nProper syntax is !diplomat addchar <standing> <tag> <name>"
            # Standing tag is okay, begin parsing the tag argument from arg string
            else:
                # -1 index of whitespace indicates that there is no more whitespace in arg string
                # Short at least one argument
                if args.find(" ") == -1:
                    tag = args
                else:
                    # Parse tags from [0...i] of args, where i is index of first whitespace
                    # Trim whitespace from tag
                    tag = args[0:args.find(" ")].strip()
                    # Trim tag from arg string, remove whitespace
                args = args[args.find(tag) + len(tag):].strip()
                self.log.debug("tag is: " + tag)
                if tag == "":
                    response = "Please include a single tag for the character that will be added to Diplomat." + \
                               "\nProper syntax is !diplomat addchar <standing> <tag> <name>"
                else:
                    # Parse name from arg string
                    # Name should be only part of arg string remaining
                    name = args
                    if name == "":
                        response = "Please include a name for the character that will be added to Diplomat." + \
                                   "\nProper syntax is !diplomat addchar <standing> <tag> <name>"
                    else:
                        if name not in self.diplomat:
                            self.diplomat[name] = {}
                            self.diplomat[name]['standing'] = standing
                            self.diplomat[name]['tags'] = []
                            self.diplomat[name]['tags'].append(tag)
                            response = "Added Character: '" + args + "'\nStanding: " + str(
                                self.diplomat[args]['standing']) + "\nTags: " + ', '.join(self.diplomat[args]['tags'])
                            self.diplomat_save()
                        else:
                            response = "Character '" + name + "' already exists in Diplomat."
        return response

    @botcmd
    def diplomat_save(self):
        self.log.info('Saving Diplomat to disk.')
        # TODO This probably needs to be fixed to not be shitty and windows bound (though it should work in Linux)
        save_location = BOT_DATA_DIR + os.sep + 'standings.json'
        # save_location = save_location.replace('\\', '\\\\')
        with open(save_location, 'w') as outfile:
            s = json.dumps(self.diplomat)
            outfile.write(s)
        self.log.info('Diplomat successfully diploamt_saved to disk')

    def is_standing(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
