import xml.etree.ElementTree as ET
import pandas as pd
from icecream import ic


def xml_to_dict(node):
    """
    Convert an XML node and its children to a dictionary.

    Args:
        node (xml.etree.ElementTree.Element): The XML node to convert.

    Returns:
        dict: A dictionary representation of the XML node and its children.
              The dictionary has the following structure:
              {
                  'name': <name attribute of the node>,
                  'value': <value attribute of the node>,
                  'children': <recursive dictionary of child nodes>
    """
    result = {}
    for child in node:
        result[child.attrib.get('name', '')] = {
            'name': child.attrib.get('name', ''),
            'value': child.attrib.get('value', ''),
            'children': xml_to_dict(child)
        }
    return result

def start_parse(xml_file):
    """
    Parses an XML file and extracts the top-level 'zknode' elements into a pandas DataFrame.
    Args:
        xml_file (str): The path to the XML file to be parsed.
    Returns:
        pandas.DataFrame: A DataFrame containing the top-level 'zknode' elements with their attributes and children.
    """
    
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
