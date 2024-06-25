import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timedelta, timezone

# Function to create a subelement with text
def create_subelement(parent, tag, text):
    element = ET.SubElement(parent, tag)
    element.text = text
    return element

# Function to gather input and create XML structure
def create_trustmark_xml(output_file_name):
    trustmark = ET.Element("tf:Trustmark", {
        "tf:id": "trustmark",
        "xmlns:tf": "https://trustmarkinitiative.org/specifications/trustmark-framework/1.4/schema/",
        "xmlns:ds": "http://www.w3.org/2000/09/xmldsig#",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
    })
    
    tf_identifier = create_subelement(trustmark, "tf:Identifier", f"https://github.com/holiczsia/TrustmarkInfrastructure/blob/main/trustmark/{output_file_name}.xml")
    
    tf_definition_ref = ET.SubElement(trustmark, "tf:TrustmarkDefinitionReference")
    create_subelement(tf_definition_ref, "tf:Identifier", input("Enter Trustmark Definition Reference Identifier: "))
    
    create_subelement(trustmark, "tf:IssueDateTime", issue_datetime)
    create_subelement(trustmark, "tf:ExpirationDateTime", expiration_datetime)
    
    create_subelement(trustmark, "tf:PolicyURL", "https://github.com/holiczsia/TrustmarkInfrastructure/blob/main/trustmark_policy/nief-trustmark-policy-1.2.pdf")
    create_subelement(trustmark, "tf:RelyingPartyAgreementURL", "https://github.com/holiczsia/TrustmarkInfrastructure/blob/main/trustmark_relying_party_agreement/nief-trustmark-relying-party-agreement-1.4.pdf")
    create_subelement(trustmark, "tf:StatusURL", f"https://github.com/holiczsia/TrustmarkInfrastructure/blob/main/trustmark_status_report/{output_file_name}_status_report.xml")
    
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

# Function to create trustmark status report
def create_trustmark_status_report_xml(output_file_name):
    trustmark_status_report = ET.Element("tf:TrustmarkStatusReport", {
        "xmlns:tf": "https://trustmarkinitiative.org/specifications/trustmark-framework/1.4/schema/",
        "xmlns:ds": "http://www.w3.org/2000/09/xmldsig#",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
    })
       
    tf_ref = ET.SubElement(trustmark_status_report, "tf:TrustmarkReference")
    create_subelement(tf_ref, "tf:Identifier", f"https://github.com/holiczsia/TrustmarkInfrastructure/blob/main/trustmark/{output_file_name}.xml")

    create_subelement(trustmark_status_report, "tf:StatusCode", input("Enter Trustmark status (ACTIVE, REVOKED, or EXPIRED): "))

    # Set issue date to current date and time
    issue_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    create_subelement(trustmark_status_report, "tf:StatusDateTime", issue_datetime)
    
    return trustmark_status_report

# Prompt for output trustmark name
output_file_name = input("Enter the trustmark name (without .xml extension): ")

# Hard-coded output file path
output_tm_path = f"./trustmark/{output_file_name}.xml"
output_tmsr_path = f"./trustmark_status_report/{output_file_name}_status_report.xml"

issue_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
expiration_datetime = (datetime.now(timezone.utc) + timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ')

# Create XML structure
trustmark_xml = create_trustmark_xml(output_file_name)

# Convert to a string with pretty print
tm_str = ET.tostring(trustmark_xml, encoding="utf-8")
parsed_tm_str = minidom.parseString(tm_str)
pretty_tm_str = parsed_tm_str.toprettyxml(indent="    ")

# Customizing the pretty print to match the style of Trustmark header
pretty_tm_str = pretty_tm_str.replace(' tf:id="trustmark"', '')
pretty_tm_str = pretty_tm_str.replace(' xmlns:tf=', '\n    xmlns:tf=')
pretty_tm_str = pretty_tm_str.replace(' xmlns:ds=', '\n    xmlns:ds=')
pretty_tm_str = pretty_tm_str.replace(' xmlns:xsi=', '\n    xmlns:xsi=')
pretty_tm_str = pretty_tm_str.replace('<tf:Trustmark\n    xmlns:tf=', '<tf:Trustmark tf:id="trustmark"\n    xmlns:tf=')

# Save to file
with open(output_tm_path, "w", encoding="utf-8") as xml_file:
    xml_file.write(pretty_tm_str)

print(f"Trustmark '{output_file_name}.xml' created successfully in the trustmark folder.")

# Create trustmark status report
trustmark_status_report_xml = create_trustmark_status_report_xml(output_file_name)

# Convert to a string with pretty print
tmsr_str = ET.tostring(trustmark_status_report_xml, encoding="utf-8")
parsed_tmsr_str = minidom.parseString(tmsr_str)
pretty_tmsr_str = parsed_tmsr_str.toprettyxml(indent="    ")

# Customizing the pretty print to match the style of Trustmark status report header
pretty_tmsr_str = pretty_tmsr_str.replace(' xmlns:tf=', '\n    xmlns:tf=')
pretty_tmsr_str = pretty_tmsr_str.replace(' xmlns:ds=', '\n    xmlns:ds=')
pretty_tmsr_str = pretty_tmsr_str.replace(' xmlns:xsi=', '\n    xmlns:xsi=')

# Save to file
with open(output_tmsr_path, "w", encoding="utf-8") as xml_file:
    xml_file.write(pretty_tmsr_str)

print(f"Trustmark Status Report '{output_file_name}_status_report.xml' created successfully in the trustmark_status_report folder.")