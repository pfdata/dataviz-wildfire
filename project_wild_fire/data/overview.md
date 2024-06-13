# Database

## BMEL

| Year | Waldbrandflächen nach Bestandsarten | Ursachen  | Waldbrände in den einzelnen Monaten des Kalenderjahres - Anzahl | Waldbrände in den einzelnen Monaten des Kalenderjahres - Fläche |
| ---- | ----------------------------------- | --------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| 1995 | available                           | available | available                                                       | available                                                       |
| 1996 | available                           | available | available                                                       | available                                                       |
| 1997 | available                           | available | available                                                       | available                                                       |
| 1998 | available                           | available | available                                                       | available                                                       |
| 1999 | available                           | available | available                                                       | available                                                       |
| 2000 | available                           | available | available                                                       | available                                                       |
| 2001 | available                           | available | available                                                       | available                                                       |
| 2002 | available                           | available | available                                                       | available                                                       |
| 2003 | available                           | available | available                                                       | available                                                       |
| 2004 | available                           | available | available                                                       | available                                                       |
| 2005 | available                           | available | available                                                       | available                                                       |
| 2006 | available                           | available | available                                                       | available                                                       |
| 2007 | available                           | available | available                                                       | available                                                       |
| 2008 | available                           | available | available                                                       | available                                                       |
| 2009 | available                           | available | available                                                       | available                                                       |
| 2010 | available                           | available | available                                                       | available                                                       |
| 2011 | available                           | available | available                                                       | available                                                       |
| 2012 | available                           | available | available                                                       | available                                                       |
| 2013 | available                           | available | available                                                       | available                                                       |
| 2014 | available                           | available | available                                                       | available                                                       |
| 2015 | available                           | available | available                                                       | available                                                       |
| 2016 | available                           | available | available                                                       | available                                                       |
| 2017 | available                           | available | available                                                       | available                                                       |
| 2018 | available                           | available | available                                                       | available                                                       |
| 2019 | available                           | available | available                                                       | available                                                       |
| 2020 | available                           | available | available                                                       | available                                                       |
| 2021 | available                           | available | available                                                       | available                                                       |
| 2022 | available                           | available | available                                                       | available                                                       |

## DWD

# Weather Database Overview

| Metric                        | Daily | Monthly | Yearly | Range from Year to Year |
| ----------------------------- | ----- | ------- | ------ | ----------------------- |
| Temperatures                  |       |         |        |                         |
| Wind Speed                    |       |         |        |                         |
| Number of Hot Days            |       |         |        |                         |
| Number of Ice Days            |       |         |        |                         |
| Number of Rainy Days          |       |         |        |                         |
| Number of Rainy Days in a Row |       |         |        |                         |
| Air temperature Mean          |       |   Ok    | Ok     |                         |
| Precipitation                 |       | Ok      | Ok     |                         |
| Precipitation GE10mm Days     |       |         | Ok     |                         |
| Precipitation GE20mm Days     |       |         | Ok     |                         |
| Summer Days                   |       |         | Ok     |                         |
| sunshine_duration             |       | Ok      | Ok     |                         |
| tropical_nights_tminGE20      |       |         | Ok     |                         |
| Frost Days                    |       |         | Ok     |                         |
| Ice Days                      |       |         | Ok     |                         |
|                               |       |         |        |                         |
|                               |       |         |        |                         |
|                               |       |         |        |                         |

## DWD Python API

| Dataset                | 1_minute | 5_minutes | 10_minutes | hourly | subdaily | daily | monthly | annual |
| ---------------------- | -------- | --------- | ---------- | ------ | -------- | ----- | ------- | ------ |
| PRECIPITATION          | +        | +         | +          | -      | -        | -     | -       | -      |
| TEMPERATURE_AIR        | -        | -         | +          | +      | +        | -     | -       | -      |
| TEMPERATURE_EXTREME    | -        | -         | +          | -      | -        | -     | -       | -      |
| WIND_EXTREME           | -        | -         | +          | -      | -        | -     | -       | -      |
| SOLAR                  | -        | -         | +          | +      | -        | +     | -       | +      |
| WIND                   | -        | -         | +          | +      | +        | -     | -       | -      |
| CLOUD_TYPE             | -        | -         | -          | +      | -        | -     | -       | -      |
| CLOUDINESS             | -        | -         | -          | +      | +        | -     | -       | -      |
| DEW_POINT              | -        | -         | -          | +      | -        | -     | -       | -      |
| PRESSURE               | -        | -         | -          | +      | +        | -     | -       | -      |
| TEMPERATURE_SOIL       | -        | -         | -          | +      | -        | +     | -       | -      |
| SUNSHINE_DURATION      | -        | -         | -          | +      | -        | -     | -       | -      |
| VISIBILITY             | -        | -         | -          | +      | +        | -     | -       | -      |
| WIND_SYNOPTIC          | -        | -         | -          | +      | -        | -     | -       | -      |
| MOISTURE               | -        | -         | -          | +      | +        | -     | -       | -      |
| CLIMATE_SUMMARY        | -        | -         | -          | -      | +        | +     | +       | +      |
| PRECIPITATION_MORE     | -        | -         | -          | -      | -        | +     | +       | +      |
| WATER_EQUIVALENT       | -        | -         | -          | -      | -        | +     | -       | -      |
| WEATHER_PHENOMENA      | -        | -         | -          | -      | -        | +     | +       | +      |
| URBAN_TEMPERATURE_AIR  | -        | -         | -          | -      | -        | +     | -       | -      |
| URBAN_PRECIPITATION    | -        | -         | -          | -      | -        | +     | -       | -      |
| URBAN_PRESSURE         | -        | -         | -          | -      | -        | +     | -       | -      |
| URBAN_TEMPERATURE_SOIL | -        | -         | -          | -      | -        | +     | -       | -      |
| URBAN_SUN              | -        | -         | -          | -      | -        | +     | -       | -      |
| URBAN_WIND             | -        | -         | -          | -      | -        | +     | -       | -      |

Quelle: [API](https://wetterdienst.readthedocs.io/en/latest/data/coverage/dwd/observation.html)
