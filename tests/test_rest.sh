#!/bin/bash

curl -X POST -d "queue=test&value=foobar" http://localhost:8888/docdb
curl http://localhost:8888/docdb
