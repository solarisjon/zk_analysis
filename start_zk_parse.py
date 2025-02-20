import streamlit as st
from parsezk import start_parse
import pandas as pd
from icecream import ic 
import os
from initialize import clean_and_recreate_directory

def display_node(node, level=0):
    """Recursively display an XML node and its children."""
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
