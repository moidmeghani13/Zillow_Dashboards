import json
import pandas as pd
import geopandas as gpd

import dash
from dash import dcc, html
import plotly.express as px

DATA_PATH = "data/processed/zhvi_long.parquet"

df = pd.read_parquet(DATA_PATH)

tx_df = df[df["StateName"] == "TX"]

latest_date = tx_df["date"].max()
map_df = tx_df[tx_df["date"] == latest_date].copy()

map_df = map_df.dropna(subset=["zhvi_yoy"])

GEO_PATH = "data/geo/us_zipcodes.geojson"

with open(GEO_PATH) as f:
    zip_geojson = json.load(f)

fig_map = px.choropleth_map(
    map_df,
    geojson=zip_geojson,
    locations="zip",
    featureidkey="properties.zip",
    color="zhvi_yoy",
    color_continuous_scale="RdYlGn",
    opacity=0.5,
    map_style="open-street-map",
    zoom=5.5,
    hover_name="City",
    hover_data={
        "zip": True,
        "zhvi_yoy": ":.2%",
    },
    center={"lat": 31.5, "lon": -99.3},
    labels={"zhvi_yoy": "YoY Price Growth"},
)

fig_map.update_layout(
    mapbox=dict(
        bearing=0,
        pitch=0
    )
)

fig_map.update_traces(marker_line_width=.25)

fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(
    title=f"Texas Home Price YoY Growth ({latest_date:%B %Y})",
    margin={"r":0,"t":50,"l":0,"b":0}
)

fig_map.update_layout(
    coloraxis_colorbar=dict(
        title="YoY Price Growth",
        tickformat=".0%",  # shows 0.05 as 5%
    )
)

#DASH APP
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Texas Housing Price Dashboard"),

        dcc.Graph(
            id="zip-map",
            figure=fig_map,
            style={"height": "85vh"},
            config={
                "displayModeBar": True,
                "displaylogo": False,
                "scrollZoom": False,
                "modeBarButtonsToAdd": [
                    "zoomInMapbox",
                    "zoomOutMapbox",
                    "resetViewMapbox",
                ],
            },
        )
    ],
    style={"width": "100%", "padding": "10px"}
)

if __name__ == "__main__":
    app.run(debug=True)