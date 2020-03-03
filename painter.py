"""
Painting ncov counts using plotly.
"""

import json
import logging
import numpy as np
import pandas as pd
from local_profiles import profiles
from mapper_server import MAPPER_SERVER

from _plotly_future_ import remove_deprecations
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


class PAINTER():
    def __init__(self):
        """
        Builtin init method.
        """
        logging.info('PAINTER starts.')
        self.count_cols = ['confirmedCount',
                           'suspectedCount',
                           'curedCount',
                           'deadCount']

    def load(self, raw_df):
        """
        Load new raw_df
        inputs:
            raw_df: DataFrame containing raw counting.
        """
        self.raw_df = raw_df.set_index('provinceName', drop=False)
        self._prepare_country_df()
        self._prepare_provinces_df()
        logging.info('New raw_df loaded.')

    def _prepare_country_df(self):
        """
        Prepare country_df for plotting.
        yield:
            self.country_df: DataFrame containing counts of provinces
            self.countryName: Name of the country
        """
        country_df = self.raw_df[['provinceName'] + self.count_cols]
        country_df = country_df.set_index('provinceName', drop=False)
        self.country_df = country_df
        self.countryName = '全国'
        logging.info('New country_df prepared.')

    def _prepare_provinces_df(self):
        """
        Prepare provinces_df for plotting.
        yield:
            self.provinceNames: List of names of provinces
            self.provinces_df: DataFrame containing counts of cities
        """
        ms = MAPPER_SERVER()
        self.provinceNames = []
        provinces_df = pd.DataFrame()
        for prov in self.country_df.index.unique():
            # Read from self.raw_df
            cities = self.raw_df.loc[prov].cities
            if not cities:
                continue
            self.provinceNames.append(prov)
            if isinstance(cities, pd.Series):
                cities = pd.DataFrame(cities).T
            else:
                cities = pd.DataFrame(cities)
            # Add provinceName
            cities['provinceName'] = prov
            # Add latitude and longtitude
            try:
                names = prov + ' ' + cities['cityName']
                latlng = [ms.checkout(name) for name in names]
            except:
                latlng = []
                for name in names:
                    latlng.append(ms.checkout(name))
            cities['latitude'] = [e[0] for e in latlng]
            cities['longitude'] = [e[1] for e in latlng]
            # Filter and order columns
            cities = cities[['provinceName', 'cityName'] +
                            self.count_cols + ['latitude', 'longitude']]
            provinces_df = provinces_df.append(cities, ignore_index=True)
        ms.solid_memory()
        self.provinces_df = provinces_df.set_index('provinceName',  drop=False)
        logging.info('New provinces_df prepared.')

    def draw(self):
        draw(self.country_df,
        self.countryName,
        self.provinces_df,
        self.provinceNames)


colorscale = px.colors.carto.Redor
showscale = False
size = 9


def draw(country_df, countryName, provinces_df, provinceNames, colorscale=colorscale, showscale=showscale, size=size):

    scatter_traces, bar_traces, table_traces, country_name = setup_traces(country_df, countryName, provinces_df, provinceNames)

    buttons = setup_buttons(provinceNames, countryName, scatter_traces, country_name)

    draw_plotly(scatter_traces, bar_traces, table_traces, buttons, provinceNames, provinces_df, countryName, country_name)



def setup_traces(country_df, countryName, provinces_df, provinceNames, colorscale=colorscale, showscale=showscale, size=size):
    """
    Setup traces.
    inputs:
        country_df: DataFrame of country
        countryName: Name of country
        provinces_df: DataFrame containing counts of cities
        provinceNames: Name list of provinces
        colorscale: Color map for Scattermapbox
        showscale: Toggle of showing colormap
        size: Marker size of Scattermapbox
    outputs:
        scatter_traces: a dict for scattermapbox, counts of every city
        bar_traces: a dict for bar, counts of each city in province and whole country
        table_traces: a dict for table, raw table of each province and whole country
        country_name: Country name with counting
    """
    scatter_traces = dict()
    bar_traces = dict()
    table_traces = dict()
    country_name = '{} {}例'.format(countryName, country_df.confirmedCount.sum())

    # for each province
    # 1. fetch its cities
    # 2. setup its scatter
    # 3. save the scatter into scatter_traces
    log_confirmedCount = np.log10(provinces_df.confirmedCount.values + 1)
    cmax, cmin = log_confirmedCount.max(), log_confirmedCount.min()
    for prov in provinceNames:
        # print(prov, end=', ')

        # fetch cities
        cities = provinces_df.loc[prov]
        if isinstance(cities, pd.Series):
            cities = pd.DataFrame(cities).T

        # setup scatter
        # prepare marker for each city
        marker = go.scattermapbox.Marker(
            color=np.log10(cities['confirmedCount'].astype(np.float)+1),
            cmax=cmax,
            cmin=cmin,
            colorscale=colorscale,
            size=size,
            showscale=showscale
        )
        # setup scatter
        scatter = go.Scattermapbox(
            lat=cities['latitude'],
            lon=cities['longitude'],
            text=cities.provinceName + '-' + cities.cityName +
            '-' + cities.confirmedCount.astype(str),
            mode='markers',
            marker=marker,
            name='{} {}例'.format(prov, cities.confirmedCount.sum()),
            visible=True,
        )
        # setup bar
        bar = go.Bar(
            x=cities.cityName,
            y=cities.confirmedCount,
            name='',
            visible=False,
        )
        # setup table
        table = go.Table(
            header=dict(
                values=cities.columns,
                font=dict(size=10),
                align='left'),
            cells=dict(
                values=[cities[k].tolist() for k in cities.columns],
                align='left'),
            visible=False,
        )

        # save the scatter
        scatter_traces[prov] = scatter
        bar_traces[prov] = bar
        table_traces[prov] = table

    # add global bar
    bar_traces[countryName] = go.Bar(
        x=country_df.provinceName,
        y=country_df.confirmedCount,
        text=country_df.confirmedCount.tolist(),
        name='',
        visible=True
    )

    # add global table
    table_traces[countryName] = go.Table(
        header=dict(
            values=country_df.columns,
            font=dict(size=10),
            align='left'),
        cells=dict(
            values=[country_df[k].tolist() for k in country_df.columns],
            align='left'),
        visible=True,
    )

    # print('done.')
    return scatter_traces, bar_traces, table_traces, country_name


