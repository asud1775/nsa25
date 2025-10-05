import io
import tempfile
import cartopy
from matplotlib import animation, pyplot as plt
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from PIL import Image

# Add parent directory to path to import data module
sys.path.append(str(Path(__file__).parent.parent))
from data.modis_aqua_data import load_nasa_modis_images

images_directory = "/Users/ashrayuddaraju/Documents/GitHub/nsa25_practice/nasa_data/images"
    
crs_proj = cartopy.crs.Robinson()
crs_data = cartopy.crs.PlateCarree()

st.set_page_config(page_title="MODIS_NASA", layout="wide")
st.title("MODIS_NASA")

with st.spinner("Reading data and generating animation..."):
    nasa_df = load_nasa_modis_images()

    # Check if data was loaded successfully
    if nasa_df is not None:
        def create_animation_from_images(df, image_column, duration=1000):
            """
            Create an animated GIF directly from PIL Images stored in the dataframe
            
            Args:
                df: DataFrame containing image data
                image_column: Name of the column containing PIL Images
                duration: Duration per frame in milliseconds
                
            Returns:
                Animated GIF data only
            """
            try:
                # Get images from the specified column
                image_data = df[image_column].dropna()
                
                if len(image_data) == 0:
                    st.error("No valid image data found in the selected column.")
                    return None, 0
                
                # Sort by year and month if available for chronological animation
                if 'year' in df.columns and 'month' in df.columns:
                    df_sorted = df.dropna(subset=[image_column]).sort_values(['year', 'month'])
                    image_data = df_sorted[image_column]
                    st.info(f"ℹ️ Images sorted chronologically by year and month")
                
                # Use all available images from filtered data
                selected_images = image_data
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                processed_images = []
                
                for i, img in enumerate(selected_images):
                    status_text.text(f"Processing image {i+1}/{len(selected_images)}")
                    
                    if hasattr(img, 'size'):  # Check if it's a PIL Image
                        # Resize image to standard size for animation consistency
                        img_resized = img.resize((800, 600), Image.Resampling.LANCZOS)
                        processed_images.append(img_resized)
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(selected_images))
                
                progress_bar.empty()
                status_text.empty()
                
                if len(processed_images) > 1:
                    # Create animated GIF
                    gif_buffer = io.BytesIO()
                    processed_images[0].save(
                        gif_buffer,
                        format='GIF',
                        save_all=True,
                        append_images=processed_images[1:],
                        duration=duration,
                        loop=0  # Infinite loop
                    )
                    gif_buffer.seek(0)
                    
                    return gif_buffer.getvalue()
                else:
                    st.warning("Need at least 2 images to create an animation.")
                    return None
                    
            except Exception as e:
                st.error(f"Error creating animation from image data: {e}")
                return None
        
        # Find image columns in the dataframe
        image_columns = []
        for col in nasa_df.columns:
            if col == 'image':  # Only consider 'image' column for animation
                image_columns.append(col)
        
        # Let user select which image column to use for animation         
        if image_columns:
            selected_image_col = image_columns[0]  # Use the first (and only) image column

            # Animation controls
            st.subheader("🎛️ Animation Settings")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Dynamic FPS selector
                st.write("**Animation Speed (FPS)**")
                fps_options = {
                    "1.0 FPS (Very Slow)": 1.0,
                    "2.0 FPS (Slow)": 2.0,
                    "5.0 FPS (Normal)": 5.0,
                    "10.0 FPS (Fast)": 10.0,
                    "15.0 FPS (Very Fast)": 15.0
                }
                
                selected_fps_label = st.selectbox(
                    "Select animation speed:",
                    options=list(fps_options.keys()),
                    index=2,  # Default to Normal (5.0 FPS)
                    key="fps_select"
                )
                
                # Get the actual FPS value
                selected_fps = fps_options[selected_fps_label]
                st.write(f"**Selected FPS:** {selected_fps}")

                # Calculate frame duration in milliseconds
                frame_duration = int(1000 / selected_fps)
                st.write(f"**Frame Duration:** {frame_duration} ms per frame")

                # Display real-time feedback
                st.metric("Current FPS", f"{selected_fps}", 
                    help=f"Frame duration: {frame_duration}ms per frame")
                
                # Additional info
                total_seconds = f"{1/selected_fps:.1f}" if selected_fps > 0 else "∞"
                st.caption(f"⏱️ {total_seconds} seconds per frame")
            
            with col2:
                # Year range filter if available
                if 'year' in nasa_df.columns:
                    min_year = int(nasa_df['year'].min())
                    max_year = int(nasa_df['year'].max())
                    year_range = st.slider(
                        "Year Range Filter:",
                        min_value=min_year,
                        max_value=max_year,
                        value=(min_year, max_year),
                        key="year_range_slider"
                    )
                    st.caption(f"Selected: {year_range[0]} - {year_range[1]}")
                else:
                    year_range = None
            
            with col3:
                # Month range filter if available
                if 'month' in nasa_df.columns:
                    # Month names mapping
                    month_names = {
                        1: "January", 2: "February", 3: "March", 4: "April",
                        5: "May", 6: "June", 7: "July", 8: "August",
                        9: "September", 10: "October", 11: "November", 12: "December"
                    }
                    
                    min_month = int(nasa_df['month'].min())
                    max_month = int(nasa_df['month'].max())
                    
                    # Create a select slider with month names
                    available_months = list(range(min_month, max_month + 1))
                    month_options = [month_names[month] for month in available_months]
                    
                    # Use select_slider for month names
                    selected_month_names = st.select_slider(
                        "Month Range Filter:",
                        options=month_options,
                        value=(month_names[min_month], month_names[max_month]),
                        key="month_range_slider"
                    )
                    
                    # Convert back to month numbers for filtering
                    name_to_number = {v: k for k, v in month_names.items()}
                    if isinstance(selected_month_names, tuple):
                        month_range = (name_to_number[selected_month_names[0]], name_to_number[selected_month_names[1]])
                    else:
                        month_range = (name_to_number[selected_month_names], name_to_number[selected_month_names])
                    st.caption(f"Selected: {month_names.get(month_range[0], month_range[0])} - {month_names.get(month_range[1], month_range[1])}")
                else:
                    month_range = None
            
            # Filter data based on year and month ranges
            filtered_nasa_df = nasa_df.copy()
            filter_info = []
            
            if year_range is not None:
                filtered_nasa_df = filtered_nasa_df[
                    (filtered_nasa_df['year'] >= year_range[0]) & 
                    (filtered_nasa_df['year'] <= year_range[1])
                ]
                filter_info.append(f"Years: {year_range[0]}-{year_range[1]}")
            
            if month_range is not None:
                filtered_nasa_df = filtered_nasa_df[
                    (filtered_nasa_df['month'] >= month_range[0]) & 
                    (filtered_nasa_df['month'] <= month_range[1])
                ]
                # Month names for display
                month_names = {
                    1: "January", 2: "February", 3: "March", 4: "April",
                    5: "May", 6: "June", 7: "July", 8: "August",
                    9: "September", 10: "October", 11: "November", 12: "December"
                }
                start_month = month_names.get(month_range[0], str(month_range[0]))
                end_month = month_names.get(month_range[1], str(month_range[1]))
                filter_info.append(f"Months: {start_month}-{end_month}")
            
            if filter_info:
                st.info(f"📊 Filtered data: {len(filtered_nasa_df)} records ({', '.join(filter_info)})")
            else:
                st.info(f"📊 Using all data: {len(filtered_nasa_df)} records")
            
            # Update image count based on filtered data
            image_count = int(filtered_nasa_df[selected_image_col].count())
            
            # Frame duration is already calculated in col1 based on selected_fps
            # No need for additional conversion
            
            # Create animation button
            if st.button("🎬 Create NASA Data Animation", type="primary", use_container_width=True):
                with st.spinner("Creating animation from NASA image data... This may take a few minutes..."):
                    # Calculate number of frames from filtered data
                    num_frames = len(filtered_nasa_df[selected_image_col].dropna())
                    
                    gif_data = create_animation_from_images(
                        filtered_nasa_df, selected_image_col, duration=frame_duration
                    )
                    
                    if gif_data is not None:
                        st.success(f"✅ Successfully created animation with {num_frames} frames!")
                        
                        # Display the animated GIF
                        st.subheader("🎬 NASA MODIS AQUA Animation")
                        st.image(gif_data, caption=f"Animated NASA Data from '{selected_image_col}' ({num_frames} frames, {selected_fps} FPS)", width=800)
                        
                        # Animation info
                        total_duration = (num_frames * frame_duration) / 1000
                        st.info(f"📊 Animation Info: {num_frames} frames • {frame_duration}ms per frame • ~{total_duration:.1f}s total duration")
                        
                        # Provide download button
                        st.download_button(
                            label="📥 Download NASA Animation (GIF)",
                            data=gif_data,
                            file_name=f"nasa_modis_animation_{num_frames}frames.gif",
                            mime="image/gif",
                            use_container_width=True
                        )
                    else:
                        st.error("❌ Failed to create animation from NASA image data.")
        else:
            st.warning("⚠️ No image columns found in the data. Need at least 2 images to create an animation.")

    else:
        st.error("❌ Failed to load NASA data. Please check the data source and file paths.")
