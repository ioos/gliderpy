## gliderpy

Gliderpy aims to facilitate effortless access to glider data hosted on ERDDAP servers. Gliderpy is a high level wrapper around [erddapy](https://github.com/ioos/erddapy), with glider specific tooling and in-built plotting methods.

Try it out on binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/oceanhackweek/ohw20-proj-glide-data-fetcher/master)

### Documentation and code

URLs for the docs and code.

### Installation

For `conda` users you can

```shell
conda install --channel conda-forge gliderpy
```

or, if you are a `pip` users

```shell
pip install gliderpy
```

### Example

```python
from gliderpy.fetchers import GliderDataFetcher

glider_grab = GliderDataFetcher()

glider_grab.fetcher.dataset_id = "whoi_406-20160902T1700"
df = glider_grab.to_pandas()

```
