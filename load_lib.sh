#!/bin/bash

git-lfs install
echo "lfs is intalled"

if [ -d "FastChat_Lib" ]; then
    echo "Library already exists. If not delete FastChat_Lib folder"
else
    GIT_LFS_SKIP_SMUDGE=1 git-lfs clone https://huggingface.co/lmsys/fastchat-t5-3b-v1.0 FastChat_Lib
    echo "FastChat Library is Downloaded"
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