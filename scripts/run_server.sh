#!/bin/bash

# Default values
CUDA_DEVICES="-1"
PORT="7070"
MODEL_PATH="../../models/qwen2.5-7b-instruct/"
MODEL_NAME="qwen2.5-7b-instruct"

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --cuda-devices)
            CUDA_DEVICES="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --model-path)
            MODEL_PATH="$2"
            shift 2
            ;;
        --model-name)
            MODEL_NAME="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done


# Set CUDA_VISIBLE_DEVICES based on input
if [ "$CUDA_DEVICES" = "-1" ]; then
    CUDA_VISIBLE_DEVICES=""
else
    CUDA_VISIBLE_DEVICES="$CUDA_DEVICES"
fi

# Calculate tensor parallel size based on the number of CUDA devices
if [ -n "$CUDA_VISIBLE_DEVICES" ]; then
    TENSOR_PARALLEL_SIZE=$(echo "$CUDA_VISIBLE_DEVICES" | tr ',' '\n' | wc -l)
else
    TENSOR_PARALLEL_SIZE=1
fi

# Resolve model path relative to the script's directory if it's not absolute
if [[ "$MODEL_PATH" != /* ]]; then
    MODEL_PATH="$MODEL_PATH"
fi

# Run the command
CUDA_VISIBLE_DEVICES="$CUDA_VISIBLE_DEVICES" python -u -m vllm.entrypoints.openai.api_server \
    --distributed-executor-backend mp \
    --disable-custom-all-reduce \
    --host 0.0.0.0 \
    --port "$PORT" \
    --model "$MODEL_PATH" \
    --served-model-name "$MODEL_NAME" \
    --tensor-parallel-size "$TENSOR_PARALLEL_SIZE" \
    --load-format safetensors \
    --api-key pRt87ruBLVV443l
