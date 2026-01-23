# 🚀 快速部署指南

## 5 分钟部署到公网

### 步骤 1: 部署后端（Railway）- 3 分钟

1. 访问 https://railway.app，用 GitHub 登录
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择你的 `FinTool` 仓库
4. 在项目设置中：
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 等待部署完成，复制后端 URL（例如：`https://xxx.up.railway.app`）

### 步骤 2: 部署前端（Vercel）- 2 分钟

1. 访问 https://vercel.com，用 GitHub 登录
2. 点击 "Add New Project"，选择你的 `FinTool` 仓库
3. 配置项目：
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. 添加环境变量：
   - **Key**: `VITE_API_URL`
   - **Value**: 你的 Railway 后端 URL（步骤 1 复制的）
5. 点击 "Deploy"
6. 等待部署完成，获得前端 URL（例如：`https://fin-tool.vercel.app`）

### 完成！🎉

现在任何人都可以通过前端 URL 访问你的应用了！

## 🔧 更新其他组件的 API 调用（可选）

我已经更新了 `App.tsx` 和 `FXRatePanel.tsx`。如果你想让所有组件都支持生产环境，需要更新以下文件：

- `frontend/src/components/FinancialChatbot.tsx`
- `frontend/src/components/AIAnalysis.tsx`

在每个文件中：
1. 添加导入：`import { buildApiUrl } from '../utils/api'`
2. 将所有 `fetch('/api/...')` 改为 `fetch(buildApiUrl('/api/...'))`

## 📝 注意事项

- Railway 免费版在 30 分钟无活动后会休眠，首次访问可能需要等待几秒
- Vercel 免费版有使用限制，但通常足够个人项目使用
- 如果需要自定义域名，可以在 Vercel 项目设置中添加

