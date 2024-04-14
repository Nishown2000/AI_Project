from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

model_id = "gg-hf/gemma-2b-it"
dtype = torch.bfloat16
access_token = "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"

pwd = os.getcwd()
model_path = os.path.join(pwd, "Gemma_Lib")

tokenizer = AutoTokenizer.from_pretrained(model_path, token=access_token)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    token=access_token,
    torch_dtype=dtype,
)

chat = [
    {"role": "user", "content": "where is india"},
]
prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

input_ids = tokenizer(prompt, add_special_tokens=False, return_tensors="pt")
outputs = model.generate(**input_ids, max_new_tokens=50)
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Extract only the model's answer
model_answer = decoded_output.split('\n')[-1].strip()

print(model_answer)