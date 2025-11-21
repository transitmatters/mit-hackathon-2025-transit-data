CENSUS_FIELDS_CATEGORIES = {
    "population": {
        "source": "decennial_dhc",  # Decennial Census -> Demographic and Housing Characteristics
        "years": 2020,  # If None, uses most recent year available 
                        # Can specify multiples: "year": [2010, 2020]
                        # This will add year as a prefix in field name, e.g. "2020_race_white"
        "fields": {
            "2020": ["P1_001N"],
        },
        "fields_universe": {
            "default": 'DENSITY_ONLY',  # Do not compute ratio
        }
    },
    "race": {
        "source": "decennial_dhc",
        "years": 2020,
        "fields": {
            "white": ["P3_002N"],
            "nonWhite": ["P3_003N", "P3_004N", "P3_005N", "P3_006N", "P3_007N", "P3_008N"],
            "black": ["P3_003N"],
            "native": ["P3_004N"],
            "asian": ["P3_005N"],
            "others": ["P3_006N", "P3_007N", "P3_008N"],
            "hispanic": ["P5_010N"],
            "hispanicOrNonWhite": ["P5_004N", "P5_005N", "P5_006N", "P5_007N", "P5_008N", "P5_009N", "P5_010N"],
        },
        "fields_universe": {
            "default": "P3_001N",  # Total population, same as P5_001N
        }
    },
    "income": {
        "source": "acs5",
        "years": 2023,
        "fields": {
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
    },
    "commute": {
        "source": "acs5",
        "years": 2023,
        "fields": {
            "workersTotal": ["B08301_001"],
            "transit": ["B08301_010"],
            "bus": ["B08301_011"],
            "rapidTransit": ["B08301_012", "B08301_014"],
            "commuterRail": ["B08301_013"],
            "car": ["B08301_002"],
            "walk": ["B08301_019"],
            "bike": ["B08301_018"],
            "walkBike": ["B08301_018", "B08301_019"],
            "fromHome": ["B08301_021"],
            "otherModes": ["B08301_016", "B08301_017", "B08301_020"],

            # Fields below require separate settings to define the universe: see fields_universe below
            "workersNotHome": ["B08303_001"],
            "time30min": ["B08303_008", "B08303_009", "B08303_010", "B08303_011", "B08303_012", "B08303_013"],
            "time45min": ["B08303_011", "B08303_012", "B08303_013"],
            "time60min": ["B08303_012", "B08303_013"],
            "time90min": ["B08303_013"],

            # Fields below require separate settings to define the universe: see fields_universe below
            "timeTransit30": ["B08134_067", "B08134_068", "B08134_069", "B08134_070"],
            "timeTransit45": ["B08134_069", "B08134_070"],
            "timeTransit60": ["B08134_070"],
        },
        "fields_universe": {
            "default": "B08301_001",  # Workers 16 years and over
            "workersNotHome": "B08303_001",  # Workers 16 years and over who did not work from home
            "time30min": "B08303_001",  # Workers 16 years and over who did not work from home
            "time45min": "B08303_001",  # Workers 16 years and over who did not work from home
            "time60min": "B08303_001",  # Workers 16 years and over who did not work from home
            "time90min": "B08303_001",  # Workers 16 years and over who did not work from home
            "timeTransit30": "B08303_001",  # Workers 16 years and over who did not work from home
            "timeTransit45": "B08303_001",  # Workers 16 years and over who did not work from home
            "timeTransit60": "B08303_001",  # Workers 16 years and over who did not work from home
        }
    },
    "vehicles": {
        "source": "acs5",
        "years": 2023,
        "fields": {
            "householdTotal": ["B25044_001"],
            "0inHousehold": ["B25044_003", "B25044_010"],
            "0or1inHousehold": ["B25044_003", "B25044_004", "B25044_010", "B25044_011"],
        },
        "fields_universe": {
            "default": "B25044_001",  # Occupied housing units
        }
    },
}
