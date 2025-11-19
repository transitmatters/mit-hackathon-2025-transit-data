# Pre-Processed Datasets

This folder contains all GIS datasets that TransitMatters pre-processed for the MIT Policy Hackathon 2025. All datasets can be used freely by participants.

## Demographics: [``demographics.gpkg``](demographics.gpkg)

The [``demographics.gpkg``](demographics.gpkg) file contains two layers, ``blockgroup`` and ``place``. Both report selected attributes (counts, densities, ratios) on **population, race, income, commutes, and vehicle ownership** computed from the US Census, but at different geographic levels:

* ``blockgroup``, with data reported for each Census block group;
* ``place``, with data reported for each officially designated ["place"](https://data.census.gov/map/040XX00US25$1600000?layer=VT_2022_160_00_PY_D1&loc=42.3785,-71.0370,z9.5467) in Massachusetts. They are mostly municipalities, such as [cities and towns](https://www.ctps.org/mpo_communities).

The table below lists the main columns of [``data/demographics.gpkg``](data/demographics.gpkg). In addition:

* Columns with the ``_density`` suffix store the number of such residents (or households) per _square meter_.
* Columns with the ``_ratio`` suffix store the proportion of such residents (or households) among all those that qualify for the survey table. (For example, ``commute_time60min_ratio`` ignores individuals who are unemployed or work from home.)

| Category | Column Name | Description | Source and Year |
|----|----|----|----|
| Population | ``population_2020`` | Total population | 2020 Decennial Census |
| Race | ``race_white`` | White alone | 2020 Decennial Census |
| Race | ``race_nonWhite`` | Anyone other than white alone | 2020 Decennial Census |
| Race | ``race_black`` | Black or African American alone | 2020 Decennial Census |
| Race | ``race_native`` | American Indian and Alaska Native alone | 2020 Decennial Census |
| Race | ``race_asian`` | Asian alone | 2020 Decennial Census |
| Race | ``race_others`` | Native Hawaiian and Other Pacific Islander, some other race alone, or two or more races | 2020 Decennial Census |
| Race | ``race_hispanic`` | Hispanic or Latino | 2020 Decennial Census |
| Race | ``race_hispanicOrNonWhite`` | Hispanic or Latino, or non-Hispanic other than white alone | 2020 Decennial Census |
| Income | ``income_median`` | Median household income | 2019-2023 ACS |
| Income | ``income_050PercentPoverty`` | Individuals with income below 50% of poverty level | 2019-2023 ACS |
| Income | ``income_100PercentPoverty`` | Individuals with income below 100% of poverty level | 2019-2023 ACS |
| Income | ``income_150PercentPoverty`` | Individuals with income below 150% of poverty level | 2019-2023 ACS |
| Income | ``income_200PercentPoverty`` | Individuals with income below 200% of poverty level | 2019-2023 ACS |
| Commute | ``commute_workersTotal`` | Total workers 16 years and over | 2019-2023 ACS |
| Commute | ``commute_transit`` | Workers using (any form of) public transporation to work | 2019-2023 ACS |
| Commute | ``commute_bus`` | Workers using buses to work | 2019-2023 ACS |
| Commute | ``commute_rapidTransit`` | Workers using subway or light rail to work | 2019-2023 ACS |
| Commute | ``commute_commuterRail`` | Workers using commuter rail or long-distance train to work | 2019-2023 ACS |
| Commute | ``commute_cars`` | Workers using car, truck or van to work (drove alone or carpooled) | 2019-2023 ACS |
| Commute | ``commute_walk`` | Workers walking to work | 2019-2023 ACS |
| Commute | ``commute_bike`` | Workers biking to work | 2019-2023 ACS |
| Commute | ``commute_walkBike`` | Workers walking or biking to work | 2019-2023 ACS |
| Commute | ``commute_workersNotHome`` | Total workers 16 years and over who did not work from home | 2019-2023 ACS |
| Commute | ``commute_time30min`` | Workers taking at least 30 minutes to travel to work | 2019-2023 ACS |
| Commute | ``commute_time45min`` | Workers taking at least 45 minutes to travel to work | 2019-2023 ACS |
| Commute | ``commute_time60min`` | Workers taking at least 60 minutes to travel to work | 2019-2023 ACS |
| Commute | ``commute_time90min`` | Workers taking at least 90 minutes to travel to work | 2019-2023 ACS |
| Commute | ``commute_timeTransit30`` | Workers who used public transportation and took at least 30 minutes to travel to work | 2019-2023 ACS |
| Commute | ``commute_timeTransit45`` | Workers who used public transportation and took at least 45 minutes to travel to work | 2019-2023 ACS |
| Commute | ``commute_timeTransit60`` | Workers who used public transportation and took at least 60 minutes to travel to work | 2019-2023 ACS |
| Vehicle Ownership | ``vehicles_householdTotal`` | Total number of households (occupied housing units, owned or rented) | 2019-2023 ACS |
| Vehicle Ownership | ``vehicles_0inHousehold`` | Households with 0 vehicles | 2019-2023 ACS |
| Vehicle Ownership | ``vehicles_0or1inHousehold`` | Households with 0 or 1 vehicles | 2019-2023 ACS |


The remaining fields are from the [US Census Tiger/Line Shapefiles](https://www.census.gov/programs-surveys/geography/technical-documentation/complete-technical-documentation/tiger-geo-line.2023.html#list-tab-240499709) with documentation [here](https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2023/TGRSHP2023_TechDoc.pdf) (Appendix G-2 for block groups, Appendix I-5 for places).

## MBTA Geospatial Files: [``mbta_network.gpkg``](mbta_network.gpkg)

The [``mbta_network.gpkg``](mbta_network.gpkg) file is a collection of external geospatial datasets in 12 layers. The table below gives the source of each layer. Documentations can be found via the **Mass.gov** links.

| Layer name | Mass.gov (with documentation) | ArcGIS online or server |
|----|----|----|
| ``rapid_transit_routes`` | [Mass.gov](https://www.mass.gov/info-details/massgis-data-mbta-rapid-transit) | [MassGIS Data Hub](https://gis.data.mass.gov/maps/a9e4d01cbfae407fbf5afe67c5382fde/explore) |
| ``rapid_transit_stops`` | [Mass.gov](https://www.mass.gov/info-details/massgis-data-mbta-rapid-transit) | [MassGIS Data Hub](https://gis.data.mass.gov/maps/a9e4d01cbfae407fbf5afe67c5382fde/explore) |
| ``commuter_rail_routes`` | [Mass.gov](https://www.mass.gov/info-details/massgis-data-trains) | [MassGIS Data Hub](https://gis.data.mass.gov/maps/b741e3542a9f40898d49e776452efe63) |
| ``commuter_rail_stops`` | [Mass.gov](https://www.mass.gov/info-details/massgis-data-trains) | [MassGIS Data Hub](https://gis.data.mass.gov/maps/b741e3542a9f40898d49e776452efe63) |
| ``bus_routes`` | [Mass.gov](https://www.mass.gov/info-details/massgis-data-mbta-bus-routes-and-stops) | [MassGIS Data Hub](https://gis.data.mass.gov/maps/cef8d0fe8b9d49fe9aa8f1b7524c6ac2/explore) |
| ``bus_stops`` | [Mass.gov](https://www.mass.gov/info-details/massgis-data-mbta-bus-routes-and-stops) | [MassGIS Data Hub](https://gis.data.mass.gov/maps/cef8d0fe8b9d49fe9aa8f1b7524c6ac2/explore) |
| ``rapid_transit_routes_gtfs`` | N/A | [MassDOT ArcGIS API](https://gis.massdot.state.ma.us/arcgis/rest/services/Multimodal/GTFS_Systemwide/MapServer/1) |
| ``rapid_transit_stops_gtfs`` | N/A | [MassDOT ArcGIS API](https://gis.massdot.state.ma.us/arcgis/rest/services/Multimodal/GTFS_Systemwide/MapServer/0) |
| ``commuter_rail_routes_gtfs`` | N/A | [MassDOT ArcGIS API](https://gis.massdot.state.ma.us/arcgis/rest/services/Multimodal/GTFS_Systemwide/MapServer/3) |
| ``commuter_rail_stops_gtfs`` | N/A | [MassDOT ArcGIS API](https://gis.massdot.state.ma.us/arcgis/rest/services/Multimodal/GTFS_Systemwide/MapServer/2) |
| ``bus_routes_gtfs`` | N/A | [MassDOT ArcGIS API](https://gis.massdot.state.ma.us/arcgis/rest/services/Multimodal/GTFS_Systemwide/MapServer/5) |
| ``bus_stops_gtfs`` | N/A | [MassDOT ArcGIS API](https://gis.massdot.state.ma.us/arcgis/rest/services/Multimodal/GTFS_Systemwide/MapServer/4) |

The ``_gtfs`` layers are parsed directly from the latest GTFS schedule bundles, with much more information for stops (e.g. accessibility and sidewalk conditions). They do not list which line the station is on, but you can join them with [MBTA_Rapid_Transit_Stop_Orders.csv](MBTA_Rapid_Transit_Stop_Orders.csv) for rapid transit.

For details on the data sources above, see [our tutorial on MBTA network data](../mbta_network_geospatial.ipynb).

## MBTA Rapid Transit Stop Orders: [``MBTA_Rapid_Transit_Stop_Orders.csv``](MBTA_Rapid_Transit_Stop_Orders.csv)

This is sourced directly from the ["MBTA Rapid Transit Stop Orders"](https://mbta-massdot.opendata.arcgis.com/datasets/e09d680af4a0441eb49ce4ef7b1796eb_0/explore) dataset on MBTA Open Data Portal. It lists, for each rapid transit route, a list of stop names (e.g. ``Wonderland``), stop IDs (e.g. ``place-wondl``), and the integer order of this stop on the line. For some applications, this table is useful for **joining stop data with route data**.

[Full documentation is available at the original data source.](https://mbta-massdot.opendata.arcgis.com/datasets/MassDOT::mbta-rapid-transit-stop-orders/about)