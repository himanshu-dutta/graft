#! /bin/bash

set -o xtrace

MODEL_NAME="llama-3.1-8b-instruct"
KEY="pRt87ruBLVV443l"
PORT=10001
DISCOURSE_AGENT_NAMES=("semantic-chunker" "ours" "random") # Variations of discourse agent


##############################
# ENGLISH -> CHINESE
##############################
for DISCOURSE_AGENT_NAME in "${DISCOURSE_AGENT_NAMES[@]}"; do
    python src/main.py \
        -i data/document_level/en-zh/iwslt2017 \
        -o results/document_level/discourse_agent_analysis/${DISCOURSE_AGENT_NAME}/en-zh/iwslt2017 \
        -s English \
        -t Chinese \
        --source-ext en \
        --target-ext zh \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --discourse-agent-name ${DISCOURSE_AGENT_NAME}
done

##############################
# CHINESE -> ENGLISH
##############################
for DISCOURSE_AGENT_NAME in "${DISCOURSE_AGENT_NAMES[@]}"; do
    python src/main.py \
        -i data/document_level/en-zh/iwslt2017 \
        -o results/document_level/discourse_agent_analysis/${DISCOURSE_AGENT_NAME}/zh-en/iwslt2017 \
        -s Chinese \
        -t English \
        --source-ext zh \
        --target-ext en \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --discourse-agent-name ${DISCOURSE_AGENT_NAME}
done

##############################
# ENGLISH -> GERMAN
##############################
for DISCOURSE_AGENT_NAME in "${DISCOURSE_AGENT_NAMES[@]}"; do
    python src/main.py \
        -i data/document_level/en-de/iwslt2017 \
        -o results/document_level/discourse_agent_analysis/${DISCOURSE_AGENT_NAME}/en-de/iwslt2017 \
        -s English \
        -t German \
        --source-ext en \
        --target-ext de \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --discourse-agent-name ${DISCOURSE_AGENT_NAME}
done

##############################
# GERMAN -> ENGLISH
##############################
for DISCOURSE_AGENT_NAME in "${DISCOURSE_AGENT_NAMES[@]}"; do
    python src/main.py \
        -i data/document_level/en-de/iwslt2017 \
        -o results/document_level/discourse_agent_analysis/${DISCOURSE_AGENT_NAME}/de-en/iwslt2017 \
        -s German \
        -t English \
        --source-ext de \
        --target-ext en \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --discourse-agent-name ${DISCOURSE_AGENT_NAME}
done

##############################
# ENGLISH -> FRENCH
##############################
for DISCOURSE_AGENT_NAME in "${DISCOURSE_AGENT_NAMES[@]}"; do
    python src/main.py \
        -i data/document_level/en-fr/iwslt2017 \
        -o results/document_level/discourse_agent_analysis/${DISCOURSE_AGENT_NAME}/en-fr/iwslt2017 \
        -s English \
        -t French \
        --source-ext en \
        --target-ext fr \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --discourse-agent-name ${DISCOURSE_AGENT_NAME}
done

##############################
# FRENCH -> ENGLISH
##############################
for DISCOURSE_AGENT_NAME in "${DISCOURSE_AGENT_NAMES[@]}"; do
    python src/main.py \
        -i data/document_level/en-fr/iwslt2017 \
        -o results/document_level/discourse_agent_analysis/${DISCOURSE_AGENT_NAME}/fr-en/iwslt2017 \
        -s French \
        -t English \
        --source-ext fr \
        --target-ext en \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --discourse-agent-name ${DISCOURSE_AGENT_NAME}
done

##############################
# ENGLISH -> JAPANESE
##############################
for DISCOURSE_AGENT_NAME in "${DISCOURSE_AGENT_NAMES[@]}"; do
    python src/main.py \
        -i data/document_level/en-ja/iwslt2017 \
        -o results/document_level/discourse_agent_analysis/${DISCOURSE_AGENT_NAME}/en-ja/iwslt2017 \
        -s English \
        -t Japanese \
        --source-ext en \
        --target-ext ja \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --discourse-agent-name ${DISCOURSE_AGENT_NAME}
done

##############################
# JAPANESE -> ENGLISH
##############################
for DISCOURSE_AGENT_NAME in "${DISCOURSE_AGENT_NAMES[@]}"; do
    python src/main.py \
        -i data/document_level/en-ja/iwslt2017 \
        -o results/document_level/discourse_agent_analysis/${DISCOURSE_AGENT_NAME}/ja-en/iwslt2017 \
        -s Japanese \
        -t English \
        --source-ext ja \
        --target-ext en \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --discourse-agent-name ${DISCOURSE_AGENT_NAME}
done
