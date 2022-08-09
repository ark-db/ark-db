<script>
    import { allSelected, inventory, costFilter, makeT3 } from "../stores.js";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    import NumberInput from "$lib/components/NumberInput.svelte";

    const min = 0;
    const max = 999999;

    $: itemCounter = makeCounter($allSelected.filter(upgrade => $costFilter.includes(upgrade.ready))
                                             .map(upgrade => upgrade.cost)
                                             .flat());

    function sortBySortId(counter) {
        return counter.sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };
    function makeCounter(list) {
        return Object.entries(list.reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {}))
                     .map(([id, count]) => ({id, count}));
    };
    function convertToT3(counter) {
        let itemCounts = [];
        
        function asT3({ id, count }) {
            let { rarity, recipe = undefined } = items[id];
            if (rarity === 2) {
                itemCounts.push({ id, count });
            } else if (rarity > 2 && recipe) {
                recipe.forEach(({ id, count: ingCount }) => asT3({id, count: ingCount*count}));
            }
        };

        counter.forEach(item => asT3(item));
        return makeCounter(itemCounts);
    };
</script>



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
        <label for="convert-t3">Convert materials to T3</label>
    </div>
</section>

<h1>Upgrade Costs</h1>
{#if itemCounter.length > 0}
    <section class="items">
        {#each sortBySortId($makeT3 ? convertToT3(itemCounter) : itemCounter) as item}
            <ItemIcon {...item} --size="100px" />
        {/each}
    </section>
{:else}
    <p class="placeholder">No upgrades found</p>
{/if}

<h1>Inventory</h1>
<section class="items">
    {#each $inventory as { id, count }}
        <div>
            <ItemIcon {id} {count} --size="100px" />
            <NumberInput {min} {max} bind:value={count} />
        </div>
    {/each}
</section>



<style>
    #settings {
        padding: calc(1em + 2.25px);
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 1em 3em;
    }
    #filter {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1em 3em;
    }
    #notready {
        background-color: rgba(255, 140, 140, 0.7);
    }
    #ready {
        background-color: rgba(151, 255, 148, 0.7);
    }
    .items {
        margin-top: 15px;
        padding: 10px;
        background-color: var(--light-strong);
        display: grid;
        grid-template-columns: repeat(auto-fit, 100px);
        justify-content: center;
        gap: 20px;
    }
</style>