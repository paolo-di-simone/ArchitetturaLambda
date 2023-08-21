#!/bin/bash
influx delete --bucket bucket --org paolo \
  --token kEqIpjRQ6jy_RdFghsuJK268Su0nByfAP8ciupp8Q5B4nCCVg_4GVCWOplm4MrmF2kpQ5zOBWkQQHlXoqwkZeg== \
  --start '2023-01-01T00:00:00Z' \
  --stop '2023-12-31T00:00:00Z' \
  --predicate '_measurement="packet"'
