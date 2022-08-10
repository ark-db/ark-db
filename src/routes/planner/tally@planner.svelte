<script>
    import { allSelected, inventory, costFilter, makeT3 } from "../stores.js";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    import NumberInput from "$lib/components/NumberInput.svelte";

    const min = 0;
    const max = 999999;

    $: itemCounter = normalize(
            makeCounter($allSelected.filter(upgrade => $costFilter.includes(upgrade.ready))
                                    .map(upgrade => upgrade.cost)
                                    .flat())
        );

    function sortBySortId(list) {
        return list.sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };

    function normalize(counter) {
        return Object.entries(counter)
                     .map(([id, count]) => ({id, count}))
    }

    function makeCounter(list) {
        return list.reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {})
    };

    function convertToT3(list) {
        let itemCounts = {};
        
        function asT3({ id, count }) {
            let { rarity, recipe = undefined } = items[id];
            if (rarity === 2) {
                itemCounts[id] = (itemCounts[id] ?? 0) + count;
            } else if (rarity > 2 && recipe) {
                recipe.forEach(({ id, count: ingCount }) => asT3({id, count: ingCount*count}));
            }
        };

        list.forEach(item => asT3(item));
        return normalize(itemCounts);
    };

    function compare(inv, costs) {
        let invDict = Object.fromEntries(inv.map(({ id, count }) => [id, count]));
        return costs.filter(({ id }) => id !== "4001").map(({ id, count }) => ({id, count: invDict[id] - count}));
    }

    function compareAsT3(inv, costs) {
        let deficits = new Set();
        let stock = Object.fromEntries(inv.map(({ id, count }) => [id, count]));

        function getDeficits(id, qtyNeeded) {
            stock[id] -= qtyNeeded;
            if (stock[id] < 0) {
                let { rarity, recipe = undefined } = items[id];
                if (rarity > 2 && recipe) {
                    recipe.forEach(({ id: matId, count: matCount}) => getDeficits(matId, matCount*-stock[id]));
                    stock[id] = 0;
                } else {
                    deficits.add(id);
                }
            }
        }

        costs.forEach(({ id, count }) => getDeficits(id, count));
        return normalize(stock).filter(({ id }) => deficits.has(id));
    }
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

<div id="group">
    <div>
        <h1 class="title">Upgrade Costs</h1>
        {#if Object.keys(itemCounter).length > 0}
            <section class="items">
                {#each sortBySortId($makeT3 ? convertToT3(itemCounter) : itemCounter) as item}
                    <ItemIcon {...item} --size="100px" />
                {/each}
            </section>

            <h1 class="title">Comparison</h1>
            <section class="items">
                {#each sortBySortId($makeT3 ? compareAsT3($inventory, itemCounter) : compare($inventory, itemCounter)) as item}
                    <ItemIcon {...item} --size="100px" />
                {/each}
            </section>
        {:else}
            <p class="placeholder">No upgrades found</p>
        {/if}

        
    </div>
    <div>
        <h1 class="title">Inventory</h1>
        <section class="items">
            {#each $inventory as { id, count }}
                <div>
                    <ItemIcon {id} {count} --size="100px" />
                    <NumberInput {min} {max} bind:value={count} />
                </div>
            {/each}
        </section>
    </div>
</div>



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
    #group {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        gap: 10px;
    }
    #group > div {
        flex: 1 1 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .items {
        margin-top: 15px;
        padding: 10px;
        border-radius: 8px;
        background-color: var(--light-strong);
        display: grid;
        grid-template-columns: repeat(auto-fit, 100px);
        justify-content: center;
        gap: 20px;
    }
</style>