# requirement_analyzer.py
from LLM_Engine import call_llm
import json

SYSTEM_PROMPT = """你是一个需求分析师，负责从用户输入的需求中识别核心业务目标、功能模块、关键流程，并以json格式输出。

格式如下：
{
  "project_name": "程序命名",
  "description": "程序描述",
  "core_features": [
    "核心功能1",
    "核心功能2",
    "核心功能3"
  ],
  "optional_features": [
    "可选功能1",
    "可选功能2"
  ],
}"""

def analyze_requirements(user_input: str) -> dict:
    """分析用户需求并返回结构化结果"""
    try:
        # 调用LLM引擎
        response = call_llm(
            prompt=user_input,
            system=SYSTEM_PROMPT,
            json_output=True,
            temperature=0.3  # 降低temperature使输出更稳定
        )
        
        # 处理可能的错误响应
        if response.startswith("[ERROR]"):
            return {"error": response}
            
        # 尝试解析JSON
        return json.loads(response)
        
    except json.JSONDecodeError:
        return {"error": "响应格式无效，解析JSON失败"}
    except Exception as e:
        return {"error": f"分析过程异常: {str(e)}"}


if __name__ == "__main__":
    user_input = input("请输入您的需求描述: ")
    analysis = analyze_requirements(user_input)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))