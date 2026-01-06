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

def extract_rules(content):
    """提取规则"""
    print("\n开始提取规则...")
    rules = []
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # 跳过空行
        if not stripped:
            continue
        
        # 跳过 payload: 行
        if 'payload:' in line.lower():
            print(f"跳过第 {i} 行: payload 声明")
            continue
        
        # 跳过以 ! 开头的注释行
        if stripped.startswith('!'):
            continue
        
        # 检测列表项（以 - 开头）
        if stripped.startswith('-'):
            # 移除前导的 - 和空格
            rule = stripped[1:].strip()
            # 移除引号
            rule = rule.strip('"').strip("'")
            
            if rule:
                rules.append(rule)
    
    print(f"✓ 成功提取 {len(rules)} 条规则")
    return rules

def convert_to_mihomo(content):
    """转换为 mihomo 格式"""
    # 提取规则
    rules = extract_rules(content)
    
    if not rules:
        raise ValueError("未能提取到任何规则")
    
    # mihomo 规则集格式
    mihomo_rules = {
        'payload': rules
    }
    
    return mihomo_rules

def save_ruleset(data, filename):
    """保存规则集到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"✓ 规则集已保存到: {filename}")

def create_readme(rule_count):
    """创建或更新 README"""
    readme_content = f"""# Mihomo YouTube Ad Block Ruleset

自动转换的 YouTube 广告拦截规则集，适用于 mihomo (Clash Meta)。

## 📊 统计信息

- **规则数量**: {rule_count:,}
- **最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- **更新频率**: 每24小时自动更新

## 📥 规则集文件

- [`mihomo-ruleset.yaml`](./mihomo-ruleset.yaml) - 主规则集文件

## 🔗 源地址

[ad-youtube-clash-premium.yaml](https://github.com/Potterli20/file/releases/download/ad-youtube-hosts/ad-youtube-clash-premium.yaml)

## 📖 使用方法

### 方法一：直接引用（推荐）

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

**重要**: 请替换 `YOUR_USERNAME` 和 `YOUR_REPO` 为你的实际 GitHub 用户名和仓库名。

### 方法二：本地使用

1. 下载 [`mihomo-ruleset.yaml`](./mihomo-ruleset.yaml) 到本地
2. 在配置中引用：

```yaml
rule-providers:
  youtube-ad-block:
    type: file
    behavior: domain
    path: ./ruleset/mihomo-ruleset.yaml

rules:
  - RULE-SET,youtube-ad-block,REJECT
```

## 🎯 功能说明

本规则集用于拦截 YouTube 广告相关的域名，包括：
- YouTube 视频广告服务器
- Google Video 广告节点
- 其他 YouTube 广告相关域名

## 🔄 更新机制

- 使用 GitHub Actions 自动化
- 每天 UTC 0:00（北京时间 8:00）自动运行
- 自动拉取源规则并转换格式
- 自动提交更新到仓库

## 📝 规则格式

规则采用域名匹配格式，以 `+.` 开头表示匹配该域名及其所有子域名。

示例：
```
+.r1---sn-25glen7l.googlevideo.com
+.r1---sn-25glenez.googlevideo.com
```

## ⚠️ 注意事项

- 规则可能会影响 YouTube 的正常播放，如遇问题请及时反馈
- 建议配合其他广告拦截规则使用以达到最佳效果
- 定期检查规则更新以保持最佳拦截效果

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目仅为格式转换工具，规则内容版权归原作者所有。

---

⭐ 如果这个项目对你有帮助，欢迎给个 Star！
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✓ README.md 已更新")

def main():
    try:
        print("=" * 60)
        print("Mihomo 规则集转换工具")
        print("=" * 60)
        
        # 下载原始规则集
        content = download_ruleset(SOURCE_URL)
        print(f"✓ 下载成功: {len(content):,} 字符, {len(content.split(chr(10)))} 行")
        
        # 显示文件预览
        lines = content.split('\n')
        print(f"\n📄 文件预览（前5行）:")
        for i, line in enumerate(lines[:5], 1):
            print(f"  {i}. {line[:80]}{'...' if len(line) > 80 else ''}")
        
        # 转换为 mihomo 格式
        mihomo_data = convert_to_mihomo(content)
        
        # 保存规则集
        save_ruleset(mihomo_data, 'mihomo-ruleset.yaml')
        
        # 创建/更新 README
        create_readme(len(mihomo_data['payload']))
        
        # 显示结果
        print("\n" + "=" * 60)
        print("✅ 转换完成！")
        print("=" * 60)
        print(f"📊 规则总数: {len(mihomo_data['payload']):,}")
        print(f"\n📝 规则示例（前5条）:")
        for i, rule in enumerate(mihomo_data['payload'][:5], 1):
            print(f"  {i}. {rule}")
        
        if len(mihomo_data['payload']) > 5:
            print(f"  ...")
            print(f"\n📝 规则示例（后3条）:")
            for i, rule in enumerate(mihomo_data['payload'][-3:], len(mihomo_data['payload']) - 2):
                print(f"  {i}. {rule}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
