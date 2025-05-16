# TCO-Dataset Evaluation Script

This repository contains an **example Python script** for evaluating multimodal large language models (MLLMs) on the TCO-Dataset, a bilingual benchmark for traditional Chinese opera image understanding.

## 📌 About the Script

File: `evaluate_tco_dataset.py`

This script:
- Loads image-question-answer triplets from local files.
- Sends each image and question to a vision-language model (e.g., OpenAI GPT-4o).
- Receives model output and compares it with the ground truth.
- Saves a summary report of all predictions.

⚠️ This is a simplified **example** for academic/research use. It assumes:
- All data files (`.png`, `.md`, `.txt`) are located in the same folder.
- Model access is via OpenAI API.

---

## 💻 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Fill in your API credentials in the script:

```python
client = OpenAI(api_key="your-api-key", base_url="https://api.openai.com/v1")
```

Update the data path and output path in the last two lines of the script:

```python
data_folder = "your_data_directory"
output_path = "results.txt"
```

Run the script:

```bash
python evaluate_tco_dataset.py
```

## 📦 Output

- A `.txt` file with prediction results.
- Terminal logs showing whether each answer is correct.

## 📝 Notes

- The model should respond with a single choice letter (A/B/C/D).
- This script uses base64-encoded image input and expects UTF-8 or GBK encoding.
- This is not a full benchmark runner; it is for demonstration purposes only.

# TCO-Dataset
