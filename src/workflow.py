from tqdm import tqdm
from typing import List

from openai import OpenAI

from agents import (
    DiscourseAgent,
    DiscourseAgentSemanticChunker,
    DiscourseAgentRandom,
    EdgeAgent,
    EdgeAgentTfidf,
    EdgeAgentPredecessor,
    MemoryAgent,
    TranslationAgent,
)
from data import Instance, Discourse


def get_discourse_agent(
    discourse_agent_name: str,
    client: OpenAI,
    model_name: str,
    source_lang: str,
    target_lang: str,
    language_pair: str,
):
    discourse_agent = None
    if discourse_agent_name == "ours":
        discourse_agent = DiscourseAgent(
            client,
            model_name,
            source_lang,
            target_lang,
            language_pair,
        )
    elif discourse_agent_name == "semantic-chunker":
        discourse_agent = DiscourseAgentSemanticChunker(
            source_lang,
            target_lang,
            language_pair,
        )
    else:
        discourse_agent = DiscourseAgentRandom(
            source_lang,
            target_lang,
            language_pair,
        )
    return discourse_agent


def get_edge_agent(
    edge_agent_strategy: str,
    client: OpenAI,
    model_name: str,
    source_lang: str,
    target_lang: str,
    language_pair: str,
):
    edge_agent = None
    if edge_agent_strategy == "ours":
        edge_agent = EdgeAgent(
            client,
            model_name,
            source_lang,
            target_lang,
            language_pair,
        )
    elif edge_agent_strategy == "tfidf":
        edge_agent = EdgeAgentTfidf(
            source_lang,
            target_lang,
            language_pair,
        )
    else:
        edge_agent = EdgeAgentPredecessor(
            source_lang,
            target_lang,
            language_pair,
        )
    return edge_agent


def workflow(
    client: OpenAI,
    model_name: str,
    instance: Instance,
    source_lang: str,
    target_lang: str,
    language_pair: str,
    discourse_agent_name: str,
    edge_agent_strategy: str,
    memory_agent_strategy: str,
):

    discourse_agent = get_discourse_agent(
        discourse_agent_name,
        client=client,
        model_name=model_name,
        source_lang=source_lang,
        target_lang=target_lang,
        language_pair=language_pair,
    )

    edge_agent = get_edge_agent(
        edge_agent_strategy=edge_agent_strategy,
        client=client,
        model_name=model_name,
        source_lang=source_lang,
        target_lang=target_lang,
        language_pair=language_pair,
    )

    translation_agent = TranslationAgent(
        client,
        model_name,
        source_lang,
        target_lang,
        language_pair,
    )
    memory_agent = MemoryAgent(
        client,
        model_name,
        language_pair,
        memory_agent_strategy,
    )
    memory_agent.reset_memory()

    discourses = discourse_agent(instance.document_source_sentences)
    instance.discourses = [
        Discourse(
            source_txt=source_txt,
            target_txt=None,
            memory_incident=dict(),
            memory_local=dict(),
        )
        for source_txt in discourses
    ]
    edges = edge_agent([discourse.source_txt for discourse in instance.discourses])
    instance.edges = edges
    translations = list()
    for did, discourse in enumerate(instance.discourses):
        incident_nodes = [uid for uid, vid in instance.edges if vid == did]
        incident_memories = [
            instance.discourses[uid].memory_local for uid in incident_nodes
        ]
        discourse.memory_incident = memory_agent.get_incident_memory(incident_memories)
        translation = translation_agent.translate(
            discourse.source_txt,
            discourse.memory_incident,
        )
        translations.append(translation)
        discourse.target_txt = translation
        discourse.memory_local = memory_agent.get_local_memory(
            discourse.source_txt,
            discourse.target_txt,
        )
        memory_agent.reset_memory()

    instance.document_translation_output = " ".join(translations)
    return instance
