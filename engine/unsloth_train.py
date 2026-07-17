"""
========================================================================================
   👑 ABDULAZIZ AGENT v1.0 — GOOGLE COLAB FINE-TUNING SCRIPT (UNSLOTH + LoRA)
   Yaratuvchi: Otajonov Abdulaziz
   Vazifasi: Qwen-2.5-Coder-1.5B (yoki 7B) modelini bizning dataset/train_tool_use.jsonl
            asosida o'qitib, tayyor Abdulaziz-v1-Q4_K_M.gguf model qilib beradi!
========================================================================================

🔥 QANDAY ISHLATILADI (Google Colab'da 100% BEPUL):
1. https://colab.research.google.com ga kiring va yangi Notebook oching.
2. Tepadagi menyudan: Runtime -> Change runtime type -> T4 GPU ni tanlang.
3. Bu skript kodini Colab katagiga ko'chiring va ishga tushiring!
"""

import os
import torch

# 1. Unsloth va kerakli kutubxonalarni o'rnatish (Colab ichida ishlaydi)
if not os.path.exists("unsloth_installed"):
    print("📦 Unsloth va tezkor LoRA vositalari o'rnatilmoqda...")
    os.system("pip install --upgrade pip")
    os.system("pip install 'unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git'")
    os.system("pip install --no-deps trl peft accelerate bitsandbytes")
    open("unsloth_installed", "w").close()

from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# 2. Model va Tokenizerni yuklash (Qwen-2.5-Coder-1.5B - 8 GB RAM noutbuk uchun ideal)
max_seq_length = 2048
dtype = None # Auto detection
load_in_4bit = True # 4-bit kvantizatsiya (T4 GPU xotirasi uchun)

print("🧠 Asosiy model (Qwen-2.5-Coder-1.5B) yuklanmoqda...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# 3. LoRA parametrlarini sozlash (Sizning uslubingiz va aql-idrokingizni singdirish)
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Target rank
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0, # Optimized
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

# 4. Datasetni yuklash (Bizning train_tool_use.jsonl faylimiz)
dataset_path = "train_tool_use.jsonl"
if not os.path.exists(dataset_path):
    print(f"⚠️ {dataset_path} topilmadi. Iltimos D:\\3D AI\\Abdulaziz-Agent\\dataset\\train_tool_use.jsonl faylini Colab oynasiga yuklang!")
    exit()

print("📚 Dataset o'qilmoqda...")
dataset = load_dataset("json", data_files=dataset_path, split="train")

def format_prompt(examples):
    formatted = []
    for msgs in examples["messages"]:
        # ShareGPT / ChatML format
        text = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False)
        formatted.append(text)
    return {"text": formatted}

dataset = dataset.map(format_prompt, batched=True)

# 5. O'qitish jarayoni (`Fine-Tuning Loop`)
print("🔥 O'qitish (LoRA Fine-Tuning) boshlandi! bu taxminan 10-15 daqiqa davom etadi...")
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 60, # Yoki num_train_epochs = 3
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

trainer.train()

# 6. GGUF formatinga eksport qilish (Noutbukingizda Oflayn Ollama uchun tayyorlash)
print("💾 Model 'Abdulaziz-v1.gguf' formatiga eksport qilinmoqda...")
model.save_pretrained_gguf("Abdulaziz-v1", tokenizer, quantization_method = "q4_k_m")
print("🎉 TABRIKLAYMIZ! 'Abdulaziz-v1-Q4_K_M.gguf' fayli tayyor! Uni Colab'dan noutbukingizga yuklab oling va models/ papkasiga joylang!")
