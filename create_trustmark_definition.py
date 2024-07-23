import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone

# Function to create a subelement with text
def create_subelement(parent, tag, text):
    element = ET.SubElement(parent, tag)
    element.text = text
    return element

# Function to gather input and create XML structure
def create_trustmark_definition_xml(output_file_name):
    trustmark_definition = ET.Element("tf:TrustmarkDefinition", {
        "xmlns:tf": "https://trustmarkinitiative.org/specifications/trustmark-framework/1.4/schema/",
        "xmlns": "http://www.w3.org/1999/xhtml",
        #"xmlns:ds": "http://www.w3.org/2000/09/xmldsig#",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"
    })

    tf_metadata = ET.SubElement(trustmark_definition, "tf:Metadata")
    create_subelement(tf_metadata, "tf:Identifier", f"https://github.com/holiczsia/TrustmarkInfrastructure/blob/main/trustmark_definition/{output_file_name}.xml")
    create_subelement(tf_metadata, "tf:Name", input("Enter Trustmark Definition Name: "))
    create_subelement(tf_metadata, "tf:Version", input("Enter Trustmark Definition Version: "))
    create_subelement(tf_metadata, "tf:Description", input("Enter Trustmark Definition Description: "))
    create_subelement(tf_metadata, "tf:PublicationDateTime", publish_datetime)

    tf_trustmark_def_org = ET.SubElement(tf_metadata, "tf:TrustmarkDefiningOrganization")
    create_subelement(tf_trustmark_def_org, "tf:Identifier", f"https://github.com/holiczsia/TrustmarkInfrastructure/")
    create_subelement(tf_trustmark_def_org, "tf:Name", "TAMU LENSS")

    tf_trustmark_def_org_contact = ET.SubElement(tf_trustmark_def_org, "tf:Contact")
    create_subelement(tf_trustmark_def_org_contact, "tf:Kind", "PRIMARY")
    create_subelement(tf_trustmark_def_org_contact, "tf:Email", "holiczsia@tamu.edu")

    tf_conformance_criteria = ET.SubElement(trustmark_definition, "tf:ConformanceCriteria")
    conformance_criterion_id = input("Enter Conformance Criterion Identifier: ")
    tf_conformance_criterion = ET.SubElement(tf_conformance_criteria, "tf:ConformanceCriterion", {"tf:id": conformance_criterion_id})
    create_subelement(tf_conformance_criterion, "tf:Number", "1")
    create_subelement(tf_conformance_criterion, "tf:Name", input("Enter Conformance Criterion Name: "))
    create_subelement(tf_conformance_criterion, "tf:Description", input("Enter Conformance Criterion Description: "))

    tf_assessmentsteps = ET.SubElement(trustmark_definition, "tf:AssessmentSteps")
    tf_assessmentstep = ET.SubElement(tf_assessmentsteps, "tf:AssessmentStep", {"tf:id": input("Enter Assessment Step Identifier: ")})
    create_subelement(tf_assessmentstep, "tf:Number", "1")
    create_subelement(tf_assessmentstep, "tf:Name", input("Enter Assessment Step Name: "))
    create_subelement(tf_assessmentstep, "tf:Description", input("Enter Assessment Step Description: "))
    tf_conformance_criterion_ref = ET.SubElement(tf_assessmentstep, "tf:ConformanceCriterion", {
        "tf:ref": conformance_criterion_id, 
        "xsi:nil": "true"
    })

    create_subelement(trustmark_definition, "tf:IssuanceCriteria", "yes(all)")

    return trustmark_definition

# Prompt for output trustmark name
output_file_name = input("Enter the trustmark definition file name (without .xml extension): ")

# Hard-coded output file path
output_tmd_path = f"./trustmark_definition/{output_file_name}.xml"

publish_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# Create XML structure
trustmark_definition_xml = create_trustmark_definition_xml(output_file_name)

# Convert to a string with pretty print
tmd_str = ET.tostring(trustmark_definition_xml, encoding="utf-8")
parsed_tmd_str = minidom.parseString(tmd_str)
pretty_tmd_str = parsed_tmd_str.toprettyxml(indent="    ")

# Customizing the pretty print to match the style of Trustmark Definition header
pretty_tmd_str = pretty_tmd_str.replace(' xmlns:tf=', '\n    xmlns:tf=')
pretty_tmd_str = pretty_tmd_str.replace(' xmlns=', '\n    xmlns=')
pretty_tmd_str = pretty_tmd_str.replace(' xmlns:xsi=', '\n    xmlns:xsi=')

# Save to file
with open(output_tmd_path, "w", encoding="utf-8") as xml_file:
    xml_file.write(pretty_tmd_str)

print(f"Trustmark Definition '{output_file_name}.xml' created successfully in the trustmark definition folder.")