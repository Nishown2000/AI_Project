#!/bin/bash

git-lfs install
echo "lfs is intalled"

if [ -d "Laama_Lib" ]; then
    echo "Library already exists. If not delete Laama_Lib folder"
else
    git-lfs clone https://Nishown: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@huggingface.co/meta-llama/Llama-2-7b-chat-hf Laama_Lib
    echo "Laama_Lib Library is Downloaded"
fi

pip install torch torchvision torchaudio
echo "torch torchvision torchaudio is installed"

pip install tensorflow
echo "tensorflow is installed"

pip install flax
echo "flax is installed"

pip install --upgrade transformers
echo "transformers is upgraded"

pip install sentencepiece
echo "sentencepiece is installed"