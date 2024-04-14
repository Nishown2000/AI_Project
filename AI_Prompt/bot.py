from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "gg-hf/gemma-2b-it"
dtype = torch.bfloat16
access_token = "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"

# Initialize model without specifying device
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    token=access_token,
    torch_dtype=dtype,
)

# Set device to CUDA if available
torch.cuda.empty_cache()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#torch.cuda.set_memory_growth(device, True)

# Move model to device
model.to(device)

tokenizer = AutoTokenizer.from_pretrained(model_id, token=access_token)

chat = [
    {"role": "user", "content": "where is india"},
]
prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

input_ids = tokenizer(prompt, add_special_tokens=False, return_tensors="pt").to(device)
outputs = model.generate(input_ids, max_length=20)
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded_output)
