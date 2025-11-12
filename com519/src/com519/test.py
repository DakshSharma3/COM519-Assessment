# import xml.etree.cElementTree as ET
#
# root = ET.Element("root")
#
#
# credentials =[["admin","password"], ["admin1","password1"], ["admin2","password2"] ]
#
#
# for credential in credentials:
#
#     sub_element = ET.SubElement(root, "credentials")
#
#     ET.SubElement(sub_element, "Username").text = credential[0]
#     ET.SubElement(sub_element, "Password").text = credential[1]
#
# ET.indent(root, space="    ")
# tree = ET.ElementTree(root)
# tree.write("filename.xml")


# importing element tree
# under the alias of ET
import xml.etree.ElementTree as ET
from fileinput import filename

# Passing the path of the
# xml document to enable the
# parsing process
tree = ET.parse('filename.xml')

# getting the parent tag of
# the xml document
root = tree.getroot()

# printing the root (parent) tag
# of the xml document, along with
# its memory location
print(root)

# printing the attributes of the
# first tag from the parent
print(root[0][0])

# printing the text contained within
# first subtag of the 5th tag from
# the parent
print(root[0][0].text)
