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
```bash
cd backend
cp .env.example .env
# .envファイルを編集してSupabase設定を追加
```

**必要な環境変数**:
```env
ENVIRONMENT=development
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-role-key
JWT_SECRET=your-jwt-secret-key
JWT_EXPIRY=24
```

## 🏃‍♂️ アプリケーションの起動

### バックエンドの起動
```bash
cd backend
source venv/bin/activate
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
source venv/bin/activate
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
source venv/bin/activate
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
source venv/bin/activate
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
source venv/bin/activate
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
source venv/bin/activate
python cleanup_database.py
```
**処理内容**:
- 全テーブルの詳細構造確認
- 重複テーブルの自動検出
- 不足テーブルの確認
- テーブル作成SQLの生成

### データベースリセット・初期化

#### 6. データベース完全リセット
```bash
cd backend
source venv/bin/activate
python reset_database.py
```
**処理内容**:
- すべてのテーブルのデータを削除
- シーケンスのリセット（IDを1から再開）
- データベースを初期状態に戻す
- 外部キー制約を考慮した安全な削除

**出力例**:
```
データベースリセットスクリプトを開始します...
=== 環境設定確認 ===
環境: development
Supabase URL: https://xxx.supabase.co
Supabase Service Key: eyJhbGciOiJIUzI1NiIs...
✅ すべての必須環境変数が設定されています

=== データベースリセット ===
1. データ削除中...
✅ analyses: 0 件のデータを削除しました
✅ feature_limits: 0 件のデータを削除しました
✅ journals: 0 件のデータを削除しました
✅ moods: 0 件のデータを削除しました
✅ profiles: 0 件のデータを削除しました
✅ usage_counts: 0 件のデータを削除しました
✅ users: 0 件のデータを削除しました

2. シーケンスリセット中...
⚠️  シーケンスリセットは手動で実行する必要があります
✅ データベースリセットが完了しました
```

#### 7. データベース状態確認
```bash
cd backend
source venv/bin/activate
python check_database_status.py
```
**処理内容**:
- 各テーブルのデータ件数確認
- 最新のデータID確認
- テストデータの挿入・削除による動作確認
- シーケンスの動作確認

**出力例**:
```
データベース状態確認スクリプトを開始します...
=== 環境設定確認 ===
環境: development
Supabase URL: https://xxx.supabase.co
Supabase Service Key: eyJhbGciOiJIUzI1NiIs...
✅ すべての必須環境変数が設定されています

=== データベース状態確認 ===

1. 各テーブルのデータ数を確認:
  - analyses: 0 件
  - feature_limits: 0 件
  - journals: 0 件
  - moods: 0 件
  - profiles: 0 件
  - usage_counts: 0 件
  - users: 1 件

2. 最新のデータを確認:
  - analyses: データなし
  - feature_limits: データなし
  - journals: データなし
  - moods: データなし
  - profiles: データなし
  - usage_counts: データなし
  - users: ID 1

3. テストデータ挿入:
✅ テストユーザーを作成しました (ID: 2)
✅ テストユーザーを削除しました (ID: 2)

=== データベース状態確認完了 ===
✅ データベース状態確認が完了しました
```

#### 8. 機能制限テーブル初期化
```bash
cd backend
source venv/bin/activate
python init_feature_limits.py
```
**処理内容**:
- `feature_limits`テーブルにデフォルトの使用制限を設定
- フリープランとプレミアムプランの制限値を設定
- 各機能（ジャーナル、気分記録、AI分析など）の制限を定義

**設定される制限値**:
- **ジャーナル**: フリー10件/月、プレミアム無制限
- **気分記録**: フリー30件/月、プレミアム無制限
- **AI分析**: フリー3回/月、プレミアム無制限
- **CBT**: フリー5回/月、プレミアム無制限
- **瞑想**: フリー10回/月、プレミアム無制限

### シーケンスリセット

#### 9. データ挿入によるシーケンスリセット
```bash
cd backend
source venv/bin/activate
python reset_sequences_via_insert.py
```
**処理内容**:
- 各テーブルにテストデータを挿入
- 挿入したデータを削除
- 新しいデータを挿入してIDが1から始まるか確認
- シーケンスの動作を検証

