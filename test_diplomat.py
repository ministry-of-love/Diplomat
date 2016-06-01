import os
import unittest
import diplomat

from errbot.backends.test import testbot

class TestDiplomat(object):
    extra_plugin_dir = '.'

    def test_isred(self, testbot):
        testbot.push_message('!isred Boneytooth Thompkins Isk-Chip')
        expected = 'Boneytooth Thompkins Isk-Chip does not exist.'
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