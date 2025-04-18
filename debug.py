import json
from Analyst import analyze_requirements, pretty_print_analysis
from Software_Architect import design_architecture, pretty_print_architecture
from Task_Scheduler import build_project

def test_full_workflow():
    # 测试用例1：简单的任务管理系统
    test_input_1 = """
    我需要开发一个个人任务管理系统，主要功能包括：
    1. 任务创建、编辑和删除
    2. 任务分类和标签
    3. 任务优先级设置
    4. 任务到期提醒
    """
    
    # 测试用例2：电商平台
    test_input_2 = """
    开发一个小型电商平台，要求包含：
    - 用户注册登录
    - 商品浏览和搜索
    - 购物车功能
    - 订单管理
    """
    
    # 选择测试用例
    user_input = test_input_1  # 可以切换为test_input_2测试不同场景
    
    print("="*50)
    print("🔍 开始需求分析阶段")
    print("="*50)
    analysis = analyze_requirements(user_input)
    pretty_print_analysis(analysis)
    
    if "error" in analysis:
        print("需求分析失败，终止流程")
        return
    
    # 模拟用户确认（在实际应用中应从用户获取）
    print("\n假设用户确认了分析结果，继续流程...\n")
    
    print("="*50)
    print("🏗️ 开始架构设计阶段")
    print("="*50)
    architecture = design_architecture(analysis)
    pretty_print_architecture(architecture)
    
    if "error" in architecture:
        print("架构设计失败，终止流程")
        return
    
    print("="*50)
    print("🚀 开始项目构建阶段")
    print("="*50)
    build_project(architecture)
    
    print("\n" + "="*50)
    print("✅ 全流程测试完成")
    print("="*50)

def debug_single_stage():
    """调试单个阶段（可选）"""
    # 可以直接在这里测试特定阶段的代码
    test_input = "我需要一个博客系统，支持文章发布和评论功能"
    
    # 测试需求分析
    analysis = analyze_requirements(test_input)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    # 测试架构设计
    if "error" not in analysis:
        architecture = design_architecture(analysis)
        print(json.dumps(architecture, indent=2, ensure_ascii=False))
    
    # 测试项目构建
    if "error" not in architecture:
        build_project(architecture)

if __name__ == "__main__":
    # 运行完整流程测试
    test_full_workflow()
    
    # 或者调试单个阶段
    # debug_single_stage()