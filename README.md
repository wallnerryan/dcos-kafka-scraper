
# DC/OS Kafka Scraper

This scraper does a specific thing, that this is.

- Take in a Node ID and Kafka Framework ID that a Broker is running on
- Find the Broker container in the Metricd "/container" API
- Translate the metrics provided from the Kafka JAR exposed by the metric API in prometheus Gauges

##  How to use

```
docker run -d \
  -e PORT0=3456 \
  -e TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOiJyd2FsbG5lciIsImV4cCI6MTUwOTgxMzI0MX0.rCAWibKuSCJByYUenZ77JSrXq9WhZVAP31XjMdcestGaRAhwN-h6ngdIte4U6Q0twmOeH-dkQX45He-XBCkv_tpwVtlR8YJHF_uhBJr0_QAhKzPa96e3rE8onmMiArdPW6I8s2dninO6mGPIru1Rrn66z65xXesD6sF8IIg186dAZ72i9pN3O6lny9iMtjnM-pqh5G5YsavUPv1JUPGzL20boeINB3IJySegw-L4P_oOuBLhOeNi-dQVW9XrCtTHGVqIkLEsr7rCeUEE9YDOn5XkUB5Q8YlzIXxFlSD1nCm1Q11eA50xZPYlU2_WrIFIt-7wQpwJjBn-rhUiK5ZDDg \
  -e DCOS_URL=https://ui.dcos.dev.bed.athenahealth.com \
  -e NODE_ID=b69b2027-ecfb-4b8c-b025-5dae47f450c9-S1 \
  -e KAFKA_ID=c26f14da-cb71-46e2-852a-e4c9f327df8d-0001  \
  -p 9091:3456 \
  wallnerryan/kafkascraper:latest
```

## Marathon

Assuming you have the following setup

 - service user username
 - service user password in DC/OS Secrets
 - Kafka clusters and brokers running on Nodes

```
{
  "id": "/logging/kafkascraper-dataexchange-source-kafka-broker0",
  "instances": 1,
  "cpus": 0.1,
  "mem": 128,
  "disk": 0,
  "gpus": 0,
  "constraints": [],
  "fetch": [],
  "storeUrls": [],
  "backoffSeconds": 1,
  "backoffFactor": 1.15,
  "maxLaunchDelaySeconds": 3600,
  "container": {
    "type": "DOCKER",
    "volumes": [],
    "docker": {
      "image": "docker.artifactory.aws.athenahealth.com/devops/kafkascraper:0.0.5",
      "network": "BRIDGE",
      "portMappings": [
        {
          "containerPort": 18294,
          "hostPort": 18294,
          "servicePort": 10620,
          "protocol": "tcp",
          "name": "metrics"
        }
      ],
      "privileged": false,
      "parameters": [],
      "forcePullImage": false
    }
  },
  "healthChecks": [],
  "readinessChecks": [],
  "dependencies": [],
  "upgradeStrategy": {
    "minimumHealthCapacity": 1,
    "maximumOverCapacity": 1
  },
  "secrets": {
    "secret0": {
      "source": "logging/svcuserpassword"
    }
  },
  "unreachableStrategy": {
    "inactiveAfterSeconds": 300,
    "expungeAfterSeconds": 600
  },
  "killSelection": "YOUNGEST_FIRST",
  "requirePorts": false,
  "env": {
    "LOGGING_SVC_P": {
      "secret": "secret0"
    },
    "DCOS_URL": "https://ui.dcos.dev.bed.athenahealth.com",
    "NODE_ID": "beea2d96-715d-42be-a9a2-f3487d078642-S51",
    "KAFKA_ID": "c26f14da-cb71-46e2-852a-e4c9f327df8d-0001",
    "LOGGING_SVC_U": "pvtc_logging_user"
  }
}
```
