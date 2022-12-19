#!/bin/bash

set -o errexit

sudo yum update
sudo yum install cargo rust git
git clone ssh://git@github.com/halcyox/metahumans.git
cd metahumans/alphademo/videoproxy
cargo build --release
cp target/release/videoproxy ~
