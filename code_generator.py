import json
from LLM_Engine import call_llm

class CodeGenerator:
    """代码生成器，使用LLM生成代码"""
    
    CODE_GENERATION_PROMPT = """
    你是一位经验丰富的软件开发工程师，现在需要根据任务描述和架构设计生成高质量的代码。
    
    请遵循以下要求：
    1. 只返回可以运行的代码内容
    2. 代码应符合架构设计中指定的技术栈
    3. 代码应具有良好的结构和可读性
    4. 包含必要的错误处理和日志记录
    
    当前任务：{task_description}
    技术栈：{tech_stack}
    架构上下文：{architecture_context}
    """
    
    def __init__(self, architecture: dict):
        self.architecture = architecture
        self.tech_stack = architecture.get('tech_stack', {})
    
    def generate_code(self, task: dict) -> str:
        """生成代码"""
        try:
            # 准备提示词
            prompt = self._prepare_prompt(task)
            
            # 调用LLM引擎
            response = call_llm(
                prompt=prompt,
                system="你是一位专业的软件开发工程师，负责根据架构设计生成代码。",
                temperature=0.2  # 使用较低的温度值以获得更稳定的输出
            )
            
            return response
        except Exception as e:
            return f"# 代码生成失败: {str(e)}"
    
    def _prepare_prompt(self, task: dict) -> str:
        """根据任务准备提示词"""
        task_description = task.get('description', '')
        tech_stack_str = ", ".join(f"{k}: {v}" for k, v in self.tech_stack.items())
        
        # 根据任务类型添加上下文
        context = {
            'task_description': task_description,
            'tech_stack': tech_stack_str,
            'architecture_context': json.dumps(task, ensure_ascii=False)
        }
        
        return self.CODE_GENERATION_PROMPT.format(**context)