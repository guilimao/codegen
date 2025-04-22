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
  "technical_constraints": [
    "优先使用某某技术",
    "尽量避免外部依赖"
  ],
  "questions_for_user": [
    "用自然语言简单描述上述结果",
    "对可能的改进，简短询问用户意见"
  ]
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

def pretty_print_analysis(result: dict):
    """美化输出分析结果"""
    if "error" in result:
        print(f"❌ 错误信息: {result['error']}")
        return
        
    print("\n🔍 需求分析结果:")
    print(f"项目名称: {result.get('project_name', '')}")
    print(f"项目描述: {result.get('description', '')}")
    
    print("\n🌟 核心功能:")
    for i, feature in enumerate(result.get('core_features', []), 1):
        print(f"{i}. {feature}")
    
    print("\n📦 可选功能:")
    for i, feature in enumerate(result.get('optional_features', []), 1):
        print(f"{i}. {feature}")
    
    print("\n⚙️ 技术约束:")
    for i, constraint in enumerate(result.get('technical_constraints', []), 1):
        print(f"{i}. {constraint}")
    
    print("\n❓ 需要确认的问题:")
    for i, question in enumerate(result.get('questions_for_user', []), 1):
        print(f"{i}. {question}")

if __name__ == "__main__":
    user_input = input("请输入您的需求描述: ")
    analysis = analyze_requirements(user_input)
    pretty_print_analysis(analysis)