import xml.etree.ElementTree as ET
import pandas as pd
from icecream import ic


def xml_to_dict(node):
    """Convert an XML node and its children to a dictionary."""
    result = {}
    for child in node:
        result[child.attrib.get('name', '')] = {
            'name': child.attrib.get('name', ''),
            'value': child.attrib.get('value', ''),
            'children': xml_to_dict(child)
        }
    return result

def start_parse(xml_file):
    
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extract the top-level zknode elements
    top_level_nodes = []
    for node in root.findall('zknode'):
        name = node.attrib.get('name', '')
        value = node.attrib.get('value', '')
        children = xml_to_dict(node)
        top_level_nodes.append({'name': name, 'value': value, 'children': children})
    
    # Convert the list of top-level nodes to a pandas DataFrame
    df = pd.DataFrame(top_level_nodes)
    
    return df
