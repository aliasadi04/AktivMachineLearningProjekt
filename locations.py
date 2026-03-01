areas = {
    # Yosemite National Park
    "yosemite": {
        "latitude": (37.4946, 37.9630),
        "longitude": (-119.8862, -119.2042),
    },
    # Mt. Fuji, Japan (Smooth / Conical)
    # Summit: 35.36°N, 138.73°E. Base diameter ~45 km.
    "fuji": {
        "latitude": (33.5, 35.5),
        "longitude": (138, 140),
    },
    # K2 / Karakoram (Rugged / Jagged)
    # Summit: 35.88°N, 76.51°E. Steep pyramid, small footprint.
    "k2": {
        "latitude": (35.82, 35.94),
        "longitude": (76.44, 76.58),
    },
    # Grand Mesa, Colorado (Flat-topped / Mesa)
    # Center: 39.07°N, -107.94°W. ~70 km east-west, 500 sq mi.
    "grand_mesa": {
        "latitude": (38.85, 39.20),
        "longitude": (-108.20, -107.55),
    },
    # Crib Goch / Snowdon Horseshoe, Wales (Ridgeline / Sharp crest)
    # Ridge at 53.075°N, -4.054°W. Tiny feature, box covers horseshoe.
    "crib_goch": {
        "latitude": (53.05, 53.09),
        "longitude": (-4.10, -4.03),
    },
    # South Downs, England (Rolling hills)
    # Centered near Butser Hill (highest point, 271m).
    "south_downs": {
        "latitude": (50.88, 51.00),
        "longitude": (-1.10, -0.80),
    },
    # Mt. Tambora, Indonesia (Volcanic caldera)
    # Summit: -8.25°S, 118.00°E. Base diameter ~60 km, caldera ~7 km.
    "tambora": {
        "latitude": (-8.52, -7.98),
        "longitude": (117.73, 118.27),
    },
    # Mont Blanc massif, Alps (Multi-peak / Complex)
    # Summit: 45.83°N, 6.86°E. Massif is 46 km long, 20 km wide.
    "mont_blanc": {
        "latitude": (45.73, 45.93),
        "longitude": (6.72, 7.10),
    },
}

peaks = {
    # === Original test areas ===
    "fuji": {"lat": 35.3606, "lon": 138.7274, "elev_m": 3776, "type": "smooth conical"},
    "k2": {"lat": 35.8818, "lon": 76.5142, "elev_m": 8611, "type": "rugged pyramid"},
    "grand_mesa": {
        "lat": 39.0666,
        "lon": -107.9367,
        "elev_m": 3352,
        "type": "flat-topped mesa",
    },
    "crib_goch": {
        "lat": 53.0755,
        "lon": -4.0535,
        "elev_m": 923,
        "type": "knife-edge ridge",
    },
    "south_downs": {
        "lat": 50.9525,
        "lon": -0.9344,
        "elev_m": 271,
        "type": "rolling hills",
    },  # Butser Hill
    "tambora": {
        "lat": -8.2500,
        "lon": 118.0000,
        "elev_m": 2851,
        "type": "volcanic caldera",
    },
    "mont_blanc": {
        "lat": 45.8326,
        "lon": 6.8652,
        "elev_m": 4810,
        "type": "multi-peak massif",
    },
    # === Seven Summits ===
    "everest": {
        "lat": 27.9881,
        "lon": 86.9250,
        "elev_m": 8849,
        "type": "highest on earth",
    },
    "aconcagua": {
        "lat": -32.6532,
        "lon": -70.0109,
        "elev_m": 6962,
        "type": "high desert peak",
    },
    "denali": {
        "lat": 63.0695,
        "lon": -151.0074,
        "elev_m": 6190,
        "type": "massive arctic peak",
    },
    "kilimanjaro": {
        "lat": -3.0674,
        "lon": 37.3556,
        "elev_m": 5895,
        "type": "freestanding volcano",
    },
    "elbrus": {
        "lat": 43.3499,
        "lon": 42.4453,
        "elev_m": 5642,
        "type": "twin-dome volcano",
    },
    "vinson": {
        "lat": -78.5254,
        "lon": -85.6171,
        "elev_m": 4892,
        "type": "antarctic peak",
    },
    "puncak_jaya": {
        "lat": -4.0833,
        "lon": 137.1833,
        "elev_m": 4884,
        "type": "tropical glacier peak",
    },
    # === Iconic / Interesting terrain ===
    "matterhorn": {
        "lat": 45.9764,
        "lon": 7.6586,
        "elev_m": 4478,
        "type": "iconic pyramid",
    },
    "rainier": {
        "lat": 46.8523,
        "lon": -121.7603,
        "elev_m": 4392,
        "type": "glaciated volcano",
    },
    "etna": {"lat": 37.7510, "lon": 14.9934, "elev_m": 3357, "type": "active volcano"},
    "olympus": {
        "lat": 40.0859,
        "lon": 22.3583,
        "elev_m": 2917,
        "type": "rugged limestone",
    },
    "table_mountain": {
        "lat": -33.9625,
        "lon": 18.4039,
        "elev_m": 1085,
        "type": "flat-topped cliff",
    },
    "half_dome": {
        "lat": 37.7459,
        "lon": -119.5332,
        "elev_m": 2694,
        "type": "granite dome",
    },
    "el_capitan": {
        "lat": 37.7340,
        "lon": -119.6368,
        "elev_m": 2308,
        "type": "sheer granite wall",
    },
    "snowdon": {"lat": 53.0685, "lon": -4.0763, "elev_m": 1085, "type": "glacial peak"},
    "piton_neiges": {
        "lat": -21.0992,
        "lon": 55.4780,
        "elev_m": 3071,
        "type": "eroded volcano",
    },  # Réunion
    "teide": {
        "lat": 28.2724,
        "lon": -16.6424,
        "elev_m": 3718,
        "type": "island stratovolcano",
    },  # Tenerife
    "vesuvius": {
        "lat": 40.8219,
        "lon": 14.4286,
        "elev_m": 1281,
        "type": "famous caldera",
    },
    "mauna_kea": {
        "lat": 19.8207,
        "lon": -155.4680,
        "elev_m": 4207,
        "type": "shield volcano",
    },
    # === Extreme terrain shapes ===
    "kangchenjunga": {
        "lat": 27.7025,
        "lon": 88.1475,
        "elev_m": 8586,
        "type": "massive multi-ridge",
    },
    "annapurna": {
        "lat": 28.5960,
        "lon": 83.8203,
        "elev_m": 8091,
        "type": "steep deadly face",
    },
    "cerro_torre": {
        "lat": -49.3176,
        "lon": -73.1040,
        "elev_m": 3128,
        "type": "needle spire",
    },
    "ayers_rock": {
        "lat": -25.3444,
        "lon": 131.0369,
        "elev_m": 863,
        "type": "monolith/inselberg",
    },  # Uluru
}
