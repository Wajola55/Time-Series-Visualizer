import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from io import BytesIO
import plotly.io as pio
from PIL import Image
from datetime import datetime


st.set_page_config(page_title="Time Series Visualizer")

page_bg_img = """
<style>
[data-testid="stSidebar"] {
background-color: #f7f7e6;
opacity: 0.8;
background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #f7f7e6 10px ), repeating-linear-gradient( #e8fc8a55, #e8fc8a );
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Define the color palette
PRIMARY_COLOR = "#dada8d"
DARKER_COLOR = "#9b9b6e"

# Set the color of the page title and subtitle
st.markdown(f"<h1 style='color:{PRIMARY_COLOR};font-size:50px;'>Time Series Visualizer</h1>", unsafe_allow_html=True)
st.write("This app allows you to visualize time series data from a CSV file. It is designed for anyone who needs to quickly explore and analyze time-based data. ")


st.markdown(f"<h1 style='color:{PRIMARY_COLOR};font-size:30px;'>How to Use</h1>", unsafe_allow_html=True)
st.write("To get started, upload a CSV file containing your time series data. Then select the X and Y axis columns, choose a chart type (line, area, or scatter) and customize the chart with title, labels, and color.") 


st.markdown(f"<h1 style='color:{PRIMARY_COLOR};font-size:30px;'>Limitations</h1>", unsafe_allow_html=True)
st.write("Please note that this app currently supports only CSV files with a time-based index.")


df = None

file = st.file_uploader("Upload CSV file", type=["csv"])

# Function to detect date column
def detect_date_column(df):
    date_columns = []
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_datetime(df[col])
                date_columns.append(col)
            except ValueError:
                pass
    return date_columns

# Display file contents as table
if file is not None:
    df = pd.read_csv(file)

    date_columns = detect_date_column(df)

    if len(date_columns) > 0:
        st.write("Detected date columns:", date_columns)
        for date_col in date_columns:
            df.set_index(date_col, inplace=True)
            st.write(df)
    else:
        st.write("No date columns detected.")
        st.write(df)

    # Plot data
    if df is not None:
        columns = df.columns.tolist()

        # Chart type selection
        st.sidebar.markdown(f"<h2 style='color:{DARKER_COLOR};font-size:22px;'>Chart Settings</h2>", unsafe_allow_html=True)
        chart_type = st.sidebar.selectbox("Select chart type", ["line", "area", "scatter", "bar", "histogram"])

        # Chart customization options
        st.sidebar.markdown(f"<h2 style='color:{DARKER_COLOR};font-size:22px;'>Chart Customization</h2>", unsafe_allow_html=True)
        chart_title = st.sidebar.text_input("Chart title", value="Time Series Chart")
        x_label = st.sidebar.text_input("X axis label", value="Date")
        y_label = st.sidebar.text_input("Y axis label", value="Value")
        color = st.sidebar.color_picker("Select chart color", value="#1f77b4")

        # Update DataFrame column names and columns list
        df.columns = [x_label if col == date_col else col for col in df.columns]
        columns = df.columns.tolist()

        


        unique_years = sorted(list(set(df.index.year)))
        selected_years = st.multiselect("Select years to display", unique_years, default=unique_years)

        df_filtered = df[df.index.year.isin(selected_years)]



        if chart_type == "line":
            fig = px.line(df_filtered, x=df_filtered.index, title=chart_title)
            fig.update_traces(line_color=color)
        elif chart_type == "area":
            fig = px.area(df_filtered, x=df_filtered.index, title=chart_title)
            fig.update_traces(line_color=color)
        elif chart_type == "scatter":
            fig = px.scatter(df_filtered, x=df_filtered.index, title=chart_title)
            fig.update_traces(marker_color=color)
        elif chart_type == "bar":
            fig = px.bar(df_filtered, x=df_filtered.index,title=chart_title)
            fig.update_traces(marker_color=color)
        elif chart_type == "histogram":
            fig = px.histogram(df_filtered, x=df_filtered.index,title=chart_title)
        fig.update_traces(marker_color=color)



        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label,
           
        )

        st.plotly_chart(fig)

        
        # Save Plotly figure as a PNG image
        img_bytes = pio.to_image(fig, format="png")

        # Encode the PNG image to base64
        b64 = base64.b64encode(img_bytes).decode()

        # Provide a download link for the chart
        href = f'<a href="data:image/png;base64,{b64}" download="{chart_title}.png">Download Chart</a>'
        st.markdown(href, unsafe_allow_html=True)



else:
    st.write("Upload a CSV file to get started.")



streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=Space+Mono&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Playfair Display', serif;
			}

			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)
# --- hide streamlit style ---

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)