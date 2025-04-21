# Load the Model
import pandas as pd
from trl import SFTTrainer
from transformers import TrainingArguments
from peft import LoraConfig
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, load_in_4bit=True)


# Setup Dataset

file_path = "trainingdataset.tsv"
dataset_df = pd.read_csv(file_path, sep="\t")
dataset_df["text"] = "Input: " + dataset_df["input"] + "\nOutput: " + dataset_df["output"]

# print(dataset_df.head())

dataset = Dataset.from_pandas(dataset_df[["text"]])

# Configure LoRA
# TODO: Look into LoRA vs QLoRA or other alternatives
lora_config = LoraConfig(
    r=16,  # Rank of low-rank matrices
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"],  # Apply to attention layers
    bias="none",
    task_type="CAUSAL_LM"
)

model = model.get_peft_model(lora_config)

# Setup Training
training_args = TrainingArguments(
    output_dir="./fine_tuned_llama",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_dir="./logs",
)

# Supervised Fine Tuning
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer,
)
trainer.train()

# Save Everything
model.save_pretrained("./fine_tuned_llama")
tokenizer.save_pretrained("./fine_tuned_llama")
