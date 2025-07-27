# CareBot AI

AIを活用したメンタルヘルスケアアプリケーション

## 📋 プロジェクト概要

CareBot AIは、ユーザーの日記や気分記録をAIが分析し、メンタルヘルスの改善をサポートするWebアプリケーションです。

### 主な機能
- **ユーザー認証**: 登録・ログイン機能
- **ジャーナル記録**: 日記の作成・管理
- **気分記録**: 1-5段階の気分スコア記録
- **AI分析**: 日記と気分記録の自動分析
- **使用回数管理**: プラン別の機能制限
- **ダッシュボード**: 統合的な情報表示

### 技術スタック
- **フロントエンド**: SvelteKit + TypeScript + Tailwind CSS
- **バックエンド**: FastAPI + Python
- **データベース**: Supabase (PostgreSQL)
- **認証**: JWT (JSON Web Tokens)

## 🚀 セットアップ

### 前提条件
- Python 3.9+
- Node.js 16+
- Supabaseアカウント

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd CareBot_AI
```

### 2. バックエンドのセットアップ
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. フロントエンドのセットアップ
```bash
cd frontend
npm install
```

### 4. 環境変数の設定
Supabaseの設定を`backend/app/config/supabase.py`で確認・修正してください。

## 🏃‍♂️ アプリケーションの起動

### バックエンドの起動
```bash
cd backend
uvicorn main:app --reload
```
- URL: http://localhost:8000
- API Docs: http://localhost:8000/docs

### フロントエンドの起動
```bash
cd frontend
npm run dev
```
- URL: http://localhost:5173

## 🛠️ 管理コマンド

### データベース管理

#### 1. テーブル状況確認
```bash
cd backend
python check_tables.py
```
**処理内容**:
- Supabaseの全テーブルの存在確認
- 各テーブルのデータ件数表示
- 重複テーブルの検出
- 不足テーブルの確認

**出力例**:
```
CareBot AI テーブル状況確認
========================================
✓ users: 3 件のデータ
✓ journals: 0 件のデータ
✓ moods: 0 件のデータ
✓ usage_counts: 0 件のデータ
✓ feature_limits: 0 件のデータ
✓ analyses: 0 件のデータ
✓ profiles: 0 件のデータ

=== 結果 ===
存在するテーブル: 7
不足テーブル: 0

=== 重複チェック ===
```

#### 2. 重複テーブル修正
```bash
cd backend
python fix_duplicate_tables.py
```
**処理内容**:
- 重複テーブルの検出（`usage_count`/`usage_counts`, `feature_limit`/`feature_limits`）
- 古いテーブルから新しいテーブルへのデータ移行
- 不要テーブルの削除指示
- `analyses`テーブルの作成指示

**出力例**:
```
=== 使用回数テーブルの修正 ===
usage_count から usage_counts に統一します
  usage_count にはデータがありません
usage_count テーブルを削除してください（Supabaseダッシュボードから）

=== 機能制限テーブルの修正 ===
feature_limit から feature_limits に統一します
  feature_limit にはデータがありません
feature_limit テーブルを削除してください（Supabaseダッシュボードから）
```

#### 3. データベースクリーンアップ（安全版）
```bash
cd backend
python clear_database_data_safe.py
```
**処理内容**:
- 外部キー制約を考慮したデータ削除
- 子テーブルから順次削除し、最後に親テーブルを削除
- データベース構成（テーブル構造）は維持
- 確認プロンプトによる安全な実行

**削除順序**:
1. analyses
2. usage_counts
3. feature_limits
4. moods
5. journals
6. profiles
7. users

**出力例**:
```
CareBot AI データベースクリーンアップツール（安全版）
============================================================
⚠️  警告: この操作により、すべてのデータが削除されます！
   データベースの構成（テーブル構造）は維持されます。
   外部キー制約を考慮して、正しい順序で削除します。

削除対象テーブル（外部キー制約を考慮した順序）:
  1. analyses
  2. usage_counts
  3. feature_limits
  4. moods
  5. journals
  6. profiles
  7. users

この操作を実行しますか？ (y/N): y

=== データ削除開始 ===
テーブル analyses のデータを削除中...
  ✓ テーブル analyses は存在します
  ✓ 0 件のデータを削除しました
...
```

#### 4. データベースクリーンアップ（基本版）
```bash
cd backend
python clear_database_data.py
```
**処理内容**:
- 全テーブルのデータを一括削除
- 外部キー制約エラーが発生する可能性あり
- より安全な`clear_database_data_safe.py`の使用を推奨

### データベース構造確認

#### 5. データベース構造詳細確認
```bash
cd backend
python cleanup_database.py
```
**処理内容**:
- 全テーブルの詳細構造確認
- 重複テーブルの自動検出
- 不足テーブルの確認
- テーブル作成SQLの生成

## 📊 API エンドポイント

### 認証
- `POST /api/auth/register` - ユーザー登録
- `POST /api/auth/login` - ユーザーログイン

### ユーザー管理
- `GET /api/users/` - ユーザー一覧
- `GET /api/users/me` - 現在のユーザー情報

### ジャーナル
- `GET /api/journals/` - ジャーナル一覧
- `POST /api/journals/` - ジャーナル作成
- `DELETE /api/journals/{id}` - ジャーナル削除

### 気分記録
- `GET /api/moods/` - 気分記録一覧
- `POST /api/moods/` - 気分記録作成

### AI分析
- `GET /api/analysis/` - 分析結果一覧
- `POST /api/analysis/` - AI分析実行
- `GET /api/analysis/{id}` - 特定の分析結果

### 使用回数管理
- `GET /api/usage/status` - 使用回数状況
- `GET /api/usage/limits` - プラン別制限

## 🔧 トラブルシューティング

### よくある問題

#### 1. バックエンド起動エラー
```bash
ERROR: Error loading ASGI app. Could not import module "main".
```
**解決方法**:
```bash
cd backend  # backendディレクトリに移動してから実行
uvicorn main:app --reload
```

#### 2. CORSエラー
**解決方法**: `backend/main.py`のCORS設定を確認

#### 3. データベース接続エラー
**解決方法**: Supabaseの設定を確認

#### 4. bcryptエラー
```bash
AttributeError: module 'bcrypt' has no attribute '__about__'
```
**解決方法**:
```bash
pip uninstall bcrypt -y && pip install bcrypt
```

## 📝 開発メモ

### データベーステーブル構成
- `users` - ユーザー情報
- `journals` - ジャーナル記録
- `moods` - 気分記録
- `usage_counts` - 使用回数管理
- `feature_limits` - 機能制限設定
- `analyses` - AI分析結果
- `profiles` - プロフィール情報

### プラン制限
- **フリープラン**: ジャーナル10件/月、気分記録30件/月、AI分析3回/月
- **プレミアムプラン**: 無制限

### 認証フロー
1. ユーザー登録/ログイン
2. JWTトークン発行
3. フロントエンドでlocalStorageに保存
4. API呼び出し時にAuthorizationヘッダーに設定

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。