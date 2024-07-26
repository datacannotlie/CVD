import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
from scipy import stats

# Loading datasets into variables
df_cvd = pd.read_csv('cardiovascular-disease-death-rate-61-20.csv')
df_h = pd.read_csv('health_care_exp_GDP_00_21.csv')

# transforming wide table to long table
df_hc = df_h.melt(id_vars="Country Name")

# Casting string datatype into int datatype (Year)
df_hc["variable"] = df_hc["variable"].astype(int)

# Slicing the dataframe to contain only data from 2000 to 2020
df_cvd = df_cvd.loc[(df_cvd['Year'] >= 2000) & (df_cvd['Year'] <= 2020)]
df_hc = df_hc.loc[(df_hc['variable'] >= 2000) & (df_hc['variable'] <= 2020)]

# Countries and their data
countries = ['Brazil', 'United States', 'Finland', 'Japan', 'Australia', 'Cuba']
color_palette = sns.color_palette("Set2", 6)

# Calculate regression parameters and x-intercepts
x_intercepts = []

for country in countries:
    hc_data = df_hc.loc[df_hc['Country Name'] == country]
    cvd_data = df_cvd.loc[df_cvd['Entity'] == country]

    if country == 'Australia':
        hc_data = hc_data[:20]
        cvd_data = cvd_data[:20]

    slope, intercept, _, _, _ = stats.linregress(hc_data['value'], cvd_data['Deaths'])
    x_intercept = -intercept / slope
    x_intercepts.append(x_intercept)

fig = go.Figure()

for country, color, x_intercept in zip(countries, color_palette, x_intercepts):
    fig.add_trace(go.Bar(x=[country], y=[x_intercept], marker_color=f'rgb{color}', name=country))

fig.update_layout(
    # title='Projected Healthcare Expenditure to minimize CVD Deaths',
    xaxis_title='Country',
    yaxis_title='Healthcare expenditure (% of GDP)',
    template='ggplot2',
    font=dict(
        family="Arial, monospace",
        size=20,
        color="black"),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Rockwell"
    ),
    hovermode="x unified",
    
    title={
    'text':'Projected Healthcare Expenditure to minimize CVD Deaths',
    'y':0.95,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'}

)

fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')

fig.write_html("hc_projection.html")

fig.show()
