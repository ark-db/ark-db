<svelte:head>
    <title>Upgrade Planner - ArkDB</title>
    <meta name="description" content="Arknights operator upgrade cost calculator and planner" />
</svelte:head>

<script>
    import { selectedChar, activeCategory } from "./stores.js"
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    import UpgradeSeries from "$lib/components/UpgradeSeries.svelte";
</script>

<div class="top">
    <div class="search">
        <SearchBar {selectedChar} />
    </div>
    <div class="settings">
        <p>There's nothing here yet!</p>
    </div>
</div>

{#if $selectedChar}
    <div class="banner">
        <div class="card">
            <OperatorIcon
                charId={$selectedChar.charId}
                name={$selectedChar.name}
                rarity={$selectedChar.rarity}    
            />
            <h1>{$selectedChar.name}</h1>
        </div>
        {#if $activeCategory}
            <div class="tooltip">
                <img src={$activeCategory} alt="Upgrade icon" />
            </div>
        {/if}
    </div>
    <div class="select">
        {#each $selectedChar.upgrades as category}
            {#if category.data.length > 0}
                <div class="series">
                    <UpgradeSeries {category} {activeCategory} />
                </div>
            {/if}
        {/each}
    </div>
{/if}



<style>
    .top {
        margin: 10px 0px 10px 0px;
        padding: 5px 10px 5px 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: center;
    }
    .top .settings p {
        text-align: center;
    }
    .top .settings {
        flex-grow: 1;
        display: flex;
        justify-content: center;
    }

    .banner {
        margin-bottom: 10px;
        padding: 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: space-between;
        gap: 1em;
    }
    .banner .card {
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: center;
        column-gap: 1em;
    }
    .banner .card h1 {
        text-align: center;
    }
    .banner .tooltip img {
        width: 100%;
        max-width: 90px;
        min-width: 90px;
    }
    .select {
        padding: 5px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: flex-start;
        justify-content: center;
    }
    .series {
        flex-grow: 1;
    }
</style>