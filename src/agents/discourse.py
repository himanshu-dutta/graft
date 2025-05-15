import os
import random
from typing import List

from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


class DiscourseAgent:
    def __init__(
        self,
        client: OpenAI,
        model_name: str,
        source_lang: str,
        target_lang: str,
        language_pair: str,
        max_discourse_length: int = 2048,
    ) -> None:
        self.client = client
        self.model_name = model_name
        self.max_discourse_length = max_discourse_length
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.language_pair = language_pair
        env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), f"../prompts/{language_pair}")
            )
        )
        self.system_prompt_template = env.get_template("discourse_agent/system.jinja")
        self.user_prompt_template = env.get_template("discourse_agent/user.jinja")

    def get_sentences(self, document: str) -> List[str]:
        import re

        return [
            s
            for s in re.findall(r"[^!?。\.\!\?]+[!?。\.\!\?]?", document, flags=re.U)
            if s.strip()
        ]

    def __call__(self, document_sentences: List[str]) -> List[str]:
        sentences = document_sentences
        discourses = []

        curr_sent_idx = 0
        while curr_sent_idx < len(sentences):
            discourse = [sentences[curr_sent_idx]]
            discourse_end_idx = curr_sent_idx + 1

            while discourse_end_idx < len(sentences):
                try:
                    prompt = self.user_prompt_template.render(
                        discourse=" ".join(discourse),
                        next_sentence=sentences[discourse_end_idx],
                    )
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                        max_tokens=1,
                        temperature=0,
                    )
                    include_sentence = (
                        response.choices[0].message.content.strip().lower()
                    )
                    if include_sentence == "yes":
                        discourse.append(sentences[discourse_end_idx])
                        discourse_end_idx += 1
                    else:
                        break
                except Exception as e:
                    print(f"Error during segmentation: {e}")
                    break

            discourses.append(" ".join(discourse))
            curr_sent_idx = discourse_end_idx
        return discourses


class DiscourseAgentNoop:
    def __init__(
        self,
        source_lang: str,
        target_lang: str,
        language_pair: str,
        max_discourse_length: int = 2048,
    ) -> None:
        self.max_discourse_length = max_discourse_length
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.language_pair = language_pair

    def random_contiguous_sublists(
        self, lst: List[str], factor: int = 1 / 3
    ) -> List[str]:
        n = len(lst)
        max_sublists = max(1, int(n * factor))
        num_sublists = random.randint(1, max_sublists)

        split_points = sorted(random.sample(range(1, n), num_sublists - 1))

        sublists = []
        prev = 0
        for point in split_points:
            sublists.append(lst[prev:point])
            prev = point
        sublists.append(lst[prev:])

        return sublists

    def __call__(self, document_sentences: List[str]) -> List[str]:
        return document_sentences


class DiscourseAgentRandom:
    def __init__(
        self,
        source_lang: str,
        target_lang: str,
        language_pair: str,
        max_discourse_length: int = 2048,
    ) -> None:
        self.max_discourse_length = max_discourse_length
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.language_pair = language_pair

    def random_contiguous_sublists(
        self, lst: List[str], factor: int = 1 / 3
    ) -> List[str]:
        n = len(lst)
        max_sublists = max(1, int(n * factor))
        num_sublists = random.randint(1, max_sublists)

        split_points = sorted(random.sample(range(1, n), num_sublists - 1))

        sublists = []
        prev = 0
        for point in split_points:
            sublists.append(lst[prev:point])
            prev = point
        sublists.append(lst[prev:])

        return sublists

    def __call__(self, document_sentences: List[str]) -> List[str]:
        sentences = document_sentences
        return " ".join(self.random_contiguous_sublists(sentences))


class DiscourseAgentSemanticChunker:
    def __init__(
        self,
        source_lang: str,
        target_lang: str,
        language_pair: str,
        max_discourse_length: int = 2048,
    ) -> None:
        self.max_discourse_length = max_discourse_length
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.language_pair = language_pair
        source_ext = language_pair.split("-")[0]
        if source_ext in ["zh", "ja"]:
            sentence_split_regex = r"(?<=[\u3002\uff01\uff1f])"
        else:
            sentence_split_regex = r"(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])$"
        self.text_splitter = SemanticChunker(
            HuggingFaceEmbeddings(),
            sentence_split_regex=sentence_split_regex,
        )

    def __call__(self, document_sentences: List[str]) -> List[str]:
        sentences = document_sentences
        document = " ".join(sentences)
        discourses = [
            doc.page_content for doc in self.text_splitter.create_documents([document])
        ]
        return discourses
