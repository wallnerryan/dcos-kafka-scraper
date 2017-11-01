#!/usr/bin/env python

from prometheus_client import start_http_server, Metric, REGISTRY
import requests
requests.packages.urllib3.disable_warnings()
import json
import commands
import sys, os
import time

class KafkaJsonCollector(object):
  def __init__(self, url, node_id, kafka_id, svc_u, svc_p):
    self._url = url
    self._node_id = node_id
    self._kafka_id = kafka_id
    self._svc_u = svc_u
    self._svc_p = svc_p
    self._token = "none"

  def get_token(self):
     print "Getting New Auth Token"
     payload={"uid": self._svc_u, "password": self._svc_p }
     token_r = requests.post('%s/acs/api/v1/auth/login' % self._url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, verify=False)
     if token_r.status_code == 200:
       token_json=json.loads(token_r.content)
       self._token = token_json['token']

  def collect(self):

     r = requests.get('%s/system/v1/agent/%s/metrics/v0/containers' % (self._url, self._node_id),  headers={'Authorization': 'token='+self._token}, verify=False)

     # if failed, refresh token
     if r.status_code == 401:
         print "Failed auth, getting new auth token"
         self.get_token()
         self.collect()
     else:
         containers=r.json()

         for c in containers:
           r = requests.get('%s/system/v1/agent/%s/metrics/v0/containers/%s/app' % (self._url, self._node_id, c),  headers={'Authorization': 'token='+self._token}, verify=False)
           try:
             app=json.loads(r.content)
             if 'dimensions' in app:
                if app['dimensions']['framework_id'] == self._kafka_id:
                    for dp in app['datapoints']:
                        dp_removed_periods = dp[u'name'].replace(".", "_")
                        dp_removed_dashes = dp_removed_periods.replace("-", "_")
                        metric = Metric( dp_removed_dashes,'', 'gauge')
                        metric.add_sample(dp_removed_dashes, value=dp[u'value'], labels={})
                        yield metric
                        print "%s:%d" % (dp[u'name'], dp[u'value'])
                    print "FOUND KAFKA CONTAINER " + c
                    print "Framework " + app['dimensions']['framework_id']
                    print "Executor " + app['dimensions']['executor_id']
                    print "Host " + app['dimensions']['hostname']
                    print "Task " + app['dimensions']['task_name']
                    print "Task ID " + app['dimensions']['task_id']

           except Exception as e:
             pass
             #print e
             #print "issue getting json"

if __name__ == "__main__":
   if sys.argv[1] == "--help" or sys.argv[1] == "help" or sys.argv[1] == "-help":
     print """
          Make sure LOGGING_SVC_U, LOGGING_SVC_P, and DCOS_URL are set in the environment
          LOGGING_SVC_U: service user used to login to dcos
          LOGGING_SVC_P: service user password used to login to dcos
     
     USAGE:
     %s <kafka_framework_id> <node_id>
     """ % sys.argv[0]
     exit(0)

   fid=sys.argv[1]
   nid=sys.argv[2]

   uid = os.environ['LOGGING_SVC_U']
   uid_p = os.environ['LOGGING_SVC_P']
   dcos_url = os.environ['DCOS_URL']

   start_http_server(int(os.environ['PORT0']))
   REGISTRY.register(KafkaJsonCollector(dcos_url, nid, fid, uid, uid_p))

   while True: time.sleep(1)
