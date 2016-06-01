from errbot import BotPlugin, botcmd, arg_botcmd
import json


class Diplomat(BotPlugin):
    """Diplomat plugin for Luvbot"""

    def __init__(self):
        self.diplomat = []

    def activate(self):
        """
        Triggers on plugin activation
        """
        self.log.info('Activating Diplomat Plugin')
        super(Diplomat, self).activate()

        if not "diplomat" in self:
            self["diplomat"] = {}

        self.log.info("Loading character database.")

        with open('./tbd.json', 'r') as input:
            # read in each file json entry
            # create new value in associative array s.t.
            # diplomat['character_name'] = [tag1, ..., tagn]
            self.diplomat = json.load(input)

            self.log.info('Loaded character database successfully.')

            # Is there more to do?
            print("hi yates")

    @arg_botcmd
    def diplomat_isred(self, message, name):
        # Check to determine if the character name passed to the function is red
        # If it exists in the player_list, return

        response = ""
        if not self.diplomat[name]:
            response = name + " does not exist."
        else:
            response = name + "\nStanding: " + self.diplomat[name]['standing'] + \
                       "\nTags: " + self.diplomat[name]['tags']
        return response

    @arg_botcmd('name', type=str)
    @arg_botcmd('tag', type=str)
    def diplomat_add_tag(self, message, name, tag):
        # Adds a tag to a character if it exists in the red list
        # If character does not exist in red list, does nothing
        response = ""
        if not self.diplomat[name]:
            response = "Character " + name + " does not exist in Diplomat"
        else:
            self.diplomat[name]['tags'].add(tag)
            response = "Added tag '" + tag + "' to character " + name
        return response

    @arg_botcmd('name', type=str)
    @arg_botcmd('tag', type=str)
    def diplomat_remove_tag(self, message, name, tag):
        response = ""
        if not self.diplomat[name]:
            response = "Character " + name + " does not exist."
        else:
            self.diplomat[name]['tags'].remove(tag)
            response = "Removed tag " + tag + " from " + name

        return response

    @arg_botcmd('name', type=str)
    def diplomat_remove_character(self, message, name):
        # Removes a character from the redlist
        # If character does not exist in the redlist, does nothing
        response = ""
        if not self.diplomat[name]:
            response = name + " does not exist."
        else:
            self.diplomat.remove(name)
            response = "Removed Character " + name + " from Diplomat."
            self.write_dictionary()
        return response


    @arg_botcmd('name', type=str)
    def addchar(self, message, name):
        # Adds a character to the redlist
        # If character already exists in the redlist, does nothing
        response = ""
        if not self.diplomat[name]:
            response = "Character " + name + " not found in Diplomat."
        else:
            response = "Removed Character " + name + " from Diplomat."
        self.write_dictionary()

    def write_dictionary(self):
        self.log.info('Saving Diplomat to disk.')
        # Write dictionary to disk
        self.log.info('Diplomat successfully saved to disk')

