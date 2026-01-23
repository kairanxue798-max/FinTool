# ✅ 部署检查清单

## 📋 部署前检查

### ✅ 代码已推送到 GitHub
- [x] 所有代码已提交
- [x] 已推送到 GitHub 主分支
- [x] 仓库地址：https://github.com/kairanxue798-max/FinTool

### ✅ 配置文件已就绪
- [x] `backend/railway.json` - Railway 配置
- [x] `backend/Procfile` - Render 配置
- [x] `frontend/vercel.json` - Vercel 配置
- [x] `frontend/src/utils/api.ts` - API 配置工具

## 🚀 部署步骤

### 第一步：部署后端到 Railway

#### 1.1 访问 Railway
- 打开浏览器，访问：https://railway.app
- 点击右上角 "Login" 或 "Get Started"
- 选择 "Login with GitHub"
- 授权 Railway 访问你的 GitHub 账号

#### 1.2 创建新项目
- 登录后，点击 "New Project"
- 选择 "Deploy from GitHub repo"
- 在仓库列表中找到 `FinTool` 或 `kairanxue798-max/FinTool`
- 点击仓库名称

#### 1.3 配置后端服务
Railway 会自动检测到 Python 项目，但需要确认配置：

1. **检查服务设置**
   - 点击服务名称（可能是 "FinTool"）
   - 进入 "Settings" 标签页

2. **设置 Root Directory**
   - 找到 "Root Directory" 设置
   - 输入：`backend`
   - 点击 "Save"

3. **设置启动命令**
   - 找到 "Start Command" 或 "Deploy" 设置
   - 输入：`uvicorn main:app --host 0.0.0.0 --port $PORT`
   - 点击 "Save"

4. **（可选）添加环境变量**
   - 如果需要 OpenAI API：
     - 进入 "Variables" 标签页
     - 添加：`OPENAI_API_KEY` = `你的 API Key`

#### 1.4 等待部署完成
- Railway 会自动开始构建和部署
- 等待状态变为 "Active"（通常需要 2-5 分钟）
- 部署完成后，点击 "Settings" → "Networking"
- 找到 "Public Domain"，复制 URL（例如：`https://xxx.up.railway.app`）
- **重要**：保存这个 URL，下一步会用到

#### 1.5 测试后端
- 在浏览器中访问：`你的后端URL/api/health`
- 应该看到：`{"status":"healthy"}`

---

### 第二步：部署前端到 Vercel

#### 2.1 访问 Vercel
- 打开浏览器，访问：https://vercel.com
- 点击右上角 "Sign Up" 或 "Login"
- 选择 "Continue with GitHub"
- 授权 Vercel 访问你的 GitHub 账号

#### 2.2 导入项目
- 登录后，点击 "Add New Project" 或 "Import Project"
- 在仓库列表中找到 `FinTool` 或 `kairanxue798-max/FinTool`
- 点击 "Import"

#### 2.3 配置项目设置
Vercel 会自动检测到 Vite 项目，但需要确认：

1. **Framework Preset**
   - 确认显示：`Vite`
   - 如果不是，手动选择 `Vite`

2. **Root Directory**
   - 点击 "Edit" 或 "Override"
   - 输入：`frontend`
   - 点击 "Continue"

3. **Build and Output Settings**
   - **Build Command**: `npm run build`（应该已自动填充）
   - **Output Directory**: `dist`（应该已自动填充）
   - **Install Command**: `npm install`（应该已自动填充）

#### 2.4 添加环境变量（重要！）
- 在 "Environment Variables" 部分
- 点击 "Add" 或 "+"
- **Key**: `VITE_API_URL`
- **Value**: 粘贴你在第一步复制的 Railway 后端 URL
  - 例如：`https://xxx.up.railway.app`
  - **注意**：不要包含末尾的 `/`
- 点击 "Add"
- 点击 "Deploy"

#### 2.5 等待部署完成
- Vercel 会自动开始构建和部署
- 等待构建完成（通常需要 1-3 分钟）
- 部署完成后，你会看到一个 URL（例如：`https://fin-tool.vercel.app`）
- **重要**：保存这个 URL，这就是你的公网访问地址

#### 2.6 测试前端
- 在浏览器中访问你的 Vercel URL
- 应该能看到 FinTool 应用界面
- 测试上传 CSV 文件功能

---

### 第三步：更新后端 CORS（可选但推荐）

为了安全，建议更新后端 CORS 配置，只允许你的前端域名：

1. **编辑 `backend/main.py`**
   - 找到 CORS 配置部分（大约第 22-28 行）
   - 将 `allow_origins=["*"]` 改为：
   ```python
   allow_origins=["https://你的-vercel-url.vercel.app"]
   ```
   - 如果有多个域名，用逗号分隔

2. **提交并推送更改**
   ```bash
   git add backend/main.py
   git commit -m "security: Update CORS to allow only frontend domain"
   git push origin main
   ```
   - Railway 会自动重新部署

---

## ✅ 部署后检查清单

### 功能测试
- [ ] 前端页面可以正常打开
- [ ] 可以上传 CSV 文件
- [ ] 财务报表可以正常生成
- [ ] FX Rate 面板可以查询汇率
- [ ] AI Chatbot 可以正常对话
- [ ] 所有 KPI 功能正常工作

### 性能检查
- [ ] 页面加载速度正常
- [ ] API 响应时间合理
- [ ] 没有控制台错误

### 安全检查
- [ ] CORS 配置正确（如果已更新）
- [ ] 环境变量已正确设置
- [ ] 敏感信息（API Key）未暴露在前端代码中

---

## 🆘 常见问题排查

### 问题 1: 前端无法连接后端
**症状**：前端页面打开，但上传文件或调用 API 失败

**解决方法**：
1. 检查 Vercel 环境变量 `VITE_API_URL` 是否正确设置
2. 确认后端 URL 格式正确（不包含末尾 `/`）
3. 检查浏览器控制台（F12）的错误信息
4. 确认后端服务正在运行（访问 `后端URL/api/health`）

### 问题 2: Railway 部署失败
**症状**：Railway 显示部署错误

**解决方法**：
1. 检查 Railway 日志（点击服务 → "Deployments" → 查看日志）
2. 确认 `Root Directory` 设置为 `backend`
3. 确认 `Start Command` 正确
4. 检查 `requirements.txt` 是否存在且格式正确

### 问题 3: Vercel 构建失败
**症状**：Vercel 显示构建错误

**解决方法**：
1. 检查 Vercel 构建日志（项目页面 → "Deployments" → 点击失败的部署）
2. 确认 `Root Directory` 设置为 `frontend`
3. 确认 `Build Command` 和 `Output Directory` 正确
4. 检查 `package.json` 是否存在

### 问题 4: CORS 错误
**症状**：浏览器控制台显示 CORS 错误

**解决方法**：
1. 确认后端 CORS 配置包含前端域名
2. 检查 `allow_origins` 配置是否正确
3. 确认前端 URL 格式正确（包含 `https://`）

---

## 📞 需要帮助？

如果遇到问题：
1. 查看详细日志（Railway 和 Vercel 都提供详细的日志）
2. 检查浏览器控制台错误信息
3. 参考 `DEPLOYMENT.md` 获取更多信息
4. 在 GitHub Issues 中提问

---

**部署完成后，你的应用就可以通过公网访问了！** 🎉

