<script lang="ts">
	import '../app.css';
	import DateTimeDisplay from '$lib/DateTimeDisplay.svelte';
	import DateTimeSettings from '$lib/DateTimeSettings.svelte';

	let { children } = $props();
</script>

<DateTimeDisplay />
<DateTimeSettings />
{@render children()}
