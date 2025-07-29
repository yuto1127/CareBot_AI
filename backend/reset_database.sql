-- SupabaseデータベースリセットSQLスクリプト
-- 各テーブルのデータを削除し、IDを1から再開するように設定

-- ========================================
-- 1. データ削除
-- ========================================

-- analysesテーブルのデータを削除
DELETE FROM analyses WHERE id > 0;

-- feature_limitsテーブルのデータを削除
DELETE FROM feature_limits WHERE id > 0;

-- journalsテーブルのデータを削除
DELETE FROM journals WHERE id > 0;

-- moodsテーブルのデータを削除
DELETE FROM moods WHERE id > 0;

-- profilesテーブルのデータを削除
DELETE FROM profiles WHERE id > 0;

-- usage_countsテーブルのデータを削除
DELETE FROM usage_counts WHERE id > 0;

-- usersテーブルのデータを削除
DELETE FROM users WHERE id > 0;

-- ========================================
-- 2. シーケンスリセット
-- ========================================

-- analysesテーブルのシーケンスをリセット
ALTER SEQUENCE analyses_id_seq RESTART WITH 1;

-- feature_limitsテーブルのシーケンスをリセット
ALTER SEQUENCE feature_limits_id_seq RESTART WITH 1;

-- journalsテーブルのシーケンスをリセット
ALTER SEQUENCE journals_id_seq RESTART WITH 1;

-- moodsテーブルのシーケンスをリセット
ALTER SEQUENCE moods_id_seq RESTART WITH 1;

-- profilesテーブルのシーケンスをリセット
ALTER SEQUENCE profiles_id_seq RESTART WITH 1;

-- usage_countsテーブルのシーケンスをリセット
ALTER SEQUENCE usage_counts_id_seq RESTART WITH 1;

-- usersテーブルのシーケンスをリセット
ALTER SEQUENCE users_id_seq RESTART WITH 1;

-- ========================================
-- 3. 確認クエリ
-- ========================================

-- 各テーブルのデータ数を確認
SELECT 'analyses' as table_name, COUNT(*) as count FROM analyses
UNION ALL
SELECT 'feature_limits' as table_name, COUNT(*) as count FROM feature_limits
UNION ALL
SELECT 'journals' as table_name, COUNT(*) as count FROM journals
UNION ALL
SELECT 'moods' as table_name, COUNT(*) as count FROM moods
UNION ALL
SELECT 'profiles' as table_name, COUNT(*) as count FROM profiles
UNION ALL
SELECT 'usage_counts' as table_name, COUNT(*) as count FROM usage_counts
UNION ALL
SELECT 'users' as table_name, COUNT(*) as count FROM users;

-- シーケンスの現在値を確認
SELECT 'analyses_id_seq' as sequence_name, last_value FROM analyses_id_seq
UNION ALL
SELECT 'feature_limits_id_seq' as sequence_name, last_value FROM feature_limits_id_seq
UNION ALL
SELECT 'journals_id_seq' as sequence_name, last_value FROM journals_id_seq
UNION ALL
SELECT 'moods_id_seq' as sequence_name, last_value FROM moods_id_seq
UNION ALL
SELECT 'profiles_id_seq' as sequence_name, last_value FROM profiles_id_seq
UNION ALL
SELECT 'usage_counts_id_seq' as sequence_name, last_value FROM usage_counts_id_seq
UNION ALL
SELECT 'users_id_seq' as sequence_name, last_value FROM users_id_seq; 