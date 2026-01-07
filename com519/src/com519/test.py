import xml.etree.cElementTree as ET

# root = ET.Element("Appointments")
# doc = ET.SubElement(root, "appointment", id = str(1))
#
# ET.SubElement(doc, "employee_id").text = "1"
# ET.SubElement(doc, "people_id").text = "1"
# ET.SubElement(doc, "branch_id").text = "3"
# ET.SubElement(doc, "date").text = "11/11/2026"
# ET.SubElement(doc, "time").text = "00:00"
# ET.SubElement(doc, "purpose").text = "Re-evaluate investment portfolio"
# ET.indent(root, space="    ", level=0)
# tree = ET.ElementTree(root)
# tree.write("appointments.xml")


tree = ET.parse("appointments.xml")
root = tree.getroot()

doc = ET.SubElement(root, "appointment", id = str(1))

ET.SubElement(doc, "employee_id").text = "1"
ET.SubElement(doc, "people_id").text = "1"
ET.SubElement(doc, "branch_id").text = "3"
ET.SubElement(doc, "date").text = "11/11/2026"
ET.SubElement(doc, "time").text = "00:00"
ET.SubElement(doc, "purpose").text = "Re-evaluate investment portfolio"
ET.indent(root, space="    ", level=0)
tree = ET.ElementTree(root)

tree.write("appointments.xml", encoding="utf-8", xml_declaration=True)




# tree = ET.parse('filename.xml')
#
# # getting the parent tag of
# # the xml document
# root = tree.getroot()
#
# # printing the root (parent) tag
# # of the xml document, along with
# # its memory location
# print(root.tag)
#
# # first tag from the parent
# print(root[0].attrib)
#
# # printing the text contained within
# # first subtag of the 5th tag from
# # # the parent
# # print(root[2][0].text)
