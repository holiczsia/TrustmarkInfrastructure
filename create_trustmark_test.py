import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timedelta, timezone

# Function to create a subelement with text
def create_subelement(parent, tag, text):
    element = ET.SubElement(parent, tag)
    element.text = text
    return element

# Function to gather input and create XML structure
def create_trustmark_xml():
    trustmark = ET.Element("tf:Trustmark", {
        "tf:id": "trustmark",
        "xmlns:tf": "https://trustmarkinitiative.org/specifications/trustmark-framework/1.4/schema/",
        "xmlns:ds": "http://www.w3.org/2000/09/xmldsig#",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
    })
    
    tf_identifier = create_subelement(trustmark, "tf:Identifier", input("Enter Trustmark Identifier: "))
    
    tf_definition_ref = ET.SubElement(trustmark, "tf:TrustmarkDefinitionReference")
    create_subelement(tf_definition_ref, "tf:Identifier", input("Enter Trustmark Definition Reference Identifier: "))
    
    # Set issue date to current date and time
    issue_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    create_subelement(trustmark, "tf:IssueDateTime", issue_datetime)
    
    # Set expiration date to 90 days after issue date
    expiration_datetime = (datetime.now(timezone.utc) + timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ')
    create_subelement(trustmark, "tf:ExpirationDateTime", expiration_datetime)
    
    create_subelement(trustmark, "tf:PolicyURL", input("Enter Policy URL: "))
    create_subelement(trustmark, "tf:RelyingPartyAgreementURL", input("Enter Relying Party Agreement URL: "))
    create_subelement(trustmark, "tf:StatusURL", input("Enter Status URL: "))
    
    provider = ET.SubElement(trustmark, "tf:Provider")
    create_subelement(provider, "tf:Identifier", input("Enter Provider Identifier: "))
    create_subelement(provider, "tf:Name", input("Enter Provider Name: "))
    
    provider_contact = ET.SubElement(provider, "tf:Contact")
    create_subelement(provider_contact, "tf:Kind", "PRIMARY")
    create_subelement(provider_contact, "tf:Email", input("Enter Provider Contact Email: "))
    
    recipient = ET.SubElement(trustmark, "tf:Recipient")
    create_subelement(recipient, "tf:Identifier", input("Enter Recipient Identifier: "))
    create_subelement(recipient, "tf:Name", input("Enter Recipient Name: "))
    
    recipient_contact = ET.SubElement(recipient, "tf:Contact")
    create_subelement(recipient_contact, "tf:Kind", "PRIMARY")
    create_subelement(recipient_contact, "tf:Email", input("Enter Recipient Contact Email: "))
    
    return trustmark

# Create XML structure
trustmark_xml = create_trustmark_xml()

# Convert to a string with pretty print
xml_str = ET.tostring(trustmark_xml, encoding="utf-8")
parsed_str = minidom.parseString(xml_str)
pretty_str = parsed_str.toprettyxml(indent="    ")

# Customizing the pretty print to match the style of Trustmark header
pretty_str = pretty_str.replace(' tf:id="trustmark"', '')
pretty_str = pretty_str.replace(' xmlns:tf=', '\n    xmlns:tf=')
pretty_str = pretty_str.replace(' xmlns:ds=', '\n    xmlns:ds=')
pretty_str = pretty_str.replace(' xmlns:xs=', '\n    xmlns:xs=')
pretty_str = pretty_str.replace('<tf:Trustmark\n    xmlns:tf=', '<tf:Trustmark tf:id="trustmark"\n    xmlns:tf=')


# Prompt for output file name
output_file_name = input("Enter the output file name (with .xml extension): ")

# Hard-coded output file path
output_file_path = f"./trustmark/{output_file_name}"


# Save to file
with open(output_file_path, "w", encoding="utf-8") as xml_file:
    xml_file.write(pretty_str)

print(f"XML file '{output_file_name}' created successfully in the trustmark folder.")
