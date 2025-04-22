from openai import OpenAI
import os

# 设置你的 OpenAI API key（推荐用环境变量）
DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def call_llm(prompt: str, system:str = " ",json_output:bool = False,model: str = "deepseek-chat", temperature: float = 0.7) -> str:
    try:
        print("LLM调用中")
        if json_output:
            response = client.chat.completions.create(
              model=model,
              messages=[
                  {"role": "system", "content": system},
                  {"role": "user", "content": prompt}
              ],
              temperature=temperature,
              response_format={
                  'type': 'json_object'
              }
            )
        else:
            response = client.chat.completions.create(
              model=model,
              messages=[
                  {"role": "system", "content": system},
                  {"role": "user", "content": prompt}
              ],
              temperature=temperature,
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] 模型调用失败：{str(e)}"


if __name__ == "__main__":
    task = "请用 Python 写一个快速排序的函数。"
    reply = call_llm(task)
    print("模型回复：\n", reply)
