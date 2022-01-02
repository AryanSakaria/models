# Instrcutions to run DELG

---

## Install DELF FIRST
```bash
conda create -n delg
conda activate delg
conda install pip
pip install 'tensorflow-gpu>=2.2.0'
pip install tensorflow-object-detection-api
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
### Prepare data
Navigate to https://github.com/Shubodh/x-view-scratch/tree/master/utils.
```bash
#if data convention as described as before is followed, with mp3d data in ../data_collection/x-view/mp3d, then this will run without issues
python create_dbow_db.py
```
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
## Extract features and perform retrieval
This next part extracts features, performs retrieval and also displays accuracy
```bash
#change the directory path in line 75
python extract_features_all_scenes.py --image_set query
python extract_features_all_scenes.py --image_set index
python perform_retrieval_all_scenes.py
```