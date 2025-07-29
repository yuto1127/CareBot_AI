-- CareBot AI - RLSポリシー設定スクリプト
-- 本番環境用のセキュリティ設定

-- ========================================
-- users テーブル
-- ========================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- ユーザーは自分のデータのみ読み取り可能
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (auth.uid()::text = id::text);

-- ユーザーは自分のデータのみ更新可能
CREATE POLICY "Users can update own data" ON users
  FOR UPDATE USING (auth.uid()::text = id::text);

-- 新規ユーザー登録時のみ挿入可能
CREATE POLICY "Users can insert own data" ON users
  FOR INSERT WITH CHECK (auth.uid()::text = id::text);

-- ========================================
-- profiles テーブル
-- ========================================
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- ユーザーは自分のプロフィールのみ読み取り可能
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid()::text = user_id::text);

-- ユーザーは自分のプロフィールのみ作成可能
CREATE POLICY "Users can create own profile" ON profiles
  FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- ユーザーは自分のプロフィールのみ更新可能
CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid()::text = user_id::text);

-- ユーザーは自分のプロフィールのみ削除可能
CREATE POLICY "Users can delete own profile" ON profiles
  FOR DELETE USING (auth.uid()::text = user_id::text);

-- ========================================
-- journals テーブル
-- ========================================
ALTER TABLE journals ENABLE ROW LEVEL SECURITY;

-- ユーザーは自分のジャーナルのみ読み取り可能
CREATE POLICY "Users can view own journals" ON journals
  FOR SELECT USING (auth.uid()::text = user_id::text);

-- ユーザーは自分のジャーナルのみ作成可能
CREATE POLICY "Users can create own journals" ON journals
  FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- ユーザーは自分のジャーナルのみ更新可能
CREATE POLICY "Users can update own journals" ON journals
  FOR UPDATE USING (auth.uid()::text = user_id::text);

-- ユーザーは自分のジャーナルのみ削除可能
CREATE POLICY "Users can delete own journals" ON journals
  FOR DELETE USING (auth.uid()::text = user_id::text);

-- ========================================
-- moods テーブル
-- ========================================
ALTER TABLE moods ENABLE ROW LEVEL SECURITY;

-- ユーザーは自分の気分記録のみ読み取り可能
CREATE POLICY "Users can view own moods" ON moods
  FOR SELECT USING (auth.uid()::text = user_id::text);

-- ユーザーは自分の気分記録のみ作成可能
CREATE POLICY "Users can create own moods" ON moods
  FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- ユーザーは自分の気分記録のみ更新可能
CREATE POLICY "Users can update own moods" ON moods
  FOR UPDATE USING (auth.uid()::text = user_id::text);

-- ユーザーは自分の気分記録のみ削除可能
CREATE POLICY "Users can delete own moods" ON moods
  FOR DELETE USING (auth.uid()::text = user_id::text);

-- ========================================
-- usage_counts テーブル
-- ========================================
ALTER TABLE usage_counts ENABLE ROW LEVEL SECURITY;

-- ユーザーは自分の使用回数のみ読み取り可能
CREATE POLICY "Users can view own usage" ON usage_counts
  FOR SELECT USING (auth.uid()::text = user_id::text);

-- ユーザーは自分の使用回数のみ作成可能
CREATE POLICY "Users can create own usage" ON usage_counts
  FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- ユーザーは自分の使用回数のみ更新可能
CREATE POLICY "Users can update own usage" ON usage_counts
  FOR UPDATE USING (auth.uid()::text = user_id::text);

-- ユーザーは自分の使用回数のみ削除可能
CREATE POLICY "Users can delete own usage" ON usage_counts
  FOR DELETE USING (auth.uid()::text = user_id::text);

-- ========================================
-- analyses テーブル
-- ========================================
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;

-- ユーザーは自分の分析結果のみ読み取り可能
CREATE POLICY "Users can view own analyses" ON analyses
  FOR SELECT USING (auth.uid()::text = user_id::text);

-- ユーザーは自分の分析結果のみ作成可能
CREATE POLICY "Users can create own analyses" ON analyses
  FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- ユーザーは自分の分析結果のみ更新可能
CREATE POLICY "Users can update own analyses" ON analyses
  FOR UPDATE USING (auth.uid()::text = user_id::text);

-- ユーザーは自分の分析結果のみ削除可能
CREATE POLICY "Users can delete own analyses" ON analyses
  FOR DELETE USING (auth.uid()::text = user_id::text);

-- ========================================
-- feature_limits テーブル
-- ========================================
ALTER TABLE feature_limits ENABLE ROW LEVEL SECURITY;

-- 全ユーザーが機能制限を読み取り可能（公開情報）
CREATE POLICY "Anyone can view feature limits" ON feature_limits
  FOR SELECT USING (true);

-- 管理者のみ更新可能（service_roleキーを使用）
CREATE POLICY "Only admins can update feature limits" ON feature_limits
  FOR UPDATE USING (auth.role() = 'service_role');

-- 管理者のみ挿入可能
CREATE POLICY "Only admins can insert feature limits" ON feature_limits
  FOR INSERT WITH CHECK (auth.role() = 'service_role');

-- 管理者のみ削除可能
CREATE POLICY "Only admins can delete feature limits" ON feature_limits
  FOR DELETE USING (auth.role() = 'service_role');

-- ========================================
-- 設定確認クエリ
-- ========================================
-- RLSが有効化されているテーブルを確認
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY tablename;

-- 各テーブルのポリシー数を確認
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname; 