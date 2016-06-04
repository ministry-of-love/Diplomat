import diplomat

from errbot.backends.test import testbot
from errbot import plugin_manager

class TestDiplomat(object):
    extra_plugin_dir = 'C:\\Users\\YatesDisgrace\\PycharmProjects\\errbot\\diplomat'

    def test_isred(self, testbot):
        testbot.push_message('!diplomat isred')
        expected = "Please include a name of a character to check."
        result = testbot.pop_message()
        assert expected == result
        
        testbot.push_message('!diplomat isred Logical Fallacy')
        expected = "logical fallacy" + "\nStanding: 10.0" + \
                   "\nTags: cool, multiboxer, spy"
        result = testbot.pop_message()
        assert expected == result
        diplomat_plugin = testbot.bot.plugin_manager.get_plugin_obj_by_name('Diplomat')
        assert 'logical fallacy' in diplomat_plugin.diplomat
        assert 'spy' in diplomat_plugin.diplomat['logical fallacy']['tags']
        assert 'multiboxer' in diplomat_plugin.diplomat['logical fallacy']['tags']
        assert 'cool' in diplomat_plugin.diplomat['logical fallacy']['tags']
        assert diplomat_plugin.diplomat['logical fallacy']['standing'] == 10.0


        testbot.push_message('!diplomat isred Fabulous Andy')
        expected = "fabulous andy does not exist in Diplomat."
        result = testbot.pop_message()
        assert expected == result

        testbot.push_message('!diplomat isred Brad Neece')
        expected = "brad neece\nStanding: -5.0" + \
             "\nTags: annoying, edgey, misunderstood, summercamp, bff"
        result = testbot.pop_message()
        assert expected == result

        assert 'brad neece' in diplomat_plugin.diplomat
        assert 'annoying' in diplomat_plugin.diplomat['brad neece']['tags']
        assert 'edgey' in diplomat_plugin.diplomat['brad neece']['tags']
        assert 'misunderstood' in diplomat_plugin.diplomat['brad neece']['tags']
        assert 'summercamp' in diplomat_plugin.diplomat['brad neece']['tags']
        assert 'bff' in diplomat_plugin.diplomat['brad neece']['tags']
        assert diplomat_plugin.diplomat['brad neece']['standing'] == -5.0

        testbot.push_message('!diplomat isred warr akini')
        expected = "warr akini\nStanding: 10.0" +\
            "\nTags: cool, dick, butt, dickbutt"
        result = testbot.pop_message()
        assert expected == result

        assert 'warr akini' in diplomat_plugin.diplomat
        assert 'cool' in diplomat_plugin.diplomat['warr akini']['tags']
        assert 'dick' in diplomat_plugin.diplomat['warr akini']['tags']
        assert 'butt' in diplomat_plugin.diplomat['warr akini']['tags']
        assert 'dickbutt' in diplomat_plugin.diplomat['warr akini']['tags']
        assert diplomat_plugin.diplomat['warr akini']['standing'] == 10.0

    def test_addtag(self, testbot):
        # Test for empty argument string
        # Expected result: Print error message and proper syntax
        testbot.push_message('!diplomat addtag')
        expected = "Please include a tag and character name" + \
                       "\nProper syntax is !diplomat addtag <tag> <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for single argument
        # Expected result: Print error message including proper syntax
        testbot.push_message('!diplomat addtag miniluv')
        expected = "Please include a name of a character to check." + \
                    "\nProper syntax is !diplomat addtag <tag> <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for adding to a character that does not exist
        # Expected result: Print error message stating character does not exist
        testbot.push_message('!diplomat addtag miniluv sjugar02')
        expected = "Character sjugar02 does not exist in Diplomat."
        result = testbot.pop_message()
        assert expected == result

        # Test for successfully adding a tag to an existing character
        # Expected result: Return message indicating the successful addition of
        # tag to character in Diplomat
        testbot.push_message('!diplomat addtag miniluv Boneytooth Thompkins isk-chip')
        expected = "Added tag 'miniluv' to character 'boneytooth thompkins isk-chip'"
        result = testbot.pop_message()
        assert expected == result
        # plugin_names = plugin_manager.BotPluginManager.get_all_plugin_names(plugin_manager.BotPluginManager)
        # assert 'miniluv' in diplomat_plugin.diplomat['boneytooth thompkins isk-chip']['tags']

    def test_removetag(self, testbot):
        # Test for empty argument string
        # Expected result: Print error message and proper syntax
        testbot.push_message('!diplomat remtag')
        expected = "Please include a tag and character name" + \
                   "\nProper syntax is !diplomat remtag <tag> <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for single argument
        # Expected result: Print error message including proper syntax
        testbot.push_message('!diplomat remtag miniluv')
        expected = "Please include a name of a character to remove a tag from." + \
                    "\nProper syntax is !diplomat remtag <tag> <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for removing a tag to a character that does not exist
        # Expected result: Print error message stating character does not exist
        testbot.push_message('!diplomat remtag miniluv sjugar02')
        expected = "Character sjugar02 does not exist in Diplomat."
        result = testbot.pop_message()
        assert expected == result

        # Test for removing a tag that doesn't exist from a character that exists
        # Expected result: returns message indicating that tag does not exist for specified character
        testbot.push_message('!diplomat remtag spy boneytooth thompkins isk-chip')
        expected = "Tag 'spy' does not exist for character 'boneytooth thompkins isk-chip'"
        result = testbot.pop_message()
        assert expected == result

        # Test for removing a tag that exists from a character that exists
        # Expected result: tag is removed
        # Returns a message indicating that the tag has been removed from the specified characters
        testbot.push_message('!diplomat remtag cool boneytooth thompkins isk-chip')
        expected = "Removed tag 'cool' from character 'boneytooth thompkins isk-chip'"
        result = testbot.pop_message()
        assert expected == result
        plugin = testbot.bot.plugin_manager.get_plugin_obj_by_name('Diplomat')
        assert 'spy' not in plugin.diplomat['boneytooth thompkins isk-chip']['tags']


    def test_remchar(self, testbot):
        # Test for empty argument string
        # Expected result: Print error message and proper syntax
        testbot.push_message('!diplomat remchar')
        expected = "Please include the name of a character to remove from Diplomat." + \
                   "\nProper syntax is !diplomat remchar <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for character that does not exist
        # Expected result: Print error message, indicating character does not exist
        testbot.push_message('!diplomat remchar miniluv')
        expected = "miniluv does not exist in Diplomat."
        result = testbot.pop_message()
        assert expected == result

        # Test for removing character which exists
        # Expected result: Print message indicating the character has been removed
        # Character is removed from Diplomat.diplomat
        testbot.push_message('!diplomat remchar boneytooth thompkins isk-chip')
        expected = "Removed character 'boneytooth thompkins isk-chip' from Diplomat."
        result = testbot.pop_message()
        assert expected == result
        plugin = testbot.bot.plugin_manager.get_plugin_obj_by_name('Diplomat')
        assert 'boneytooth thompkins isk-chip' not in plugin.diplomat

    def test_addchar(self, testbot):
        # Test for empty argument string
        # Expected result: Print error message and proper syntax
        testbot.push_message('!diplomat addchar')
        expected = "Please include a standing, tag and character name to add to Diplomat." + \
                   "\nProper syntax is !diplomat addchar <standing> <tag> <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for invalid standing parameter
        # Expected result: return error message containing proper syntax for standing
        #                  return error message with proper syntax for command

        testbot.push_message("!diplomat addchar 6ab miniluv boneytooth thompkins isk-chip")
        expected = "Please include the standing as a valid numeric (-10.0 ... 10.0)" + \
                          "\nProper syntax is !diplomat addchar <standing> <tag> <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for two missing arguments with valid standing
        # Expected result: Print error message and proper syntax
        testbot.push_message('!diplomat addchar -10.0')
        expected = "Please include a single tag for the character that will be added to Diplomat." + \
                        "\nProper syntax is !diplomat addchar <standing> <tag> <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for single missing argument with valid standing and tag
        # Expected result: Return  error message with proper syntax
        testbot.push_message('!diplomat addchar +10.0 cool')
        expected = "Please include a name for the character that will be added to Diplomat." + \
                        "\nProper syntax is !diplomat addchar <standing> <tag> <name>"
        result = testbot.pop_message()
        assert expected == result

        # Test for character which does not exist within Diplomat
        # Expected Result: Character is added to Diplomat
        #                  Successful message is returned

        testbot.push_message('!diplomat addchar 10.0 cool sjugar02')
        expected = "Added Character: 'sjugar02'\nStanding: 10.0\nTags: cool"
        result = testbot.pop_message()
        assert expected == result
        plugin = testbot.bot.plugin_manager.get_plugin_obj_by_name('Diplomat')
        assert 'sjugar02' in plugin.diplomat
        assert '10.0' == plugin.diplomat['sjugar02']['standing']
        assert 'cool' in plugin.diplomat['sjugar02']['tags']

        # Test for adding character which already exists within Diplomat.
        # Expected Result: Error message is returned.
        #                  New character is not added.
        #                  Existing character is not changed

        testbot.push_message('!diplomat addchar 10.0 douchey boneytooth thompkins isk-chip')
        expected = "Character 'boneytooth thompkins isk-chip' already exists in Diplomat."
        result = testbot.pop_message()
        assert expected == result
        diplomat_plugin = testbot.bot.plugin_manager.get_plugin_obj_by_name('Diplomat')
        assert 'douchey' not in diplomat_plugin.diplomat['boneytooth thompkins isk-chip']['tags']
        assert 'cool' in diplomat_plugin.diplomat['boneytooth thompkins isk-chip']['tags']
        assert 'sexy' in diplomat_plugin.diplomat['boneytooth thompkins isk-chip']['tags']
        assert 'good' in diplomat_plugin.diplomat['boneytooth thompkins isk-chip']['tags']
        assert diplomat_plugin.diplomat['boneytooth thompkins isk-chip']['standing'] == -10.0

    def test_write_dictionary(self, testbot):
        pass