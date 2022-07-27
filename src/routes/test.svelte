<script>
    import { writable } from 'svelte/store';
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "../lib/components/OperatorIcon.svelte";
    const selectedChar = writable({charId: "", name: ""});
</script>

<div class="select">
    <SearchBar {selectedChar} />
    {#if $selectedChar.charId}
        <div class="heading">
            <OperatorIcon {selectedChar} />
            <p>{$selectedChar.name}</p>
        </div>
    {/if}
</div>