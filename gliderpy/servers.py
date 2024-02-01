"""
Server names and aliases that point to an ERDDAP instance

"""

server_vars = {
    "https://gliders.ioos.us/erddap": [
        "latitude",
        "longitude",
        "pressure",
        "profile_id",
        "salinity",
        "temperature",
        "time",
    ],
}

server_parameter_rename = {
    "ctdgv_m_glider_instrument_practical_salinity (1)": "salinity",
    "ctdgv_m_glider_instrument_sci_water_pressure_dbar (dbar)": "pressure",
    "ctdgv_m_glider_instrument_sci_water_temp (deg_c)": "temperature",
    "dataset_url": "dataset_url",
    "latitude (degrees_north)": "latitude",
    "longitude (degrees_east)": "longitude",
    "pres (decibar)": "pressure",
    "pressure (dbar)": "pressure",
    "profile_id": "profile_id",
    "psal (psu)": "salinity",
    "salinity (1)": "salinity",
    "temp (degree_celsius)": "temperature",
    "temperature (celsius)": "temperature",
    "time (utc)": "time",
}
