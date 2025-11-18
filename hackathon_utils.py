import requests
import urllib.parse
import os
# import json
# import re
# import importlib
# import sys

import pandas as pd
import numpy as np

# from census import Census
import us

import geopandas as gpd
import pygris
from pygris.utils import erase_water
from pygris.data import get_census, get_lodes

# from datetime import datetime


CENSUS_LATEST_YEARS = {
    'dec/dhc': 2020,  # Available for blocks
    'acs/acs5': 2023,  # Only block groups and higher
    'acs/acs1': 2024,  # Only places and higher
}


def to_list(x):
    """
    Given a parameter x that's either a single element or a list, convert it to a list.
    :param x: Parameter that's either a single element or a list
    :return: List of parameter(s)
    """
    return x if type(x) is list else [x]


def query_arcgis_feature_server(url_feature_server='', object_id_field="OBJECTID", epsg=3857):
    '''
    # Retrieve data from ArcGIS server (Get around 1000 limit)
    # This is used for importing rapid transit and bus routes from MassDOT
    # sourced from  https://gis.stackexchange.com/questions/266897/how-to-get-around-the-1000-objectids-limit-on-arcgis-server

    # Input: URL of layer
    # Example: mbta_rt_stops = query_arcgis_feature_server('https://gis.massdot.state.ma.us/arcgis/rest/services/MBTA/MBTA_Rapid_Transit/MapServer/0')

    This function downloads all of the features available on a given ArcGIS
    feature server. The function is written to bypass the limitations imposed
    by the online service, such as only returning up to 1,000 or 2,000 featues
    at a time.

    Parameters
    ----------
    url_feature_server : string
        Sting containing the URL of the service API you want to query. It should
        end in a forward slash and look something like this:
        'https://gis.massdot.state.ma.us/arcgis/rest/services/MBTA/MBTA_Rapid_Transit/MapServer/0'

    Returns
    -------
    geodata_final : gpd.GeoDataFrame
        This is a GeoDataFrame that contains all of the features from the
        Feature Server. After calling this function, the `geodata_final` object
        can be used to store the data on disk in several different formats
        including, but not limited to, Shapefile (.shp), GeoJSON (.geojson),
        GeoPackage (.gpkg), or PostGIS.
        See https://geopandas.org/en/stable/docs/user_guide/io.html#writing-spatial-data
        for more details.

    '''
    if url_feature_server == '':
        geodata_final = gpd.GeoDataFrame()
        return geodata_final

    # Fixing last character in case the URL provided didn't end in a
    # forward slash
    if url_feature_server[-1] != '/':
        url_feature_server = url_feature_server + '/'

    # Getting the layer definitions. This contains important info such as the
    # name of the column used as feature_ids/object_ids, among other things.
    layer_def = requests.get(url_feature_server + '?f=pjson').json()

    # The `objectIdField` is the column name used for the
    # feature_ids/object_ids
    if 'objectIdField' in layer_def:
        fid_colname = layer_def['objectIdField']
    else:
        fid_colname = object_id_field

    # The `maxRecordCount` tells us the maximum number of records this REST
    # API service can return at once. The code below is written such that we
    # perform multiple calls to the API, each one being short enough never to
    # go beyond this limit.
    record_count_max = layer_def['maxRecordCount']

    # Part of the URL that specifically requests only the object IDs
    url_query_get_ids = (f'query?f=geojson&returnIdsOnly=true'
                         f'&where={fid_colname}+is+not+null')

    url_comb = url_feature_server + url_query_get_ids

    # Getting all the object IDs
    service_request = requests.get(url_comb)
    # all_objectids = np.sort(service_request.json()['properties']['objectIds'])
    all_objectids = np.sort(service_request.json()['objectIds'])

    # This variable will store all the parts of the multiple queries. These
    # parts will, at the end, be concatenated into one large GeoDataFrame.
    geodata_parts = []

    # This part of the query is fixed and never actually changes
    url_query_fixed = ('query?f=geojson&outFields=*&where=')

    # Identifying the largest query size allowed per request. This will dictate
    # how many queries will need to be made. We start the search at
    # the max record count, but that generates errors sometimes - the query
    # might time out because it's too big. If the test query times out, we try
    # shrink the query size until the test query goes through without
    # generating a time-out error.
    block_size = min(record_count_max, len(all_objectids))
    worked = False
    while not worked:
        # Moving the "cursors" to their appropriate locations
        id_start = all_objectids[0]
        id_end = all_objectids[block_size - 1]

        readable_query_string = (f'{fid_colname}>={id_start} '
                                 f'and {fid_colname}<={id_end}')

        url_query_variable = urllib.parse.quote(readable_query_string)

        url_comb = url_feature_server + url_query_fixed + url_query_variable

        url_get = requests.get(url_comb)

        if 'error' in url_get.json():
            block_size = int(block_size / 2) + 1
        else:
            geodata_part = gpd.read_file(url_get.text)

            geodata_parts.append(geodata_part.copy())
            worked = True

    # Performing the actual query to the API multiple times. This skips the
    # first few rows/features in the data because those rows were already
    # captured in the query performed in the code chunk above.
    for i in range(block_size, len(all_objectids), block_size):
        # Moving the "cursors" to their appropriate locations and finding the
        # limits of each block
        sub_list = all_objectids[i:i + block_size]
        id_start = sub_list[0]
        id_end = sub_list[-1]

        readable_query_string = (f'{fid_colname}>={id_start} '
                                 f'and {fid_colname}<={id_end}')

        # Encoding from readable text to URL
        url_query_variable = urllib.parse.quote(readable_query_string)

        # Constructing the full request URL
        url_comb = url_feature_server + url_query_fixed + url_query_variable

        # Actually performing the query and storing its results in a
        # GeoDataFrame
        geodata_part = (gpd.read_file(url_comb,
                                      driver='GeoJSON'))

        # Appending the result to `geodata_parts`
        if geodata_part.shape[0] > 0:
            geodata_parts.append(geodata_part)

    # Concatenating all of the query parts into one large GeoDataFrame
    geodata_final = (pd.concat(geodata_parts,
                               ignore_index=True)
                     .sort_values(by=fid_colname)
                     .reset_index(drop=True))

    # Checking if any object ID is missing
    ids_queried = set(geodata_final[fid_colname])
    for i, this_id in enumerate(all_objectids):
        if this_id not in ids_queried:
            print('WARNING! The following ObjectID is missing from the final '
                  f'GeoDataFrame: ObjectID={this_id}')
            pass

    # Checking if any object ID is included twice
    geodata_temp = geodata_final[[fid_colname]].copy()
    geodata_temp['temp'] = 1
    geodata_temp = (geodata_temp
                    .groupby(fid_colname)
                    .agg({'temp': 'sum'})
                    .reset_index())
    geodata_temp = geodata_temp.loc[geodata_temp['temp'] > 1].copy()
    for i, this_id in enumerate(geodata_temp[fid_colname].values):
        n_times = geodata_temp['temp'].values[i]
        print('WARNING! The following ObjectID is included multiple times in'
              f'the final GeoDataFrame: ObjectID={this_id}\tOccurrences={n_times}')
        
    # Converting to the desired EPSG (3857 by default)
    geodata_final = geodata_final.to_crs(epsg=epsg)

    return geodata_final


