import plotly.express as px
import pandas as pd

# Read the CSV file
data = pd.read_csv('healthcare.csv')

# Convert 'Year' to numeric type if it's not already
data['Year'] = pd.to_numeric(data['Year'], errors='coerce')

# Filter the data for years between 2000 and 2020 and specific countries
countries_of_interest = ['Australia', 'Cuba', 'Japan', 'Brazil', 'Finland', 'United States']
data = data[(data['Year'] >= 2000) & (data['Year'] <= 2020) & (data['Country Name'].isin(countries_of_interest))]

# Sort the data by Year and Country Name
data = data.sort_values(['Year', 'Country Name'])

# Create animated line graph
fig = px.line(
    data,
    x='Year',
    y='Expenditure',
    color='Country Name',
    line_group='Country Name',
    hover_name='Country Name',
    range_y=[0, data['Expenditure'].max() * 1.1],  # Set y-axis range with a little headroom
    title='Healthcare Expenditure as % of GDP (2000-2020)',
    labels={'Expenditure': '% of GDP', 'Country Name': 'Country'}
)

fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Healthcare Expenditure (% of GDP)',
    legend_title='Country',
    hovermode="x unified",
    font=dict(
        family="Arial, sans-serif",
        size=20,
        color="black"
    ),

    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Rockwell"
    ),

    title={
        'text': 'Healthcare Expenditure as % of GDP (2000-2020)',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

fig.update_traces(mode="lines+markers", marker=dict(size=8))

# Save and show the figure
fig.write_html("line_hc_2000_2020.html")
fig.show()