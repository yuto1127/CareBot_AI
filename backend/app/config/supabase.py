from supabase import create_client, Client

# Supabase設定
SUPABASE_URL = "https://yfslwlwhnmkvkcuapqvs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlmc2x3bHdobm1rdmtjdWFwcXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0NDAzNzgsImV4cCI6MjA2OTAxNjM3OH0.cfK5sLZASwVuFRVEIDEMNvetHIRYtAKaIpaq9RT-T_Y"

# Supabaseクライアントの初期化
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) 