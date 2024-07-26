import plotly.express as px
import pandas as pd

data = pd.read_csv('cardiovascular-disease-death-rate-61-20.csv')

# Convert 'Year' to numeric type if it's not already
data['Year'] = pd.to_numeric(data['Year'], errors='coerce')

# Filter the data for years between 2000 and 2020 and specific countries
countries_of_interest = ['Australia', 'Cuba', 'Japan', 'Brazil', 'Finland', 'United States']
data = data[(data['Year'] >= 2000) & (data['Year'] <= 2020) & (data['Entity'].isin(countries_of_interest))]

# Sort the data by Year and Entity
data = data.sort_values(['Year', 'Entity'])

# Create animated line graph
fig = px.line(
    data,
    x='Year', 
    y='Deaths', 
    color='Entity',
    line_group='Entity',
    hover_name='Entity',
    range_y=[0, data['Deaths'].max() * 1.1],  # Set y-axis range with a little headroom
    title='Deaths by CVD / 100,000 people (2000-2020)',
    labels={'Deaths': 'Deaths per 100,000', 'Entity': 'Country'}
)

fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Deaths per 100,000',
    legend_title='Country',
    hovermode="x unified",
    font=dict(
        family="Arial, monospace",
        size=20,
        color="black"),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Rockwell"
    ),
    
    title={
        'text': "Deaths by CVD / 100,000 people (2000-2020)",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    
)

fig.update_traces(mode="lines+markers", marker=dict(size=8))

# Add animation
fig.update_traces(mode="lines+markers")

fig.write_html("line_cvd_2000_2020.html")

fig.show()