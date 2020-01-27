# SN_boxy

This repository contains an implementation of YOLOv3 (https://github.com/experiencor/keras-yolo3) with and without Switchable Normalization (https://arxiv.org/abs/1806.10779) on the boxy dataset (https://boxy-dataset.com/boxy/).

## This repository is organized as follows:

- **utils** : All source code for production
- **tests** : All code for testing
- **configs** : Configuration files.
- **data** : Example a small amount of data from boxy dataset to validate installation

## Setup
Clone repository and create a new environment
```
conda create -n SN_boxy python=3.6
source activate SN_boxy
cd SN_boxy
pip install -r requirements.txt
```
## Data

Full boxy dataset available at https://boxy-dataset.com/boxy/.
Place training data 



## Configs

- Use /configs/config_boxy.json file 


## Test

- Test that json labels from boxy dataset (training and validation) are valid
```
# Example

python label_checks.py -/SN_boxy/labels_train/boxy_labels_train.json 

```

## Run Inference
- Run predict.py on raw images to detect vehicles
```
# Example

python predict.py -c /SN_boxy/configs/config_boxy.json /SN_boxy/data/raw/

```

## Build Model
- Include instructions of how to build the model
- This can be done either locally or on the cloud
```
# Example

# Step 1
# Step 2
```

## Serve Model
- Include instructions of how to set up a REST or RPC endpoint
- This is for running remote inference via a custom model
```
# Example

# Step 1
# Step 2
```

## Analysis
- Include some form of EDA (exploratory data analysis)
- And/or include benchmarking of the model and results
```
# Example

# Step 1
# Step 2
```
