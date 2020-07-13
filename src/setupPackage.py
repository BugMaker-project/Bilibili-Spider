import os
import lxml.etree
class Tool:
    def __init__(self):
        self.file="setting.xml"
        self.content=lxml.etree.parse(self.file)
        self.mirror=None
    def setup(self):
        root = self.content.getroot()
        for article in root:
            for field in article:
                if field.tag == "mirror":
                    self.mirror = field.text
                if field.tag == "pyqt":
                    os.system("pip3 install -i %s %s" % (self.mirror, field.text))
                if field.tag == "requests":
                    os.system("pip3 install -i %s %s" % (self.mirror, field.text))
                if field.tag == "numpy":
                    os.system("pip3 install -i %s %s" % (self.mirror, field.text))
                if field.tag == "youget":
                    os.system("pip3 install -i %s %s" % (self.mirror, field.text))
def main():
    tool=Tool()
    tool.setup()
if __name__=="__main__":
    main()