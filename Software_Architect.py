from LLM_Engine import call_llm
import json

ARCHITECTURE_PROMPT = """
你是一位经验丰富的软件系统架构师，现在你需要根据一份结构化的功能需求，输出一个完整的软件系统架构设计。

请以JSON 格式输出以下内容：
{
  "project_name": "项目名称",
  "tech_stack": {
    "frontend": "前端技术,
    "backend": "后端技术",
    "database": "数据库",
    "communication": "模块之间通信协议",
    "infrastructure": "部署平台"
  },
  "modules": [
    {
      "name": "模块名称",
      "description": "模块职责说明",
      "interfaces": [
        {
          "name": "接口名称",
          "method": "GET/POST/PUT/DELETE",
          "endpoint": "URL 或接口路径",
          "description": "接口功能简要说明"
        }
      ]
    }
  ]
}
"""

def design_architecture(structured_requirements: dict) -> dict:
    """根据结构化需求设计系统架构"""
    try:
        # 将结构化需求转换为字符串作为提示
        requirements_str = json.dumps(structured_requirements, ensure_ascii=False)
        
        # 调用LLM引擎
        response = call_llm(
            prompt=requirements_str,
            system=ARCHITECTURE_PROMPT,
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
        return {"error": f"架构设计过程异常: {str(e)}"}

def pretty_print_architecture(result: dict):
    """美化输出架构设计结果"""
    if "error" in result:
        print(f"❌ 错误信息: {result['error']}")
        return
        
    print("\n🏗️ 架构设计结果:")
    print(f"项目名称: {result.get('project_name', '')}")
    
    print("\n🛠️ 技术栈:")
    tech_stack = result.get('tech_stack', {})
    print(f"前端: {tech_stack.get('frontend', '')}")
    print(f"后端: {tech_stack.get('backend', '')}")
    print(f"数据库: {tech_stack.get('database', '')}")
    print(f"通信协议: {tech_stack.get('communication', '')}")
    print(f"基础设施: {tech_stack.get('infrastructure', '')}")
    
    print("\n📦 系统模块:")
    for module in result.get('modules', []):
        print(f"\n模块名称: {module.get('name', '')}")
        print(f"模块描述: {module.get('description', '')}")
        print("接口:")
        for interface in module.get('interfaces', []):
            print(f"  {interface.get('method', '')} {interface.get('endpoint', '')} - {interface.get('description', '')}")

if __name__ == "__main__":
    # 示例用法
    from Analyst import analyze_requirements
    
    user_input = input("请输入您的需求描述: ")
    analysis = analyze_requirements(user_input)
    
    if "error" not in analysis:
        architecture = design_architecture(analysis)
        pretty_print_architecture(architecture)
    else:
        print("需求分析失败，无法进行架构设计")