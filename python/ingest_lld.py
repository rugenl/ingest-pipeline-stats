#!/bin/python3

import re
import requests
import json

pw = "secret"

pipes = {"init"}
pipes.remove("init")

node_stats = requests.get(
    "https://elastic.stack:9200/_nodes/stats/ingest",
    auth=("zabbix-user", pw),
    verify="ca.cer",
)

json_stats = json.loads(node_stats.text)

for k, v in json_stats["nodes"].items():
    for pipe_name, pipe_data in v["ingest"]["pipelines"].items():
        if pipe_data["count"] > 0:
            pipes.add(pipe_name)

stats = []
for pipe in pipes:
    stats.append({"{#PIPELINE}": pipe})

print(" - es_ingest_pipelines", json.dumps({"data": stats}))
