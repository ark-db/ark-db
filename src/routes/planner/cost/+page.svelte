<svelte:head>
    <title>Cost Calculator</title>
    <meta name="description" content="A calculator for upgrade costs of operators in Arknights." />
</svelte:head>

<script>
    import { allSelectedWithCost, inventory, costFilter, itemFilter, makeT3 } from "../../stores.js";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    import NumberInput from "$lib/components/NumberInput.svelte";

    const min = 0;
    const max = 999999;

    $: itemCounter = makeCounter($allSelectedWithCost.filter(upgrade => $costFilter.includes(upgrade.ready))
                                                     .map(upgrade => upgrade.cost)
                                                     .flat()
                                                     .filter(({ id }) => $itemFilter.includes(items[id].type)));

    function sortItems(list) {
        return list.sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };

    function normalize(counter) {
        return Array.from(counter).map(([id, count]) => ({id, count}));
    }

    function makeCounter(list) {
        return new Map(
            Object.entries(
                list.reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {})
            )
        );
    };

    function convertToT3(counter) {
        let itemCounts = new Map();
        
        function convert(id, count) {
            let { rarity, recipe = undefined } = items[id];
            if (rarity === 2) {
                itemCounts.set(id, (itemCounts.get(id) ?? 0) + count);
            } else if (rarity > 2 && recipe) {
                recipe.forEach(({ id, count: ingCount }) => convert(id, ingCount*count));
            }
        };

        for (const [id, count] of counter) {
            convert(id, count);
        };
        return itemCounts;
    };

    function getDeficits(inv, costs) {
        let stock = Object.fromEntries(inv.map(({ id, count }) => [id, count]));
        let deficits = Array.from(costs)
                            .map(([ id, count ]) => ({id: id, count: stock[id] - count}))
                            .filter(({ id, count }) => id !== "4001" && count < 0)
        return deficits;
    }

    function getDeficitsT3(inv, costs) {
        let deficits = new Set();
        let stock = new Map(inv.map(({ id, count }) => ([id, count])));

        function searchForDeficits(id, qtyNeeded) {
            stock.set(id, stock.get(id) - qtyNeeded);
            if (stock.get(id) < 0) {
                let { rarity, recipe = undefined } = items[id];
                if (rarity > 2 && recipe) {
                    recipe.forEach(({ id: matId, count }) => searchForDeficits(matId, -stock.get(id)*count));
                    stock.set(id, 0);
                } else {
                    deficits.add(id);
                }
            }
        }

        for (const [id, count] of costs) {
            searchForDeficits(id, count);
        };
        return normalize(stock).filter(({ id }) => deficits.has(id));
    }
</script>



<section class="content settings">
    <div id="filter-status">
        <label>
            <input type="checkbox" bind:group={$costFilter} value={false}>
            Include <span id="notready">unprepared</span> upgrades
        </label>
        <label>
            <input type="checkbox" bind:group={$costFilter} value={true}>
            Include <span id="ready">prepared</span> upgrades
        </label>
    </div>
    <label>
        <input type="checkbox" bind:checked={$makeT3} disabled={!$itemFilter.includes("material")}>
        Reduce items to T3
    </label>
</section>

<section class="content settings">
    <label>
        <input type="checkbox" bind:group={$itemFilter} value={"material"}>
        Show materials
    </label>
    <label>
        <input type="checkbox" bind:group={$itemFilter} value={"skill"}>
        Show skillbooks
    </label>
    <label>
        <input type="checkbox" bind:group={$itemFilter} value={"chip"}>
        Show chip items
    </label>
    <label>
        <input type="checkbox" bind:group={$itemFilter} value={"module"}>
        Show module items
    </label>
    <label>
        <input type="checkbox" bind:group={$itemFilter} value={"misc"}>
        Show miscellaneous
    </label>
</section>

<section class="costs">
    <div>
        <h1 class="title">Upgrade Costs</h1>
        {#if itemCounter.size > 0}
            {@const costs = sortItems(normalize($makeT3 ? convertToT3(itemCounter) : itemCounter))}
            {#key $makeT3}
            <section class="items">
                {#each costs as item}
                    <ItemIcon {...item} --size="100px" />
                {/each}
            </section>
            {/key}
        {:else}
            <p class="placeholder">No upgrades found</p>
        {/if}
    </div>
    
    {#if itemCounter.size > 0}
        {@const deficits = sortItems($makeT3 ? getDeficitsT3($inventory, itemCounter) : getDeficits($inventory, itemCounter))}
        {#key [$makeT3, $inventory]}
        <div>
            <h1 class="title">Item Deficits</h1>
            {#if deficits.length > 0}
                <section class="items">
                    {#each deficits as item}
                        <ItemIcon {...item} --size="100px" />
                    {/each}
                </section>
            {:else}
                <p class="placeholder">No deficits!</p>
            {/if}
        </div>
        {/key}
    {/if}
</section>

<h1 class="title">Inventory</h1>
<section class="content items inv">
    {#each $inventory as item}
        <div>
            <ItemIcon {...item} --size="100px" />
            <NumberInput {min} {max} bind:value={item.count} />
        </div>
    {/each}
</section>



<style>
    .settings {
        padding: calc(1em + 2.25px);
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 1em 3em;
    }
    #filter-status {
        display: flex;
        flex-wrap: wrap;
        gap: 1em 3em;
    }
    #notready {
        background-color: rgba(255, 140, 140, 0.7);
    }
    #ready {
        background-color: rgba(151, 255, 148, 0.7);
    }
    .costs {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        gap: 10px;
    }
    .costs > div {
        flex: 1 1 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .items {
        margin-top: 25px;
        padding: 10px;
        border-radius: 8px;
        background-color: var(--light-strong);
        display: grid;
        grid-template-columns: repeat(auto-fit, 100px);
        justify-content: center;
        gap: 20px;
    }
    .items.inv {
        margin-top: 15px;
        gap: 30px;
    }
    .items > div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>