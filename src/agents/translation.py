import os
import json
from typing import Dict

from openai import OpenAI
from jinja2 import Environment, FileSystemLoader


class TranslationAgent:
    def __init__(
        self,
        client: OpenAI,
        model_name: str,
        source_lang: str,
        target_lang: str,
        language_pair: str,
    ) -> None:
        self.client = client
        self.model_name = model_name
        self.source_lang = source_lang
        self.target_lang = target_lang
        env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), f"../prompts/{language_pair}")
            )
        )
        self.system_prompt_template = env.get_template("translation_agent/system.jinja")
        self.user_prompt_template = env.get_template("translation_agent/user.jinja")

    def translate(self, discourse: str, memory: Dict[str, str]) -> str:
        system_prompt = self.system_prompt_template.render(
            source_lang=self.source_lang,
            target_lang=self.target_lang,
            include_examples=True,
        )
        prompt = self.user_prompt_template.render(
            incident_memory=json.dumps(memory, indent=2, ensure_ascii=False),
            source_discourse=discourse,
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=4096,
                temperature=0.1,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error during translation: {e}")
            return ""
