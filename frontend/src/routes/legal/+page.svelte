<script lang="ts">
  import { goto } from '$app/navigation';
  import { fetchAPI } from '$lib/api';

  let agreedToPrivacyPolicy = false;
  let agreedToTermsOfService = false;
  let agreedToSafetyGuidelines = false;
  let loading = false;
  let error = '';

  async function handleAgree() {
    if (agreedToPrivacyPolicy && agreedToTermsOfService && agreedToSafetyGuidelines) {
      loading = true;
      error = '';

      try {
        // バックエンドに同意記録を送信
        await fetchAPI('/auth/legal-agreement', {
          method: 'POST',
          body: JSON.stringify({
            privacy_policy_agreed: true,
            terms_of_service_agreed: true,
            safety_guidelines_agreed: true
          })
        });

        // 同意をlocalStorageに保存
        localStorage.setItem('legal_agreement', 'true');
        localStorage.setItem('agreement_date', new Date().toISOString());
        
        // 登録ページにリダイレクト
        goto('/register');
      } catch (err: any) {
        console.error('同意記録エラー:', err);
        error = '同意の記録に失敗しました。もう一度お試しください。';
      } finally {
        loading = false;
      }
    }
  }

  function handleDecline() {
    // ホームページに戻る
    goto('/');
  }
</script>