def load_census_shapes(state='MA', level='block', year=None, remove_water=True, epsg=3857):
    """
    Load the shape files for a given state's blocks, block groups or tracts.
    :param state: State, either as string or using the us package: states.MA
    :param level: Geographic level, either 'block', 'blockgroup', 'tract' or 'place'
    :param year: Survey year (last year in the period for 5-year ACS). 
        Setting this to None will automatically load the latest available year.
    :param remove_water: Whether water bodies are automatically removed
    :param epsg: Coordinate system. 3857 is good for general use (using meters as units).
        A more precise EPSG for Greater Boston is 2249 (using feet as units).
    :return: GeoPandas DataFrame
    """
    geometry_funcs = {
        'block': pygris.blocks,
        'blockgroup': pygris.block_groups,
        'block group': pygris.block_groups,
        'block_group': pygris.block_groups,
        'tract': pygris.tracts,
        'place': pygris.places,
    }
    for k, v in list(geometry_funcs.items()):  # Allow 'blocks', 'blockgroups', 'tracts', 'places'
        geometry_funcs[k + 's'] = v

    shapes = geometry_funcs[level](state=state, year=year, cache=True)
    if remove_water:
        # Bug with pygris: erase_water() uses counties() with cb=True and resolution="500k", which doesn't work
        # with 2025 as of November 17. If this happens, we use 2024.
        if year is None or year >= 2025:
            shapes = erase_water(shapes, year=2024)
        else:
            shapes = erase_water(shapes, year=year)
    if epsg:
        shapes = shapes.to_crs(epsg=epsg)
    return shapes


