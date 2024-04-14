#!/bin/bash

git-lfs install
echo "lfs is intalled"

if [ -d "Gemma_Lib" ]; then
    echo "Library already exists. If not delete Gemma_Lib folder"
else
    git-lfs clone https://Nishown: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@huggingface.co/google/gemma-1.1-2b-it Gemma_Lib
    echo "Gemma_Lib Library is Downloaded"
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