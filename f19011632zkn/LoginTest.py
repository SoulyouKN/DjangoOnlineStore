import unittest

from getXML import GetXML

class mylogin(unittest.TestCase):
    def setUp(self):
        print("-----Test Staring-----")
        self.mylists = GetXML.getxmldata("loginConfig.xml")