import os
import streamlit as st
import pandas as pd
from icecream import ic 
#
from parsezk import start_parse
from initialize import clean_and_recreate_directory

def display_node(node, level=0):
    """
    Recursively display an XML node and its children using Streamlit.
    Args:
        node (dict): A dictionary representing the XML node. It should have 'name', 'value', and 'children' keys.
        level (int, optional): The current level of indentation for displaying the node. Defaults to 0.
    Raises:
        KeyError: If the expected keys ('name', 'value', 'children') are not found in the node dictionary.
        Exception: For any other exceptions that occur during the display process.
    """
   
    try:
        indent = ' ' * (level * 4)
        st.write(f"{indent}**Name**: {node['name']}")
        st.write(f"{indent}**Value**: {node['value']}")
        
        if node['children']:
            st.write(f"{indent}**Children**:")
            for child_name, child_node in node['children'].items():
                with st.expander(f"{indent}{child_name}", expanded=False):
                    display_node(child_node, level + 1)
    except KeyError as e:
        st.error(f"KeyError: {e} - node: {node}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    """
    Main function to set up and run the ZooKeeper Analysis app.
    This function performs the following tasks:
    1. Sets the page configuration including title, icon, and layout.
    2. Applies a custom color theme and hides the default footer.
    3. Adds the NetApp logo to the sidebar.
    4. Provides a file uploader in the sidebar for uploading a ZooKeeper zkdata.xml file.
    5. Cleans and recreates the uploads directory.
    6. Displays the uploaded file information.
    7. On clicking the "Start" button, saves the uploaded file to the uploads directory.
    8. Parses the uploaded file and displays the analysis results in the main window.
    9. Allows the user to select a row from the parsed data to view detailed XML information.
    Note:
    - The function uses Streamlit for the web interface.
    - The function assumes the existence of helper functions `clean_and_recreate_directory`, `start_parse`, and `display_node`.
    """
    # Set the title of the app
    st.set_page_config(page_title="ZooKeeper Analysis", page_icon="netapp_logo.png", layout="wide")
    
    # Set the color theme
    st.markdown(
        """
        <style>
        .css-18e3th9 { background-color: #0067C5; /* NetApp blue */ }
        .css-1d391kg { background-color: #0067C5; /* NetApp blue */ }
        .css-1v3fvcr { color: white; }
        .css-145kmo2 { color: white; }
        .css-1cpxqw2 { color: white; }
        .css-1inwz65 { color: white; }
        .css-1r6slb0 { color: white; }
        .css-1a32fsj { color: white; }
        footer { visibility: hidden; }
        .footer { visibility: visible; position: fixed; left: 0; bottom: 0; width: 100%; background-color: #0067C5; color: white; text-align: center; padding: 10px; }
        </style>
        Created by Jon Bowman
        """, unsafe_allow_html=True
    )
    
    # Add NetApp logo at the top of the sidebar
    st.sidebar.image("netapp_logo.png", use_container_width=True)

    uploaded_file = st.sidebar.file_uploader("Upload ZooKeeper zkdata.xml file", type="xml", accept_multiple_files=False)
    uploads_path = "./uploads"
    clean_and_recreate_directory(uploads_path)

    ic(uploaded_file)

    if st.button("Start"):
        if uploaded_file:
            file_paths = []
            file_path = os.path.join(uploads_path, uploaded_file.name)
            ic(file_path)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        

            # Main window content
            st.title("SolidFire ZooKeeper Analysis")

            response_df = start_parse(file_path)
            
            # Display the DataFrame
            selected_row = st.selectbox("Select a row to view details", response_df.to_dict('records'), format_func=lambda x: x['name'])

            
            if selected_row:
                st.write("### Detailed XML View")
                display_node(selected_row)

if __name__ == "__main__":
    main()
