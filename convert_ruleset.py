#!/usr/bin/env python3
import yaml
import requests
from datetime import datetime

# 源规则集URL
SOURCE_URL = "https://github.com/Potterli20/file/releases/download/ad-youtube-hosts/ad-youtube-clash-premium.yaml"

def download_ruleset(url):
    """下载原始规则集"""
    print(f"正在下载规则集: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def convert_to_mihomo(content):
    """转换为 mihomo 格式"""
    data = yaml.safe_load(content)
    
    # mihomo 规则集格式
    mihomo_rules = {
        'payload': []
    }
    
    # 提取规则
    if 'rules' in data:
        for rule in data['rules']:
            # 处理不同类型的规则
            if isinstance(rule, str):
                # 如果规则已经是字符串格式，直接添加
                mihomo_rules['payload'].append(rule)
            elif isinstance(rule, dict):
                # 如果是字典格式，转换为字符串
                rule_type = list(rule.keys())[0]
                rule_value = rule[rule_type]
                mihomo_rules['payload'].append(f"{rule_type},{rule_value}")
    
    # 如果原文件直接包含 payload
    if 'payload' in data:
        mihomo_rules['payload'] = data['payload']
    
    return mihomo_rules

def save_ruleset(data, filename):
    """保存规则集到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
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
        
        # 保存规则集
        save_ruleset(mihomo_data, 'mihomo-ruleset.yaml')
        
        # 创建/更新 README
        create_readme()
        
        print(f"\n✅ 转换完成！规则数量: {len(mihomo_data['payload'])}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        raise

if __name__ == "__main__":
    main()
