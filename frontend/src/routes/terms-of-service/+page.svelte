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
        <h1 class="text-3xl font-bold text-blue-600">利用規約</h1>
        <button
          on:click={goBack}
          class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
        >
          戻る
        </button>
      </div>
      
      <div class="space-y-8 text-gray-700">
        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">1. サービスの概要</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              CareBot AIは、メンタルウェルネスをサポートするAIアシスタントアプリケーションです。
              本サービスは、ユーザーの自己理解とセルフケアを促進することを目的としています。
            </p>
            <div class="bg-blue-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium mb-2 text-blue-800">提供機能</h3>
              <ul class="text-sm space-y-1">
                <li>• ジャーナル記録機能</li>
                <li>• 気分記録・分析機能</li>
                <li>• AI分析・洞察機能</li>
                <li>• CBT（認知行動療法）セッション</li>
                <li>• 瞑想・リラクゼーション機能</li>
                <li>• ポモドーロタイマー</li>
              </ul>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">2. 医療機器規制回避の文言統一</h2>
          <div class="space-y-4">
            <div class="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
              <h3 class="text-lg font-medium mb-2 text-red-800">重要なお知らせ</h3>
              <p class="text-sm leading-relaxed">
                本アプリケーションは医療機器ではありません。診断、治療、予防を目的としたものではなく、
                あくまでセルフケアと自己理解をサポートするツールとして提供されます。
              </p>
            </div>
            <div class="bg-yellow-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium mb-2 text-yellow-800">医療機器ではない理由</h3>
              <ul class="text-sm space-y-1">
                <li>• 医療診断を行わない</li>
                <li>• 治療方法を提案しない</li>
                <li>• 医薬品の使用を推奨しない</li>
                <li>• 医療行為の代替ではない</li>
                <li>• 専門家の助言を優先する</li>
              </ul>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">3. 用語の定義</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              当アプリケーションでは以下の用語を使用します：
            </p>
            <div class="grid md:grid-cols-3 gap-4">
              <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-green-800">ウェルネス</h3>
                <p class="text-sm">
                  心身の健康維持と向上を指します。身体的、精神的、社会的に良好な状態を目指す包括的な概念です。
                </p>
              </div>
              <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-blue-800">セルフケア</h3>
                <p class="text-sm">
                  自己管理による健康維持を指します。自分自身で行う健康管理活動全般を意味します。
                </p>
              </div>
              <div class="bg-purple-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-purple-800">自己理解</h3>
                <p class="text-sm">
                  自分の感情や思考パターンの理解を指します。自己認識と内省を通じた成長を目指します。
                </p>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">4. 利用条件</h2>
          <div class="space-y-4">
            <div class="bg-gray-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium mb-2 text-gray-800">利用可能な方</h3>
              <ul class="text-sm space-y-1">
                <li>• 13歳以上の方</li>
                <li>• 有効なメールアドレスをお持ちの方</li>
                <li>• 本規約に同意いただける方</li>
                <li>• 適切な使用目的でご利用いただける方</li>
              </ul>
            </div>
            <div class="bg-red-50 p-4 rounded-lg">
              <h3 class="text-lg font-medium mb-2 text-red-800">禁止事項</h3>
              <ul class="text-sm space-y-1">
                <li>• 他人のアカウントを使用すること</li>
                <li>• サービスを悪用すること</li>
                <li>• 不適切なコンテンツを投稿すること</li>
                <li>• システムに負荷をかける行為</li>
                <li>• 他のユーザーに迷惑をかける行為</li>
              </ul>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">5. 免責事項</h2>
          <div class="space-y-4">
            <div class="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-500">
              <h3 class="text-lg font-medium mb-2 text-orange-800">重要な免責事項</h3>
              <p class="text-sm leading-relaxed">
                当アプリケーションの利用により生じるいかなる問題についても、当社は責任を負いません。
                深刻なメンタルヘルスの問題がある場合は、必ず専門家に相談してください。
              </p>
            </div>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="bg-yellow-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-yellow-800">当社の責任範囲外</h3>
                <ul class="text-sm space-y-1">
                  <li>• 医療診断・治療</li>
                  <li>• 緊急時の対応</li>
                  <li>• 専門的なカウンセリング</li>
                  <li>• 薬物療法の提案</li>
                  <li>• 法的助言</li>
                </ul>
              </div>
              <div class="bg-green-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-green-800">推奨される対応</h3>
                <ul class="text-sm space-y-1">
                  <li>• 専門家への相談</li>
                  <li>• 医療機関の受診</li>
                  <li>• カウンセリングの利用</li>
                  <li>• 緊急時の専門機関連絡</li>
                  <li>• 家族・友人への相談</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">6. サービス利用制限</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              プランに応じて以下の利用制限が適用されます：
            </p>
            <div class="grid md:grid-cols-2 gap-4">
              <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-blue-800">フリープラン</h3>
                <ul class="text-sm space-y-1">
                  <li>• ジャーナル：月10件まで</li>
                  <li>• 気分記録：月30件まで</li>
                  <li>• AI分析：月3回まで</li>
                  <li>• CBT：月5回まで</li>
                  <li>• 瞑想：月10回まで</li>
                </ul>
              </div>
              <div class="bg-purple-50 p-4 rounded-lg">
                <h3 class="text-lg font-medium mb-2 text-purple-800">プレミアムプラン</h3>
                <ul class="text-sm space-y-1">
                  <li>• ジャーナル：無制限</li>
                  <li>• 気分記録：無制限</li>
                  <li>• AI分析：無制限</li>
                  <li>• CBT：無制限</li>
                  <li>• 瞑想：無制限</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">7. 知的財産権</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              本サービスのコンテンツ、デザイン、技術等に関する知的財産権は当社に帰属します。
              ユーザーが作成したコンテンツの著作権はユーザーに帰属します。
            </p>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">8. 規約の変更</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              当社は、必要に応じて本規約を変更することがあります。
              変更があった場合は、アプリケーション内でお知らせいたします。
              変更後もサービスを継続してご利用いただく場合、変更された規約に同意したものとみなします。
            </p>
          </div>
        </section>

        <section>
          <h2 class="text-2xl font-semibold mb-4 text-gray-800">9. お問い合わせ</h2>
          <div class="space-y-4">
            <p class="text-sm leading-relaxed">
              利用規約に関するお問い合わせは、以下の方法でお受けいたします：
            </p>
            <div class="bg-gray-50 p-4 rounded-lg">
              <ul class="text-sm space-y-1">
                <li>• メール：terms@carebot-ai.com</li>
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