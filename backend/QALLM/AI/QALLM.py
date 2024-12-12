import google.generativeai as genai
import os
from openai import OpenAI
from huggingface_hub import login
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig 
from transformers import pipeline
client = OpenAI(api_key="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")

os.environ["GOOGLE_API_KEY"] = "AIzaSyBwRi6f7aoxXxpwy5RhOThn0cOOV9_zI50"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
gemini_model = genai.GenerativeModel("models/gemini-1.5-pro")

API_TOKEN = "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"
login(token=API_TOKEN)

model_id = "meta-llama/Llama-3.2-3B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id, token=True, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, token=True, trust_remote_code=True)

def gemini(prompt, model = gemini_model):
    response = model.generate_content(prompt).text.strip()
    return(response)

def chatgpt(prompt, client = client):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    return(response)

def llama(prompt):
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype="auto",
        device_map="auto",
    )
    
    messages = [{"role": "user", "content": prompt}]
    
    outputs = pipe(messages, max_new_tokens=256)
    
    response = outputs[0]["generated_text"][-1]['content']
    return response
  
#zero-shot prompt
def zero_shot_prompt(context, question):
  prompt = f"""
    Read the following text and answer the question below. The answer must be within the paragraph and be one continuous phrase or keyword, not separated, without explanation or additional information outside the paragraph.   
    Văn bản:
    {context}
    
    Câu hỏi:
    {question}
    
    Trả lời:
  """
  return(prompt)

#one-shot prompt
def one_shot_prompt(context, question):
  prompt = f"""
    Read the following text and answer the question below. The answer must be within the paragraph and be one continuous phrase or keyword, not separated, without explanation or additional information outside the paragraph.   

    Ví dụ:
    Văn bản: "Albert Einstein là nhà vật lý nổi tiếng với thuyết tương đối."
    Câu hỏi: "Ai là người phát triển thuyết tương đối?"
    Trả lời: "Albert Einstein"
    
    Văn bản:
    {context}
    
    Câu hỏi:
    {question}
    
    Trả lời:
  """
  return(prompt)
    
#few_shot prompt
def few_shot_prompt(context, question):
  prompt = f"""
    Read the following text and answer the question below. The answer must be within the paragraph and be one continuous phrase or keyword, not separated, without explanation or additional information outside the paragraph.   
    
    Ví dụ:
    Văn bản: "Albert Einstein là nhà vật lý nổi tiếng với thuyết tương đối."
    Câu hỏi: "Ai là người phát triển thuyết tương đối?"
    Trả lời: "Albert Einstein"
    
    Văn bản: "Kháng sinh được dùng để điều trị các bệnh nhiễm trùng do vi khuẩn gây ra."
    Câu hỏi: "Kháng sinh dùng để điều trị cái gì?"
    Trả lời: "nhiễm trùng do vi khuẩn"
    
    Văn bản: "Isaac Newton đã phát hiện ra định luật vạn vật hấp dẫn vào thế kỷ 17."
    Câu hỏi: "Định luật vạn vật hấp dẫn được phát hiện vào thời kỳ nào?"
    Trả lời: "thế kỷ 17"
    
    Văn bản: "Paris là thủ đô của Pháp và là một trung tâm văn hóa lớn."
    Câu hỏi: "Paris là thủ đô của quốc gia nào?"
    Trả lời: "Pháp"
    
    Văn bản: "Con người khám phá ra lửa có thể được tạo ra bằng cách đánh đá vào nhau vì nó tạo ra tia lửa."
    Câu hỏi: "Tại sao lửa có thể được tạo ra khi đánh đá vào nhau?"
    Trả lời: "tạo ra tia lửa"
    
    Văn bản: "Việc xây dựng cây cầu mất 5 năm do địa hình phức tạp và thời tiết xấu."
    Câu hỏi: "Việc xây dựng cây cầu mất bao lâu?"
    Trả lời: "5 năm"
    
    Văn bản:
    {context}
    
    Câu hỏi:
    {question}
    
    Trả lời:
  """
  return(prompt)

#chain_of_thought prompt
def chain_of_thought_prompt(context, question):
  prompt = f"""
    Read the following context and answer the question below. Follow these steps to ensure accuracy:

    1. Read and fully understand the provided context.
    2. Identify the sentence or sentences in the context that may contain the answer to the question.
    3. Analyze the sentence(s) to confirm the exact information that answers the question.
    4. Provide the exact phrase or continuous keyword from the sentence(s) that answers the question, ensuring the answer is unbroken and directly addresses the question.
    5. Ensure no additional explanation or words are included outside of the exact phrase.
    Văn bản:
    {context}
    
    Câu hỏi:
    {question}
    
    Trả lời:
  """
  return(prompt)

def infer(source, technique_prompt, context, question):
  if technique_prompt == "zero-shot":
    prompt = zero_shot_prompt(context, question)
  elif technique_prompt == "one-shot":
    prompt = one_shot_prompt(context, question)
  elif technique_prompt == "few-shot":
    prompt = few_shot_prompt(context, question)
  elif technique_prompt == "chain-of-thought":
    prompt = chain_of_thought_prompt(context, question)
    
  if source == "gemini-1.5-pro":
    answer = gemini(prompt)
  if source == "gpt-4.o-mini":
    answer = chatgpt(prompt)
  if source == "llama-3.2-3b-instruct":
    answer = llama(prompt)
  return answer