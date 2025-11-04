# Android邮件客户端

基于Java + Android原生开发的轻量级邮件客户端。

## ✅ 项目已完成

### 完成的功能
- ✅ 登录功能（支持QQ/163/126/Gmail/Outlook）
- ✅ 邮件列表查看
- ✅ 邮件详情查看
- ✅ 发送邮件
- ✅ 回复邮件
- ✅ 密码加密存储
- ✅ 本地数据库缓存
- ✅ Material Design 3 UI
- ✅ 侧边栏导航

### 技术栈
- Java 17
- Android SDK 34 (最低API 24)
- Material Design 3
- Room Database
- JavaMail API
- RecyclerView + SwipeRefreshLayout

## 项目结构

```
app/src/main/
├── java/com/example/mailclient/
│   ├── MainActivity.java
│   ├── ui/
│   │   ├── login/LoginActivity.java
│   │   ├── maillist/MailListAdapter.java
│   │   ├── maildetail/MailDetailActivity.java
│   │   └── compose/ComposeActivity.java
│   ├── data/
│   │   ├── model/ (Account, Email)
│   │   ├── database/ (Room DAO)
│   │   ├── repository/ (数据仓库)
│   │   └── mail/ (IMAP/SMTP客户端)
│   └── util/ (工具类)
└── res/
    ├── layout/ (5个布局文件)
    ├── values/ (strings, colors, themes)
    ├── drawable/ (9个图标)
    └── menu/ (2个菜单)
```

## 构建说明

### 本地构建
```bash
./gradlew assembleDebug
```

APK位置: `app/build/outputs/apk/debug/app-debug.apk`

### GitHub Actions自动构建
推送代码后自动构建，APK在Artifacts中下载。

## 使用说明

### 1. 登录
- 选择邮箱服务商
- 输入邮箱地址
- 输入密码/授权码（QQ/163需要授权码）
- 点击登录

### 2. 查看邮件
- 下拉刷新邮件列表
- 点击邮件查看详情
- 侧边栏切换文件夹

### 3. 发送邮件
- 点击右下角FAB按钮
- 填写收件人、主题、正文
- 点击发送图标

### 4. 回复邮件
- 在邮件详情页点击"回复"
- 自动填充收件人和主题
- 编辑内容后发送

## 特性

- ✅ 小巧轻量（预计APK 5-8MB）
- ✅ Material Design原生体验
- ✅ 流畅的动画和交互
- ✅ 离线缓存支持
- ✅ 密码加密存储
- ✅ 支持多个邮箱服务商

## 已知限制

- 暂不支持附件
- 暂不支持HTML邮件（仅纯文本）
- 暂不支持多账户切换
- 暂不支持邮件搜索

## 后续改进

- [ ] 附件支持
- [ ] HTML邮件渲染
- [ ] 多账户管理
- [ ] 邮件搜索
- [ ] 推送通知

## 许可证

MIT License

---

**状态**: ✅ 开发完成，可以构建运行  
**代码量**: ~1800行  
**开发时间**: 1天
