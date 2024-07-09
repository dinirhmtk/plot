import streamlit as st
import pandas as pd
import plotly.express as px # type: ignore

# Load the Excel file
file_path = 'indikator.xlsx'
xls = pd.ExcelFile(file_path)

# Load the data from each sheet
sheet_names = xls.sheet_names
data = {sheet: pd.read_excel(xls, sheet) for sheet in sheet_names}

# Streamlit app
st.title('Visualisasi Data Perusahaan Asuransi')

# Step 1: Select sheet
selected_sheet = st.selectbox('Pilih Sheet', sheet_names)

# Load the selected sheet data
selected_data = data[selected_sheet]

# Ensure 'report_date' column exists and is in datetime format
if 'REPORT_DATE' in selected_data.columns:
    selected_data['REPORT_DATE'] = pd.to_datetime(selected_data['REPORT_DATE'])
else:
    st.error('Kolom Report Date tidak ditemukan pada sheet yang dipilih.')
    st.stop()

# Step 2: Select companies
companies = selected_data['NAMA_PA_Infobank'].unique().tolist()
selected_companies = st.multiselect('Pilih Perusahaan Asuransi', companies, default=companies)

# Filter data based on selected companies
filtered_data = selected_data[selected_data['NAMA_PA_Infobank'].isin(selected_companies)]

# Step 3: Select two ratios
ratios = selected_data.columns[2:].tolist()
selected_ratio_x = st.selectbox('Pilih Rasio untuk Sumbu X', ratios)
selected_ratio_y = st.selectbox('Pilih Rasio untuk Sumbu Y', ratios)

# Plot scatter plot for the selected ratios
if selected_ratio_x and selected_ratio_y:
    fig = px.scatter(filtered_data, x=selected_ratio_x, y=selected_ratio_y, color='NAMA_PA_Infobank', hover_name='NAMA_PA_Infobank',
                     animation_frame='REPORT_DATE',
                     title=f'Scatter Plot {selected_ratio_x} vs {selected_ratio_y} dari Perusahaan Asuransi yang Dipilih',
                     labels={selected_ratio_x: selected_ratio_x, selected_ratio_y: selected_ratio_y})
    st.plotly_chart(fig)