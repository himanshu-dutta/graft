import re
import os
import json

from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
from typing import List, Dict, Any


class MemoryAgent:
    def __init__(
        self,
        client: OpenAI,
        model_name: str,
        language_pair: str,
        memory_mode: str = "ours",
    ) -> None:
        self.client = client
        self.model_name = model_name
        self.memory_mode = memory_mode

        # include context_summary
        all_keys = {
            "target_noun_target_pronoun_mapping",
            "source_entity_target_entity_mapping",
            "discourse_connectives",
            "source_phrase_target_phrase_mapping",
            "translation_summary",
            "context_summary",
        }

        mode_to_disable = {
            "ours": set(),
            "wo-noun-pronoun": {"target_noun_target_pronoun_mapping"},
            "wo-entity-entity": {"source_entity_target_entity_mapping"},
            "wo-connectives": {"discourse_connectives"},
            "wo-phrase-translation": {"source_phrase_target_phrase_mapping"},
            "wo-summary": {"translation_summary"},
            "wo-context-summary": {"context_summary"},
            "none": all_keys.copy(),
        }
        if memory_mode not in mode_to_disable:
            raise ValueError(f"Unknown memory_mode: {memory_mode}")
        self.disabled_keys = mode_to_disable[memory_mode]

        env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), f"../prompts/{language_pair}")
            )
        )
        self.discourse_connectives_prompt = env.get_template(
            "memory_agent/discourse_connectives.jinja"
        )
        self.source_entity_target_entity_prompt = env.get_template(
            "memory_agent/source_entity_target_entity.jinja"
        )
        self.target_noun_target_pronoun_prompt = env.get_template(
            "memory_agent/target_noun_target_pronoun.jinja"
        )
        self.source_phrase_target_phrase_prompt = env.get_template(
            "memory_agent/source_phrase_target_phrase.jinja"
        )
        self.translation_summary_prompt = env.get_template(
            "memory_agent/translation_summary.jinja"
        )
        self.context_summary_prompt = env.get_template(
            "memory_agent/context_summary.jinja"
        )

    def reset_memory(self) -> None:
        self.memory = dict()

    def parse_noun_pronoun_map(self, output: str):
        lines = [
            l.strip()
            for l in output.splitlines()
            if l.strip() and l.strip() != "(none)"
        ]
        return dict(line.split(":", 1) for line in lines)

    def parse_entity_map(self, output: str):
        lines = [
            l.strip()
            for l in output.splitlines()
            if l.strip() and l.strip() != "(none)"
        ]
        return dict(line.split(":", 1) for line in lines)

    def parse_connective(self, output: str):
        c = output.strip()
        return "" if c == "(none)" else c

    def parse_phrase_map(self, output: str):
        lines = [
            l.strip()
            for l in output.splitlines()
            if l.strip() and l.strip() != "(none)"
        ]
        return dict(line.split(":", 1) for line in lines)

    def parse_summary(self, output: str):
        s = output.strip()
        return "" if s == "(none)" else s

    def parse_context_summary(self, output: str):
        s = output.strip()
        return "" if s == "(none)" else s

    def get_local_memory(self, discourse: str, translation: str) -> dict:
        local_memory = {
            "target_noun_target_pronoun_mapping": {},
            "source_entity_target_entity_mapping": {},
            "source_phrase_target_phrase_mapping": {},
            "discourse_connectives": "",
            "translation_summary": "",
            "context_summary": "",
        }

        # target_noun_target_pronoun_mapping
        target_noun_target_pronoun_prompt = (
            self.target_noun_target_pronoun_prompt.render(
                source_discourse=discourse,
                target_discourse=translation,
            )
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": target_noun_target_pronoun_prompt},
                ],
                max_tokens=8192,
                temperature=0,
            )
            response = response.choices[0].message.content.strip()
            local_memory["target_noun_target_pronoun_mapping"] = (
                self.parse_noun_pronoun_map(response)
            )
        except Exception as e:
            pass

        # source_entity_target_entity_mapping
        source_entity_target_entity_prompt = (
            self.source_entity_target_entity_prompt.render(
                source_discourse=discourse,
                target_discourse=translation,
            )
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": source_entity_target_entity_prompt},
                ],
                max_tokens=8192,
                temperature=0,
            )
            response = response.choices[0].message.content.strip()
            local_memory["source_entity_target_entity_mapping"] = self.parse_entity_map(
                response
            )
        except Exception as e:
            pass

        # discourse_connectives
        discourse_connectives_prompt = self.discourse_connectives_prompt.render(
            source_discourse=discourse,
            target_discourse=translation,
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": discourse_connectives_prompt},
                ],
                max_tokens=8192,
                temperature=0,
            )
            response = response.choices[0].message.content.strip()
            local_memory["discourse_connectives"] = self.parse_connective(response)
        except Exception as e:
            pass

        # source_phrase_target_phrase_mapping
        source_phrase_target_phrase_prompt = (
            self.source_phrase_target_phrase_prompt.render(
                source_discourse=discourse,
                target_discourse=translation,
            )
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": source_phrase_target_phrase_prompt},
                ],
                max_tokens=8192,
                temperature=0,
            )
            response = response.choices[0].message.content.strip()
            local_memory["source_phrase_target_phrase_mapping"] = self.parse_phrase_map(
                response
            )
        except Exception as e:
            pass

        # translation_summary
        translation_summary_prompt = self.translation_summary_prompt.render(
            source_discourse=discourse,
            target_discourse=translation,
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": translation_summary_prompt},
                ],
                max_tokens=8192,
                temperature=0,
            )
            response = response.choices[0].message.content.strip()
            local_memory["translation_summary"] = self.parse_summary(response)
        except Exception as e:
            pass

        # context_summary
        ctx_prompt = self.context_summary_prompt.render(
            source_discourse=discourse,
            target_discourse=translation,
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": ctx_prompt}],
                max_tokens=8192,
                temperature=0,
            )
            local_memory["context_summary"] = self.parse_context_summary(
                response.choices[0].message.content.strip()
            )
        except Exception:
            pass

        for key in self.disabled_keys:
            if key in (
                "target_noun_target_pronoun_mapping",
                "source_entity_target_entity_mapping",
                "source_phrase_target_phrase_mapping",
            ):
                local_memory[key] = {}
            else:
                local_memory[key] = ""
        return local_memory

    def get_incident_memory(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        combined = {
            "target_noun_target_pronoun_mapping": {},
            "source_entity_target_entity_mapping": {},
            "discourse_connectives": "",
            "source_phrase_target_phrase_mapping": {},
            "translation_summary": "",
            "context_summary": "",
        }

        summaries = []
        contexts = []
        for mem in memories:
            combined["target_noun_target_pronoun_mapping"].update(
                mem.get("target_noun_target_pronoun_mapping", {})
            )
            combined["source_entity_target_entity_mapping"].update(
                mem.get("source_entity_target_entity_mapping", {})
            )
            combined["source_phrase_target_phrase_mapping"].update(
                mem.get("source_phrase_target_phrase_mapping", {})
            )
            combined["discourse_connectives"] = mem.get("discourse_connectives", "")
            summary = mem.get("translation_summary", "").strip()
            if summary:
                summaries.append(summary)
            context = mem.get("context_summary", "").strip()
            if context:
                contexts.append(context)
        combined["translation_summary"] = " ".join(summaries) or "(none)"
        combined["context_summary"] = " ".join(contexts) or "(none)"

        for key in self.disabled_keys:
            if key in (
                "target_noun_target_pronoun_mapping",
                "source_entity_target_entity_mapping",
                "source_phrase_target_phrase_mapping",
            ):
                combined[key] = {}
            elif key in ("discourse_connectives",):
                combined[key] = ""
            else:
                combined[key] = "(none)"
        return combined

    def encode_memory(self, memory: Dict[str, Any]) -> str:
        """
        Encode the combined memory into a string suited for LLM consumption.
        """
        lines = []
        # noun-pronoun map
        lines.append("Target noun→pronoun mappings:")
        if memory["target_noun_target_pronoun_mapping"]:
            for noun, pron in memory["target_noun_target_pronoun_mapping"].items():
                lines.append(f"- {noun} → {pron}")
        else:
            lines.append("- (none)")
        # entity map
        lines.append("Source entity→target entity mappings:")
        if memory["source_entity_target_entity_mapping"]:
            for src, tgt in memory["source_entity_target_entity_mapping"].items():
                lines.append(f"- {src} → {tgt}")
        else:
            lines.append("- (none)")
        # connectives
        lines.append("Discourse connectives at end of connected discourses:")
        if memory["discourse_connectives"]:
            for conn in memory["discourse_connectives"]:
                lines.append(f"- {conn}")
        else:
            lines.append("- (none)")
        # phrase map
        lines.append("Source phrase→target phrase mappings:")
        if memory["source_phrase_target_phrase_mapping"]:
            for src, tgt in memory["source_phrase_target_phrase_mapping"].items():
                lines.append(f"- {src} → {tgt}")
        else:
            lines.append("- (none)")
        # summary
        lines.append("Combined translation summary:")
        lines.append(memory["translation_summary"])
        # context summary
        lines.append("Combined discourse context summary:")
        lines.append(memory["context_summary"] or "(none)")

        return "\n".join(lines)
