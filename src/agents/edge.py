import os
from typing import List, Tuple

from openai import OpenAI
from jinja2 import Environment, FileSystemLoader

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EdgeAgent:
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
        self.user_prompt_template = env.get_template("edge_agent/user.jinja")

    def __call__(self, discourses: List[str]) -> List[Tuple[int, int]]:

        edges = list()

        for uid in range(len(discourses)):
            u_discourse = discourses[uid]
            if uid < len(discourses) - 1:
                edges.append((uid, uid + 1))

            for vid in range(uid + 2, len(discourses)):
                v_discourse = discourses[vid]

                try:
                    prompt = self.user_prompt_template.render(
                        discourse_1=u_discourse,
                        discourse_2=v_discourse,
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
                        edges.append((uid, vid))

                except Exception as e:
                    print(f"Error during segmentation: {e}")

        return edges


class EdgeAgentPredecessor:
    def __init__(
        self,
        source_lang: str,
        target_lang: str,
        language_pair: str,
    ) -> None:

        self.source_lang = source_lang
        self.target_lang = target_lang
        self.language_pair = language_pair

    def __call__(self, discourses: List[str]) -> List[Tuple[int, int]]:
        edges = list()
        for uid in range(len(discourses)):
            if uid < len(discourses) - 1:
                edges.append((uid, uid + 1))
        return edges


class EdgeAgentTfidf:
    def __init__(
        self,
        source_lang: str,
        target_lang: str,
        language_pair: str,
        threshold: float = 0.8,
        max_discourse_length: int = 2048,
    ) -> None:
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.language_pair = language_pair
        self.threshold = threshold
        self.max_discourse_length = max_discourse_length

    def __call__(self, discourses: List[str]) -> List[Tuple[int, int]]:
        edges = []

        vectorizer = TfidfVectorizer(max_features=self.max_discourse_length)
        tfidf_matrix = vectorizer.fit_transform(discourses)

        for u in range(len(discourses)):
            u_vec = tfidf_matrix[u]

            if u < len(discourses) - 1:
                edges.append((u, u + 1))

            for v in range(u + 2, len(discourses)):
                v_vec = tfidf_matrix[v]
                sim = cosine_similarity(u_vec, v_vec)[0][0]
                if sim >= self.threshold:
                    edges.append((u, v))

        return edges
