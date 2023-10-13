"""
Server names and aliases that point to an ERDDAP instance

"""


server_vars = {
    "https://gliders.ioos.us/erddap": [
        "pressure",
        "latitude",
        "longitude",
        "salinity",
        "temperature",
        "time",
        "profile_id",
    ],
}

server_parameter_rename = {
    "latitude (degrees_north)": "latitude",
    "longitude (degrees_east)": "longitude",
    "salinity (1)": "salinity",
    "psal (psu)": "salinity",
    "ctdgv_m_glider_instrument_practical_salinity (1)": "salinity",
    "temperature (celsius)": "temperature",
    "temp (degree_celsius)": "temperature",
    "ctdgv_m_glider_instrument_sci_water_temp (deg_c)": "temperature",
    "pres (decibar)": "pressure",
    "pressure (dbar)": "pressure",
    "ctdgv_m_glider_instrument_sci_water_pressure_dbar (dbar)": "pressure",
    "dataset_url": "dataset_url",
}
