from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "lmsys/fastchat-t5-3b-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# User input
user_input = "what is dog"

# Tokenize the input
input_ids = tokenizer.encode(user_input, return_tensors="pt")

# Generate response
output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)

# Decode and print the response
response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)
