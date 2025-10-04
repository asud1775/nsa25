import streamlit as st
import pandas as pd
import sys
import os

# Add the parent directory to the path to import from data module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the restored dataframe from modis_aqua_data
from data import modis_aqua_data
restored_df = modis_aqua_data.load_nasa_modis_images()

def main():
    """
    Main function for the NASA Data Display Streamlit app
    """
    st.set_page_config(
        page_title="NASA Data Display",
        page_icon="🛰️",
        layout="wide"
    )
    
    st.title("🛰️ NASA MODIS AQUA Data Display")
    st.markdown("---")
    
    # Check if dataframe was loaded successfully
    if restored_df is not None:
        st.success(f"✅ Successfully loaded NASA data with {restored_df.shape[0]} rows and {restored_df.shape[1]} columns")
        
        # Display basic information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Rows", restored_df.shape[0])
        
        with col2:
            st.metric("Total Columns", restored_df.shape[1])
        
        with col3:
            st.metric("Data Size", f"{restored_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        st.markdown("---")
        
        # Display column information
        st.subheader("📋 Dataset Information")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("**Columns:**")
            for col in restored_df.columns:
                st.write(f"• {col}")
        
        with col2:
            st.write("**Data Types:**")
            dtype_df = pd.DataFrame({
                'Column': restored_df.dtypes.index,
                'Data Type': restored_df.dtypes.values
            })
            st.dataframe(dtype_df, use_container_width=True)
        
        st.markdown("---")
        
        # Display data preview
        st.subheader("🔍 Data Preview")
        
        # Add filters/options
        preview_options = st.radio(
            "Choose preview option:",
            ["First 10 rows", "Last 10 rows", "Random sample", "Custom range"]
        )
        
        if preview_options == "First 10 rows":
            st.dataframe(restored_df.head(10), use_container_width=True)
        
        elif preview_options == "Last 10 rows":
            st.dataframe(restored_df.tail(10), use_container_width=True)
        
        elif preview_options == "Random sample":
            sample_size = st.slider("Sample size:", 1, min(100, len(restored_df)), 10)
            st.dataframe(restored_df.sample(n=sample_size), use_container_width=True)
        
        elif preview_options == "Custom range":
            col1, col2 = st.columns(2)
            with col1:
                start_row = st.number_input("Start row:", 0, len(restored_df)-1, 0)
            with col2:
                end_row = st.number_input("End row:", start_row+1, len(restored_df), min(start_row+10, len(restored_df)))
            
            st.dataframe(restored_df.iloc[start_row:end_row], use_container_width=True)
        
        st.markdown("---")
        
        # Display statistical summary
        st.subheader("📊 Statistical Summary")
        
        # Only show numeric columns for statistics
        numeric_cols = restored_df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) > 0:
            st.write("**Numeric Columns Summary:**")
            st.dataframe(restored_df[numeric_cols].describe(), use_container_width=True)
        else:
            st.info("No numeric columns found for statistical summary.")
        
        # Show non-numeric columns info
        non_numeric_cols = restored_df.select_dtypes(exclude=['number']).columns
        if len(non_numeric_cols) > 0:
            st.write("**Non-numeric Columns:**")
            for col in non_numeric_cols:
                unique_count = restored_df[col].nunique()
                st.write(f"• **{col}**: {unique_count} unique values")
        
        st.markdown("---")
        
        # Data download option
        st.subheader("💾 Download Data")
        
        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')
        
        csv_data = convert_df_to_csv(restored_df)
        
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name="nasa_modis_data.csv",
            mime="text/csv"
        )
        
    else:
        st.error("❌ Failed to load NASA data. Please check the data file and try again.")
        st.info("Make sure the 'nasa_data_df.pkl' file exists in the 'nasa_data' directory.")

if __name__ == "__main__":
    main()