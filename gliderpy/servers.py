"""
Server names and aliases that point to an ERDDAP instance

"""


server_alias = {
    "National Glider Data Assembly Center": "https://gliders.ioos.us/erddap",
    "NGDAC": "https://gliders.ioos.us/erddap",
    "IOOS": "https://gliders.ioos.us/erddap",
    "Ocean Observatories Initiative": "https://erddap-uncabled.oceanobservatories.org/uncabled/erddap",
    "OOI": "https://erddap-uncabled.oceanobservatories.org/uncabled/erddap",
    "Institut français de recherche pour l'exploitation de la mer": "http://www.ifremer.fr/erddap",
    "ifremer": "http://www.ifremer.fr/erddap",
    "ifremer.fr": "http://www.ifremer.fr/erddap",
}

server_vars = {
    "https://gliders.ioos.us/erddap": [
        "depth",
        "latitude",
        "longitude",
        "salinity",
        "temperature",
        "time",
    ],
    "http://www.ifremer.fr/erddap": [
        "time",
        "latitude",
        "longitude",
        "PSAL",
        "TEMP",
        "PRES",
        "platform_deployment",
    ],
    "https://erddap-uncabled.oceanobservatories.org/uncabled/erddap": [
        "latitude",
        "longitude",
        "ctdgv_m_glider_instrument_practical_salinity",
        "ctdgv_m_glider_instrument_sci_water_temp",
        "ctdgv_m_glider_instrument_sci_water_pressure_dbar",
        "time",
        "quality_flag",
        "trajectory",
    ],
}


def server_select(server_string):
    """
    Attempts to match the supplied string to a known ERDDAP server by address or alias
    """
    if server_string in server_vars.keys():
        # If string matches exactly, return unchanged
        return server_string
    for server in server_vars.keys():
        # If string contains base ERDDAP address, return base ERDDAP address
        if server in server_string:
            return server
    for alias in server_alias:
        # If string matches one of the aliases, return the corresponding ERDDAP address
        if server_string.lower() == alias.lower():
            return server_alias[alias]
    # If the server is not recognised, print options of working servers and exit
    raise ValueError(
        "Supplied server/alias not recognised. Please use one of the following supported servers:\n"
        + str(server_vars.keys())[10:-1]
    )
