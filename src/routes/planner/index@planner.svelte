<svelte:head>
    <title>Upgrade Planner - ArkDB</title>
    <meta name="description" content="Arknights operator upgrade cost calculator and planner" />
</svelte:head>

<script>
    import { selectedChar, activeCategory, selectedUpgradeNames, allSelected, splitByStatus, showCost } from "../stores.js";
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    import UpgradeSeries from "$lib/components/UpgradeSeries.svelte";
    import TaskItem from "$lib/components/TaskItem.svelte";
    import { flip } from "svelte/animate";
    import { dndzone } from "svelte-dnd-action";

    let innerWidth;
    $: uid = $allSelected.length;
    $: allReady = $allSelected.filter(upgrade => upgrade.ready);
    $: allNotReady = $allSelected.filter(upgrade => !upgrade.ready);
    const flipDurationMs = 150;

    function submitUpgrades() {
        let allSelectedNames = Object.values($selectedUpgradeNames).map(set => Array.from(set)).flat();
        let upgrades = $selectedChar.upgrades.map(category => category.data.flat()).flat();
        let newUpgrades = upgrades.filter(upgrade => allSelectedNames.includes(upgrade.name))
                                  .filter(upgrade => !$allSelected.filter(upgrade => upgrade.charId === $selectedChar.charId)
                                                                  .map(upgrade => upgrade.name)
                                  .includes(upgrade.name));
        $allSelected = [...$allSelected,
                        ...newUpgrades.map(upgrade => ({...upgrade,
                                                        charId: $selectedChar.charId,
                                                        id: uid++,
                                                        ready: false}))]
        selectedUpgradeNames.reset();
        $selectedChar = {};
    }
    function remove(upgrade) {
        $allSelected = $allSelected.filter(up => !(up.charName === upgrade.charName
                                                   && up.name === upgrade.name));
    }
    function handleDnd(event) {
        $allSelected = event.detail.items;
    }
    function handleDndReady(event) {
        allReady = event.detail.items;
    }
    function handleDndNotReady(event) {
        allNotReady = event.detail.items;
    }
</script>



<svelte:window bind:innerWidth={innerWidth} />

<section id="top">
    <SearchBar {selectedChar} />
    <section id="settings">
        <div>
            <input id="split-status" type="checkbox" bind:checked={$splitByStatus}>
            <label for="split-status">Organize upgrades by status</label>
        </div>
        <div>
            <input id="show-cost" type="checkbox" bind:checked={$showCost}>
            <label for="show-cost">Show upgrade costs</label>
        </div>
    </section>
</section>

{#key $selectedChar}
{#if $selectedChar?.charId !== undefined}
    <section id="banner">
        <div id="card">
            <OperatorIcon charId={$selectedChar.charId} --size="100px" --border="7.5px" />
            <h1>{$selectedChar.name}</h1>
        </div>
        {#if $activeCategory && innerWidth >= 800}
            <img src={$activeCategory} alt="Upgrade icon" />
        {/if}
        <button on:click={submitUpgrades}>
            <p>Save and add to list</p>
        </button>
    </section>
{/if}
{#if $selectedChar?.upgrades !== undefined}
    <section id="select">
        {#each $selectedChar.upgrades as category}
            {#if category.data.length > 0}
                <div class="series">
                    <UpgradeSeries {category} {activeCategory} {selectedUpgradeNames} />
                </div>
            {/if}
        {/each}
    </section>
{/if}
{/key}

<h1>Upgrades</h1>
{#if $allSelected.length > 0}
    <section id="taskboard">
    {#if $splitByStatus}
        {#if allNotReady.length > 0}
            <section use:dndzone={{items: allNotReady, flipDurationMs, dropFromOthersDisabled: true}}
                     on:consider={handleDndNotReady}
                     on:finalize={handleDndNotReady}
            >
                {#each allNotReady as upgrade (upgrade.id)}
                    <div animate:flip="{{duration: flipDurationMs}}">
                        <TaskItem {...upgrade} {splitByStatus} {showCost} bind:ready={upgrade.ready} on:click={() => remove(upgrade)} />
                    </div>
                {/each}
            </section>
        {/if}
        {#if allReady.length > 0}
            <section use:dndzone={{items: allReady, flipDurationMs, dropFromOthersDisabled: true}}
                     on:consider={handleDndReady}
                     on:finalize={handleDndReady}
            >
                {#each allReady as upgrade (upgrade.id)}
                    <div animate:flip="{{duration: flipDurationMs}}">
                        <TaskItem {...upgrade} {splitByStatus} {showCost} bind:ready={upgrade.ready} on:click={() => remove(upgrade)} />
                    </div>
                {/each}
            </section>
        {/if}
    {:else}
        <section use:dndzone={{items: $allSelected, flipDurationMs}}
                 on:consider={handleDnd}
                 on:finalize={handleDnd}
        >
            {#each $allSelected as upgrade (upgrade.id)}
                <div animate:flip="{{duration: flipDurationMs}}">
                    <TaskItem {...upgrade} {splitByStatus} {showCost} bind:ready={upgrade.ready} on:click={() => remove(upgrade)} />
                </div>
            {/each}
        </section>
    {/if}
    </section>
{:else}
    <p class="placeholder">No upgrades added yet</p>
{/if}



<style>
    #top {
        padding: 10px;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-around;
        gap: 1em;
    }
    #top #settings {
        flex-grow: 1;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1em 3em;
    }
    #banner {
        padding: 10px;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 0.5em 2em;
    }
    #banner #card {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        column-gap: 1em;
    }
    #banner #card h1 {
        margin: 0.5em 0 0.5em 0;
        text-align: center;
        font-size: 2em;
    }
    #banner img {
        height: 100%;
        max-height: 90px;
        min-height: 90px;
    }
    #banner button {
        margin-right: 1em;
        padding: 0 1em 0 1em;
        border: 2px solid var(--green-strong);
        border-radius: 4em;
        background-color: transparent;
        transition: all 0.1s ease;
    }
    #banner button:hover {
        border: 2px solid var(--green-moderate);
        background-color: var(--green-moderate);
    }
    button > p {
        color: var(--green-strong);
        transition: color 0.1s ease;
    }
    button:hover > p {
        color: white;
    }
    #select {
        padding: 5px;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        justify-content: center;
    }
    #select .series {
        flex-grow: 1;
    }
    #taskboard {
        margin-top: 15px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    #taskboard section {
        padding: 10px;
        background-color: var(--light-strong);
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        row-gap: 5px;
    }
</style>