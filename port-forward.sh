#!/bin/bash

# Forward port 8080 from the rc-recommunity deployment
kubectl port-forward -n rc-recommunity deployment/rc-recommunity 8080:8080 &

# Forward port 27017 from the mongodb service
kubectl port-forward -n rc-recommunity service/mongodb 27017:27017 &
