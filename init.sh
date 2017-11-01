#!/bin/bash

echo "Environment for scrapper"
echo $DCOS_URL
echo $PORT0
echo $NODE_ID
echo $KAFKA_ID

echo "Running metrics process"
python find_kafka_stats.py $KAFKA_ID $NODE_ID
