import os
import ctranslate2
import sentencepiece as spm


# [Modify] Set paths to the CTranslate2 and SentencePiece models
ct_model_path = "ollama/src/nllb-200-3.3B-int8"
sp_model_path = "ollama/src/flores200_sacrebleu_tokenizer_spm.model"

device = "cuda"  # or "cpu"

# Load the source SentecePiece model
sp = spm.SentencePieceProcessor()
sp.load(sp_model_path)

translator = ctranslate2.Translator(ct_model_path, device)

# source_sents = ["Ntabwo ntekereza ko iyi modoka ishaje izagera hejuru yumusozi.",
#                 "Kanda iyi buto hanyuma umuryango ukingure",
#                 "Ngendahimana yashakaga ikaramu"
#                ]

source_sents = ["Could you please tell me the road to Hamelen"]

# Source and target langauge codes
src_lang = "eng_latn" # "kin_Latn"
tgt_lang = "deu_Latn"

beam_size = 4

source_sentences = [sent.strip() for sent in source_sents]
target_prefix = [[tgt_lang]] * len(source_sentences)

# Subword the source sentences
source_sents_subworded = sp.encode_as_pieces(source_sentences)
source_sents_subworded = [[src_lang] + sent + ["</s>"] for sent in source_sents_subworded]
print("First subworded source sentence:", source_sents_subworded[0], sep="\n")

# Translate the source sentences
translator = ctranslate2.Translator(ct_model_path, device=device)
translations_subworded = translator.translate_batch(
    source_sents_subworded, 
    batch_type="tokens", 
    max_batch_size=2024, 
    beam_size=beam_size, 
    target_prefix=target_prefix
)

translations_subworded = [translation.hypotheses[0] for translation in translations_subworded]
for translation in translations_subworded:
    if tgt_lang in translation:
        translation.remove(tgt_lang)

# Desubword the target sentences
translations = sp.decode(translations_subworded)

for translation in translations:
    print(translation)