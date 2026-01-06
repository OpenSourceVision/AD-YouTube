# Mihomo YouTube Ad Block Ruleset

自动转换的 YouTube 广告拦截规则集，适用于 mihomo (Clash Meta)。

## 📊 统计信息

- **规则数量**: 3,959
- **最后更新**: 2026-01-06 11:07:32 UTC
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
