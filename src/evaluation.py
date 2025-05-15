import json
from pathlib import Path
from typing import List, Dict, Any
import re

import sacrebleu
from bert_score import score as bert_score
from comet import download_model, load_from_checkpoint
import nltk
from tqdm import tqdm

COMET_CHECKPOINT = "Unbabel/wmt22-comet-da"
COMET_MODEL_PATH = download_model(COMET_CHECKPOINT)
COMET_MODEL = load_from_checkpoint(COMET_MODEL_PATH)

TOKENIZER_BY_LANG = {
    "de": "13a",
    "fr": "13a",
    "zh": "zh",
    "ja": "ja-mecab",
    "en": "13a",
}

LANGUAGE_PAIRS = {
    ("en", "de"),
    ("en", "fr"),
    ("en", "zh"),
    ("en", "ja"),
    ("de", "en"),
    ("fr", "en"),
    ("zh", "en"),
    ("ja", "en"),
}

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


def load_document(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def split_text_into_sentences(text: str, lang: str, n: int) -> List[str]:
    text = text.strip()
    if lang in ("zh", "ja"):
        parts = re.split(r"(?<=[。！？!?])", text)
        parts = [p.strip() for p in parts if p.strip()]
    else:
        lang_map = {"en": "english", "de": "german", "fr": "french"}
        nltk_lang = lang_map.get(lang, "english")
        parts = nltk.sent_tokenize(text, language=nltk_lang)
    if len(parts) >= n:
        return parts[:n]
    if parts:
        return parts + [parts[-1]] * (n - len(parts))
    return [""] * n


def compute_doc_bleu(system: str, reference: str, target_lang: str) -> float:
    tokenizer = TOKENIZER_BY_LANG[target_lang]
    return sacrebleu.corpus_bleu([system], [[reference]], tokenize=tokenizer).score


def compute_average_sentence_bleu(
    systems: List[str], references: List[str], target_lang: str
) -> float:
    tokenizer = TOKENIZER_BY_LANG[target_lang]
    total = 0.0
    for sys_s, ref_s in zip(systems, references):
        total += sacrebleu.sentence_bleu(sys_s, [ref_s], tokenize=tokenizer).score
    return total / len(systems) if systems else 0.0


def compute_doc_ter(system: str, reference: str, target_lang: str) -> float:
    tokenizer = TOKENIZER_BY_LANG[target_lang]
    return sacrebleu.corpus_ter(
        [system],
        [[reference]],
        asian_support=True if target_lang in ["zh", "ja"] else False,
        normalized=True,
    ).score


def compute_ter(systems: List[str], references: List[str], target_lang: str) -> float:
    tokenizer = TOKENIZER_BY_LANG[target_lang]
    return sacrebleu.corpus_ter(
        systems,
        [references],
        asian_support=True if target_lang in ["zh", "ja"] else False,
        normalized=True,
    ).score


def compute_doc_bert_score_doc(system: str, reference: str, target_lang: str) -> float:
    P, R, F1 = bert_score(
        [system], [reference], lang=target_lang, rescale_with_baseline=True
    )
    return float(F1.mean())


def compute_bert_score(
    systems: List[str], references: List[str], target_lang: str
) -> float:
    P, R, F1 = bert_score(
        systems, references, lang=target_lang, rescale_with_baseline=True
    )
    return float(F1.mean())


def compute_doc_comet_doc(doc_src: str, system: str, reference: str) -> float:
    data = [{"src": doc_src, "mt": system, "ref": reference}]
    scores = COMET_MODEL.predict(data, batch_size=1, gpus=1)
    sc = scores["scores"] if isinstance(scores, dict) else scores
    return float(sc[0]) if sc else 0.0


def compute_comet(systems: List[str], references: List[str], doc_src: str) -> float:
    data = [
        {"src": doc_src, "mt": mt, "ref": ref} for mt, ref in zip(systems, references)
    ]
    scores = COMET_MODEL.predict(data, batch_size=8, gpus=1)
    sc = scores["scores"] if isinstance(scores, dict) else scores
    return float(sum(sc) / len(sc)) if sc else 0.0


def evaluate_document(path: Path) -> Dict[str, Any]:
    doc = load_document(path)
    pair = (doc.get("source_ext"), doc.get("target_ext"))
    if pair not in LANGUAGE_PAIRS:
        print(f"Skipping unsupported pair: {pair} in file {path.name}")
        return {}
    tgt_lang = pair[1]
    print(f"Evaluating document {path.name} with language pair {pair}")

    sys_doc = doc.get("document_translation_output", "")
    ref_doc = doc.get("document_reference_translation", "")

    doc_bleu = compute_doc_bleu(sys_doc, ref_doc, tgt_lang)
    doc_ter = compute_doc_ter(sys_doc, ref_doc, tgt_lang)
    doc_bert = compute_doc_bert_score_doc(sys_doc, ref_doc, tgt_lang)
    doc_comet = compute_doc_comet_doc(doc.get("document_source", ""), sys_doc, ref_doc)

    src_sents = doc.get("document_source_sentences", [])
    n = len(src_sents)
    sent_sys = split_text_into_sentences(sys_doc, tgt_lang, n)
    sent_ref = split_text_into_sentences(ref_doc, tgt_lang, n)

    sbleu = compute_average_sentence_bleu(sent_sys, sent_ref, tgt_lang)
    ster = compute_ter(sent_sys, sent_ref, tgt_lang)
    sbert = compute_bert_score(sent_sys, sent_ref, tgt_lang)
    scomet = compute_comet(sent_sys, sent_ref, doc.get("document_source", ""))

    return {
        "file": path.name,
        "docBLEU": doc_bleu,
        "docTER": doc_ter,
        "docBERTScore_F1": doc_bert,
        "docCOMET": doc_comet,
        "sBLEU": sbleu,
        "sTER": ster,
        "sBERTScore_F1": sbert,
        "sCOMET": scomet,
    }


def evaluate_folder(folder: str) -> None:
    folder = Path(folder)
    json_files = [f for f in folder.glob("*.json") if f.name != "results.json"]
    print(f"Found {len(json_files)} JSON files to evaluate in '{folder}'")
    results = []

    for f in tqdm(json_files, desc="Evaluating files", unit="file"):
        res = evaluate_document(f)
        if res:
            results.append(res)

    if not results:
        print("No valid results to aggregate.")
        return

    keys = [k for k in results[0] if k != "file"]
    avg = {k: sum(r[k] for r in results) / len(results) for k in keys}
    summary = {"average": avg, "files": results}

    out_path = folder / "results.json"
    with open(out_path, "w", encoding="utf-8") as wf:
        json.dump(summary, wf, ensure_ascii=False, indent=2)
    print(f"Results saved to {out_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate translation outputs in a folder."
    )
    parser.add_argument(
        "--input_folder", required=True, help="Path to folder with JSON outputs."
    )
    args = parser.parse_args()
    evaluate_folder(args.input_folder)
