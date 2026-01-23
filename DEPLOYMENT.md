# 🚀 部署指南 - 将 FinTool 部署为公网网站

本指南将帮助你将 FinTool 部署为任何人都可以访问的公网网站。

## 📋 部署架构

- **前端**: Vercel（免费、自动 HTTPS、全球 CDN）
- **后端**: Railway 或 Render（支持 Python/FastAPI）

## 🎯 方案一：Vercel + Railway（推荐）

### 第一步：部署后端到 Railway

1. **注册 Railway 账号**
   - 访问 https://railway.app
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的 `FinTool` 仓库
   - Railway 会自动检测到 Python 项目

3. **配置后端服务**
   - 在 Railway 项目设置中：
     - **Root Directory**: 设置为 `backend`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - 添加环境变量（如果需要）：
     ```
     OPENAI_API_KEY=your_api_key_here (可选)
     ```

4. **获取后端 URL**
   - Railway 会自动分配一个 URL，例如：`https://your-app-name.up.railway.app`
   - 复制这个 URL，稍后会用到

### 第二步：部署前端到 Vercel

1. **注册 Vercel 账号**
   - 访问 https://vercel.com
   - 使用 GitHub 账号登录

2. **导入项目**
   - 点击 "Add New Project"
   - 选择你的 `FinTool` 仓库
   - 配置项目：
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **配置环境变量**
   - 在 Vercel 项目设置中添加：
     ```
     VITE_API_URL=https://your-app-name.up.railway.app
     ```
   - 替换为你的 Railway 后端 URL

4. **部署**
   - 点击 "Deploy"
   - Vercel 会自动构建并部署
   - 部署完成后会获得一个 URL，例如：`https://fin-tool.vercel.app`

### 第三步：更新前端配置

前端代码已经配置为使用环境变量 `VITE_API_URL`。如果环境变量未设置，会回退到本地开发模式。

## 🎯 方案二：Vercel + Render

### 第一步：部署后端到 Render

1. **注册 Render 账号**
   - 访问 https://render.com
   - 使用 GitHub 账号登录

2. **创建 Web Service**
   - 点击 "New +" → "Web Service"
   - 连接你的 GitHub 仓库
   - 配置：
     - **Name**: `fin-tool-backend`
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - 点击 "Create Web Service"

3. **获取后端 URL**
   - Render 会分配一个 URL，例如：`https://fin-tool-backend.onrender.com`

### 第二步：部署前端到 Vercel

同方案一第二步，但环境变量使用 Render 的 URL：
```
VITE_API_URL=https://fin-tool-backend.onrender.com
```

## 🔧 本地测试部署配置

在部署前，你可以本地测试生产构建：

```bash
# 设置环境变量（Linux/Mac）
export VITE_API_URL=https://your-backend-url.com

# 构建前端
cd frontend
npm run build

# 预览构建结果
npm run preview
```

## 📝 重要注意事项

1. **CORS 配置**
   - 后端已经配置了 `allow_origins=["*"]`，这在生产环境可能不安全
   - 建议更新为只允许你的前端域名：
   ```python
   allow_origins=["https://your-frontend.vercel.app"]
   ```

2. **环境变量安全**
   - 不要在代码中硬编码 API URL
   - 使用环境变量管理敏感信息
   - Vercel 和 Railway 都支持环境变量加密存储

3. **文件上传限制**
   - Vercel 和 Railway 都有文件大小限制
   - 大文件上传可能需要配置额外的存储服务

4. **数据库（如果需要）**
   - 当前项目使用内存存储，重启后数据会丢失
   - 如需持久化，可以添加 PostgreSQL 或 MongoDB

## 🎉 部署完成后的步骤

1. **测试所有功能**
   - 上传 CSV 文件
   - 生成财务报表
   - 测试 FX Rate 功能
   - 测试 AI Chatbot

2. **自定义域名（可选）**
   - Vercel 支持自定义域名
   - 在项目设置中添加你的域名
   - 配置 DNS 记录

3. **监控和日志**
   - Vercel 提供访问统计和错误日志
   - Railway/Render 提供应用日志
   - 定期检查错误和性能

## 🆘 常见问题

**Q: 前端无法连接到后端？**
- 检查环境变量 `VITE_API_URL` 是否正确设置
- 确认后端服务正在运行
- 检查 CORS 配置

**Q: 部署后功能不工作？**
- 检查浏览器控制台的错误信息
- 查看 Vercel 和 Railway 的日志
- 确认所有环境变量都已正确设置

**Q: 如何更新部署？**
- 推送代码到 GitHub 主分支
- Vercel 和 Railway 会自动重新部署

## 📚 相关资源

- [Vercel 文档](https://vercel.com/docs)
- [Railway 文档](https://docs.railway.app)
- [Render 文档](https://render.com/docs)

