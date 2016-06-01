from errbot import BotPlugin, arg_botcmd, botcmd
import json


class Diplomat(BotPlugin):
    """Diplomat plugin for Luvbot"""

    def activate(self):
        """
        Triggers on plugin activation
        """
        self.log.info('Activating Diplomat Plugin')
        super(Diplomat, self).activate()

        if not "diplomat" in self:
            self["diplomat"] = []

        self.log.info("Loading character database.")

        with open('./tbd.json', 'r') as input:
            # read in each file json entry
            # create new value in associative array s.t.
            # diplomat['character_name'] = [tag1, ..., tagn]
            self.diplomat = json.load(input)

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

    @arg_botcmd('--name', dest='name', type=str, default=None)
    def diplomat_isred(self, message, name):
        # Check to determine if the character name passed to the function is red
        # If it exists in the player_list, return
        self.log.info("Loading character database.")
        response = ""
        if name is None:
            response = "Please include a name of a person to check." + \
                "\nProper syntax is !diplomat isred --name <name>"
        else:
            if not self.diplomat[name]:
                response = name + " does not exist."
            else:
                response = name + "\nStanding: " + self.diplomat[name]['standing'] + \
                           "\nTags: " + ', '.join(self.diplomat[name]['tags'])
        return response

    @arg_botcmd('--name', dest='name', type=str, default=None)
    @arg_botcmd('--tag', dest='tag', type=str, default=None)
    def diplomat_addtag(self, message, name, tag):
        # Adds a tag to a character if it exists in the red list
        # If character does not exist in red list, does nothing
        response = ""
        if name is None:
            response = "Please include a name of a character to check." + \
                "\nProper syntax is !diplomat addtag --name <name> --tag <tag1 tag2...tagN>"
        elif tag is None:
            response = "Please include a tag to add to the specified character." + \
                "\nProper syntax is !diplomat addtag --name <name> --tag <tag1 tag2...tagN>"
        elif name is None and tag is None:
            response = "You didn't include a name of a character or a tag to add, what's wrong with you?" + \
                "\nProper syntax is !diplomat addtag --name <name> --tag <tag1 tag2...tagN>"
        else:
            if not self.diplomat[name]:
                response = "Character " + name + " does not exist in Diplomat"
            else:
                self.diplomat[name]['tags'].add(tag)
                response = "Added tag '" + tag + "' to character " + name
        return response

    @arg_botcmd('--name', dest='name', type=str, default=None)
    @arg_botcmd('--tag', dest='tag', type=str, default=None)
    def diplomat_remtag(self, message, name, tag):
        response = ""
        if name is None:
            response = "Please include a name of a character to check." + \
                "\nProper syntax is !diplomat remtag --name <name> --tag <tag1 tag2...tagN>"
        elif tag is None:
            response = "Please include a tag to remove from the specified character." + \
                "\nProper syntax is !diplomat remtag --name <name> --tag <tag1 tag2...tagN>"
        elif name is None and tag is None:
            response = "You didn't include a name of a character or a tag to remove, what's wrong with you?" + \
                "\nProper syntax is !diplomat remtag --name <name> --tag <tag1 tag2...tagN>"
        else:
            if not self.diplomat[name]:
                response = "Character " + name + " does not exist."
            else:
                count = 0
                response = "Removed the following tags from " + name + ": "
                for t in tag:
                    self.diplomat[name]['tags'].remove(t)
                    response += t + ", "

        return response

    @arg_botcmd('--name', dest='name', type=str, default=None)
    def diplomat_remchar(self, message, name):
        response = ""
        if name is None:
            response = "Please include a name of a character to remove." + \
                "\nProper syntax is !diplomat remchar --name <name>"
        else:
            if not self.diplomat[name]:
                response = name + " does not exist in Diplomat."
            else:
                del self.diplomat[name]
                response = "Removed Character " + name + " from Diplomat."
                self.write_dictionary()
        return response

    @arg_botcmd('--name', dest='name', type=str, default=None)
    @arg_botcmd('--standing', dest='standing', type=int, default=0.0)
    @arg_botcmd('--tag', dest='tag', type=str, default=None)
    def diplomat_addchar(self, message, name, standing, tag):
        response = ""
        if name is None:
            response = "Please include a name of a character to check." + \
                "\nProper syntax is !diplomat addchar --name <name> --standing <standing> --tag <tag1 tag2...tagN>"
        elif tag is None:
            response = "Please include a tag to remove from the specified character." + \
                "\nProper syntax is !diplomat addchar --name <name> --standing <standing>--tag <tag1 tag2...tagN>"
        elif name is None and tag is None:
            response = "You didn't include a name of a character dd, what's wrong with you?" + \
                "\nProper syntax is !diplomat addchar --name <name> --standing <standing> --tag <tag1 tag2...tagN>"
        else:
            if not self.diplomat[name]:
                self.diplomat[name] = []
                self.diplomat[name]['standing'] = standing
                self.diplomat[name] = tag.split(' ', ',')
            else:
                response = "Removed Character " + name + " from Diplomat."
        self.write_dictionary()
        return response

    def write_dictionary(self):
        # self.log.info('Saving Diplomat to disk.')
        # Write dictionary to disk
        # self.log.info('Diplomat successfully saved to disk')
        pass
