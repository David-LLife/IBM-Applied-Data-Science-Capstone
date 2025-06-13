# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

print(spacex_df['Launch Site'].value_counts())
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id=
                                'site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    ],
                                value='ALL',
                                placeholder='Select a Launch Site here',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    5000: '5000',
                                                    10000: '10000',},
                                                value=[min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
     Output(component_id = 'success-pie-chart', component_property = 'figure'),
     [Input(component_id = 'site-dropdown', component_property = 'value')]
)
def piegraph_update(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(
                spacex_df[spacex_df['class'] == 1],
                names = 'Launch Site',
                title = 'Successful Launches by Site',
                color_discrete_sequence=px.colors.sequential.Agsunset
            )
    else:
        fig = px.pie(
                spacex_df.loc[spacex_df['Launch Site'] == site_dropdown],
                names = 'class',
                title = f'Percentage of Successful Launches (class=1) for Site {site_dropdown}',
                color_discrete_sequence=["red", "blue"],
                category_orders={"class": [0, 1]}
            )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
     Output(component_id='success-payload-scatter-chart', component_property='figure'),
     [
        Input(component_id = 'site-dropdown', component_property = 'value'),
        Input(component_id="payload-slider", component_property="value")
     ]
)
def scatter_plot_update(site_dropdown, payload_slider):
    lowest, highest = payload_slider
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(lowest, highest)]
    if site_dropdown == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version Category"
        )
    else:
        fig = px.scatter(
            filtered_df[filtered_df['Launch Site'] == site_dropdown],
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version Category"
        )
    return fig

# Run the app
if __name__ == '__main__':
    print(spacex_df[['class', 'Launch Site']].value_counts())
    app.run()