**出力例**:
```
データ挿入によるシーケンスリセットスクリプトを開始します...
=== 環境設定確認 ===
環境: development
Supabase URL: https://xxx.supabase.co
Supabase Service Key: eyJhbGciOiJIUzI1NiIs...
✅ すべての必須環境変数が設定されています

=== データ挿入によるシーケンスリセット ===
1. 現在のシーケンス値を確認中...

2. テストデータを挿入してシーケンス値を確認中...
✅ users: テストデータ挿入 (ID: 1)
✅ journals: テストデータ挿入 (ID: 1)
✅ moods: テストデータ挿入 (ID: 1)
✅ profiles: テストデータ挿入 (ID: 1)
✅ usage_counts: テストデータ挿入 (ID: 1)

3. テストデータを削除中...
✅ journals: テストデータ削除 (ID: 1)
✅ moods: テストデータ削除 (ID: 1)
✅ profiles: テストデータ削除 (ID: 1)
✅ usage_counts: テストデータ削除 (ID: 1)

4. シーケンスリセットの確認...

5. シーケンスリセットの検証...
✅ users: 検証データ挿入 (ID: 2)
⚠️  users: シーケンスがリセットされていません (ID: 2)
✅ users: 検証データ削除完了

=== シーケンスリセット完了 ===
✅ データ挿入によるシーケンスリセットが完了しました
✅ 新しいデータを挿入すると、IDは1から開始されるはずです
```

#### 10. PostgreSQL直接接続によるシーケンスリセット
```bash
cd backend
source venv/bin/activate
python reset_sequences_psql.py
```
**処理内容**:
- PostgreSQLに直接接続
- 各シーケンスの現在値を確認
- `ALTER SEQUENCE`コマンドでシーケンスをリセット
- 変更をコミット

**注意**: Supabaseの制限により、この方法は動作しない可能性があります。

#### 11. REST APIによるシーケンスリセット
```bash
cd backend
source venv/bin/activate
python reset_sequences.py
```
**処理内容**:
- Supabase REST APIを使用
- 利用可能なRPC関数を確認
- シーケンスリセットの代替方法を試行

### ロール管理

#### 12. カスタムロール管理
```bash
cd backend
source venv/bin/activate
python manage_roles.py
```
**処理内容**:
- カスタムロールの作成（admin, premium, moderator）
- ユーザーへのロール割り当て
- ロールの確認・削除
- ロール権限の管理

**利用可能なコマンド**:
```bash
# ロール一覧表示
python manage_roles.py list

# ロール作成
python manage_roles.py create admin

# ユーザーにロール割り当て
python manage_roles.py assign user@example.com admin

# ロール確認
python manage_roles.py check user@example.com
```

### Supabase接続テスト

#### 13. Supabase接続テスト
```bash
cd backend
source venv/bin/activate
python test_supabase_connection.py
```
**処理内容**:
- Supabaseへの接続確認
- 各テーブルの存在確認
- RLSポリシーの確認
- 基本的なCRUD操作のテスト

**出力例**:
```
Supabase接続テストスクリプトを開始します...
=== 環境設定確認 ===
環境: development
Supabase URL: https://xxx.supabase.co
Supabase Service Key: eyJhbGciOiJIUzI1NiIs...
✅ すべての必須環境変数が設定されています

=== Supabase接続テスト ===
1. 接続テスト中...
✅ Supabaseに正常に接続しました

2. テーブル存在確認中...
✅ users テーブルが存在します
✅ journals テーブルが存在します
✅ moods テーブルが存在します
✅ profiles テーブルが存在します
✅ usage_counts テーブルが存在します
✅ analyses テーブルが存在します
✅ feature_limits テーブルが存在します

3. RLSポリシー確認中...
✅ users テーブルのRLSが有効です
✅ journals テーブルのRLSが有効です
✅ moods テーブルのRLSが有効です
✅ profiles テーブルのRLSが有効です
✅ usage_counts テーブルのRLSが有効です
✅ analyses テーブルのRLSが有効です
✅ feature_limits テーブルのRLSが有効です

4. 基本的なCRUD操作テスト中...
✅ テストユーザーの作成に成功しました
✅ テストユーザーの取得に成功しました
✅ テストユーザーの更新に成功しました
✅ テストユーザーの削除に成功しました

=== Supabase接続テスト完了 ===
✅ すべてのテストが成功しました
```

## 📊 API エンドポイント

### 認証
- `POST /api/auth/register` - ユーザー登録
- `POST /api/auth/login` - ユーザーログイン
- `GET /api/auth/me` - 現在のユーザー情報

### ユーザー管理
- `GET /api/users/` - ユーザー一覧
- `GET /api/users/me` - 現在のユーザー情報
- `PUT /api/users/me` - ユーザー情報更新

### プロフィール
- `GET /api/profiles/me` - 自分のプロフィール取得
- `POST /api/profiles/me` - プロフィール作成
- `PUT /api/profiles/me` - プロフィール更新

### ジャーナル
- `GET /api/journals/` - ジャーナル一覧
- `POST /api/journals/` - ジャーナル作成
- `PUT /api/journals/{id}` - ジャーナル更新
- `DELETE /api/journals/{id}` - ジャーナル削除

