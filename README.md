# 创建项目
cargo install create-tauri-app
cargo create-tauri-app

# 安装依赖
pnpm install

# 启动方式一
pnpm tauri dev

# 启动方式二
cargo tauri dev

# 创建src-tauri（不用执行，create-tauri-app会自动创建）
cargo install tauri-cli
cargo tauri init
