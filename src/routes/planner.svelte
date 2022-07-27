<svelte:head>
    <title>Upgrade Planner - ArkDB</title>
    <meta name="description" content="Arknights operator upgrade cost calculator and planner" />
</svelte:head>

<script>
    import { writable } from 'svelte/store';
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    const selectedChar = writable("");
</script>

<div class="select">
    <SearchBar {selectedChar} />
    {#if $selectedChar.charId}
        <div class="heading">
            <OperatorIcon {...$selectedChar} />
            <h1>{$selectedChar.name}</h1>
        </div>
    {/if}
</div>

<style>
    .select {
        margin-top: 10px;
        background-color: rgb(235, 238, 244);
        padding: 10px;
    }
    .heading {
        margin: 20px;
        display: flex;
        align-items: center;
    }
    .heading h1 {
        margin-left: 0.75em;
    }
</style>