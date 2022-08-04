<script>
    import { allSelected } from "../stores.js";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";

    let filters = [false];
    $: itemCounter = counter($allSelected.filter(upgrade => filters.includes(upgrade.ready))
                                         .map(upgrade => upgrade.cost)
                                         .flat());

    const counter = (list) => {
        return Object.entries(list.reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {}))
                     .map(item => ({id: item[0], count: item[1]}))
                     .sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };
</script>



<div class="page">
    <section id="settings">
        <div>
            <input id="show-ready" type="checkbox" bind:group={filters} value={false}>
            <label for="show-ready">Include <span id="notready">unprepared</span> upgrades</label>
        </div>
        <div>
            <input id="show-ready" type="checkbox" bind:group={filters} value={true}>
            <label for="show-ready">Include <span id="ready">prepared</span> upgrades</label>
        </div>
    </section>

    <h1>Upgrade Costs</h1>
    {#if itemCounter.length > 0}
        <section id="costs">
            {#each itemCounter as item}
                <ItemIcon {...item} --size="100px" />
            {/each}
        </section>
    {:else}
        <section id="placeholder">
            <p>No upgrades found</p>
        </section>
    {/if}
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
        justify-content: center;
        gap: 1em 3em;
    }
    #settings input[type=checkbox] {
        transform: scale(1.5);
        margin-right: 0.5em;
    }
    #settings #notready {
        background-color: rgba(255, 140, 140, 0.7);
    }
    #settings #ready {
        background-color: rgba(151, 255, 148, 0.7);
    }
    .page > h1 {
        margin: 0.6em 0 0.2em 0;
        text-align: center;
    }
    #costs {
        margin-top: 15px;
        padding: 10px;
        background-color: rgb(235, 238, 244);
        display: grid;
        grid-template-columns: repeat(auto-fit, 100px);
        justify-content: center;
        gap: 16px;
    }
    #placeholder {
        margin: 15px;
        border-radius: 10px;
        background-color: rgb(245, 248, 254);
        display: flex;
        justify-content: center;
    }
</style>