def get_census_fields(categories, api_key,
                      state='MA', level='blockgroup', year=None,
                      compute_ratios=True, add_place_names=False):
    """
    Pull tabular census data from either US Decennial Census or American Community Survey,
    using respective APIs.
    
    ACS data is available at block group level and higher, while Decennial Census data is 
    available at block level and higher.

    :param categories: A dict object that specifies several categories of data (e.g. race, income)
        needed. Each category can have its own:
        * source: 'decennial', 'decennial_dhc', 'acs', 'acs5', 'acs1'
        * fields: dict of field names and corresponding census field codes (list)
        * fields_universe: dict of field names and corresponding census field codes (single code)
            whose data is the total count in this universe (e.g. population whose income is determined)
        Example: {"income": {
            "source": "acs5",
            "fields": {
                "householdTotal": ["C17002_001"],
                "median": ["B19013_001"],
                "050PercentPoverty": ["C17002_002"],
                "100PercentPoverty": ["C17002_002", "C17002_003"],
                "150PercentPoverty": ["C17002_002", "C17002_003", "C17002_004", "C17002_005"],
                "200PercentPoverty": ["C17002_002", "C17002_003", "C17002_004", "C17002_005", "C17002_006", "C17002_007"],
            },
            "fields_universe": {
                "default": "C17002_001",  # Population for whom poverty status is determined
                "median": 'NO_DENSITY_OR_RATIO',  # Not a population count, do not compute density or ratio
            }
        }}
    :param api_key: Census API key. Get one at https://api.census.gov/data/key_signup.html
    :param state: State, either as string or using the us package: states.MA
    :param level: Geographic level, either 'block', 'blockgroup', 'tract' or 'place'
        ('block' only for Decennial Census)
    :param year: Survey year (last year in the period for 5-year ACS). 
        Setting this to None will load the latest available year, as specified in CENSUS_LATEST_YEARS.
    :param compute_ratios: Whether to compute ratio fields for each field requested, using the 
        corresponding universe field. (e.g. % of population with income below poverty level).
    :param add_place_names: Whether to add place names when level is 'place'.
        (Note that if a separate GeoDataFrame from load_census_shapes() is eventually joined with this,
        the NAME field would already have been included there.)
    :return: A pd.DataFrame with the following column for each field:
        * "CATEGORY_FIELD", e.g. "income_100PercentPoverty": Sum of values of given fields.
        * "CATEGORY_FIELD_ratio", e.g. "income_100PercentPoverty_ratio": Ratio of the above sum to
          the universe field.
    """
    # Convert state from string ('MA') to FIPS code (25)
    if type(state) is str:
        state = us.states.lookup(state)
    state_id = state.fips

    # (1) Decompose categories into individual fields requested
    # e.g. income_median, income_100PercentPoverty, etc.
    fields = []
    for cat_name, cat_dict in categories.items():
        for field_name, field_codes in cat_dict['fields'].items():
            fields.append({
                'name': f"{cat_name}_{field_name}",  # 'income_100PercentPoverty'
                'source': cat_dict['source'],  # 'decennial_dhc', 'acs', 'acs1', 'acs5'
                'sum_codes': field_codes,  #  ["C17002_002", "C17002_003"]: they will be summed
                'universe_code': cat_dict['fields_universe'].get(
                    field_name, 
                    cat_dict['fields_universe']['default']
                ),  # "C17002_001", Field code whose data is the total count in this universe (e.g. population whose income is determined)
                    # If None, this field is not treated as a population count (e.g. income_median), and density and ratio fields will not be created
            })

    # (2) Add suffic 'E' to ACS field codes (E for estimates), so C17002_002 becomes C17002_002E
    # Also ensure that sum_codes is a list
    def add_e(c):
        if c is None or c in ['DENSITY_ONLY', 'NO_DENSITY_OR_RATIO']:
            return c
        return c if c.endswith('E') else c + 'E'

    for field in fields:
        if field['source'].startswith('acs'):
            field['sum_codes'] = [add_e(c) for c in to_list(field['sum_codes'])]
            field['universe_code'] = add_e(field['universe_code'])

    # ACS_TOTAL_POPULATION_e = "B01001_001"

    # (3) Gather all field codes queried for each source
    codes_by_source = {}
    for field in fields:
        source = field['source']
        if source not in codes_by_source:
            codes_by_source[source] = set()
        codes_by_source[source].update(field['sum_codes'])

        if field['universe_code'] and field['universe_code'] not in ['DENSITY_ONLY', 'NO_DENSITY_OR_RATIO']:
            codes_by_source[source].add(field['universe_code'])
            
        # if source.startswith('acs'):
        #     codes_by_source[source].add(ACS_TOTAL_POPULATION_e)
        if add_place_names and level.startswith('place'):
            codes_by_source[source].add('NAME')

    # Helper function for API endpoints
    def source_to_api_dir(source):
        """
        Map source string to Census API directory, such as 'acs/acs5', 'dec/dhc'.

        The complete list of directories is at the Census API homepage: https://api.census.gov/data.html,
        specifically in the "Dataset Name" column.

        :param source: Source string, e.g. 'acs', 'acs5', 'acs1', 'decennial_dhc'
        :return: API directory string, e.g. 'acs/acs5', 'dec/dhc'
        """
        if source.startswith('acs'):
            return 'acs/acs1' if source in ['acs1'] else 'acs/acs5'
        elif source.startswith('dec'):  # e.g. decennial_dhc
            dec_suffix = source.split('_')[-1] if '_' in source else 'dhc'
            return f"dec/{dec_suffix}"
        elif source == 'dhc':
            return "dec/dhc"
        else:
            raise Exception(f"Unknown source: {source}")

    # Geography hierarchy from census API. 
    # They can be found in the "geographies" column of https://api.census.gov/data.html
    GEO_HIERARCHIES = {
        'block': ['state', 'county', 'tract', 'block'],
        'blockgroup': ['state', 'county', 'tract', 'block group'],
        'block group': ['state', 'county', 'tract', 'block group'],
        'block_group': ['state', 'county', 'tract', 'block group'],
        'tract': ['state', 'county', 'tract'],
        'place': ['state', 'place'],
    }
    for k, v in list(GEO_HIERARCHIES.items()):  # Allow 'blocks', 'blockgroups', 'tracts', 'places'
        GEO_HIERARCHIES[k + 's'] = v

    # (4) Make API call
    df_by_source = {}
    for source, all_fields in codes_by_source.items():
        api_dir = source_to_api_dir(source)  # API endpoint, 'acs/acs5' or 'dec/dhc'
        year_to_use = year if year is not None else CENSUS_LATEST_YEARS[api_dir]

        # Format geography hierarchy
        geo_hierarchy = GEO_HIERARCHIES[level]
        geo_for = geo_hierarchy[-1] + ":*"
        geo_in = []
        for i in range(len(geo_hierarchy)-1):
            higher_geo = geo_hierarchy[i]
            if higher_geo == 'state':
                geo_in.append(f"state:{state_id}")
            else:
                geo_in.append(f"{higher_geo}:*")

        # Make API call
        df_by_source[source] = pd.DataFrame(get_census(
            dataset=api_dir,
            year=year_to_use,
            variables=list(all_fields),
            params={
                "for": geo_for,
                "in": geo_in,
                "key": api_key
            },
            return_geoid=True,
            guess_dtypes=True
        ))

    # (5) Compute user-requested fields
    df_processed_by_source = {}  # DataFrames with computed fields for each source (rather than raw codes)
    final_df_fields = []         # For sorting columns later
    final_df_fields_set = set()  # Avoid duplicates in final_df_fields

    def add_fieldname(field_name, prepend=False):
        if field_name not in final_df_fields_set:
            if prepend:
                final_df_fields.insert(0, field_name)
            else:
                final_df_fields.append(field_name)
            final_df_fields_set.add(field_name)

    for field in fields:
        add_fieldname(field['name'])

        source = field['source']
        df_raw = df_by_source[source]
        df_proc = df_processed_by_source.get(source, pd.DataFrame())

        # Add missing basic fields
        for col in ['NAME', 'GEOID']:  # Reverse order to have GEOID first
            if col in df_raw.columns and col not in df_proc.columns:
                df_proc[col] = df_raw[col]
                add_fieldname(col, prepend=True)  # GEOID and NAME go to the front
        
        # Compute sum
        df_proc[field['name']] = df_raw[field['sum_codes']].sum(axis=1)

        # Compute ratio if applicable
        if compute_ratios and field['universe_code'] and field['universe_code'] not in ['DENSITY_ONLY', 'NO_DENSITY_OR_RATIO']:
            ratio_entry_name = f"{field['name']}_ratio"
            df_proc[ratio_entry_name] = df_proc[field['name']] / df_raw[field['universe_code']]  # Ratio of universe
            add_fieldname(ratio_entry_name)

            # if source.startswith('acs'):
            #     ACS_TOTAL_POPULATION_e = "B01001_001E"
            #     ratio_totpop_entry_name = f"{field['name']}_ratiototpop"
            #     df_proc[ratio_totpop_entry_name] = df_proc[field['name']] / df_raw[
            #         ACS_TOTAL_POPULATION_e]  # Ratio of total population
        
        df_processed_by_source[source] = df_proc
    
    # (6) Merge all sources together
    join_on = ['GEOID']
    if 'NAME' in final_df_fields_set:
        join_on.append('NAME')

    df = None
    for source, df_proc in df_processed_by_source.items():
        df = (df_proc if df is None 
              else df.merge(df_proc, on=join_on, how='outer'))

    return df[final_df_fields]  # Sort columns


