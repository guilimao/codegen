import os
import json
import queue
from datetime import datetime
from Code_Generator import CodeGenerator

class ProjectBuilder:
    """根据架构设计构建项目结构和文件"""
    
    def __init__(self, architecture: dict):
        self.architecture = architecture
        self.project_name = architecture.get('project_name', 'untitled_project')  
        self.base_dir = os.path.join(os.getcwd(), self.project_name)
        self.created_dirs = set()
        
    def _ensure_dir_exists(self, *path_parts):
        """确保目录存在，如果不存在则创建"""
        dir_path = os.path.join(self.base_dir, *path_parts)
        if dir_path not in self.created_dirs:
            os.makedirs(dir_path, exist_ok=True)
            self.created_dirs.add(dir_path)
        return dir_path
    
    def create_project_structure(self):
        """根据架构设计创建基础项目结构"""
        try:
            # 创建主要目录
            self._ensure_dir_exists('src')
            self._ensure_dir_exists('src', 'frontend')
            self._ensure_dir_exists('src', 'backend')
            self._ensure_dir_exists('src', 'database')
            self._ensure_dir_exists('tests')
            self._ensure_dir_exists('docs')
            self._ensure_dir_exists('config')
            
            # 创建模块目录
            for module in self.architecture.get('modules', []):
                module_name = module.get('name', '').lower().replace(' ', '_')
                self._ensure_dir_exists('src', 'backend', module_name)
                
            # 创建架构文档
            self._create_architecture_doc()
            
            return True
        except Exception as e:
            print(f"创建项目结构时出错: {str(e)}")
            return False
    
    def _create_architecture_doc(self):
        """创建架构设计文档"""
        doc_path = os.path.join(self.base_dir, 'docs', 'architecture.md')
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(f"# {self.project_name} 架构设计文档\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 技术栈
            f.write("## 技术栈\n")
            tech_stack = self.architecture.get('tech_stack', {})
            for key, value in tech_stack.items():
                f.write(f"- {key}: {value}\n")
            
            # 模块
            f.write("\n## 系统模块\n")
            for module in self.architecture.get('modules', []):
                f.write(f"\n### {module.get('name', '')}\n")
                f.write(f"{module.get('description', '')}\n")
                f.write("\n**接口:**\n")
                for interface in module.get('interfaces', []):
                    f.write(f"- {interface.get('method', '')} {interface.get('endpoint', '')}: {interface.get('description', '')}\n")
            
            # 数据模型
            f.write("\n## 数据模型\n")
            for model in self.architecture.get('data_models', []):
                f.write(f"\n### {model.get('name', '')}\n")
                for field in model.get('fields', []):
                    f.write(f"- {field.get('name', '')} ({field.get('type', '')}): {field.get('description', '')}\n")

class TaskScheduler:
    """任务调度器，管理代码生成任务队列"""
    
    def __init__(self, architecture: dict):
        self.architecture = architecture
        self.task_queue = queue.Queue()
        self.code_generator = CodeGenerator(architecture)
        self._init_tasks()
        
    def _init_tasks(self):
        """根据架构设计初始化任务队列"""
        # 添加前端框架初始化任务
        frontend_tech = self.architecture.get('tech_stack', {}).get('frontend', '')
        if frontend_tech:
            self.task_queue.put({
                'type': 'frontend_init',
                'tech': frontend_tech,
                'description': f'初始化{frontend_tech}前端项目'
            })
        
        # 添加后端框架初始化任务
        backend_tech = self.architecture.get('tech_stack', {}).get('backend', '')
        if backend_tech:
            self.task_queue.put({
                'type': 'backend_init',
                'tech': backend_tech,
                'description': f'初始化{backend_tech}后端项目'
            })
        
        # 为每个模块添加代码生成任务
        for module in self.architecture.get('modules', []):
            module_name = module.get('name', '')
            self.task_queue.put({
                'type': 'module',
                'module_name': module_name,
                'description': f'为{module_name}模块生成代码',
                'interfaces': module.get('interfaces', [])
            })
        
        # 为每个数据模型添加代码生成任务
        for model in self.architecture.get('data_models', []):
            model_name = model.get('name', '')
            self.task_queue.put({
                'type': 'data_model',
                'model_name': model_name,
                'description': f'为{model_name}数据模型生成代码',
                'fields': model.get('fields', [])
            })
    
    def get_next_task(self):
        """获取下一个任务"""
        if not self.task_queue.empty():
            return self.task_queue.get()
        return None
    
    def has_tasks(self):
        """检查是否还有任务"""
        return not self.task_queue.empty()
    
    def process_task(self, task: dict, project_name: str) -> bool:
        """处理单个任务"""
        print(f"\n🔄 正在处理任务: {task.get('description', '')}")
        
        # 生成代码
        code = self.code_generator.generate_code(task)
        
        # 保存代码到文件
        file_path = self._determine_file_path(task, project_name)
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                print(f"✅ 代码已保存到: {file_path}")
                return True
            except Exception as e:
                print(f"❌ 保存文件失败: {str(e)}")
                return False
        return False
    
    def _determine_file_path(self, task: dict, project_name: str) -> str:
        """根据任务类型确定文件保存路径"""
        base_dir = os.path.join(os.getcwd(), project_name)
        
        if task['type'] == 'frontend_init':
            return os.path.join(base_dir, 'src', 'frontend', 'app.js')
        elif task['type'] == 'backend_init':
            return os.path.join(base_dir, 'src', 'backend', 'main.py')
        elif task['type'] == 'module':
            module_name = task['module_name'].lower().replace(' ', '_')
            return os.path.join(base_dir, 'src', 'backend', module_name, f'{module_name}.py')
        elif task['type'] == 'data_model':
            model_name = task['model_name'].lower().replace(' ', '_')
            return os.path.join(base_dir, 'src', 'database', 'models', f'{model_name}.py')
        else:
            return None

def build_project(architecture: dict):
    """主函数：构建整个项目"""
    # 1. 创建项目结构
    builder = ProjectBuilder(architecture)
    if not builder.create_project_structure():
        print("❌ 项目结构创建失败")
        return
    
    print("✅ 项目结构创建完成")
    
    # 2. 初始化任务调度器
    scheduler = TaskScheduler(architecture)
    
    # 3. 处理任务队列
    while scheduler.has_tasks():
        task = scheduler.get_next_task()
        scheduler.process_task(task, builder.project_name)

if __name__ == "__main__":
    # 示例用法
    from Software_Architect import design_architecture
    
    # 模拟架构设计输入
    sample_architecture = {
        "project_name": "TaskManagementSystem",
        "tech_stack": {
            "frontend": "React",
            "backend": "Python Flask",
            "database": "PostgreSQL",
            "communication": "REST API",
            "infrastructure": "Docker"
        },
        "modules": [
            {
                "name": "User Management",
                "description": "处理用户注册、登录和权限管理",
                "interfaces": [
                    {
                        "name": "register",
                        "method": "POST",
                        "endpoint": "/api/users/register",
                        "description": "注册新用户"
                    }
                ]
            }
        ],
        "data_models": [
            {
                "name": "User",
                "fields": [
                    {
                        "name": "id",
                        "type": "Integer",
                        "description": "用户唯一标识"
                    }
                ]
            }
        ]
    }
    
    # 构建项目
    build_project(sample_architecture)