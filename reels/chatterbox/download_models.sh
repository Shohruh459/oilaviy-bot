#!/bin/bash
cd "$(dirname "$0")"
H=https://huggingface.co
for f in ve.safetensors t3_cfg.safetensors s3gen.safetensors conds.pt; do
  [ -s pretrained_models/$f ] || curl -sS -L --retry 3 -o pretrained_models/$f "$H/ResembleAI/chatterbox/resolve/main/$f?download=true"; echo "got $f $(stat -c %s pretrained_models/$f)"
done
curl -sS -L -o pretrained_models/tokenizer.json "$H/ResembleAI/chatterbox/resolve/main/grapheme_mtl_merged_expanded_v1.json?download=true"; echo "got tokenizer $(stat -c %s pretrained_models/tokenizer.json)"
for f in t3_finetuned_merged.safetensors reference_voice.wav inference.py TRAINING.md; do
  curl -sS -L --retry 3 -o uz_abd/$f "$H/Abduqayum/uzbek-tts-natural-speech-chatterbox/resolve/main/$f?download=true"; echo "got abd/$f $(stat -c %s uz_abd/$f)"
done
for f in adapter_model.safetensors adapter_config.json scripts/uz_normalize.py docs/pip_freeze.txt; do
  mkdir -p uz_uaz/$(dirname $f); curl -sS -L --retry 3 -o uz_uaz/$f "$H/UAzimov/Uzbek-tts-chatterbox/resolve/main/$f?download=true"; echo "got uaz/$f $(stat -c %s uz_uaz/$f)"
done
echo DL_DONE
