# 方舟 (Volcengine Ark) API 接入参考

> 记录于 2026-06-15，在 prompt-reverse-engineer 视觉反推任务中完成配置。

## 基本信息

- **API Base URL**: `https://ark.cn-beijing.volces.com/api/v3`
- **API Key**: `ark-YOUR-KEY-HERE`
- **Coding Plan**: 是（端点级密钥，有模型访问限制）

## 可用模型（已验证）

| 模型 ID | 类型 | 状态 |
|---------|------|:--:|
| `deepseek-v4-pro-260425` | 通用推理 | ✅ |
| `deepseek-v4-flash-260425` | 快速推理 | ✅ |
| `deepseek-v3-2-251201` | 通用推理 | ✅ |
| `doubao-seed-1-6-vision-250815` | **视觉分析** | ✅ |
| `doubao-seed-1-6-251015` | 文本推理 | ✅ |
| `glm-4-7-251222` | 文本推理 | ✅ |

## 不可用模型

Kimi-K2 全系不可用：`kimi-k2-250711`(Shutdown) / `kimi-k2-250905`(Retiring) / `kimi-k2-thinking-251104`(Retiring)。`kimi-k2.6` 不在模型列表中。

## Hermes 配置

在 `config.yaml` 中：

```yaml
custom_providers:
  - name: ark-kimi
    base_url: https://ark.cn-beijing.volces.com/api/v3
    api_key: ark-5be46393-...
    model: deepseek-v4-pro-260425
  - name: ark-vision
    base_url: https://ark.cn-beijing.volces.com/api/v3
    api_key: ark-5be46393-...
    model: doubao-seed-1-6-vision-250815

auxiliary:
  vision:
    provider: ark-vision
    model: doubao-seed-1-6-vision-250815
    base_url: https://ark.cn-beijing.volces.com/api/v3
    api_key: ark-5be46393-...
```

修改配置后需重启 Gateway：`hermes gateway restart`

## 调试经验

1. 端点级密钥不传 model 时报 `MissingParameter`，说明鉴权通过
2. 传错 model 名时报 `InvalidEndpointOrModel.NotFound`
3. 列出所有可用模型：`GET /api/v3/models`（部分模型列表可能受密钥权限限制）
4. 列出端点：`GET /api/v3/endpoints`（端点级密钥通常无此权限）
