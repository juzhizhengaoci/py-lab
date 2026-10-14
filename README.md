# py-lab · Python 练习场

> 从零手写 Web Server 起步，一路走到 FastAPI 服务化与 AI 应用工程。
> **规则：每个项目一个 venv，不复制粘贴，没跑通不开下一个。**

这是一个"边做边补语法"的练习仓库——不是教程笔记的复制粘贴，是**每一行都自己敲过并跑通**的代码。
有 Java / MySQL 后端底子，所以不走"先系统学一遍语法"的弯路，直接从项目切入。

---

## 一、路线图与进度

| 阶段 | 项目 | 估时 | 状态 |
|---|---|---|---|
| **01** | **Let's Build A Web Server** —— 用 `socket` 手写 HTTP 服务与 WSGI 服务器 | ~6h | 🔄 **进行中** |
| 02 | Write yourself a Git —— 补「文件格式 / 内容寻址 / 压缩」这套认知 | ~10h | ⬜ 未开始 |
| 03 | Neural Networks: Zero to Hero（Karpathy）—— 转 AI 的正门 | ~25h | ⬜ 未开始 |
| 04 | Write your own miniature Redis —— 用新语言复刻旧认知 | ~10h | ⬜ 未开始 |
| 05 | 向量检索 + FastAPI 服务化 —— 拼成能上线的 AI 应用 | ~8h+ | ⬜ 未开始 |

**为什么第一个项目是手写 Web Server？** 因为终点是 FastAPI，而 FastAPI 底下就是 ASGI/WSGI。
亲手摸过那一层之后，任何 Python Web 框架都不再是黑箱。

详细的分段执行表、过关标准与坑位提示 → [`起步方案.md`](./起步方案.md)

---

## 二、当前项目：toy-webserver

对应教程 *Let's Build A Web Server*（Ruslan Spivak）。

| 段 | 内容 | 过关标准 | 状态 |
|---|---|---|---|
| Part 1 | `socket` 起服务器：bind → listen → accept → recv → 手写 HTTP 响应 | `curl -v http://localhost:8888/` 打回 `Hello, World!`；能解释 `listen(1)` 的 1 是什么 | ⬜ |
| Part 2 | 解析请求 → 构造 `environ` 字典 → handler 生成响应 → 抽成 `WSGIServer` 类 | 能跑通 WSGI 服务器；能说出 `environ` 里 5 个 key 的来历 | ⬜ |
| Part 2+ | 自己加一条 404 路由（教程里没有） | 访问不存在的路径返回 404 而不是崩 | ⬜ |
| Part 3 | 加并发。⚠️ 原文用 `os.fork()`，**Windows 上必须改写成 `multiprocessing` / `threading`** | 两个终端同时请求，第二个不用等第一个跑完 | ⬜ |
| 复盘 | 500 字：我写的这个服务器和 FastAPI 是什么关系 | 能讲清楚"服务器"与"框架"各管什么 | ⬜ |

### 已知的三个坑（提前记录，避免重复踩）

1. **教程只有 3 篇，没有 part4** —— 站上 `lsbaws-part4` 是 404。
2. **Part 3 的代码在 Windows 上跑不了** —— `os.fork()` 是 Unix 专属系统调用；最终版还 `import StringIO`（Python 2 的模块名）。**必须自己改写。**
3. **Part 1 / Part 2 是干净的 Python 3 代码** —— 可以放心跟着敲，**Part 2 结束时目标就已经达成**，Part 3 是加餐。

> 卡壳记录写在 [`toy-webserver/NOTES.md`](./toy-webserver/NOTES.md)——每次卡住超过 10 分钟就记一行：
> "我当时以为是什么 / 实际是什么"。代码三个月后会忘，思维盲区不记下来会一直踩。

---

## 三、目录结构

```
py-lab/
├── README.md                 本文件：路线图与进度看板
├── .gitignore
├── 起步方案.md                逐段执行表 / 过关标准 / 节奏安排 / 提问姿势
└── toy-webserver/            项目 01：手写 Web Server
    ├── .gitignore
    ├── webserver1.py         Part 1 实现（进行中）
    ├── NOTES.md              卡壳日志 + 进度表
    └── 从这里开始.md          照着做的第一步操作手册
```

---

## 四、环境

| 项 | 说明 |
|---|---|
| Python | **Microsoft Store 版 3.13.14**（`python` 命令指向它） |
| 虚拟环境 | **每个项目一个 venv**，`.venv/` 已被 `.gitignore` 排除，不进仓库 |
| 代码位置 | 一律放 **D 盘**（`D:\Learning\`），C 盘只留系统 |

激活虚拟环境：

```bash
cd toy-webserver
source .venv/Scripts/activate      # Git Bash
# PowerShell:  .\.venv\Scripts\Activate.ps1
# CMD:         .venv\Scripts\activate.bat
# 都不行就：    .venv\Scripts\python.exe your_script.py
python -V                          # 前面应出现 (.venv)
```

---

## 五、三条硬规则

1. **不许复制粘贴** —— 包括复制自己上一段写的代码。手敲会疼，疼就是在学。
2. **卡住 20 分钟内不许问 AI** —— 20 分钟后可以问，但只准问"为什么"，不准问"帮我写出来"。
3. **没跑通不许开第二个项目** —— 同时开三个 = 三个都停在 30%。

**正确的提问姿势：**

| ❌ 让 AI 替你完成任务 | ✅ 让 AI 补上你思维里的洞 |
|---|---|
| "帮我写一个 HTTP 服务器" | "我 `recv(1024)` 只拿到了部分请求头，为什么？" |
| "这段代码为什么报错"（贴一堆） | "`accept()` 阻塞不返回，我怀疑是……，这样理解对吗？" |
| "给我完整的 webserver2.py" | "`environ` 里的 `wsgi.input` 为什么要包一层 `io.BytesIO`？" |

---

## 六、参考资料

- 教程：<https://ruslanspivak.com/lsbaws-part1/>（part2 / part3 同规律）
- 配套代码：<https://github.com/rspivak/lsbaws>
- 配套仓库里的 `part2/flaskapp.py`、`djangoapp.py` 需要额外装 Flask/Django —— **核心目标不需要它们，别为了跑通这些去装包。**

---

## 七、不要做的事

- ❌ 别先去"系统学一遍 Python 语法"再动手 —— 有 Java 底子，语法差异一周能磨平，**边做边补最快**。
- ❌ 别同时开两个项目。
- ❌ 别在这台机器上再装新的 Python 版本 —— 环境越多，debug 环境的时间越长。
