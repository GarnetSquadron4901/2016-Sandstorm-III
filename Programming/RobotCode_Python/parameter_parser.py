import wpilib
from xml.etree import ElementTree

class Parameters:
    XML_FILE = '/parameters.xml'
    def __init__(self):
        self.load_xml()

    def load_xml(self):
