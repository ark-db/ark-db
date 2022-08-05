<script>
    import { allSelected, inventory, costFilter, makeT3 } from "../stores.js";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    //import plusIcon from "$lib/images/plus.svg";
    //import minusIcon from "$lib/images/minus.svg";

    $: itemCounter = makeCounter($allSelected.filter(upgrade => $costFilter.includes(upgrade.ready))
                                             .map(upgrade => upgrade.cost)
                                             .flat());

    function makeCounter(list) {
        return Object.entries(list.reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {}))
                     .map(item => ({id: item[0], count: item[1]}))
                     .sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };
    function convertToT3(list) {
        return makeCounter(list.map(item => ([...items[item.id].asT3.map(mat => ({id: mat.id, count: mat.count * item.count}))]))
                               .filter(item => item.length)
                               .flat());
    };
</script>



<div class="page">
    <section id="settings">
        <div id="filter">
            <div>
                <input id="show-notready" type="checkbox" bind:group={$costFilter} value={false}>
                <label for="show-notready">Include <span id="notready">unprepared</span> upgrades</label>
            </div>
            <div>
                <input id="show-ready" type="checkbox" bind:group={$costFilter} value={true}>
                <label for="show-ready">Include <span id="ready">prepared</span> upgrades</label>
            </div>
        </div>
        <div>
            <input id="convert-t3" type="checkbox" bind:checked={$makeT3}>
            <label for="convert-t3">Convert upgrade cost materials to T3</label>
        </div>
    </section>

    <h1>Upgrade Costs</h1>
    {#if itemCounter.length > 0}
        <section class="items">
            {#each $makeT3 ? convertToT3(itemCounter) : itemCounter as item}
                <ItemIcon {...item} --size="100px" />
            {/each}
        </section>
    {:else}
        <p class="placeholder">No upgrades found</p>
    {/if}

    <h1>Inventory</h1>
    <!--<section class="items">
        {#each $inventory as { id, count }}
            <div class="item">
                <ItemIcon {id} --size="100px" />
                <div class="inputs">
                    <input type="image" src={minusIcon} alt="delete" on:click={() => count === 0 ? count : count--}/>
                    <input type="number" min={0} max={1e5} use:validator={count} bind:value={count} placeholder="Lorem ipsum"/>
                    <input type="image" src={plusIcon} alt="delete" on:click={() => count === 1e5 ? count : count++}/>
                </div>
            </div>
        {/each}
    </section>-->
    <p class="placeholder">Coming soon!</p>
</div>



<style>
    .page {
        margin-top: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    #settings {
        padding: calc(1em + 2.25px);
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 1em 3em;
    }
    #settings input[type=checkbox] {
        transform: scale(1.5);
        margin-right: 0.5em;
    }
    #settings #filter {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1em 3em;
    }
    span#notready {
        background-color: rgba(255, 140, 140, 0.7);
    }
    span#ready {
        background-color: rgba(151, 255, 148, 0.7);
    }
    .page h1 {
        margin: 0.6em 0 0.2em 0;
        text-align: center;
    }
    .items {
        margin-top: 15px;
        padding: 10px;
        background-color: rgb(235, 238, 244);
        display: grid;
        grid-template-columns: repeat(auto-fit, 100px);
        justify-content: center;
        gap: 16px;
    }
    .placeholder {
        margin: 15px;
        padding: 1em;
        border-radius: 10px;
        background-color: rgb(245, 248, 254);
        text-align: center;
    }
</style>