"""This script will be to show how extract information from the dwd database"""

from wetterdienst import Wetterdienst, Resolution, Period
from wetterdienst.provider.dwd.observation import (
    DwdObservationRequest,
    DwdObservationDataset,
    # DwdObservationResolution,
)
from wetterdienst.provider.dwd.observation import (
    DwdObservationRequest,
    # DwdObservationPeriod,
)

"""The big treasure of the DWD is buried under a clutter of a file_server. 
The data you find here can reach back to 19th century and is represented by
 over 1000 stations in Germany according to the report referenced above. 
 The amount of stations that cover a specific parameter may differ strongly, 
 so don’t expect the amount of data to be that generous for all the parameters."""

# Here you get all information following the paramenters from all stations available
stations = DwdObservationRequest(
    parameter=DwdObservationDataset.PRECIPITATION_MORE,
    resolution=Resolution.DAILY,
    period=Period.HISTORICAL,
)

# To check the raw information from a specific station use the example bellow
print(stations.filter_by_station_id(1).values.all().df)