### 気分記録
- `GET /api/moods/` - 気分記録一覧
- `POST /api/moods/` - 気分記録作成
- `PUT /api/moods/{id}` - 気分記録更新
- `DELETE /api/moods/{id}` - 気分記録削除

### AI分析
- `GET /api/analysis/` - 分析結果一覧
- `POST /api/analysis/` - AI分析実行
- `GET /api/analysis/{id}` - 特定の分析結果

### 使用回数管理
- `GET /api/usage/status` - 使用回数状況
- `GET /api/usage/limits` - プラン別制限

### 管理者機能
- `GET /api/admin/users` - 全ユーザー一覧
- `PUT /api/admin/users/{id}/role` - ユーザーロール更新
- `GET /api/admin/users/role/{role}` - 特定ロールのユーザー一覧

## 🔧 トラブルシューティング

### よくある問題

#### 1. バックエンド起動エラー
```bash
ERROR: Error loading ASGI app. Could not import module "main".
```
**解決方法**:
```bash
cd backend  # backendディレクトリに移動してから実行
source venv/bin/activate
uvicorn main:app --reload
```

#### 2. CORSエラー
```
Access to fetch at 'http://localhost:8000/api/auth/login' from origin 'http://localhost:5173' has been blocked by CORS policy
```
**解決方法**: 
- `backend/main.py`のCORS設定を確認
- 環境変数`ENVIRONMENT`が正しく設定されているか確認
- `.env`ファイルで`ENVIRONMENT=development`を設定

#### 3. データベース接続エラー
```
[Errno 8] nodename nor servname provided, or not known
```
**解決方法**: 
- Supabaseの設定を確認
- `.env`ファイルの`SUPABASE_URL`と`SUPABASE_SERVICE_KEY`を正しく設定
- Supabase Dashboardでプロジェクトの設定を確認

#### 4. bcryptエラー
```bash
AttributeError: module 'bcrypt' has no attribute '__about__'
```
**解決方法**:
```bash
pip uninstall bcrypt -y && pip install bcrypt
```

#### 5. シーケンスリセットエラー
```
Could not find the function public.exec_sql(sql) in the schema cache
```
**解決方法**:
- Supabase DashboardのSQL Editorで手動実行
- 以下のSQLを実行:
```sql
ALTER SEQUENCE users_id_seq RESTART WITH 1;
ALTER SEQUENCE journals_id_seq RESTART WITH 1;
ALTER SEQUENCE moods_id_seq RESTART WITH 1;
ALTER SEQUENCE profiles_id_seq RESTART WITH 1;
ALTER SEQUENCE usage_counts_id_seq RESTART WITH 1;
ALTER SEQUENCE analyses_id_seq RESTART WITH 1;
ALTER SEQUENCE feature_limits_id_seq RESTART WITH 1;
```

#### 6. RLSポリシーエラー
```
new row violates row-level security policy for table "users"
```
**解決方法**:
- バックエンドが`SUPABASE_SERVICE_KEY`を使用しているか確認
- `backend/app/database/supabase_db.py`で`supabase_admin`クライアントを使用しているか確認

## 📝 開発メモ

### データベーステーブル構成
- `users` - ユーザー情報（ID, email, password, name, plan_type, role, created_at）
- `profiles` - プロフィール情報（ID, user_id, avatar_url, bio, preferences）
- `journals` - ジャーナル記録（ID, user_id, content, created_at）
- `moods` - 気分記録（ID, user_id, mood, note, created_at）
- `usage_counts` - 使用回数管理（ID, user_id, feature_type, usage_count, month）
- `feature_limits` - 機能制限設定（ID, feature_name, free_limit, premium_limit）
- `analyses` - AI分析結果（ID, user_id, analysis_type, summary, insights, recommendations）

### プラン制限
- **フリープラン**: ジャーナル10件/月、気分記録30件/月、AI分析3回/月
- **プレミアムプラン**: 無制限

### 認証フロー
1. ユーザー登録/ログイン
2. JWTトークン発行
3. フロントエンドでlocalStorageに保存
4. API呼び出し時にAuthorizationヘッダーに設定

### 環境変数設定
```env
# 環境設定
ENVIRONMENT=development  # development または production

# Supabase設定
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key

# JWT設定
JWT_SECRET=your-secret-key
JWT_EXPIRY=24  # 時間単位

# ログ設定
LOG_LEVEL=INFO
```

### セキュリティ設定
- **RLS (Row Level Security)**: すべてのテーブルで有効
- **JWT認証**: トークンベースの認証
- **パスワードハッシュ**: bcryptによる安全なハッシュ化
- **CORS設定**: 開発・本番環境に応じた設定

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。