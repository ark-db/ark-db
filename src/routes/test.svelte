<script>
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "../lib/components/OperatorIcon.svelte";
    let charId = "";
    function handleMessage(event) {
		charId = event.detail.charId;
	}
</script>

<SearchBar on:message={handleMessage} />
{#if charId}
    <OperatorIcon bind:charId={charId} />
{/if}