def join_census_and_add_densities(df_geo, df_census, 
                                  density_fields=None, categories=None):
    """
    Join census tabular data with geospatial shapes, and compute density per square meter
    for each data field if applicable.

    To specify which fields should have density fields computed, use one of two methods:
    1. Pass a list of field names in density_fields parameter.
    2. Use the same categories parameter as in get_census_fields(). In case case, all fields
       that do not have fields_universe set to 'NO_DENSITY_OR_RATIO' will have density computed.

    The new density fields will be named as "CATEGORY_FIELD_density", e.g. 
    "income_100PercentPoverty_density".

    :param df_census: DataFrame returned by get_census_fields()
    :param shapes: GeoDataFrame returned by load_census_shapes()
    :param density_fields: List of field names (same as in df_census) for which density fields
        should be computed. If None, the categories parameter is used to determine which fields
        should have density fields computed.
    :param categories: Same categories dict passed to get_census_fields(). If the density_fields 
        parameter is None, this will be used to determine which fields should have density computed.
    """
    # Join tabular data with shapes
    join_on = ['GEOID']
    if 'NAME' in df_census.columns and 'NAME' in df_geo.columns:
        join_on.append('NAME')
    df_geodata = df_geo.merge(df_census, on=join_on,
                              how='outer')  # Keep all geometries, even if no census data is available
    
    # Determine density fields from categories, if density_fields is not given
    if density_fields is None:
        density_fields = []
        if categories is not None:
            for cat_name, cat_dict in categories.items():
                for field_name in cat_dict['fields'].keys():
                    universe_code = cat_dict['fields_universe'].get(
                        field_name, 
                        cat_dict['fields_universe']['default']
                    )
                    if universe_code and universe_code != 'NO_DENSITY_OR_RATIO':  # Includes DENSITY_ONLY
                        density_fields.append(f"{cat_name}_{field_name}")

            # Remove non-existent fields
            density_fields = [f for f in density_fields if f in df_geodata.columns]

    # Compute density fields (respect original order in df)
    final_df_fields = []  # For sorting columns later
    density_fields = set(density_fields)  # For faster lookup
    for col in df_geodata.columns:
        final_df_fields.append(col)
        if col in density_fields:
            density_field_name = f"{col}_density"
            df_geodata[density_field_name] = df_geodata[col] / df_geodata.geometry.area  # Density per square meter (assumes EPSG 3857)
            final_df_fields.append(density_field_name)
    
    return df_geodata[final_df_fields]  # Sort columns
