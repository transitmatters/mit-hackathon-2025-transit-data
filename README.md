# MIT Policy Hackathon 2025: Transit Challenge

This repository is home to documentation overviews, lists of datasets, tutorials, and pre-processed data that we provide. 

## Overview

We provide three main categories of datasets:

1. **Data on MBTA’s network:** routes, stops, schedules and frequency. Two types of network data exist: [geospatial (GIS) network data](mbta_network_geospatial.ipynb) of routes and stops, and the [General Transit Feed Specification (GTFS) format](mbta_gtfs_data.ipynb) that gives the full schedules.
2. **Data on MBTA’s [ridership](mbta_ridership_data.ipynb) and [performance](mbta_performance_data.ipynb)** (travel times, headways, etc.). Both can be accessed as CSV data tables via the [**MBTA Open Data Portal**](https://mbta-massdot.opendata.arcgis.com/). Additionally, the [MBTA Rider Census](https://www.mbta.com/performance-metrics/the-rider-census) reports demographic data of passengers.
3. [**Demographics data**](demographics_geospatial.ipynb) of residents in Greater Boston (population, income, race, commute destinations, etc.). The primary source of data is the **US Census** (which we use for our pre-processed dataset). Additionally, datasets for **travel and employment patterns** are described [here](travel_patterns_employment.ipynb).

## List of Subpages

This documentation consists of several subpages, each as a writeup with links to datasets, figures, and occasionally some Python code:

* [Demographic data](demographics_geospatial.ipynb)
* [Travel patterns and employment data](travel_patterns_employment.ipynb)
* [MBTA network geospatial data](mbta_network_geospatial.ipynb)
* [MBTA network schedules GTFS data](mbta_gtfs_data.ipynb)
* [MBTA ridership data](mbta_ridership_data.ipynb)
* [MBTA performance data](mbta_performance_data.ipynb)
* [Quick introduction to GIS, and a sample project that we provide](geospatial_qgis_example.ipynb)

## Pre-processed Datasets

We provide a few GIS (GeoPackage) files with the MBTA network and selected US Census data. They're in the [``data/``](data/) folder with documentations there. 

_Alternatively, you can find the pre-processed GIS datasets in this Google Driver folder (Link TBA)._

We also provide a [sample QGIS project](qgis_sample_project.qgz), as an example to illustrate the datasets and using them in GIS software. Details are in [this tutorial page](geospatial_qgis_example.ipynb). 

## Additional Resources

The following resources can be helpful for data exploration and additional datasets:

* **[TransitMatters Data Dashboard](https://dashboard.transitmatters.org/):** Interactive web app that gives easy visualization of system performance, such as travel times and number of trips on each route between stops. Also gives aggregated ridership for each route.
* **MassGIS:** The state’s official datasets, accessed via either [this Mass.gov page](https://www.mass.gov/info-details/massgis-data-layers) (as a static list), the [MassGIS Data Hub](https://gis.data.mass.gov/) (an ArcGIS Server), or the interactive [MassMapper](https://maps.massgis.digital.mass.gov/MassMapper/MassMapper.html?bl=MassGIS%20Basemap__100&l=massgis%3AGISDATA.MBTA_NODE__GISDATA.MBTA_NODE%3A%3ADefault__ON__100%2Cmassgis%3AGISDATA.MBTA_ARC__GISDATA.MBTA_ARC%3A%3ADefault__ON__100%2Cmassgis%3AGISDATA.MBTA_NODE__GISDATA.MBTA_NODE%3A%3ALabels__ON__100%2CBasemaps_L3Parcels____ON__100&b=-71.17148843849154%2C42.36958967917281%2C-71.04883638465853%2C42.41649765155441). Contain many additional data categories beyond transit, such as demographics, other infrastructure, and environmental monitoring.
* **[MassDOT GeoDOT Open Data Portal](https://geodot-massdot.hub.arcgis.com/pages/open-data-portal):** Official data on other modes of transportation.
* **[Boston Region MPO / CTPS website](https://ctps.org/):** The Boston Region Metropolitan Planning Organization (MPO) provides many datasets and interactive [data dashboards](https://ctps.shinyapps.io/pbpp-dashboard-r/?_gl=1*1fx4ohh*_ga*MzI3MTYyNTQyLjE3NTY0Mjg5MTA.*_ga_TVRXRVW1YN*czE3NjM1MTAwNDAkbzEzJGcxJHQxNzYzNTExODUyJGozOSRsMCRoMA..) to assist with transit planning in the region. They also cover many other modes of transportation and their integration with public transit, such as park-and-rides and biking. 
* **[Bluebikes system data](https://bluebikes.com/system-data):** The leading bikeshare service in Greater Boston.
* **[MBTA Bus Route Profiles](https://www.mbta.com/projects/better-bus-project/update/bus-route-profiles-now-available):** In 2018, MBTA published detailed reports of each bus route with descriptions and analysis, including scheduled frequencies, ridership, crowding, on-time performance etc. The data is outdated, but a great visual introduction of specific bus routes.

## Python Package Installations

For those who are interested in using the Python code provided in these tutorials, you can install all prerequisite packages via ``pip`` by running these commands in a terminal:

```
pip install requests numpy pandas us geopandas pygris
pip install git+https://github.com/CityScope/pyGTFSHandler.git
pip install matplotlib mapclassify folium osmnx geopy
```