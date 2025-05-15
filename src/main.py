import os
import re
import json
import argparse
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

from openai import OpenAI

from workflow import workflow
from data import load_data, save_data, Instance


def translate_document(
    instance: Instance,
    source_lang: str,
    target_lang: str,
    source_ext: str,
    target_ext: str,
    client: dict,
    model_name: str,
    discourse_agent_name: str = "ours",
    edge_agent_strategy: str = "ours",
    memory_agent_strategy: str = "ours",
) -> None:
    client = OpenAI(
        base_url=client["base_url"],
        api_key=client["api_key"],
    )
    instance = workflow(
        client,
        model_name,
        instance,
        source_lang,
        target_lang,
        f"{source_ext}-{target_ext}",
        discourse_agent_name,
        edge_agent_strategy,
        memory_agent_strategy,
    )
    return instance


def process_files(
    input_path: str,
    output_path: str,
    source_lang: str = "Chinese",
    target_lang: str = "English",
    source_ext: str = "zh",
    target_ext: str = "en",
    model_name: str = "qwen2.5-7b-instruct",
    api_key: str = "pRt87ruBLVV443l",
    port: int = 8000,
    discourse_agent_name: str = "ours",
    edge_agent_strategy: str = "ours",
    memory_agent_strategy: str = "ours",
):
    mp.set_start_method("spawn", force=True)
    instances = load_data(
        input_path,
        source_lang,
        target_lang,
        source_ext,
        target_ext,
    )

    partial_process = partial(
        translate_document,
        source_lang=source_lang,
        target_lang=target_lang,
        source_ext=source_ext,
        target_ext=target_ext,
        client={
            "base_url": f"http://localhost:{port}/v1",
            "api_key": api_key,
        },
        model_name=model_name,
        discourse_agent_name=discourse_agent_name,
        edge_agent_strategy=edge_agent_strategy,
        memory_agent_strategy=memory_agent_strategy,
    )

    processed_instances = []
    with mp.Pool(processes=min(8, mp.cpu_count())) as pool:
        pbar = tqdm(total=len(instances))
        for processed_instance in pool.imap_unordered(partial_process, instances):
            processed_instances.append(processed_instance)
            pbar.update()

    save_data(output_path, processed_instances)


def main():
    parser = argparse.ArgumentParser(description="Batch Translation Pipeline")
    parser.add_argument(
        "-i",
        "--input-path",
        type=str,
        help="Path to the input folder",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        type=str,
        help="Path to the output folder",
    )
    parser.add_argument(
        "-s",
        "--source-lang",
        type=str,
        help="Source language",
        default="Chinese",
    )
    parser.add_argument(
        "-t",
        "--target-lang",
        type=str,
        help="Target language",
        default="English",
    )
    parser.add_argument(
        "--source-ext",
        type=str,
        help="Source file extension",
        default="zh",
    )
    parser.add_argument(
        "--target-ext",
        type=str,
        help="Target file extension",
        default="en",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Port number for the client",
    )
    parser.add_argument(
        "-m",
        "--model-name",
        type=str,
        help="Model name to call",
        default="qwen2.5-7b-instruct",
    )
    parser.add_argument(
        "-k",
        "--api-key",
        type=str,
        help="API key for model server",
        default="pRt87ruBLVV443l",
    )
    parser.add_argument(
        "--discourse-agent-name",
        type=str,
        help="Choose between the discourse agents: ours, semantic-chunker, random",
        choices=[
            "ours",
            "semantic-chunker",
            "random",
        ],
        default="ours",
    )
    parser.add_argument(
        "--edge-agent-strategy",
        type=str,
        help="Choose between the edge strategy: ours, only-predecessor, tfidf",
        choices=[
            "ours",
            "only-predecessor",
            "tfidf",
        ],
        default="ours",
    )
    parser.add_argument(
        "--memory-agent-strategy",
        type=str,
        help="Choose between the memory strategy: ours, none",
        choices=[
            "ours",
            "wo-noun-pronoun",
            "wo-entity-entity",
            "wo-connectives",
            "wo-phrase-translation",
            "wo-summary",
            "wo-context-summary",
            "none",
        ],
        default="ours",
    )

    args = parser.parse_args()

    process_files(
        args.input_path,
        args.output_path,
        args.source_lang,
        args.target_lang,
        args.source_ext,
        args.target_ext,
        args.model_name,
        args.api_key,
        args.port,
        args.discourse_agent_name,
        args.edge_agent_strategy,
        args.memory_agent_strategy,
    )


if __name__ == "__main__":
    main()
