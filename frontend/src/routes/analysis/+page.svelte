<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';

  let analyses: any[] = [];
  let loading = false;
  let error = '';
  let isLoggedIn = false;
  let selectedAnalysisType = 'general';

  const analysisTypes = [
    { value: 'general', label: '総合分析' },
    { value: 'mood_trend', label: '気分傾向分析' },
    { value: 'stress_analysis', label: 'ストレス分析' }
  ];

  onMount(() => {
    const token = localStorage.getItem('token');
    isLoggedIn = !!token;
    if (isLoggedIn) {
      loadAnalyses();
    }
  });

  async function loadAnalyses() {
    try {
      analyses = await fetchAPI('/analysis');
    } catch (err) {
      console.error('分析履歴の取得に失敗しました:', err);
    }
  }

  async function runAnalysis() {
    loading = true;
    error = '';

    try {
      const result = await fetchAPI('/analysis', {
        method: 'POST',
        body: JSON.stringify({
          analysis_type: selectedAnalysisType
        })
      });

      // 分析結果を履歴に追加
      analyses.unshift(result);
    } catch (err: any) {
      if (err.message && err.message.includes('使用回数制限')) {
        error = 'AI分析の使用回数制限に達しました。プレミアムプランにアップグレードしてください。';
      } else {
        error = '分析の実行に失敗しました。';
      }
    } finally {
      loading = false;
    }
  }

  async function deleteAnalysis(id: number) {
    try {
      await fetchAPI(`/analysis/${id}`, { method: 'DELETE' });
      analyses = analyses.filter(a => a.id !== id);
    } catch (err) {
      console.error('分析の削除に失敗しました:', err);
    }
  }

  function getAnalysisTypeLabel(type: string) {
    const found = analysisTypes.find(t => t.value === type);
    return found ? found.label : type;
  }

  function getStressLevelColor(level: string) {
    switch (level) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  }
</script>

<div class="p-4">
  <div class="flex justify-between items-center mb-4">
    <a href="/" class="inline-block mb-4 bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded shadow">ホームに戻る</a>
    <div class="flex gap-2">
      {#if isLoggedIn}
        <a href="/dashboard" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded shadow">ダッシュボード</a>
        <a href="/profile" class="bg-gray-500 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded shadow">プロフィール</a>
      {:else}
        <a href="/login" class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded shadow">ログイン</a>
        <a href="/register" class="bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2 px-4 rounded shadow">新規登録</a>
      {/if}
    </div>
  </div>

  <h1 class="text-2xl font-bold mb-6 text-purple-600">AI分析</h1>

  {#if !isLoggedIn}
    <div class="bg-yellow-50 border border-yellow-200 rounded-md p-4 mb-6">
      <p class="text-yellow-800">ログインするとAI分析機能をご利用いただけます。</p>
      <a href="/login" class="text-blue-600 hover:text-blue-800 underline">ログインする</a>
    </div>
  {:else}
    <!-- 分析実行セクション -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-xl font-bold mb-4 text-gray-800">新しい分析を実行</h2>
      
      {#if error}
        <div class="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
          {#if error.includes('使用回数制限')}
            <div class="mt-2">
              <a href="/dashboard" class="text-blue-600 hover:text-blue-800 underline">プランアップグレード</a>
            </div>
          {/if}
        </div>
      {/if}

      <div class="space-y-4">
        <div>
          <label for="analysis-type" class="block text-sm font-medium text-gray-700 mb-2">分析タイプ</label>
          <select
            id="analysis-type"
            bind:value={selectedAnalysisType}
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            {#each analysisTypes as type}
              <option value={type.value}>{type.label}</option>
            {/each}
          </select>
        </div>

        <button
          on:click={runAnalysis}
          disabled={loading}
          class="w-full bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-md transition-colors"
        >
          {loading ? '分析中...' : '分析を実行'}
        </button>
      </div>
    </div>

    <!-- 分析履歴 -->
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-bold mb-4 text-gray-800">分析履歴</h2>
      
      {#if analyses.length > 0}
        <div class="space-y-4">
          {#each analyses as analysis}
            <div class="border rounded-lg p-4">
              <div class="flex justify-between items-start mb-3">
                <div>
                  <h3 class="font-semibold text-gray-800">
                    {getAnalysisTypeLabel(analysis.analysis_type)}
                  </h3>
                  <p class="text-sm text-gray-600">
                    {new Date(analysis.created_at).toLocaleString()}
                  </p>
                </div>
                <button
                  on:click={() => deleteAnalysis(analysis.id)}
                  class="text-red-500 hover:text-red-700 text-sm"
                >
                  削除
                </button>
              </div>

              <div class="space-y-3">
                <div>
                  <h4 class="font-medium text-gray-700 mb-1">サマリー</h4>
                  <p class="text-gray-800">{analysis.summary}</p>
                </div>

                {#if analysis.insights}
                  <div>
                    <h4 class="font-medium text-gray-700 mb-1">洞察</h4>
                    <ul class="list-disc list-inside text-gray-800 space-y-1">
                      {#each JSON.parse(analysis.insights) as insight}
                        <li>{insight}</li>
                      {/each}
                    </ul>
                  </div>
                {/if}

                {#if analysis.recommendations}
                  <div>
                    <h4 class="font-medium text-gray-700 mb-1">推奨事項</h4>
                    <ul class="list-disc list-inside text-gray-800 space-y-1">
                      {#each JSON.parse(analysis.recommendations) as recommendation}
                        <li>{recommendation}</li>
                      {/each}
                    </ul>
                  </div>
                {/if}

                {#if analysis.mood_score}
                  <div>
                    <h4 class="font-medium text-gray-700 mb-1">気分スコア</h4>
                    <p class="text-gray-800">{analysis.mood_score.toFixed(1)}/5.0</p>
                  </div>
                {/if}

                {#if analysis.stress_level}
                  <div>
                    <h4 class="font-medium text-gray-700 mb-1">ストレスレベル</h4>
                    <p class="text-gray-800 {getStressLevelColor(analysis.stress_level)}">
                      {analysis.stress_level === 'high' ? '高' : 
                       analysis.stress_level === 'medium' ? '中' : '低'}
                    </p>
                  </div>
                {/if}
              </div>
            </div>
          {/each}
        </div>
      {:else}
        <p class="text-gray-500">まだ分析履歴がありません。上記のボタンから分析を実行してください。</p>
      {/if}
    </div>
  {/if}
</div> 