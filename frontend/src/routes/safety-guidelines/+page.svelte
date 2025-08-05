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
        <h1 class="text-3xl font-bold text-blue-600">セーフティガード機能</h1>
        <button
          on:click={goBack}
          class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
        >
          戻る
        </button>
      </div>
      
      <div class="space-y-8 text-gray-700">
        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">1. 危機的状況検知システム</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              当アプリケーションは、ユーザーの入力内容を分析し、危機的状況を検知する機能を備えています。
              自傷や他害の可能性が検知された場合、適切な対応を行います。
            </p>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="bg-red-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-red-800">検知対象</h3>
                <ul class="text-sm space-y-1">
                  <li>• 自傷・自殺の可能性</li>
                  <li>• 他者への危害の可能性</li>
                  <li>• 深刻な精神的不調</li>
                  <li>• 薬物・アルコールの乱用</li>
                  <li>• 極端な孤立・引きこもり</li>
                </ul>
              </div>
              <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-blue-800">検知方法</h3>
                <ul class="text-sm space-y-1">
                  <li>• AIによる自然言語分析</li>
                  <li>• キーワード・フレーズ検出</li>
                  <li>• 感情分析による異常検知</li>
                  <li>• 行動パターンの変化検知</li>
                  <li>• 複数指標の組み合わせ分析</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">2. 専門機関誘導プロトコル</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              危機的状況が検知された場合、以下のプロトコルに従います：
            </p>
            <div class="space-y-4">
              <div class="bg-yellow-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-yellow-800">即座の対応</h3>
                <ul class="text-sm space-y-1">
                  <li>• 危機的状況の確認メッセージ表示</li>
                  <li>• 緊急時の専門機関連絡情報の提供</li>
                  <li>• 安全確認のための質問</li>
                  <li>• 専門家への相談を強く推奨</li>
                </ul>
              </div>
              <div class="bg-orange-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-orange-800">専門機関情報</h3>
                <ul class="text-sm space-y-1">
                  <li>• 自殺防止相談窓口：0120-738-556</li>
                  <li>• 精神保健福祉センター</li>
                  <li>• 地域の精神科医療機関</li>
                  <li>• カウンセリングセンター</li>
                  <li>• 緊急時：119番（救急）</li>
                </ul>
              </div>
              <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-green-800">フォローアップ</h3>
                <ul class="text-sm space-y-1">
                  <li>• 専門機関受診の確認</li>
                  <li>• 継続的なサポートの提供</li>
                  <li>• 家族・友人への相談推奨</li>
                  <li>• 定期的な状況確認</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">3. AIの行動制限プロンプト</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              AIシステムは以下の制限を設けています：
            </p>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="bg-red-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-red-800">禁止事項</h3>
                <ul class="text-sm space-y-1">
                  <li>• 医療診断や治療の提案</li>
                  <li>• 薬物の使用を推奨</li>
                  <li>• 危険な行為を助長</li>
                  <li>• 具体的な自傷方法の説明</li>
                  <li>• 他者への危害を推奨</li>
                </ul>
              </div>
              <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-blue-800">推奨事項</h3>
                <ul class="text-sm space-y-1">
                  <li>• 専門家の助言を優先</li>
                  <li>• 安全な対処法の提案</li>
                  <li>• 専門機関への相談推奨</li>
                  <li>• 家族・友人への相談推奨</li>
                  <li>• 緊急時の対応手順説明</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">4. 緊急時対応フロー</h2>
          <div class="space-y-4">
            <div class="bg-red-100 p-6 rounded-lg border-l-4 border-red-500">
              <h3 class="text-xl font-semibold mb-4 text-red-800">緊急時の対応手順</h3>
              <div class="space-y-3">
                <div class="flex items-start space-x-3">
                  <span class="bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">1</span>
                  <div>
                    <h4 class="font-medium text-red-800">即座の安全確認</h4>
                    <p class="text-sm">現在の状況を確認し、安全を最優先に考えます</p>
                  </div>
                </div>
                <div class="flex items-start space-x-3">
                  <span class="bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">2</span>
                  <div>
                    <h4 class="font-medium text-red-800">専門機関への連絡</h4>
                    <p class="text-sm">適切な専門機関への連絡を強く推奨します</p>
                  </div>
                </div>
                <div class="flex items-start space-x-3">
                  <span class="bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">3</span>
                  <div>
                    <h4 class="font-medium text-red-800">家族・友人への相談</h4>
                    <p class="text-sm">信頼できる人に相談することを推奨します</p>
                  </div>
                </div>
                <div class="flex items-start space-x-3">
                  <span class="bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">4</span>
                  <div>
                    <h4 class="font-medium text-red-800">継続的なサポート</h4>
                    <p class="text-sm">専門家の指導のもと、継続的なケアを受けます</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">5. データ保護とプライバシー</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              危機的状況の検知と対応においても、ユーザーのプライバシーを最大限に保護します：
            </p>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-green-800">保護措置</h3>
                <ul class="text-sm space-y-1">
                  <li>• データの暗号化保存</li>
                  <li>• アクセス権限の厳格な管理</li>
                  <li>• 最小限の情報共有</li>
                  <li>• ユーザーの同意に基づく対応</li>
                </ul>
              </div>
              <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-blue-800">例外事項</h3>
                <ul class="text-sm space-y-1">
                  <li>• 緊急時の人命保護</li>
                  <li>• 法的義務がある場合</li>
                  <li>• ユーザーの明示的な同意</li>
                  <li>• 専門機関との連携</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">6. システムの限界</h2>
          <div class="space-y-4">
            <div class="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500">
              <h3 class="text-lg font-medium mb-2 text-yellow-800">重要な注意事項</h3>
              <p class="text-sm leading-relaxed">
                本システムは完璧ではありません。AIによる検知には限界があり、
                すべての危機的状況を正確に検知できるわけではありません。
                ユーザー自身の判断と専門家の助言を最優先にしてください。
              </p>
            </div>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="bg-red-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-red-800">システムの限界</h3>
                <ul class="text-sm space-y-1">
                  <li>• 誤検知の可能性</li>
                  <li>• 見逃しの可能性</li>
                  <li>• 文脈理解の限界</li>
                  <li>• 文化的・言語的差異</li>
                </ul>
              </div>
              <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-green-800">推奨される対応</h3>
                <ul class="text-sm space-y-1">
                  <li>• 専門家の判断を優先</li>
                  <li>• 自己判断の重要性</li>
                  <li>• 複数の情報源の活用</li>
                  <li>• 継続的な学習・改善</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">7. お問い合わせ</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              セーフティガード機能に関するお問い合わせは、以下の方法でお受けいたします：
            </p>
            <div class="bg-gray-50 p-4 rounded-lg">
              <ul class="text-sm space-y-1">
                <li>• メール：safety@carebot-ai.com</li>
                <li>• お問い合わせフォーム：アプリ内の「お問い合わせ」から</li>
                <li>• 対応時間：平日 9:00-18:00（土日祝日除く）</li>
                <li>• 緊急時：各専門機関に直接お問い合わせください</li>
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