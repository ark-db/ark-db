<svelte:head>
    <title>Upgrade Planner - ArkDB</title>
    <meta name="description" content="Arknights operator upgrade cost calculator and planner" />
</svelte:head>

<script>
    import { selectedChar, activeCategory, selectedUpgradeNames } from "./stores.js"
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    import UpgradeSeries from "$lib/components/UpgradeSeries.svelte";

    let innerWidth;
    let upgradeListByChar = {};
    $: allSelectedUpgrades = Object.entries(upgradeListByChar).map(([charId, upgrades]) => (upgrades.map(upgrade => ({charId, ...upgrade})))).flat();
    $: console.log(allSelectedUpgrades);

    const submitUpgrades = () => {
        let allSelectedNames = Object.values($selectedUpgradeNames).map(set => Array.from(set)).flat(); 
        let upgrades = $selectedChar.upgrades.map(category => category.data.flat()).flat();
        let selectedUpgrades = upgrades.filter(upgrade => allSelectedNames.includes(upgrade.name));

        if ($selectedChar.charId in upgradeListByChar) {
            upgradeListByChar[$selectedChar.charId] = [...upgradeListByChar[$selectedChar.charId],
                                                       selectedUpgrades.filter(upgrade => !upgradeListByChar[$selectedChar.charId].map(upgrade => upgrade.name).includes(upgrade.name))
                                                                       .map(upgrade => ({...upgrade, ready: false}))]
                                                       .flat();
        } else {
            upgradeListByChar[$selectedChar.charId] = selectedUpgrades.map(upgrade => ({...upgrade, ready: false}));
        }

        selectedUpgradeNames.reset();
        $selectedChar = {};
        console.log(upgradeListByChar);
    }
</script>

<svelte:window bind:innerWidth={innerWidth} />



<div class="top">
    <div class="search">
        <SearchBar {selectedChar} />
    </div>
    <div class="settings">
        <p>There's nothing here yet!</p>
    </div>
</div>

{#key $selectedChar}
    {#if $selectedChar?.charId !== undefined}
        <div class="banner">
            <div class="card">
                <OperatorIcon charId={$selectedChar.charId} />
                <h1>{$selectedChar.name}</h1>
            </div>
            {#if $activeCategory && innerWidth >= 700}
                <div class="tooltip">
                    <img src={$activeCategory} alt="Upgrade icon" />
                </div>
            {/if}
            <button on:click={submitUpgrades}>
                <p>Save & add to list</p>
            </button>
        </div>
    {/if}
    {#if $selectedChar?.upgrades !== undefined}
        <div class="select">
            {#each $selectedChar.upgrades as category}
                {#if category.data.length > 0}
                    <div class="series">
                        <UpgradeSeries {category} {activeCategory} {selectedUpgradeNames} />
                    </div>
                {/if}
            {/each}
        </div>
    {/if}
{/key}



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
        height: 100%;
        max-height: 90px;
        min-height: 90px;
    }
    .banner button {
        background-color: rgb(136, 255, 96);
        padding: 0 1em 0 1em;
    }

    .select {
        padding: 5px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: flex-start;
        justify-content: center;
    }
    .select .series {
        flex-grow: 1;
    }
</style>