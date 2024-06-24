#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_trustmark_definition():
    ns = {
        'tf': "https://trustmarkinitiative.org/specifications/trustmark-framework/1.4/schema/",
        'ds': "http://www.w3.org/2000/09/xmldsig#"
    }
    
    ET.register_namespace('tf', ns['tf'])
    ET.register_namespace('ds', ns['ds'])
    
    trustmark_definition = ET.Element("{%s}TrustmarkDefinition" % ns['tf'], {
        'xmlns:tf': ns['tf'],
        'xmlns:ds': ns['ds'],
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xmlns': "http://www.w3.org/1999/xhtml"
    })

    # Signature element
    signature = ET.SubElement(trustmark_definition, "{%s}Signature" % ns['ds'])
    # The content of the signature is omitted for this example

    # Metadata element
    metadata = ET.SubElement(trustmark_definition, "{%s}Metadata" % ns['tf'])
    
    identifier = ET.SubElement(metadata, "{%s}Identifier" % ns['tf'])
    identifier.text = "https://example.org/trustmark-definitions/example-definition"

    name = ET.SubElement(metadata, "{%s}Name" % ns['tf'])
    name.text = "Example Trustmark Definition"

    version = ET.SubElement(metadata, "{%s}Version" % ns['tf'])
    version.text = "1.0"

    description = ET.SubElement(metadata, "{%s}Description" % ns['tf'])
    description.text = "This is an example trustmark definition."

    publication_date_time = ET.SubElement(metadata, "{%s}PublicationDateTime" % ns['tf'])
    publication_date_time.text = "2024-06-24T00:00:00"

    trustmark_defining_organization = ET.SubElement(metadata, "{%s}TrustmarkDefiningOrganization" % ns['tf'])
    trustmark_defining_organization.text = "Example Organization"

    definition_requirements = ET.SubElement(trustmark_definition, "{%s}DefinitionRequirements" % ns['tf'])
    requirement = ET.SubElement(definition_requirements, "{%s}Requirement" % ns['tf'])
    identifier = ET.SubElement(requirement, "{%s}Identifier" % ns['tf'])
    identifier.text = "https://example.org/requirements/example-requirement"
    name = ET.SubElement(requirement, "{%s}Name" % ns['tf'])
    name.text = "Example Requirement"
    description = ET.SubElement(requirement, "{%s}Description" % ns['tf'])
    description.text = "Description of the example requirement."

    issuance_criteria = ET.SubElement(trustmark_definition, "{%s}IssuanceCriteria" % ns['tf'])
    issuance_criteria.text = "yes(all)"

    return trustmark_definition

def prettify_xml(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

if __name__ == "__main__":
    trustmark_definition = create_trustmark_definition()
    pretty_xml_string = prettify_xml(trustmark_definition)
    
    with open("TrustmarkDefinition.xml", "w") as f:
        f.write(pretty_xml_string)

