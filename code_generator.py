# main.py
from Software_Architect import design_architecture
from Project_Builder import ProjectBuilder
from Task_Scheduler import TaskScheduler

def build_project(architecture: Dict):
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
        print(f"\n🔄 正在处理任务: {task.get('description', '')}")
        
        # 生成代码
        code = scheduler.generate_code_for_task(task)
        
        # 保存代码到文件
        file_path = builder.get_file_path_for_task(task)
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                print(f"✅ 代码已保存到: {file_path}")
            except Exception as e:
                print(f"❌ 保存文件失败: {str(e)}")

if __name__ == "__main__":
    # 示例用法
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