import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone

# Function to create a subelement with text
def create_subelement(parent, tag, text):
    element = ET.SubElement(parent, tag)
    element.text = text
    return element

# Function to gather input and create XML structure
def create_trust_interoperability_profile_xml(output_file_name):
    tip = ET.Element("tf:TrustInteroperabilityProfile", {
        "xmlns:tf": "https://trustmarkinitiative.org/specifications/trustmark-framework/1.4/schema/",
        "xmlns:ds": "http://www.w3.org/2000/09/xmldsig#",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
    })
    
    create_subelement(tip, "tf:Identifier", f"https://github.com/holiczsia/TrustmarkInfrastructure/blob/main/trust_interoperability_profile/{output_file_name}.xml")
    create_subelement(tip, "tf:PublicationDateTime", publish_datetime)

    tf_references = ET.SubElement(tip, "tf:References")
    tf_trustmark_def_req = ET.SubElement(tf_references, "tf:TrustmarkDefinitionRequirement", {"tf:id": "TD_1"})
    tf_definition_ref = ET.SubElement(tf_trustmark_def_req, "tf:TrustmarkDefinitionReference")
    create_subelement(tf_definition_ref, "tf:Identifier", input("Enter Trustmark Definition Reference Identifier: "))
   
    create_subelement(tip, "tf:TrustExpression", "TD_1")
    
    return tip

# Prompt for output trustmark name
output_file_name = input("Enter the trust interoperability profile file name (without .xml extension): ")

# Hard-coded output file path
output_tip_path = f"./trust_interoperability_profile/{output_file_name}.xml"

publish_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# Create XML structure
tip_xml = create_trust_interoperability_profile_xml(output_file_name)

# Convert to a string with pretty print
tip_str = ET.tostring(tip_xml, encoding="utf-8")
parsed_tip_str = minidom.parseString(tip_str)
pretty_tip_str = parsed_tip_str.toprettyxml(indent="    ")

# Customizing the pretty print to match the style of Trust Interoperability Profile header
pretty_tip_str = pretty_tip_str.replace(' xmlns:tf=', '\n    xmlns:tf=')
pretty_tip_str = pretty_tip_str.replace(' xmlns:ds=', '\n    xmlns:ds=')
pretty_tip_str = pretty_tip_str.replace(' xmlns:xsi=', '\n    xmlns:xsi=')

# Save to file
with open(output_tip_path, "w", encoding="utf-8") as xml_file:
    xml_file.write(pretty_tip_str)

print(f"Trust Interoperability Profile '{output_file_name}.xml' created successfully in the trust interoperability profile folder.")