#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from xml.dom import minidom

# Define the namespaces
namespaces = {
    'tf': 'https://trustmarkinitiative.org/specifications/trustmark-framework/1.4/schema/',
    'ds': 'http://www.w3.org/2000/09/xmldsig#',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# Register namespaces
for prefix, uri in namespaces.items():
    ET.register_namespace(prefix, uri)

def create_element(tag, text=None):
    """Helper function to create an element with namespaces."""
    elem = ET.Element(f'{{{namespaces["tf"]["ds"]["xsi"]}}}{tag}')
    if text:
        elem.text = text
    return elem

# Create the root element
trustmark = create_element('Trustmark')

# Add required sub-elements with their content
provider_id = create_element('ProviderId', 'https://provider.example')
trustmark.append(provider_id)

trustmark_def_id = create_element('TrustmarkDefinitionId', 'https://trustmark.example/trustmark-def-id')
trustmark.append(trustmark_def_id)

trustmark_id = create_element('TrustmarkId', 'https://trustmark.example/trustmark-id')
trustmark.append(trustmark_id)

recipient_id = create_element('RecipientId', 'https://recipient.example')
trustmark.append(recipient_id)

issue_date_time = create_element('IssueDateTime', '2024-01-01T00:00:00Z')
trustmark.append(issue_date_time)

expiration_date_time = create_element('ExpirationDateTime', '2025-01-01T00:00:00Z')
trustmark.append(expiration_date_time)

status_url = create_element('StatusURL', 'https://provider.example/status')
trustmark.append(status_url)

relying_party_agreement_url = create_element('RelyingPartyAgreementURL', 'https://provider.example/relying-party-agreement')
trustmark.append(relying_party_agreement_url)

# Adding a nested subelement example under <tf:ProviderId>
provider_info = create_element('ProviderInfo')
provider_name = create_element('ProviderName', 'Example Provider Name')
provider_info.append(provider_name)
provider_id.append(provider_info)

# Function to prettify the XML
def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Get the pretty XML string
pretty_xml_string = prettify_xml(trustmark)

# Write to a file
with open('trustmark.xml', 'w') as f:
    f.write(pretty_xml_string)

print("XML file 'trustmark.xml' created successfully.")