<main class="min-h-screen bg-gray-50 py-8">
  <div class="max-w-4xl mx-auto px-4">
    <div class="bg-white rounded-lg shadow-lg p-8">
      <h1 class="text-3xl font-bold text-center mb-8 text-blue-600">
        法的・倫理的ポジショニング
      </h1>
      
      <div class="space-y-8">
        <!-- プライバシーポリシー -->
        <section class="border-b pb-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-semibold text-gray-800">1. プライバシーポリシー</h2>
            <a 
              href="/privacy-policy" 
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors text-sm"
            >
              詳細を見る
            </a>
          </div>
          
          <div class="space-y-4 text-gray-700">
            <div>
              <h3 class="text-lg font-medium mb-2">メンタルヘルスデータの取り扱い方針</h3>
              <p class="text-sm leading-relaxed">
                当アプリケーションは、ユーザーのメンタルヘルスに関する情報を慎重に取り扱います。
                日記、気分記録、分析結果などの個人情報は、適切な暗号化とアクセス制御により保護されます。
              </p>
            </div>
            
            <div>
              <h3 class="text-lg font-medium mb-2">要配慮個人情報の保護措置</h3>
              <p class="text-sm leading-relaxed">
                メンタルヘルス情報は要配慮個人情報として扱い、以下の措置を講じます：
              </p>
              <ul class="text-sm list-disc list-inside mt-2 space-y-1">
                <li>データの暗号化保存</li>
                <li>アクセス権限の厳格な管理</li>
                <li>定期的なセキュリティ監査</li>
                <li>従業員への教育・訓練</li>
              </ul>
            </div>
            
            <div>
              <h3 class="text-lg font-medium mb-2">第三者提供禁止</h3>
              <p class="text-sm leading-relaxed">
                ユーザーの個人情報、特にメンタルヘルスに関する情報を第三者に提供することはありません。
                ただし、法的義務がある場合や、ユーザーの明示的な同意がある場合は除きます。
              </p>
            </div>
            
            <div>
              <h3 class="text-lg font-medium mb-2">データ削除権</h3>
              <p class="text-sm leading-relaxed">
                ユーザーはいつでもアカウントの削除を要求でき、その際は関連するすべてのデータを完全に削除します。
                データ削除後は復元できませんのでご注意ください。
              </p>
            </div>
          </div>
        </section>

        <!-- 利用規約 -->
        <section class="border-b pb-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-semibold text-gray-800">2. 利用規約</h2>
            <a 
              href="/terms-of-service" 
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors text-sm"
            >
              詳細を見る
            </a>
          </div>
          
          <div class="space-y-4 text-gray-700">
            <div>
              <h3 class="text-lg font-medium mb-2">医療機器規制回避の文言統一</h3>
              <p class="text-sm leading-relaxed">
                本アプリケーションは医療機器ではありません。診断、治療、予防を目的としたものではなく、
                あくまでセルフケアと自己理解をサポートするツールとして提供されます。
              </p>
            </div>
            
            <div>
              <h3 class="text-lg font-medium mb-2">「ウェルネス」「セルフケア」「自己理解」への用語変更</h3>
              <p class="text-sm leading-relaxed">
                当アプリケーションでは以下の用語を使用します：
              </p>
              <ul class="text-sm list-disc list-inside mt-2 space-y-1">
                <li><strong>ウェルネス</strong>：心身の健康維持と向上</li>
                <li><strong>セルフケア</strong>：自己管理による健康維持</li>
                <li><strong>自己理解</strong>：自分の感情や思考パターンの理解</li>
              </ul>
            </div>
            
            <div>
              <h3 class="text-lg font-medium mb-2">免責事項</h3>
              <p class="text-sm leading-relaxed">
                当アプリケーションの利用により生じるいかなる問題についても、当社は責任を負いません。
                深刻なメンタルヘルスの問題がある場合は、必ず専門家に相談してください。
              </p>
            </div>
          </div>
        </section>

        <!-- セーフティガード機能 -->
        <section class="border-b pb-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-semibold text-gray-800">3. セーフティガード機能</h2>
            <a 
              href="/safety-guidelines" 
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors text-sm"
            >
              詳細を見る
            </a>
          </div>
          
          <div class="space-y-4 text-gray-700">
            <div>
              <h3 class="text-lg font-medium mb-2">危機的状況検知システム</h3>
              <p class="text-sm leading-relaxed">
                当アプリケーションは、ユーザーの入力内容を分析し、危機的状況を検知する機能を備えています。
                自傷や他害の可能性が検知された場合、適切な対応を行います。
              </p>
            </div>
            
            <div>
              <h3 class="text-lg font-medium mb-2">専門機関誘導プロトコル</h3>
              <p class="text-sm leading-relaxed">
                危機的状況が検知された場合、以下のプロトコルに従います：
              </p>
              <ul class="text-sm list-disc list-inside mt-2 space-y-1">
                <li>専門機関への連絡情報の提供</li>
                <li>緊急時の対応手順の案内</li>
                <li>必要に応じた関係者への通知</li>
              </ul>
            </div>
            
            <div>
              <h3 class="text-lg font-medium mb-2">AIの行動制限プロンプト</h3>
              <p class="text-sm leading-relaxed">
                AIシステムは以下の制限を設けています：
              </p>
              <ul class="text-sm list-disc list-inside mt-2 space-y-1">
                <li>医療診断や治療の提案は行わない</li>
                <li>薬物の使用を推奨しない</li>
                <li>危険な行為を助長しない</li>
                <li>専門家の助言を優先する</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- 同意チェックボックス -->
        <section class="bg-blue-50 p-6 rounded-lg">
          <h2 class="text-xl font-semibold mb-4 text-blue-800">同意確認</h2>
          
          <div class="space-y-4">
            <label class="flex items-start space-x-3">
              <input
                type="checkbox"
                bind:checked={agreedToPrivacyPolicy}
                class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span class="text-sm text-gray-700">
                プライバシーポリシーに同意します
              </span>
            </label>
            
            <label class="flex items-start space-x-3">
              <input
                type="checkbox"
                bind:checked={agreedToTermsOfService}
                class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span class="text-sm text-gray-700">
                利用規約に同意します
              </span>
            </label>
            
            <label class="flex items-start space-x-3">
              <input
                type="checkbox"
                bind:checked={agreedToSafetyGuidelines}
                class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span class="text-sm text-gray-700">
                セーフティガード機能について理解し、同意します
              </span>
            </label>
          </div>
        </section>

        <!-- エラーメッセージ -->
        {#if error}
          <div class="mb-4 p-3 bg-red-100 text-red-700 rounded text-center">
            {error}
          </div>
        {/if}

        <!-- ボタン -->
        <div class="flex justify-center space-x-4">
          <button
            on:click={handleAgree}
            disabled={!agreedToPrivacyPolicy || !agreedToTermsOfService || !agreedToSafetyGuidelines || loading}
            class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? '処理中...' : '同意して登録に進む'}
          </button>
          
          <button
            on:click={handleDecline}
            class="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
          >
            同意しない
          </button>
        </div>

        <div class="text-center text-sm text-gray-500 mt-4">
          <p>同意しない場合、アプリケーションの利用はできません。</p>
        </div>
      </div>
    </div>
  </div>
</main> 