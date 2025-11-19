#!/bin/bash

curl -f http://localhost:5000 || exit 1
echo "OK"
