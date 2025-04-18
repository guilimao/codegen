# task_scheduler.py
import os
import json
from typing import List, Dict
from LLM_Engine import call_llm

TASK_PROMPT_TEMPLATE = """
你是一位资深软件开发工程师，现在需要根据以下任务说明和架构设计实现具体的代码模块。

架构设计摘要:
{architecture_summary}

任务详情:
{task_description}

请严格按照以下要求输出代码:
1. 只返回代码内容，不要包含任何解释或注释
2. 确保代码符合架构设计中指定的技术栈
3. 代码应该完整可运行，包含必要的导入和依赖
4. 文件路径: {file_path}
"""

class TaskScheduler:
    def __init__(self, architecture: dict):
        self.architecture = architecture
        self.task_queue = []
        self.generated_files = []
        
    def create_project_structure(self):
        """根据架构设计创建基础项目结构"""
        project_name = self.architecture.get('project_name', 'my_project')
        
        try:
            # 创建项目根目录
            os.makedirs(project_name, exist_ok=True)
            
            # 根据技术栈创建基本目录结构
            tech_stack = self.architecture.get('tech_stack', {})
            
            if tech_stack.get('frontend'):
                os.makedirs(f"{project_name}/frontend/src", exist_ok=True)
                
            if tech_stack.get('backend'):
                os.makedirs(f"{project_name}/backend", exist_ok=True)
                
            if tech_stack.get('database'):
                os.makedirs(f"{project_name}/models", exist_ok=True)
                
            # 创建配置文件
            with open(f"{project_name}/README.md", 'w') as f:
                f.write(f"# {project_name}\n\n## 技术栈\n")
                for k, v in tech_stack.items():
                    f.write(f"- {k}: {v}\n")
            
            self.generated_files.append(f"创建项目目录结构: {project_name}/")
            return True
            
        except Exception as e:
            print(f"创建项目结构失败: {str(e)}")
            return False
    
    def build_task_queue(self):
        """根据架构设计构建任务队列"""
        self.task_queue = []
        
        # 添加模块开发任务
        for module in self.architecture.get('modules', []):
            task = {
                'type': 'module_implementation',
                'module_name': module.get('name'),
                'description': f"实现 {module.get('name')} 模块: {module.get('description')}",
                'interfaces': module.get('interfaces', []),
                'file_path': self._get_module_file_path(module.get('name'))
            }
            self.task_queue.append(task)
        
        # 添加数据模型任务
        for model in self.architecture.get('data_models', []):
            task = {
                'type': 'data_model',
                'model_name': model.get('name'),
                'description': f"实现 {model.get('name')} 数据模型",
                'fields': model.get('fields', []),
                'file_path': self._get_model_file_path(model.get('name'))
            }
            self.task_queue.append(task)
        
        # 添加配置文件任务
        config_task = {
            'type': 'config_files',
            'description': "生成项目配置文件",
            'tech_stack': self.architecture.get('tech_stack', {}),
            'file_paths': self._get_config_file_paths()
        }
        self.task_queue.append(config_task)
        
        return len(self.task_queue)
    
    def execute_tasks(self):
        """执行任务队列中的所有任务"""
        if not self.task_queue:
            print("任务队列为空，请先构建任务队列")
            return
            
        for task in self.task_queue:
            try:
                if task['type'] == 'module_implementation':
                    self._generate_module(task)
                elif task['type'] == 'data_model':
                    self._generate_data_model(task)
                elif task['type'] == 'config_files':
                    self._generate_config_files(task)
                    
            except Exception as e:
                print(f"执行任务失败: {task.get('description')} - 错误: {str(e)}")
    
    def _generate_module(self, task: Dict):
        """生成模块代码"""
        architecture_summary = {
            'tech_stack': self.architecture.get('tech_stack'),
            'module_description': {
                'name': task['module_name'],
                'interfaces': task['interfaces']
            }
        }
        
        prompt = TASK_PROMPT_TEMPLATE.format(
            architecture_summary=json.dumps(architecture_summary, indent=2),
            task_description=task['description'],
            file_path=task['file_path']
        )
        
        code = call_llm(
            prompt=prompt,
            system="你是一位资深软件开发工程师，专注于编写高质量、可维护的代码。",
            temperature=0.2
        )
        
        self._write_file(task['file_path'], code)
        self.generated_files.append(f"生成模块: {task['file_path']}")
    
    def _generate_data_model(self, task: Dict):
        """生成数据模型代码"""
        architecture_summary = {
            'tech_stack': self.architecture.get('tech_stack'),
            'model_description': {
                'name': task['model_name'],
                'fields': task['fields']
            }
        }
        
        prompt = TASK_PROMPT_TEMPLATE.format(
            architecture_summary=json.dumps(architecture_summary, indent=2),
            task_description=task['description'],
            file_path=task['file_path']
        )
        
        code = call_llm(
            prompt=prompt,
            system="你是一位资深软件开发工程师，专注于数据模型设计和实现。",
            temperature=0.2
        )
        
        self._write_file(task['file_path'], code)
        self.generated_files.append(f"生成数据模型: {task['file_path']}")
    
    def _generate_config_files(self, task: Dict):
        """生成配置文件"""
        tech_stack = task['tech_stack']
        
        # 生成 package.json 如果使用 Node.js
        if tech_stack.get('backend') == 'Node.js' or tech_stack.get('frontend') == 'React':
            content = {
                "name": self.architecture.get('project_name', 'my_project'),
                "version": "1.0.0",
                "description": "",
                "main": "index.js",
                "scripts": {
                    "start": "node backend/server.js"
                },
                "dependencies": {
                    "express": "^4.18.2" if tech_stack.get('backend') == 'Node.js' else "",
                    "react": "^18.2.0" if tech_stack.get('frontend') == 'React' else ""
                }
            }
            
            file_path = f"{self.architecture.get('project_name', 'my_project')}/package.json"
            self._write_file(file_path, json.dumps(content, indent=2))
            self.generated_files.append(f"生成配置文件: {file_path}")
    
    def _write_file(self, file_path: str, content: str):
        """将内容写入文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    def _get_module_file_path(self, module_name: str) -> str:
        """根据模块名获取文件路径"""
        tech_stack = self.architecture.get('tech_stack', {})
        project_name = self.architecture.get('project_name', 'my_project')
        
        if tech_stack.get('backend') == 'Node.js':
            return f"{project_name}/backend/{module_name.lower()}.js"
        elif tech_stack.get('backend') == 'Django':
            return f"{project_name}/backend/{module_name.lower()}/views.py"
        else:
            return f"{project_name}/backend/{module_name.lower()}.py"
    
    def _get_model_file_path(self, model_name: str) -> str:
        """根据模型名获取文件路径"""
        tech_stack = self.architecture.get('tech_stack', {})
        project_name = self.architecture.get('project_name', 'my_project')
        
        if tech_stack.get('database') == 'MongoDB':
            return f"{project_name}/models/{model_name.lower()}_schema.js"
        elif tech_stack.get('database') == 'PostgreSQL':
            return f"{project_name}/models/{model_name.lower()}.py"
        else:
            return f"{project_name}/models/{model_name.lower()}.py"
    
    def _get_config_file_paths(self) -> List[str]:
        """获取配置文件路径列表"""
        tech_stack = self.architecture.get('tech_stack', {})
        project_name = self.architecture.get('project_name', 'my_project')
        paths = []
        
        if tech_stack.get('infrastructure') == 'Docker':
            paths.append(f"{project_name}/Dockerfile")
        if tech_stack.get('infrastructure') == 'Kubernetes':
            paths.append(f"{project_name}/k8s-deployment.yaml")
        
        return paths

    def print_summary(self):
        """打印生成结果摘要"""
        print("\n📋 任务执行结果:")
        print(f"总任务数: {len(self.task_queue)}")
        print(f"生成文件数: {len(self.generated_files)}")
        print("\n生成的文件列表:")
        for file in self.generated_files:
            print(f"- {file}")


if __name__ == "__main__":
    # 示例用法
    from Software_Architect import design_architecture
    
    # 模拟架构设计输入
    sample_architecture = {
        "project_name": "ecommerce_platform",
        "tech_stack": {
            "frontend": "React",
            "backend": "Node.js",
            "database": "MongoDB",
            "communication": "REST API",
            "infrastructure": "Docker"
        },
        "modules": [
            {
                "name": "Product",
                "description": "商品管理模块",
                "interfaces": [
                    {
                        "name": "getProducts",
                        "method": "GET",
                        "endpoint": "/api/products",
                        "description": "获取商品列表"
                    }
                ]
            }
        ],
        "data_models": [
            {
                "name": "Product",
                "fields": [
                    {
                        "name": "name",
                        "type": "string",
                        "description": "商品名称"
                    },
                    {
                        "name": "price",
                        "type": "number",
                        "description": "商品价格"
                    }
                ]
            }
        ]
    }
    
    # 创建任务调度器
    scheduler = TaskScheduler(sample_architecture)
    
    # 创建项目结构
    if scheduler.create_project_structure():
        # 构建任务队列
        task_count = scheduler.build_task_queue()
        print(f"构建了 {task_count} 个任务")
        
        # 执行任务
        scheduler.execute_tasks()
        
        # 打印结果
        scheduler.print_summary()