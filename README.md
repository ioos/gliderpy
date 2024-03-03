## gliderpy

Gliderpy aims to facilitate effortless access to glider data hosted on ERDDAP servers.
Gliderpy is a high level wrapper around [erddapy](https://github.com/ioos/erddapy),
with glider specific tooling and in-built plotting methods.

Try it out on binder [![Binder](https://mybinder.org/badge_logo.svg)](https://github.com/ioos/gliderpy/blob/main/notebooks/00-quick_intro.ipynb)

And check the docs for more info: https://ioos.github.io/gliderpy

### Installation

For `conda` users you can

```shell
conda install --channel conda-forge gliderpy
```

or, if you are a `pip` users

```shell
pip install gliderpy
```

gliderpy aims to make querying and downloading glider data easier. Here is how one would build a query using erddapy:

```shell
from erddapy import ERDDAP

e = ERDDAP(
    server="https://gliders.ioos.us/erddap",
    protocol="tabledap",
    response="csv",
)
e.dataset_id = "whoi_406-20160902T1700"

e.variables = [
    "depth",
    "latitude",
    "longitude",
    "salinity",
    "temperature",
    "profile_id",
    "time",
]

df = e.to_pandas(
    index_col="time (UTC)",
    parse_dates=True,
)
df.head()
```
And here is how to use gliderpy to obtain the same results but with fewer lines and a cleaner code:
```shell
from gliderpy.fetchers import GliderDataFetcher

glider_grab = GliderDataFetcher()

glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
df = glider_grab.to_pandas()
df.head()
```
Much easier, right? The variable names are standardized by gliderpy, making it easier to fetch from different data sources and comparing the results.

The gliderpy library can subset the data on the server side by passing a geographic bounding box and time interval.

Querying multiple datasets
The most common use is to search all datasets for data that falls within the certain space-time bounds.
glider_grab = GliderDataFetcher()
```shell
df = glider_grab.query(10, 40, -90, 8, "2010-01-01", "2013-06-02")

datasets = glider_grab.to_pandas()
datasets.keys()
datasets["ru23-20121025T1944"].head()
```
Dataset search
One can query all dataset_ids available in the server.
```shell
from gliderpy.fetchers import DatasetList

datasets = DatasetList()
ds_ids = datasets.get_ids()

print(f"found {len(ds_ids)} glider datasets on the server {datasets.e.server}.")
```
