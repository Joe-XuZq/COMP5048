import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plotly.validators.pointcloud.marker import border

# Load the CSV data into a DataFrame
df = pd.read_csv('grouped subset of Group Dynamic.csv')

# Create the Dash application
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    style={'background-image': 'url("/assets/world map.png")',
           'background-repeat': 'no-repeat',
           'background-size': 'cover',
           'height': '100vh'
           },
    children=[
        html.Div(
            dcc.Graph(
                id='sankey-diagram-na'
            ),
            style={'position': 'absolute', 'top': '100px', 'left': '10px'}
        ),
        html.Div(
            dcc.Graph(
                id='sankey-diagram-jp'
            ),
            style={'position': 'absolute', 'top': '100px', 'right': '0px'}
        ),
        html.Div(
            dcc.Graph(
                id='sankey-diagram-eu'
            ),
            style={'position': 'absolute', 'top': '50px', 'left': '650px'}
        ),
        html.Div(
            dcc.Graph(
                id='sankey-diagram-other'
            ),
            style={'position': 'absolute', 'bottom': '10px', 'left': '850px'}
        ),
        # dcc.Slider(
        #     id='year-slider',
        #     min=df['Year'].min(),
        #     max=2015,
        #     value=df['Year'].min(),
        #     marks={str(year): str(year) for year in df['Year'].unique()},
        #     step=None
        # ),
        dcc.Interval(
            id='interval',
            interval=2000,  # Update every 1 second (adjust as needed)
            n_intervals=0
        )
    ])


# Create the Sankey diagram
def create_sankey_diagram(filtered_df, region, year):
    node_labels = (
            filtered_df['Genre'].unique().tolist() +
            filtered_df['Publisher'].unique().tolist() +
            filtered_df['Game'].unique().tolist()
    )
    node_indices = {label: index for index, label in enumerate(node_labels)}

    source_indices = [node_indices[genre] for genre in filtered_df['Genre']]
    target_indices_publisher = [
        node_indices[publisher] for publisher in filtered_df['Publisher']
    ]
    target_indices_game = [
        node_indices[game] for game in filtered_df['Game']
    ]

    values_publisher = filtered_df.groupby(['Genre', 'Publisher'])[f'{region}_Sales'].sum()
    values_game = filtered_df.groupby(['Genre', 'Publisher', 'Game'])[f'{region}_Sales'].max()

    link_source = (
            source_indices +
            target_indices_publisher
    )
    link_target = (
            target_indices_publisher +
            target_indices_game
    )
    link_value = (
            values_publisher.tolist() +
            values_game.tolist()
    )

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=node_labels,
        ),
        link=dict(
            source=link_source,
            target=link_target,
            value=link_value,
            color='rgba(0, 0, 255, 0.3)',
        )
    )])

    fig.update_layout(
        title_text=f"Best-Selling Publishers and Games under Each Genre in {region} for {year}",
        title_x=0,
        font=dict(size=10.5, color='darkred'),
        margin=dict(l=0, r=30, b=20, t=30),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        height=300,
        width=550
    )

    return fig


# Define the callback function for NA region
@app.callback(
    Output('sankey-diagram-na', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_sankey_na(n_intervals):
    year = df['Year'].min() + (n_intervals % (df['Year'].max() - df['Year'].min() + 1))
    filtered_df = df[df['Year'] == year]
    genre_max_sales = filtered_df.groupby('Genre')['NA_Sales'].transform(max)
    filtered_df = filtered_df[filtered_df['NA_Sales'] == genre_max_sales]
    filtered_df = filtered_df.groupby(['Genre', 'Publisher', 'Game'])['NA_Sales'].sum().reset_index()
    fig_na = create_sankey_diagram(filtered_df, region='NA', year=year)

    return fig_na


# Define the callback function for JP region
@app.callback(
    Output('sankey-diagram-jp', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_sankey_jp(n_intervals):
    year = df['Year'].min() + (n_intervals % (df['Year'].max() - df['Year'].min() + 1))
    filtered_df = df[df['Year'] == year]
    genre_max_sales = filtered_df.groupby('Genre')['JP_Sales'].transform(max)
    filtered_df = filtered_df[filtered_df['JP_Sales'] == genre_max_sales]
    filtered_df = filtered_df.groupby(['Genre', 'Publisher', 'Game'])['JP_Sales'].sum().reset_index()
    fig_jp = create_sankey_diagram(filtered_df, region='JP', year=year)

    return fig_jp


# Define the callback function for EU region
@app.callback(
    Output('sankey-diagram-eu', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_sankey_eu(n_intervals):
    year = df['Year'].min() + (n_intervals % (df['Year'].max() - df['Year'].min() + 1))
    filtered_df = df[df['Year'] == year]
    genre_max_sales = filtered_df.groupby('Genre')['EU_Sales'].transform(max)
    filtered_df = filtered_df[filtered_df['EU_Sales'] == genre_max_sales]
    filtered_df = filtered_df.groupby(['Genre', 'Publisher', 'Game'])['EU_Sales'].sum().reset_index()
    fig_eu = create_sankey_diagram(filtered_df, region='EU', year=year)

    return fig_eu


# Define the callback function for Other region
@app.callback(
    Output('sankey-diagram-other', 'figure'),
    [Input('interval', 'n_intervals')]
)
def update_sankey_other(n_intervals):
    year = df['Year'].min() + (n_intervals % (df['Year'].max() - df['Year'].min() + 1))
    filtered_df = df[df['Year'] == year]
    genre_max_sales = filtered_df.groupby('Genre')['Other_Sales'].transform(max)
    filtered_df = filtered_df[filtered_df['Other_Sales'] == genre_max_sales]
    filtered_df = filtered_df.groupby(['Genre', 'Publisher', 'Game'])['Other_Sales'].sum().reset_index()
    fig_other = create_sankey_diagram(filtered_df, region='Other', year=year)

    return fig_other


# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
