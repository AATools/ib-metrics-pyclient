# IBM IB metrics exporter

[![Build Status](https://travis-ci.com/AATools/ib-metrics-pyclient.svg?branch=master)](https://travis-ci.com/AATools/ib-metrics-pyclient) [![Coverage Status](https://coveralls.io/repos/github/AATools/ib-metrics-pyclient/badge.svg?branch=master)](https://coveralls.io/github/AATools/ib-metrics-pyclient?branch=master)

This is python client for collecting IBM Integration Bus metrics and exporting to [Prometheus pushgateway](https://github.com/prometheus/pushgateway). 
The collected metrics can be explored in Prometheus or Grafana.

The metrics are collected using [mqsilist](https://www.ibm.com/support/knowledgecenter/en/SSMKHH_9.0.0/com.ibm.etools.mft.doc/an07250_.htm) command. So, you need to install `IBM Integration Bus`.

Tested for IBM IB v9 and Python 2.6 and 2.7 on Linux.

## Collected metrics

By default, metrics are collected every 15 seconds.

The metrics provided by the client:
* `ib_broker_status...` - current status of IB brokers;
* `ib_exec_group_status...` - current status of IB execution groups;
* `ib_application_status...` - current status of IB applications;
* `ib_message_flow_status...` -  current status of IB message flows.

You can run `IB metrics pyclient` and [MQ metrics pyclient](https://github.com/AATools/mq-metrics-pyclient) together. Metrics from both clients will be sent to the same pushgateway. Conflicts will not arise.

## Getting Started

Python 2.6 or 2.7 should be already installed.

Download Prometheus Pushgateway from the [release page](https://github.com/prometheus/pushgateway/releases) and unpack the tarball.

### Run Prometheus Pushgateway

```bash
cd pushgateway
nohup ./pushgateway > pushgateway.log &
```

For Pushgateway the default port is used (":9091").

### Run ib-metrics-pyclient

```bash
git clone https://github.com/AATools/ib-metrics-pyclient
cd ib-metrics-pyclient
chmod u+x ./iib_metrics_client.py
nohup ./iib_metrics_client.py &
```

After that, you should set up your Prometheus server to collect metrics from Pushgateway (`http://<hostname>:9091/metrics`).

## Grafana dashboard

The Grafana dashboard visualizes collected metrics.

## Simple process scheme

![](../images/ib_metrics_pyclient_scheme.jpg?raw=true)
