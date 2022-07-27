<script>
    import { writable } from 'svelte/store';
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "../lib/components/OperatorIcon.svelte";
    const selectedChar = writable("")
</script>

<SearchBar {selectedChar} />
{#if $selectedChar}
    <OperatorIcon {selectedChar} />
{/if}