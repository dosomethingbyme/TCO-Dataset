import os
import base64
from openai import OpenAI
from llama_index.core.llms import ChatMessage


def encode_image(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def process_data(folder_path, output_file):
    TRUEDATA = 0
    FALSEDATA = 0
    client = OpenAI(api_key="", base_url="")
    results = []


    data_files = set(f.split('.')[0] for f in os.listdir(folder_path))
    print("data_files:", data_files, "data_files_length:", len(data_files))

    for data_id in sorted(data_files, key=int, reverse=False):
        md_file = os.path.join(folder_path, f"{data_id}.md")
        txt_file = os.path.join(folder_path, f"{data_id}.txt")
        img_file = os.path.join(folder_path, f"{data_id}.png")


        with open(md_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) < 5:
            print(f"文件 {md_file} 内容不足，跳过。")
            continue

        question = lines[0].strip()
        options = {"A": lines[1].strip(), "B": lines[2].strip(), "C": lines[3].strip(), "D": lines[4].strip()}
        image_base64 = encode_image(img_file)

        with open(txt_file, "r", encoding="utf-8") as f:
            correct_answer = f.read().strip().upper()

        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "根据下面这张图片回答这个选择题："f"{question}\nA: {options['A']}\nB: {options['B']}\nC: {options['C']}\nD: {options['D']}\n请仅回答正确选项的字母(A、B、C 或 D),不允许有其他任何内容。"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}",
                        }
                    },
                ],
            }
            # ChatMessage(role="assistant", content="A"),
        ]

        response = client.chat.completions.create(
            model="llama3.2-vision",
            messages=message,
            max_tokens=10, 
            temperature=0,

        )
        print("response.choices[0]:", response.choices[0])
        model_answer = response.choices[0].message.content.strip(".").upper()

        if model_answer not in options:
            model_answer = "无效回答"

        correctness = "回答正确" if model_answer == correct_answer else "回答错误"
        if model_answer == correct_answer:
            TRUEDATA += 1
        else:
            FALSEDATA += 1


        result_line = f"问题{data_id}：大模型选择{model_answer}，正确答案{correct_answer}，{correctness}。"
        results.append(result_line)
        print(result_line)
        print("===========================================================")


    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(f"测试完成，结果已保存至 {output_file}")
    print(f"正确案例： {TRUEDATA}, 错误案例： {FALSEDATA}")



data_folder = ""  
output_path = ""
process_data(data_folder, output_path)
