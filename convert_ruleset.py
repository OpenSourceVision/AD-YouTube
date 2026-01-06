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

def debug_content(content):
    """调试：显示文件内容的前几行"""
    lines = content.split('\n')
    print("\n=== 文件前20行内容 ===")
    for i, line in enumerate(lines[:20], 1):
        print(f"{i:3d}: {repr(line)}")
    print("=" * 50)

def clean_yaml_content(content):
    """清理YAML内容，移除特殊标记"""
    # 移除 ! Checksum 这样的特殊标记
    content = re.sub(r'\s*!\s*Checksum:\s*\S+', '', content)
    return content

def extract_payload_manually(content):
    """手动提取payload内容"""
    print("\n使用手动提取方法...")
    mihomo_rules = {'payload': []}
    
    lines = content.split('\n')
    in_payload = False
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # 检测 payload 开始
        if 'payload:' in line.lower():
            in_payload = True
            print(f"找到 payload 起始位置: 第 {i} 行")
            continue
        
        # 如果在 payload 区域
        if in_payload:
            # 检测是否是列表项（以 - 开头，且有缩进）
            if line.startswith('  -') or line.startswith('- '):
                # 移除前导的 - 和空格
                rule = stripped[1:].strip()
                # 移除引号
                rule = rule.strip('"').strip("'")
                if rule:
                    mihomo_rules['payload'].append(rule)
            # 如果遇到非缩进且非空的行，可能 payload 结束
            elif stripped and not line.startswith(' ') and not line.startswith('\t'):
                # 但要确保不是注释
                if not stripped.startswith('#'):
                    print(f"payload 区域可能结束于第 {i} 行: {repr(line)}")
                    break
    
    print(f"提取到 {len(mihomo_rules['payload'])} 条规则")
    return mihomo_rules

def convert_to_mihomo(content):
    """转换为 mihomo 格式"""
    # 调试：显示原始内容
    debug_content(content)
    
    # 清理内容
    cleaned_content = clean_yaml_content(content)
    
    # mihomo 规则集格式
    mihomo_rules = {'payload': []}
    
    # 尝试标准YAML解析
    try:
        print("\n尝试标准 YAML 解析...")
        data = yaml.safe_load(cleaned_content)
        
        if data is None:
            print("YAML 解析结果为 None")
            return extract_payload_manually(content)
        
        print(f"YAML 解析成功，顶层键: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        
        # 提取规则
        if isinstance(data, dict) and 'payload' in data:
            if isinstance(data['payload'], list):
                mihomo_rules['payload'] = data['payload']
                print(f"从 payload 字段提取到 {len(mihomo_rules['payload'])} 条规则")
            else:
                print(f"payload 字段类型不是列表: {type(data['payload'])}")
        elif isinstance(data, dict) and 'rules' in data:
            print("尝试从 rules 字段提取...")
            for rule in data['rules']:
                if isinstance(rule, str):
                    mihomo_rules['payload'].append(rule)
        
    except yaml.YAMLError as e:
        print(f"YAML 解析失败: {e}")
        return extract_payload_manually(content)
    
    # 如果标准解析没有得到结果，使用手动提取
    if not mihomo_rules['payload']:
        print("标准解析未得到规则，尝试手动提取...")
        return extract_payload_manually(content)
    
    return mihomo_rules

def save_ruleset(data, filename):
    """保存规则集到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"\n规则集已保存到: {filename}")

def create_readme(rule_count):
    """创建或更新 README"""
    readme_content = f"""# Mihomo YouTube Ad Block Ruleset

自动转换的 YouTube 广告拦截规则集，适用于 mihomo (Clash Meta)。

## 📊 统计信息

- **规则数量**: {rule_count}
- **最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- **更新频率**: 每24小时自动更新

## 📥 规则集文件

- [`mihomo-ruleset.yaml`](./mihomo-ruleset.yaml) - 主规则集文件

## 🔗 源地址

[ad-youtube-clash-premium.yaml](https://github.com/Potterli20/file/releases/download/ad-youtube-hosts/ad-youtube-clash-premium.yaml)

## 📖 使用方法

### 方法一：在配置文件中使用

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

**注意**: 请替换 `YOUR_USERNAME` 和 `YOUR_REPO` 为你的实际 GitHub 用户名和仓库名。

### 方法二：本地使用

下载 `mihomo-ruleset.yaml` 文件到本地，然后在配置中引用：

```yaml
rule-providers:
  youtube-ad-block:
    type: file
    behavior: domain
    path: ./ruleset/mihomo-ruleset.yaml

rules:
  - RULE-SET,youtube-ad-block,REJECT
```

## 🤝 贡献

本项目使用 GitHub Actions 自动更新，无需手动维护。

## 📄 许可证

本项目仅为格式转换，规则内容版权归原作者所有。

---

⭐ 如果这个项目对你有帮助，欢迎给个 Star！
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("README.md 已更新")

def main():
    try:
        # 下载原始规则集
        content = download_ruleset(SOURCE_URL)
        
        print(f"\n下载的内容长度: {len(content)} 字符")
        print(f"内容行数: {len(content.split(chr(10)))}")
        
        # 转换为 mihomo 格式
        mihomo_data = convert_to_mihomo(content)
        
        # 检查是否有有效数据
        if not mihomo_data['payload']:
            raise ValueError("未能提取到任何规则，请检查源文件格式")
        
        # 保存规则集
        save_ruleset(mihomo_data, 'mihomo-ruleset.yaml')
        
        # 创建/更新 README
        create_readme(len(mihomo_data['payload']))
        
        print(f"\n✅ 转换完成！")
        print(f"📊 规则总数: {len(mihomo_data['payload'])}")
        print(f"\n📝 前5条规则示例:")
        for i, rule in enumerate(mihomo_data['payload'][:5], 1):
            print(f"  {i}. {rule}")
        
        if len(mihomo_data['payload']) > 5:
            print(f"\n... 还有 {len(mihomo_data['payload']) - 5} 条规则")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
