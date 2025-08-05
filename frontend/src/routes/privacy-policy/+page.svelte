<script lang="ts">
  import { goto } from '$app/navigation';

  function goBack() {
    goto('/legal');
  }
</script>

<main class="min-h-screen bg-gray-50 py-8">
  <div class="max-w-4xl mx-auto px-4">
    <div class="bg-white rounded-lg shadow-lg p-8">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-blue-600">プライバシーポリシー</h1>
        <button
          on:click={goBack}
          class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
        >
          戻る
        </button>
      </div>
      
      <div class="space-y-8 text-gray-700">
        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">1. 情報収集について</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              当アプリケーションでは、以下の情報を収集いたします：
            </p>
            <ul class="text-sm list-disc list-inside space-y-2 ml-4">
              <li>アカウント情報（メールアドレス、ユーザー名）</li>
              <li>プロフィール情報（アバター、自己紹介、設定）</li>
              <li>ジャーナル記録（日記の内容）</li>
              <li>気分記録（気分スコア、メモ）</li>
              <li>使用履歴（機能の利用回数、利用日時）</li>
              <li>AI分析結果（分析内容、推奨事項）</li>
            </ul>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">2. メンタルヘルスデータの取り扱い方針</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              当アプリケーションは、ユーザーのメンタルヘルスに関する情報を慎重に取り扱います。
              日記、気分記録、分析結果などの個人情報は、適切な暗号化とアクセス制御により保護されます。
            </p>
            <div class="bg-blue-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium mb-2 text-blue-800">特別な保護措置</h3>
              <ul class="text-sm space-y-1">
                <li>• データの暗号化保存（AES-256）</li>
                <li>• アクセス権限の厳格な管理</li>
                <li>• 定期的なセキュリティ監査</li>
                <li>• 従業員への教育・訓練</li>
                <li>• データアクセスログの記録</li>
              </ul>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">3. 要配慮個人情報の保護措置</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              メンタルヘルス情報は要配慮個人情報として扱い、以下の措置を講じます：
            </p>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-green-800">技術的保護措置</h3>
                <ul class="text-sm space-y-1">
                  <li>• データベースの暗号化</li>
                  <li>• 通信の暗号化（HTTPS）</li>
                  <li>• アクセス制御システム</li>
                  <li>• データバックアップの暗号化</li>
                </ul>
              </div>
              <div class="bg-yellow-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-yellow-800">組織的保護措置</h3>
                <ul class="text-sm space-y-1">
                  <li>• アクセス権限の管理</li>
                  <li>• 従業員の教育・訓練</li>
                  <li>• 定期的な監査</li>
                  <li>• インシデント対応体制</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">4. 第三者提供禁止</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              ユーザーの個人情報、特にメンタルヘルスに関する情報を第三者に提供することはありません。
              ただし、以下の場合は除きます：
            </p>
            <div class="bg-red-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium mb-2 text-red-800">例外事項</h3>
              <ul class="text-sm space-y-1">
                <li>• 法的義務がある場合</li>
                <li>• ユーザーの明示的な同意がある場合</li>
                <li>• 緊急時の人命保護のため必要な場合</li>
                <li>• 統計情報として個人を特定できない形で提供する場合</li>
              </ul>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">5. データ削除権</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              ユーザーはいつでもアカウントの削除を要求でき、その際は関連するすべてのデータを完全に削除します。
            </p>
            <div class="bg-orange-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium mb-2 text-orange-800">削除されるデータ</h3>
              <ul class="text-sm space-y-1">
                <li>• アカウント情報</li>
                <li>• プロフィール情報</li>
                <li>• ジャーナル記録</li>
                <li>• 気分記録</li>
                <li>• AI分析結果</li>
                <li>• 使用履歴</li>
              </ul>
              <p class="text-xs mt-2 text-orange-700">
                ※ データ削除後は復元できませんのでご注意ください
              </p>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">6. データ保持期間</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              ユーザーデータは以下の期間保持されます：
            </p>
            <ul class="text-sm list-disc list-inside space-y-2 ml-4">
              <li>アカウント削除まで：ユーザーがアカウントを削除するまで</li>
              <li>ログデータ：最大1年間</li>
              <li>バックアップデータ：最大30日間</li>
            </ul>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">7. お問い合わせ</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              プライバシーポリシーに関するお問い合わせは、以下の方法でお受けいたします：
            </p>
            <div class="bg-gray-50 p-4 rounded-lg">
              <ul class="text-sm space-y-1">
                <li>• メール：privacy@carebot-ai.com</li>
                <li>• お問い合わせフォーム：アプリ内の「お問い合わせ」から</li>
                <li>• 対応時間：平日 9:00-18:00（土日祝日除く）</li>
              </ul>
            </div>
          </div>
        </section>

        <div class="text-center text-xs text-gray-500 mt-8 pt-4 border-t">
          <p>最終更新日：2024年1月1日</p>
        </div>
      </div>
    </div>
  </div>
</main> 