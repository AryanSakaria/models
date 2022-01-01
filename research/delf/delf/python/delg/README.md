# Instrcutions to run DELG

---

## Install DELF FIRST
```bash
conda create -n delg
conda activate delg
conda install pip
pip install 'tensorflow-gpu>=2.2.0'
git clone https://github.com/google-research/tf-slim.git
cd tf-slim
pip install .
From home, do mkdir protoc. Do the following commands inside protoc
wget https://github.com/google/protobuf/releases/download/v3.3.0/protoc-3.3.0-linux-x86_64.zip
PATH_TO_PROTOC=`pwd`
pip install matplotlib numpy scikit-image scipy
sudo apt-get install python3-tk
git clone https://github.com/AryanSakaria/models.git
cd models/research
export PYTHONPATH=$PYTHONPATH:`pwd`
#From models/research/delf/ do:
${PATH_TO_PROTOC?}/bin/protoc delf/protos/*.proto --python_out=.
pip install -e . (Do this from models/research/delf/)
```
---
## Test DELF installation
```bash
python -c 'import delf'
```
---
## Run DELG
### Download model

This is necessary to reproduce the main paper results. This example shows the
R50-DELG model, pretrained on GLD; see the available pre-trained models
[here](../../../README.md#pre-trained-models), for other variants (eg, R101,
trained on GLDv2-clean).

```bash
# From models/research/delf/delf/python/delg
mkdir parameters && cd parameters

# R50-DELG-GLD model.
wget http://storage.googleapis.com/delf/r50delg_gld_20200814.tar.gz
tar -xvzf r50delg_gld_20200814.tar.gz
```