# Claude Code OLED Status Display

STM32F103C8T6 + SSD1306 OLED 桌面状态显示器，通过 Claude Code 的 hooks 自动同步工作状态，8 种小猫动画实时反馈。

## 硬件

| 组件 | 型号 |
|------|------|
| MCU | STM32F103C8T6 (Cortex-M3, 64KB Flash, 20KB RAM) |
| 屏幕 | 0.96 寸 SSD1306 I2C OLED (128x64) |
| 调试器 | DAPmini (CMSIS-DAP + 虚拟串口 COM7) |
| 连接 | SWD (PA13/PA14) + USART1 (PA9/PA10) |

## 屏幕布局

```
┌──────────────────────────────────────┐
│          Booting...  (居中)           │  Pages 0-1: 状态名
│                                      │
│           ▐▛█████▜▌                  │
│           ▝▜█████▛▘                  │  Pages 2-7: 72x48
│             ▘▘  ▝▝                  │  大猫精灵 (居中)
│                                      │
└──────────────────────────────────────┘
```

## 8 种状态 + 动画

| 状态 | 命令 | 图标 | 动画 |
|------|------|------|------|
| 初始化 | `INIT` | 招手小猫 | 3帧 — 爪子上下摆动 |
| 空闲 | `IDLE` | 睡觉 + Zzz | 2帧 — 身体呼吸 |
| 写代码 | `CODE` | 小猫 + 键盘 | 3帧 — 键盘闪烁 |
| 写文档 | `DOCS` | 小猫 + 纸张 | 2帧 — 瞳孔扫视 |
| 分析 | `THINK` | 思考气泡 | 3帧 — 气泡脉冲 |
| 搜索 | `SEARCH` | 放大镜 | 2帧 — 眼球扫描 |
| 实验 | `EXPER` | 烧杯 + 气泡 | 3帧 — 气泡上升 |
| 出错 | `ERROR` | 惊恐 + ! | 3帧 — 感叹号抖动 |

- 帧率 500ms，SysTick 驱动
- 状态切换动画自动归零
- 30 秒无操作自动切回 IDLE

## 串口协议

- USART1: 115200 baud, 8N1
- PC → STM32: `CODE\n`, `THINK\n`, `STATUS\n` 等
- STM32 → PC: `CODE\r\n` 等状态名

## 文件结构

```
E:\STM32project\claudecode\
├── Hardware/              # SSD1306 I2C 驱动 (PB8=SCL, PB9=SDA)
│   ├── OLED.c / OLED.h
│   └── OLED_Font.h        # 8x16 英文字体
├── Library/               # STM32F10x StdPeriph V3.5.0
├── Start/                 # CMSIS + startup_stm32f10x_md.s
├── System/                # Delay (SysTick 阻塞式)
├── User/
│   ├── main.c             # 主循环：串口解析 → 状态切换 → 刷新
│   ├── serial.c / .h      # USART1 中断接收 + 环形缓冲
│   ├── display.c / .h     # 屏幕合成 + 小猫位图 blit
│   ├── state_machine.c/.h # 状态枚举 + 空闲超时 + 动画驱动
│   ├── cat_sprites.h      # 21 帧小猫位图 (72x48, 432B/帧)
│   ├── stm32f10x_conf.h   # 外设配置
│   └── stm32f10x_it.c/.h  # 中断服务 (USART1 + SysTick)
├── gen_sprites_v5.py      # Python 精灵生成器 (动画版)
├── pc_bridge.py           # PC 端串口桥接脚本
├── claudecode.uvprojx     # Keil MDK 工程
└── README.md
```

## 编译 & 烧录

```bash
# 编译 (Keil MDK V5)
"/e/Keil_v5/UV4/UV4.exe" -j0 -b claudecode.uvprojx -o build.log

# 烧录 (pyOCD + DAPmini)
pyocd flash -t STM32F103C8 ./Objects/claudecode.hex
```

## PC Bridge

```bash
# 发送状态
python pc_bridge.py CODE

# 查询当前状态
python pc_bridge.py STATUS
# → STM32 Status: CODE

# 可用命令: INIT IDLE CODE DOCS THINK SEARCH EXPER ERROR STATUS
```

## Claude Code Hooks 自动同步

在 `.claude/settings.local.json` 中配置，工具使用自动映射到 OLED 状态：

| Hook 事件 | 匹配器 | OLED 状态 |
|-----------|--------|-----------|
| SessionStart | — | INIT |
| PostToolUse | Write / Edit | CODE |
| PostToolUse | Read | DOCS |
| PostToolUse | Grep / Glob | SEARCH |
| PostToolUse | Agent | THINK |
| PostToolUse | Bash | EXPER |
| PostToolUseFailure | — | ERROR |
| Stop | — | IDLE |

配置后打开 `/hooks` 重新加载即可生效。
