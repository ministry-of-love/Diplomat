import diplomat

from errbot.backends.test import testbot
from errbot import plugin_manager

class TestDiplomat(object):
    extra_plugin_dir = '.'

    def test_isred(self, testbot):
        # testbot.push_message('!diplomat isred')
        # expected = "Please include a name of a person to check."
        # result = testbot.pop_message()
        # assert expected == result
        
        testbot.push_message('!diplomat isred --name Logical Fallacy')
        expected = 'Logical Fallacy does not exist.'
        result = testbot.pop_message()
        assert expected == result

        testbot.push('!isred --name Brad Neece')
        expected = "Brad Neece\nStanding: -10.0" + \
            "\nTags: annoying, edgey, misunderstood, summercamp"
        result = testbot.pop_message()
        assert expected == result

        testbot.push('!isred --name warr akini')
        expected = "Warr Akini\nStanding: -10.0" +\
            "\nTags: cool, dick, butt, dickbutt"
        result = testbot.pop_message()
        assert expected == result

    def test_addtag(self, testbot):
        testbot.push_message('!diplomat addtag ____ ____')

        expected = ''
        result = testbot.pop_message()
        assert expected == result



    def test_removetag(self, testbot):
        testbot.push_message('not implemented')

    def test_remchar(self, testbot):
        testbot.push_message('not implemented')

    def test_addchar(self, testbot):
        testbot.push_message('not implemented')

    def test_write_dictionary(self, testbot):
        testbot.push_message('not implemented')