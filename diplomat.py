from errbot import BotPlugin, arg_botcmd, botcmd
import json, os
from errbot import plugin_manager

class Diplomat(BotPlugin):
    """Diplomat plugin for Luvbot"""

    def activate(self):
        """
        Triggers on plugin activation
        """
        self.log.info('Activating Diplomat Plugin')
        super(Diplomat, self).activate()

        if "diplomat" not in self:
            self.diplomat = {}

        self.log.info("Loading character database.")
        with open('C:\\Users\\YatesDisgrace\\PycharmProjects\\errbot\\diplomat\\test.json', 'r') as infile:
            # read in each file json entry
            # create new value in associative array s.t.
            # diplomat['character_name'] = [tag1, ..., tagn]
            self.diplomat = json.load(infile)

            # self.log.info('Loaded character database successfully.')

    def deactivate(self):
        self.write_dictionary()
        super(Diplomat, self).deactivate()

    # def get_configuration_template(self):
    #     """
    #     Defines the configuration structure this plugin supports
    #
    #     You should delete it if your plugin doesn't use any configuration like this
    #     """
    #     return {'EXAMPLE_KEY_1': "Example value",
    #             'EXAMPLE_KEY_2': ["Example", "Value"]
    #            }
    #
    # def check_configuration(self, configuration):
    #     """
    #     Triggers when the configuration is checked, shortly before activation
    #
    #     Raise a errbot.utils.ValidationException in case of an error
    #
    #     You should delete it if you're not using it to override any default behaviour
    #     """
    #     super(Diplo, self).check_configuration(configuration)
    #
    # def callback_connect(self):
    #     """
    #     Triggers when bot is connected
    #
    #     You should delete it if you're not using it to override any default behaviour
    #     """
    #     pass
    #
    # def callback_message(self, message):
    #     """
    #     Triggered for every received message that isn't coming from the bot itself
    #
    #     You should delete it if you're not using it to override any default behaviour
    #     """
    #     pass
    #
    # def callback_botmessage(self, message):
    #     """
    #     Triggered for every message that comes from the bot itself
    #
    #     You should delete it if you're not using it to override any default behaviour
    #     """
    #     pass

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

    # @arg_botcmd('--name', dest='name', type=str, default=None)
    # @arg_botcmd('--tag', dest='tag', type=str, default=None)
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
        return response

    # @arg_botcmd('--name', dest='name', type=str, default=None)
    # @arg_botcmd('--tag', dest='tag', type=str, default=None)
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
                else:
                    response = "Tag '" + tag + "' does not exist for character '" + name + "'"
        return response

    # @arg_botcmd('--name', dest='name', type=str, default=None)
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
            self.write_dictionary()
        return response

    # @arg_botcmd('--name', dest='name', type=str, default=None)
    # @arg_botcmd('--standing', dest='standing', type=int, default=0.0)
    # @arg_botcmd('--tag', dest='tag', type=str, default=None)
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
            if not self._isStanding(standing):
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
                            response = "Added Character: '" + args + "'\nStanding: " + str(self.diplomat[args]['standing']) + \
                                       "\nTags: " + ', '.join(self.diplomat[args]['tags'])
                            self.write_dictionary()
                        else:
                            response = "Character '" + name + "' already exists in Diplomat."
        return response

    def write_dictionary(self):
        # self.log.info('Saving Diplomat to disk.')
        # Write dictionary to disk
        # self.log.info('Diplomat successfully saved to disk')
        pass
    def _isStanding(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
