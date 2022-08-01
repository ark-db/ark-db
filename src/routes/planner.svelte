<svelte:head>
    <title>Upgrade Planner - ArkDB</title>
    <meta name="description" content="Arknights operator upgrade cost calculator and planner" />
</svelte:head>

<script>
    import { selectedChar, activeCategory, selectedUpgradeNames } from "./stores.js"
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    import UpgradeSeries from "$lib/components/UpgradeSeries.svelte";
    import TaskItem from "$lib/components/TaskItem.svelte";
    import { flip } from "svelte/animate";
    import { dndzone } from "svelte-dnd-action";

    let innerWidth;
    let uid = 0;
    let allSelected = [];
    const flipDurationMs = 150;

    function submitUpgrades() {
        let allSelectedNames = Object.values($selectedUpgradeNames).map(set => Array.from(set)).flat();
        let upgrades = $selectedChar.upgrades.map(category => category.data.flat()).flat();
        let newUpgrades = upgrades.filter(upgrade => allSelectedNames.includes(upgrade.name))
                                  .filter(upgrade => !allSelected.filter(upgrade => upgrade.charId === $selectedChar.charId)
                                                                 .map(upgrade => upgrade.name)
                                  .includes(upgrade.name));

        allSelected = [...allSelected, ...newUpgrades.map(upgrade => ({...upgrade, charId: $selectedChar.charId, id: uid++, ready: false}))]

        selectedUpgradeNames.reset();
        $selectedChar = {};
    }
    function handleDnd(event) {
        allSelected = event.detail.items;
    }
</script>

<svelte:window bind:innerWidth={innerWidth} />


<div class="page">
    <section id="top">
        <SearchBar {selectedChar} />
        <div class="settings">
            <p>There's nothing here yet!</p>
        </div>
    </section>

    {#key $selectedChar}
    {#if $selectedChar?.charId !== undefined}
        <section id="banner">
            <div id="card">
                <OperatorIcon
                    charId={$selectedChar.charId}
                    --size="100px"
                    --border="7.5px"
                />
                <h1>{$selectedChar.name}</h1>
            </div>
            {#if $activeCategory && innerWidth >= 700}
                <img src={$activeCategory} alt="Upgrade icon" />
            {/if}
            <button on:click={submitUpgrades}>
                <p>Save & add to list</p>
            </button>
        </section>
    {/if}
    {#if $selectedChar?.upgrades !== undefined}
        <section id="select">
            {#each $selectedChar.upgrades as category}
                {#if category.data.length > 0}
                    <div class="series">
                        <UpgradeSeries
                            {category}
                            {activeCategory}
                            {selectedUpgradeNames}
                        />
                    </div>
                {/if}
            {/each}
        </section>
    {/if}
    {/key}

    {#if allSelected.length > 0}
        <section
            id="taskboard"
            use:dndzone={{items: allSelected, flipDurationMs}}
            on:consider={handleDnd}
            on:finalize={handleDnd}
        >
            <h1>Upgrades</h1>
            {#each allSelected as upgrade (upgrade.id)}
                <div animate:flip="{{duration: flipDurationMs}}">
                    <TaskItem
                        charId={upgrade.charId}
                        upgradeName={upgrade.name}
                        bind:ready={upgrade.ready}
                    />
                </div>
            {/each}
        </section>
    {:else}
        <section id="placeholder">
            <p>No upgrades added yet</p>
        </section>
    {/if}
</div>


<style>
    .page {
        margin-top: 5px;
        padding: 5px 0 5px 0;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    #top {
        padding: 5px 10px 5px 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: center;
    }
    #top .settings p {
        text-align: center;
    }
    #top .settings {
        flex-grow: 1;
        display: flex;
        justify-content: center;
    }

    #banner {
        padding: 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: space-between;
        gap: 1em;
    }
    #banner #card {
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: center;
        column-gap: 1em;
    }
    #banner #card h1 {
        text-align: center;
    }
    #banner img {
        height: 100%;
        max-height: 90px;
        min-height: 90px;
    }
    #banner button {
        background-color: rgb(136, 255, 96);
        padding: 0 1em 0 1em;
    }

    #select {
        padding: 5px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: flex-start;
        justify-content: center;
    }
    #select .series {
        flex-grow: 1;
    }

    #placeholder {
        margin: 15px;
        background-color: rgb(245, 248, 254);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    #taskboard {
        padding: 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-direction: column;
        row-gap: 5px;
    }
    #taskboard h1 {
        text-align: center;
    }
</style>