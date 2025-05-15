#! /bin/bash

set -o xtrace

MODEL_NAME="llama-3.3-70b-instruct"
KEY="pRt87ruBLVV443l"
PORT=10001


##############################
# ENGLISH -> CHINESE
##############################

# fiction
python src/main.py \
    -i data/document_level/en-zh/mzprt/fiction \
    -o results/document_level/model_wise/${MODEL_NAME}/en-zh/mzprt/fiction \
    -s English \
    -t Chinese \
    --source-ext en \
    --target-ext zh \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# qa 
python src/main.py \
    -i data/document_level/en-zh/mzprt/qa \
    -o results/document_level/model_wise/${MODEL_NAME}/en-zh/mzprt/qa \
    -s English \
    -t Chinese \
    --source-ext en \
    --target-ext zh \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# news
python src/main.py \
    -i data/document_level/en-zh/wmt2022/news \
    -o results/document_level/model_wise/${MODEL_NAME}/en-zh/wmt2022/news \
    -s English \
    -t Chinese \
    --source-ext en \
    --target-ext zh \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# social 
python src/main.py \
    -i data/document_level/en-zh/wmt2022/social \
    -o results/document_level/model_wise/${MODEL_NAME}/en-zh/wmt2022/social \
    -s English \
    -t Chinese \
    --source-ext en \
    --target-ext zh \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# military 
python src/main.py \
    -i data/document_level/en-zh/ours/military \
    -o results/document_level/model_wise/${MODEL_NAME}/en-zh/ours/military \
    -s English \
    -t Chinese \
    --source-ext en \
    --target-ext zh \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# iwslt2017 
python src/main.py \
    -i data/document_level/en-zh/iwslt2017 \
    -o results/document_level/model_wise/${MODEL_NAME}/en-zh/iwslt2017 \
    -s English \
    -t Chinese \
    --source-ext en \
    --target-ext zh \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# guofeng_v1 
python src/main.py \
    -i data/document_level/en-zh/guofeng_v1/TEST_2 \
    -o results/document_level/model_wise/${MODEL_NAME}/en-zh/guofeng_v1/TEST_2 \
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

# fiction
python src/main.py \
    -i data/document_level/en-zh/mzprt/fiction \
    -o results/document_level/model_wise/${MODEL_NAME}/zh-en/mzprt/fiction \
    -s Chinese \
    -t English \
    --source-ext zh \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# qa 
python src/main.py \
    -i data/document_level/en-zh/mzprt/qa \
    -o results/document_level/model_wise/${MODEL_NAME}/zh-en/mzprt/qa \
    -s Chinese \
    -t English \
    --source-ext zh \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# news
python src/main.py \
    -i data/document_level/en-zh/wmt2022/news \
    -o results/document_level/model_wise/${MODEL_NAME}/zh-en/wmt2022/news \
    -s Chinese \
    -t English \
    --source-ext zh \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# social 
python src/main.py \
    -i data/document_level/en-zh/wmt2022/social \
    -o results/document_level/model_wise/${MODEL_NAME}/zh-en/wmt2022/social \
    -s Chinese \
    -t English \
    --source-ext zh \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# military 
python src/main.py \
    -i data/document_level/en-zh/ours/military \
    -o results/document_level/model_wise/${MODEL_NAME}/zh-en/ours/military \
    -s Chinese \
    -t English \
    --source-ext zh \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# iwslt2017 
python src/main.py \
    -i data/document_level/en-zh/iwslt2017 \
    -o results/document_level/model_wise/${MODEL_NAME}/zh-en/iwslt2017 \
    -s Chinese \
    -t English \
    --source-ext zh \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


# guofeng_v1 
python src/main.py \
    -i data/document_level/en-zh/guofeng_v1/TEST_2 \
    -o results/document_level/model_wise/${MODEL_NAME}/zh-en/guofeng_v1/TEST_2 \
    -s Chinese \
    -t English \
    --source-ext zh \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}



##############################
# ENGLISH -> GERMAN
##############################

python src/main.py \
    -i data/document_level/en-de/iwslt2017 \
    -o results/document_level/model_wise/${MODEL_NAME}/en-de/iwslt2017 \
    -s English \
    -t German \
    --source-ext en \
    --target-ext de \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


##############################
# GERMAN -> ENGLISH
##############################

python src/main.py \
    -i data/document_level/en-de/iwslt2017 \
    -o results/document_level/model_wise/${MODEL_NAME}/de-en/iwslt2017 \
    -s German \
    -t English \
    --source-ext de \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}



##############################
# ENGLISH -> FRENCH
##############################

python src/main.py \
    -i data/document_level/en-fr/iwslt2017 \
    -o results/document_level/model_wise/${MODEL_NAME}/en-fr/iwslt2017 \
    -s English \
    -t French \
    --source-ext en \
    --target-ext fr \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


##############################
# FRENCH -> ENGLISH
##############################

python src/main.py \
    -i data/document_level/en-fr/iwslt2017 \
    -o results/document_level/model_wise/${MODEL_NAME}/fr-en/iwslt2017 \
    -s French \
    -t English \
    --source-ext fr \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}



##############################
# ENGLISH -> JAPANESE
##############################

python src/main.py \
    -i data/document_level/en-ja/iwslt2017 \
    -o results/document_level/model_wise/${MODEL_NAME}/en-ja/iwslt2017 \
    -s English \
    -t Japanese \
    --source-ext en \
    --target-ext ja \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}


##############################
# JAPANESE -> ENGLISH
##############################

python src/main.py \
    -i data/document_level/en-ja/iwslt2017 \
    -o results/document_level/model_wise/${MODEL_NAME}/ja-en/iwslt2017 \
    -s Japanese \
    -t English \
    --source-ext ja \
    --target-ext en \
    -m ${MODEL_NAME} \
    -k ${KEY} \
    -p ${PORT}