def setup_buttons(provinceNames, countryName, scatter_traces, country_name):
    """
    Setup button for each province.
    inputs:
        countryName: Name of country
        provinceNames: Name list of provinces
        scatter_traces: Traces of Scattermapbox
        country_name: Running title of country
    outputs:
        buttons: buttons paired with provinces
    """
    buttons = []

    def one_hot(trg, lst=provinceNames):
        # Get one hot presention of trg in lst
        # if trg is True or False, return a list of trg
        if trg is True or trg is False:
            return [trg for e in lst]
        # return one hot
        return [e == trg for e in lst]

    # Add button to show all provinces
    # visible of traces: [scattermapbox] + [bar] + [table]
    visible = one_hot(True) + one_hot(False) + one_hot(False) + [True, True]
    title = country_name
    label = countryName
    buttons.append(dict(
        label=label,
        method='update',
        args=[{'visible': visible},
              {'title': title}]
    ))

    # Add button for each province
    for prov in provinceNames:
        visible = one_hot(prov) * 3 + [False, False]
        title = scatter_traces[prov].name
        label = prov
        buttons.append(dict(
            label=label,
            method='update',
            args=[{'visible': visible},
                  {'title': title}]
        ))

    # print('Done.')
    return buttons


def draw_plotly(scatter_traces, bar_traces, table_traces, buttons, provinceNames, provinces_df, countryName, country_name, HTML_FILENAME='index.html'):
    """
    Plot plotly graph.
    inputs:
        scatter_traces: a dict for scattermapbox, counts of every city
        bar_traces: a dict for bar, counts of each city in province and whole country
        table_traces: a dict for table, raw table of each province and whole country
        buttons:buttons paired with provinces
        provinceNames: Name list of provinces
        provinces_df: DataFrame containing counts of cities
        countryName: Name of country
        country_name: Country name with counting
    """

    fig = plotly.subplots.make_subplots(
        rows=2, cols=2,
        shared_xaxes=False,
        specs=[[{"type": "mapbox"}, {"type": "bar"}],
            [{"type": "table", "colspan":2}, None]]
    )

    # order can not be changed
    # add scatters
    for prov in provinceNames:
        # print(prov, end=', ')
        fig.add_trace(scatter_traces[prov], row=1, col=1)
    # add bars
    for prov in provinceNames:
        # print(prov, end=', ')
        fig.add_trace(bar_traces[prov], row=1, col=2)
    # add tables
    for prov in provinceNames:
        # print(prov, end=', ')
        fig.add_trace(table_traces[prov], row=2, col=1)
    # add global bar
    fig.add_trace(bar_traces[countryName], row=1, col=2)
    # add global table
    fig.add_trace(table_traces[countryName], row=2, col=1)

    # print('done.')

    fig.update_mapboxes(
        accesstoken=profiles.mapbox_ak,
        bearing=0,
        pitch=0,
        zoom=2,
        center=go.layout.mapbox.Center(
            lat=provinces_df.latitude.mean(),
            lon=provinces_df.longitude.mean())
    )

    fig.update_layout(
        showlegend=False,
        autosize=True,
        hovermode='closest',
        # mapbox=mapbox,
        clickmode='event',
        title_text=country_name,
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=buttons
        )],
    )

    fig.update_yaxes(type="log")
    fig.update_layout(yaxis={'title_text': 'Count in log',
                            'title_standoff': 0})
    fig.layout.update({'height':800})
    fig.write_html(HTML_FILENAME)
    fig.show()