# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import logging
import numpy as np
import pandas as pd
import plotly
import chart_studio
import plotly.express as px
import plotly.graph_objects as go


# %%
PROVINCES_JSON_FILENAME = 'provinces.json'
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoibGlzdGVuemNjIiwiYSI6ImNrMzU5MmpxZDAxMXEzbXQ0dnd4YTZ2NDAifQ.GohcgYXFsbDqfsi_7SXdpA'
HTML_FILENAME = 'a.html'
px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

LOG_FILENAME = "lastlog.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
with open(LOG_FILENAME, 'w') as f:
    f.writelines([LOG_FORMAT, '\n'])
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format=LOG_FORMAT)


# %%
provinces_df = pd.read_json(PROVINCES_JSON_FILENAME)
provinces_df


# %%
# fig = px.scatter_mapbox(provinces_df, lat="lat", lon="lng",
#                         color="log_confirmedCount",
#                         # size="confirmedCount",
#                         size_max=20,
#                         color_continuous_scale=px.colors.carto.Redor,
#                         zoom=2
#                        )
# with open(HTML_FILENAME, 'w') as f:
#     f.write(fig.to_html())


# %%
provinces_df.provinceName + '-' + provinces_df.cityName + '-' + provinces_df.confirmedCount.astype(str)


# %%
marker = go.scattermapbox.Marker(
    size=9,
    color=np.log10(provinces_df['confirmedCount']+1),
    colorscale=px.colors.carto.Redor,
    showscale=True)

mapbox = go.layout.Mapbox(
    accesstoken=MAPBOX_ACCESS_TOKEN,
    bearing=0,
    pitch=0,
    zoom=3,
    center=go.layout.mapbox.Center(
        lat=provinces_df.lat.mean(),
        lon=provinces_df.lng.mean()))

displays = dict(
    # Scattermapbox
    mode='markers',
    marker=marker,
    lat=provinces_df.lat,
    lon=provinces_df.lng,
    text=provinces_df.provinceName + '-' + provinces_df.cityName + '-' + provinces_df.confirmedCount.astype(str),
    # Layout
    autosize=True,
    hovermode='closest',
    mapbox=mapbox,
)


scatter = go.Scattermapbox(
        lat=displays['lat'],
        lon=displays['lon'],
        mode=displays['mode'],
        text=displays['text'],
        marker=displays['marker'])

fig = go.FigureWidget([scatter])

fig.update_layout(
    autosize=displays['autosize'],
    hovermode=displays['hovermode'],
    mapbox=displays['mapbox'],
    clickmode='event',
    title_text='a',
)

def update_point(trace, points, selector):
    print('aaaaaa')
    fig.update_layout(title_text='GDP and Life Expectancy (Americas, 2007)')

fig.data[0].on_click(update_point, append=False)
print('Done.')


# %%
with open(HTML_FILENAME, 'w') as f:
    f.write(fig.to_html())
