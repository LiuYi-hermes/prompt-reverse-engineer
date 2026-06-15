# Prompt Reverse Engineer

An OpenClaw skill for reverse-engineering image prompts from any image.

## Description

输入一张图片，反推生成这张图片所需的完整提示词。

**Use Cases:**
- 用户上传/提供一张图片，询问"这张图怎么生成的"、"帮我写这个图的提示词"、"反推prompt"
- 用户想复刻/模仿某张图的风格或效果
- 用户需要分析图片的摄影参数、光影、构图
- 用户想在不同平台（Midjourney/DALL-E/Stable Diffusion/Flux/Seedream/GPT Image 2）复现同一张图

## Features

- **72-parameter analysis system** across 7 categories (Frame, Subject, Photography, Lighting, Post-processing, Constraints, Output)
- **Five-layer progressive analysis** (outer to inner, coarse to fine)
- **Multi-platform output** optimized for GPT Image 2.0, Midjourney, DALL-E, Stable Diffusion, Flux, Seedream
- **Automatic local archiving** with searchable history
- **Detailed subject analysis**: pose, proportion, facial features, expression, hairstyle, makeup, jewelry, clothing, props

## Installation

1. Copy this skill directory to your OpenClaw skills folder:
   ```bash
   cp -r prompt-reverse-engineer-skill ~/.qclaw/skills/prompt-reverse-engineer
   ```

2. The skill will be automatically loaded on next OpenClaw startup.

## Usage

Simply upload or reference an image and ask:
- "反推这张图的提示词"
- "分析这张图怎么生成的"
- "帮我复刻这个风格"
- "reverse engineer this image"

## Parameter System

The skill uses a comprehensive 72-parameter system organized into 7 blocks:

| Block | Name | Parameters | Core | Enhanced | Optional |
|-------|------|------------|------|----------|----------|
| A | Frame | 10 | 5 | 2 | 3 |
| B | Subject | 18 | 8 | 7 | 3 |
| C | Photography | 9+ | 4 | 1 | 4 |
| D | Lighting | 8 | 2 | 3 | 3 |
| E | Post-processing | 8+ | 3 | 1 | 4 |
| F | Constraints | 5+ | 1 | 1 | 3 |
| G | Output Medium | 10 | 1 | 7 | 2 |

See `references/parameter_system.md` for the complete parameter definitions.

## File Structure

```
prompt-reverse-engineer/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── LICENSE                     # MIT License
├── references/
│   └── parameter_system.md     # Complete 72-parameter system
├── scripts/
│   └── save_result.py          # Local archiving utility
└── assets/                     # Skill assets
```

## Output Format

### GPT Image 2.0 (Chinese)

```
这是一张[画幅比例]的[画面类型]，[场景/背景描述]。画面是[主体概览]，[景别]，人物占画面高度约[X]%，[居中/偏左/偏右]。

姿势与动态：[全身姿态描述，包括肢体角度、四肢具体位置、身体扭转方向、重心分布]。

面部与表情：[脸型]，面部占比约1/X身高。[眉毛形状与角度]，[眼型与眼神方向]，[鼻型]，[唇形与表情]。整体表情[精确情绪描述]。

发型与发饰：[发型名称与结构细节]，[发饰类型、材质、颜色、佩戴位置与垂坠状态]，[额饰/鬓角细节]，[发丝纹理与光泽]。

妆容与妆造：[底妆质感]，[眉形、眼妆细节]，[唇妆]，[腮红位置与颜色]，[修容高光区域]，[特殊妆效]。

装饰与珠宝：[项链层数、材质、吊坠形状、大小与位置]，[耳饰长度、造型、垂落位置与摆动状态]，[手镯/臂钏/戒指的材质、数量与佩戴位置]，[其他配饰]。

服装与道具：[服装层次、颜色、材质、纹样、褶皱状态]，[手持道具的具体形态、尺寸、装饰细节、握持方式]。

[重要细节——材质质感、颜色关系、飘带/特效的动态轨迹、空间关系]。

[光影描述——主光方向/质感/光比、补光情况、轮廓光、环境光、光色温度]。

[风格描述——调色倾向、对比度/饱和度、胶片/媒介参考、摄影流派引用、后期处理]。

格式：[画幅/硬约束]。
```

## Credits

- Parameter system inspired by professional photography and AI image generation best practices

## License

MIT License - see LICENSE file for details.
