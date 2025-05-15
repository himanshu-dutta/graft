#! /bin/bash

set -o xtrace

MODEL_NAME="llama-3.1-8b-instruct"
KEY="pRt87ruBLVV443l"
PORT=10001
EDGE_AGENT_STRATEGIES=("ours" "tfidf" "only-predecessor") # Variants of EDGE_AGENT_STRATEGY

##############################
# EXPERIMENT LOOP
##############################

##############################
# ENGLISH -> CHINESE
##############################
for EDGE_AGENT_STRATEGY in "${EDGE_AGENT_STRATEGIES[@]}"; do
    python src/main.py \
        -i data/document_level/en-zh/iwslt2017 \
        -o results/document_level/edge_agent_analysis/${EDGE_AGENT_STRATEGY}/en-zh/iwslt2017 \
        -s English \
        -t Chinese \
        --source-ext en \
        --target-ext zh \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --edge-agent-strategy ${EDGE_AGENT_STRATEGY}
    
done

##############################
# CHINESE -> ENGLISH
##############################
for EDGE_AGENT_STRATEGY in "${EDGE_AGENT_STRATEGIES[@]}"; do
    python src/main.py \
        -i data/document_level/en-zh/iwslt2017 \
        -o results/document_level/edge_agent_analysis/${EDGE_AGENT_STRATEGY}/zh-en/iwslt2017 \
        -s Chinese \
        -t English \
        --source-ext zh \
        --target-ext en \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --edge-agent-strategy ${EDGE_AGENT_STRATEGY}
    
done

##############################
# ENGLISH -> GERMAN
##############################
for EDGE_AGENT_STRATEGY in "${EDGE_AGENT_STRATEGIES[@]}"; do
    python src/main.py \
        -i data/document_level/en-de/iwslt2017 \
        -o results/document_level/edge_agent_analysis/${EDGE_AGENT_STRATEGY}/en-de/iwslt2017 \
        -s English \
        -t German \
        --source-ext en \
        --target-ext de \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --edge-agent-strategy ${EDGE_AGENT_STRATEGY}
    
done

##############################
# GERMAN -> ENGLISH
##############################
for EDGE_AGENT_STRATEGY in "${EDGE_AGENT_STRATEGIES[@]}"; do
    python src/main.py \
        -i data/document_level/en-de/iwslt2017 \
        -o results/document_level/edge_agent_analysis/${EDGE_AGENT_STRATEGY}/de-en/iwslt2017 \
        -s German \
        -t English \
        --source-ext de \
        --target-ext en \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --edge-agent-strategy ${EDGE_AGENT_STRATEGY}
    
done

##############################
# ENGLISH -> FRENCH
##############################
for EDGE_AGENT_STRATEGY in "${EDGE_AGENT_STRATEGIES[@]}"; do
    python src/main.py \
        -i data/document_level/en-fr/iwslt2017 \
        -o results/document_level/edge_agent_analysis/${EDGE_AGENT_STRATEGY}/en-fr/iwslt2017 \
        -s English \
        -t French \
        --source-ext en \
        --target-ext fr \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --edge-agent-strategy ${EDGE_AGENT_STRATEGY}
    
done

##############################
# FRENCH -> ENGLISH
##############################
for EDGE_AGENT_STRATEGY in "${EDGE_AGENT_STRATEGIES[@]}"; do
    python src/main.py \
        -i data/document_level/en-fr/iwslt2017 \
        -o results/document_level/edge_agent_analysis/${EDGE_AGENT_STRATEGY}/fr-en/iwslt2017 \
        -s French \
        -t English \
        --source-ext fr \
        --target-ext en \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --edge-agent-strategy ${EDGE_AGENT_STRATEGY}
    
done

##############################
# ENGLISH -> JAPANESE
##############################
for EDGE_AGENT_STRATEGY in "${EDGE_AGENT_STRATEGIES[@]}"; do
    python src/main.py \
        -i data/document_level/en-ja/iwslt2017 \
        -o results/document_level/edge_agent_analysis/${EDGE_AGENT_STRATEGY}/en-ja/iwslt2017 \
        -s English \
        -t Japanese \
        --source-ext en \
        --target-ext ja \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --edge-agent-strategy ${EDGE_AGENT_STRATEGY}
    
done

##############################
# JAPANESE -> ENGLISH
##############################
for EDGE_AGENT_STRATEGY in "${EDGE_AGENT_STRATEGIES[@]}"; do
    python src/main.py \
        -i data/document_level/en-ja/iwslt2017 \
        -o results/document_level/edge_agent_analysis/${EDGE_AGENT_STRATEGY}/ja-en/iwslt2017 \
        -s Japanese \
        -t English \
        --source-ext ja \
        --target-ext en \
        -m ${MODEL_NAME} \
        -k ${KEY} \
        -p ${PORT} \
        --edge-agent-strategy ${EDGE_AGENT_STRATEGY}
    
done
