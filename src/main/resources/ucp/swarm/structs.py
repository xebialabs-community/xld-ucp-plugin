#!/usr/bin/env python
#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
def generateToken(deployed):
  return {
    "username": deployed.container.username,
    "password": deployed.container.password
  }

def generateService(deployed):
  return {
    "EndpointSpec": {
      "Mode": deployed.networkMode,
      "Ports": [
          {
              "Protocol": port.protocol,
              "PublishedPort": port.publishedPort,
              "TargetPort": port.targetPort,
              "PublishMode": port.publishMode
          } for port in deployed.ports
      ]
    },
    "Labels": deployed.labels,
    "Mode": {
      "Replicated": {
        "Replicas": deployed.replicas
      }
    },
    "Name": deployed.serviceName,
    "TaskTemplate": {
      "ContainerSpec": {
        "Image": deployed.image,
        "Labels": {
          "com.docker.ucp.access.label": "/",
          "com.docker.ucp.collection": "swarm",
          "com.docker.ucp.collection.root": "true",
          "com.docker.ucp.collection.swarm": "true"
        },
        "Env": ["{}={}".format(key, val) for key, val in deployed.envVars.items()],
        "StopGracePeriod": deployed.stopGracePeriod,
        "Isolation": "default"
      },
      "Resources": {
        "Limits": {},
        "Reservations": {}
      },
      "RestartPolicy": {
        "Condition": deployed.restartCondition,
        "MaxAttempts": int(deployed.restartMaxAttempts)
      },
      "Placement": {
        "Constraints": [
          "node.labels.com.docker.ucp.collection.swarm==true",
          "node.labels.com.docker.ucp.orchestrator.swarm==true"
        ],
        "Platforms": [
          {
            "Architecture": "amd64",
            "OS": "linux"
          }
        ]
      },
      "LogDriver": {},
      "ForceUpdate": 1,
      "Runtime": "container"
    },
    "Placement": {},
    "Resources": {
      "Limits": {
        "MemoryBytes": deployed.memoryLimit
      },
      "Reservations": {}
    },
    "RestartPolicy": {
      "Condition": "on-failure",
      "Delay": 10000000000,
      "MaxAttempts": 10
    }
  }

def generateNetwork(deployed):
  return {
    "Scope": deployed.scope,
    "Driver": deployed.driver,
    "EnableIPv6": deployed.enableIPv6,
    "IPAM": {
      "Driver": "default",
      "Config": [
        {
          "Subnet": "10.0.0.0/24",
          "Gateway": "10.0.0.1"
        }
      ]
    },
    "Ingress": deployed.ingress,
    "Internal": deployed.internal,
    "Attachable": deployed.attachable,
    "Name": deployed.networkName,
    "Options": {
      "com.docker.network.bridge.default_bridge": "true",
      "com.docker.network.bridge.enable_icc": "true",
      "com.docker.network.bridge.enable_ip_masquerade": "true",
      "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
      "com.docker.network.bridge.name": "docker0",
      "com.docker.network.driver.mtu": "1500"
    }
  }
