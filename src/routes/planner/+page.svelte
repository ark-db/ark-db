<svelte:head>
    <title>Upgrade Planner</title>
    <meta name="description" content="An Arknights operator upgrade planner." />
</svelte:head>

<script>
    import { writable } from "svelte/store";
    import { selectedChar, activeCategory, allSelected, splitByStatus, showCost } from "../stores.js";
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    import UpgradeSeries from "$lib/components/UpgradeSeries.svelte";
    import TaskItem from "$lib/components/TaskItem.svelte";
    import { flip } from "svelte/animate";
    import { dndzone } from "svelte-dnd-action";

    let innerWidth;
    const flipDurationMs = 150;
    $: allReady = $allSelected.filter(upgrade => upgrade.ready);
    $: allNotReady = $allSelected.filter(upgrade => !upgrade.ready);

    $: selectedUpgradeNames = writable(new Array($selectedChar?.upgrades?.length).fill(new Set()))

    function reindex() {
        for (let [idx, upgrade] of $allSelected.entries()) {
            upgrade.id = idx;
        }
        $allSelected = $allSelected;
    }

    function submitUpgrades() {
        let selectedNames = $selectedUpgradeNames.map(set => Array.from(set)).flat();
        let allNames = $selectedChar.upgrades.map(category => category.names).flat();
        let newNames = allNames.filter(name => selectedNames.includes(name))
                               .filter(name => !$allSelected.filter(upgrade => upgrade.charId === $selectedChar.charId)
                                                            .map(upgrade => upgrade.name)
                                                            .includes(name));
        $allSelected = [...$allSelected,
                        ...newNames.map(name => ({name,
                                                  charId: $selectedChar.charId,
                                                  ready: false}))]

        reindex();

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

<section class="content top">
    <SearchBar {selectedChar} />
    <section class="settings">
        <label>
            <input type="checkbox" bind:checked={$splitByStatus}>
            Organize upgrades by status
        </label>
        <label>
            <input type="checkbox" bind:checked={$showCost}>
            Show upgrade costs
        </label>
    </section>
</section>

{#key $selectedChar}
{#if $selectedChar?.charId !== undefined}
    <section class="content banner">
        <div>
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
    <section class="content select">
        {#each $selectedChar.upgrades as category, idx}
            {#if category.names.length > 0}
                <div>
                    <UpgradeSeries {category} {idx} {activeCategory} {selectedUpgradeNames} />
                </div>
            {/if}
        {/each}
    </section>
{/if}
{/key}

<h1 class="title">Upgrades</h1>
{#if $allSelected.length > 0}
    <section class="content taskboard">
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
    .top {
        margin-bottom: 5px;
        padding: 10px;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 1em;
    }
    .settings {
        margin-right: calc(1em - 7.75px);
        padding-bottom: 5px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1em 3em;
    }
    .banner {
        padding: 10px;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 0.5em 2em;
    }
    .banner div {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        column-gap: 1em;
    }
    .banner h1 {
        margin: 0.5em 0 0.5em 0;
        text-align: center;
        font-size: 2em;
    }
    img {
        height: 100%;
        max-height: 90px;
        min-height: 90px;
    }
    button {
        margin-right: 1em;
        padding: 0 1em 0 1em;
        border: 2px solid var(--green-strong);
        border-radius: 4em;
        background-color: transparent;
        transition: all 0.1s ease;
    }
    button:hover {
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
    .select {
        padding: 5px;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        justify-content: center;
    }
    .select div {
        flex-grow: 1;
    }
    .taskboard {
        margin-top: 15px;
        padding: 10px;
        border: 1px solid var(--light-moderate);
        background-color: var(--dark-moderate);
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
    }
    .taskboard section {
        flex: 1 1 0;
        display: flex;
        flex-direction: column;
        row-gap: 5px;
    }
</style>