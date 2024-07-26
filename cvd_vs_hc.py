import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

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

fig = go.Figure()

for country, color in zip(countries, color_palette):
    cvd_data = df_cvd.loc[df_cvd['Entity'] == country].reset_index(drop=True)
    hc_data = df_hc.loc[df_hc['Country Name'] == country].reset_index(drop=True)

    # Sort healthcare expenditure data by year
    hc_data = hc_data.sort_values(by='variable').reset_index(drop=True)

    # Merge the dataframes based on the year
    merged_data = pd.merge(cvd_data, hc_data, left_on='Year', right_on='variable', how='inner')

    fig.add_trace(go.Scatter(x=merged_data['value'], y=merged_data['Deaths'], mode='markers', name=country, marker=dict(color=f'rgb{color}', size=12)))

    # Add regression line
    X = merged_data['value']
    Y = merged_data['Deaths']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    fig.add_trace(go.Scatter(x=merged_data['value'], y=model.predict(X), mode='lines', name=f'{country} Regression', line=dict(color=f'rgb{color}')))

fig.update_layout(
    # title='CVD Deaths as Function of Healthcare Expenditure',
    xaxis_title='Healthcare expenditure (% of GDP)',
    yaxis_title='Deaths per 100,000 people',
    legend=dict(font=dict(size=12)),
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
    'text':'CVD Deaths as Function of Healthcare Expenditure',
    'y':0.95,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'}
)


fig.write_html("cvd_hc.html")

fig.show()
