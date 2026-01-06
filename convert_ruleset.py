#!/usr/bin/env python3
import yaml
import requests
from datetime import datetime
import re

# 源规则集URL
SOURCE_URL = "https://github.com/Potterli20/file/releases/download/ad-youtube-hosts/ad-youtube-clash-premium.yaml"

def download_ruleset(url):
    """下载原始规则集"""
    print(f"正在下载规则集: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def clean_yaml_content(content):
    """清理YAML内容，移除特殊标记"""
    # 移除 ! Checksum 这样的特殊标记
    content = re.sub(r'\s*!\s*Checksum:\s*\S+', '', content)
    return content

def convert_to_mihomo(content):
    """转换为 mihomo 格式"""
    # 清理内容
    content = clean_yaml_content(content)
    
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"YAML解析错误，尝试使用备用方法: {e}")
        # 如果标准解析失败，尝试手动提取payload
        return extract_payload_manually(content)
    
    # mihomo 规则集格式
    mihomo_rules = {
        'payload': []
    }
    
    # 提取规则
    if 'payload' in data and data['payload']:
        # 如果原文件直接包含 payload
        if isinstance(data['payload'], list):
            mihomo_rules['payload'] = data['payload']
        else:
            print("警告: payload 不是列表格式")
    elif 'rules' in data:
        # 从 rules 字段提取
        for rule in data['rules']:
            if isinstance(rule, str):
                mihomo_rules['payload'].append(rule)
            elif isinstance(rule, dict):
                rule_type = list(rule.keys())[0]
                rule_value = rule[rule_type]
                mihomo_rules['payload'].append(f"{rule_type},{rule_value}")
    else:
        print("警告: 未找到有效的规则数据")
    
    return mihomo_rules

def extract_payload_manually(content):
    """手动提取payload内容（备用方法）"""
    print("使用手动提取方法...")
    mihomo_rules = {'payload': []}
    
    # 查找 payload: 后的内容
    lines = content.split('\n')
    in_payload = False
    
    for line in lines:
        stripped = line.strip()
        
        # 检测 payload 开始
        if stripped.startswith('payload:'):
            in_payload = True
            continue
        
        # 如果在 payload 区域
        if in_payload:
            # 检测是否是列表项（以 - 开头）
            if stripped.startswith('-'):
                # 移除前导的 - 和空格
                rule = stripped[1:].strip()
                # 移除引号
                rule = rule.strip('"').strip("'")
                if rule:
                    mihomo_rules['payload'].append(rule)
            # 如果遇到非缩进的行，说明 payload 结束
            elif stripped and not line.startswith(' ') and not line.startswith('\t'):
                break
    
    return mihomo_rules

def save_ruleset(data, filename):
    """保存规则集到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"规则集已保存到: {filename}")

def create_readme():
    """创建或更新 README"""
    readme_content = f"""# Mihomo 规则集

自动转换的 YouTube 广告拦截规则集，适用于 mihomo (Clash Meta)。

## 规则集文件

- `mihomo-ruleset.yaml` - 主规则集文件

## 更新频率

每24小时自动更新一次

## 最后更新

{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## 源地址

https://github.com/Potterli20/file/releases/download/ad-youtube-hosts/ad-youtube-clash-premium.yaml

## 使用方法

在 mihomo 配置文件中添加：

```yaml
rule-providers:
  youtube-ad-block:
    type: http
    behavior: domain
    url: "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/mihomo-ruleset.yaml"
    path: ./ruleset/youtube-ad-block.yaml
    interval: 86400

rules:
  - RULE-SET,youtube-ad-block,REJECT
```

替换 `YOUR_USERNAME` 和 `YOUR_REPO` 为你的 GitHub 用户名和仓库名。

## 许可证

本项目仅为格式转换，规则内容版权归原作者所有。
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("README.md 已更新")

def main():
    try:
        # 下载原始规则集
        content = download_ruleset(SOURCE_URL)
        
        # 转换为 mihomo 格式
        mihomo_data = convert_to_mihomo(content)
        
        # 检查是否有有效数据
        if not mihomo_data['payload']:
            raise ValueError("未能提取到任何规则，请检查源文件格式")
        
        # 保存规则集
        save_ruleset(mihomo_data, 'mihomo-ruleset.yaml')
        
        # 创建/更新 README
        create_readme()
        
        print(f"\n✅ 转换完成！规则数量: {len(mihomo_data['payload'])}")
        print(f"前5条规则示例:")
        for i, rule in enumerate(mihomo_data['payload'][:5], 1):
            print(f"  {i}. {rule}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
