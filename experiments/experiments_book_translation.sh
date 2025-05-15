#! /bin/bash

set -o xtrace

MODEL_NAME="llama-3.1-70b-instruct"
KEY="pRt87ruBLVV443l"
PORT=10001


##############################
# ENGLISH -> CHINESE
##############################


# guofeng_v1 
python src/main.py \
    -i data/document_level/en-zh/guofeng_v1_full \
    -o results/document_level/model_wise/${MODEL_NAME}/en-zh/guofeng_v1_full \
    -s English \
    -t Chinese \
    --source-ext en \
    --target-ext zh \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


##############################
# CHINESE -> ENGLISH
##############################

# guofeng_v1 
python src/main.py \
    -i data/document_level/en-zh/guofeng_v1_full \
    -o results/document_level/model_wise/${MODEL_NAME}/zh-en/guofeng_v1_full \
    -s Chinese \
    -t English \
    --source-ext zh \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}
