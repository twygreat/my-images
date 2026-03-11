#!/usr/bin/env python3
"""
GitHub 图床上传脚本
用于上传图片到 GitHub 仓库并返回可访问的 URL
"""

import os
import sys
import base64
import subprocess
import time
from datetime import datetime
from pathlib import Path

# 配置
GITHUB_USER = "twygreat"
REPO_NAME = "my-images"
DEFAULT_BRANCH = "main"

# 分类目录映射
CATEGORIES = {
    "xiaohongshu": "小红书",
    "wechat": "微信公众号",
    "weibo": "微博",
    "blog": "博客",
    "other": "其他"
}

def get_repo_path():
    """获取仓库本地路径"""
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(workspace, 'my-images')

def upload_to_github(image_path, category):
    """上传图片到 GitHub"""
    
    # 验证分类
    if category not in CATEGORIES:
        print(f"❌ 无效的分类: {category}")
        print(f"可选分类: {', '.join(CATEGORIES.keys())}")
        return None
    
    # 验证文件
    if not os.path.exists(image_path):
        print(f"❌ 文件不存在: {image_path}")
        return None
    
    # 获取文件名（添加时间戳避免重复）
    ext = os.path.splitext(image_path)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}{ext}"
    
    # 月份文件夹（如 2026-03）
    month_folder = datetime.now().strftime("%Y-%m")
    
    # 仓库路径
    repo_path = get_repo_path()
    category_path = os.path.join(repo_path, category, month_folder)
    
    # 创建月份文件夹
    os.makedirs(category_path, exist_ok=True)
    
    dest_path = os.path.join(category_path, filename)
    
    # 复制文件
    import shutil
    shutil.copy2(image_path, dest_path)
    
    print(f"📁 复制到: {category}/{filename}")
    
    # Git 操作
    os.chdir(repo_path)
    
    # 配置 git（如果需要）
    subprocess.run(["git", "config", "user.name", "OpenClaw"], capture_output=True)
    subprocess.run(["git", "config", "user.email", "openclaw@local"], capture_output=True)
    
    # 添加文件
    subprocess.run(["git", "add", "."], capture_output=True)
    
    # 提交
    commit_msg = f"Upload image to {category}"
    subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
    
    # 推送
    result = subprocess.run(["git", "push", "origin", DEFAULT_BRANCH], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"⚠️ 推送中...")
        # 等待一下再推送
        time.sleep(1)
        subprocess.run(["git", "push", "-u", "origin", DEFAULT_BRANCH], capture_output=True)
    
    # 生成 URL（包含月份文件夹）
    image_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{DEFAULT_BRANCH}/{category}/{month_folder}/{filename}"
    
    return image_url

def main():
    if len(sys.argv) < 2:
        print("📖 GitHub 图床上传工具")
        print("")
        print("用法: python upload_image.py <图片路径> [分类]")
        print("")
        print("可选分类:")
        for key, name in CATEGORIES.items():
            print(f"  {key:<15} - {name}")
        print("")
        print("示例:")
        print("  python upload_image.py photo.jpg xiaohongshu")
        print("  python upload_image.py C:\\images\\pic.png wechat")
        sys.exit(0)
    
    image_path = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else "other"
    
    print(f"📤 上传图片...")
    print(f"   文件: {image_path}")
    print(f"   分类: {category} ({CATEGORIES.get(category, '未知')})")
    print("")
    
    url = upload_to_github(image_path, category)
    
    if url:
        print("")
        print("✅ 上传成功！")
        print("")
        print(f"🔗 图片 URL:")
        print(f"   {url}")
        print("")
        print("📋 Markdown 格式:")
        print(f"   ![image]({url})")
        print("")
        print("📋 小红书使用:")
        print(f"   python xhs_client.py publish \"标题\" \"内容\" \"{url}\"")
    else:
        print("❌ 上传失败")
        sys.exit(1)

if __name__ == "__main__":
    main()