#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙心 OS Hooks 集成
before_start: 每次对话前自动触发场景识别

版本：v1.0
创建：2026-04-17
"""

import sys
import io
import json
import os

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加框架路径
framework_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, framework_dir)

from core import DragonHeartOS


def before_start(input_text: str, context: dict = None) -> dict:
    """
    龙心 OS before_start hook
    每次对话前自动触发，感知上下文并识别场景
    
    Args:
        input_text: 用户输入文本
        context: 上下文信息
        
    Returns:
        dict: 调度结果
    """
    try:
        # 初始化龙心 OS
        os = DragonHeartOS()
        
        # 处理输入
        result = os.process(input_text, context)
        
        # 输出调度结果
        output = {
            'hook': 'before_start',
            'success': True,
            'scene_code': result['scene']['scene_code'],
            'scene_name': result['scene']['scene_name'],
            'engines': result['route']['engines'],
            'route_type': result['route']['route_type'],
            'confidence': result['scene']['confidence'],
            'dispatch_mode': result['dispatch']['mode'],
            'dispatch_action': result['dispatch']['action'],
            'reasoning': result['route']['reasoning'],
            'timestamp': result['timestamp']
        }
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return output
        
    except Exception as e:
        error_output = {
            'hook': 'before_start',
            'success': False,
            'error': str(e),
            'fallback': 'S0',
            'fallback_engine': '人机协同五象限'
        }
        print(json.dumps(error_output, ensure_ascii=False, indent=2))
        return error_output


def after_complete(result: dict, feedback: str = None) -> dict:
    """
    龙心 OS after_complete hook
    对话完成后记录反馈
    
    Args:
        result: 执行结果
        feedback: 用户反馈
        
    Returns:
        dict: 反馈记录结果
    """
    try:
        os = DragonHeartOS()
        
        # 记录反馈
        if feedback:
            os.learner.log_feedback(
                result.get('scene_code', 'S0'),
                result.get('engines', []),
                feedback,
                f"执行结果：{result}"
            )
        
        output = {
            'hook': 'after_complete',
            'success': True,
            'feedback_recorded': feedback is not None,
            'timestamp': result.get('timestamp', 'unknown')
        }
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return output
        
    except Exception as e:
        error_output = {
            'hook': 'after_complete',
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_output, ensure_ascii=False, indent=2))
        return error_output


def on_error(error: str, context: dict = None) -> dict:
    """
    龙心 OS on_error hook
    错误时记录并降级
    
    Args:
        error: 错误信息
        context: 上下文信息
        
    Returns:
        dict: 错误处理结果
    """
    try:
        os = DragonHeartOS()
        
        # 记录错误
        os.learner.log_feedback(
            'S9',  # 系统进化场景
            ['龙心 OS'],
            'negative',
            f"错误：{error}"
        )
        
        output = {
            'hook': 'on_error',
            'success': True,
            'error_logged': True,
            'fallback': 'S0',
            'fallback_engine': '人机协同五象限',
            'error': error
        }
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return output
        
    except Exception as e:
        error_output = {
            'hook': 'on_error',
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_output, ensure_ascii=False, indent=2))
        return error_output


def main():
    """测试 hooks"""
    print("=" * 70)
    print("龙心 OS Hooks 测试")
    print("=" * 70)
    
    # 测试 before_start
    print("\n1. 测试 before_start hook")
    print("-" * 70)
    result = before_start("如何把超级个体概念落地实施？")
    
    # 测试 after_complete
    print("\n2. 测试 after_complete hook")
    print("-" * 70)
    after_complete(result, 'positive')
    
    # 测试 on_error
    print("\n3. 测试 on_error hook")
    print("-" * 70)
    on_error("测试错误")
    
    # 获取状态
    print("\n4. 获取龙心 OS 状态")
    print("-" * 70)
    os = DragonHeartOS()
    status = os.get_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
