<script>
    import { allSelected, inventory, costFilter, itemFilter, makeT3 } from "@stores";
    import { sortItems } from "@utils";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    import NumberInput from "$lib/components/NumberInput.svelte";

    const min = 0;
    const max = 999999;
    let itemCounter = new Map();

    async function getCost({ charId, name }) {
        let res = await fetch(`/api/operators/cost?id=${charId}&upgrade=${name}`);
        let resData = await res.json();
        return resData;
    };
    
    $: Promise.all($allSelected.filter(({ ready }) => $costFilter.includes(ready))
                               .map(upgrade => getCost(upgrade)))
              .then(costs => {
                    itemCounter = new Map(Object.entries(
                        costs.flat()
                             .filter(({ id }) => $itemFilter.includes(items[id].type))
                             .reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {})
                    ))
              });

    const normalize = counter => Array.from(counter).map(([id, count]) => ({id, count}));

    function convertToT3(counter) {
        const itemCounts = new Map();
        
        function convert(id, count) {
            const { rarity, recipe = undefined } = items[id];
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
        const stock = Object.fromEntries(inv.map(({ id, count }) => [id, count]));
        const deficits = Array.from(costs)
                              .map(([ id, count ]) => ({id, count: stock[id] - count}))
                              .filter(({ id, count }) => id !== "4001" && count < 0);
        return deficits;
    };

    function getDeficitsT3(inv, costs) {
        const stock = new Map(inv.map(({ id, count }) => ([id, count])));
        const deficits = new Set();

        function searchForDeficits(id, qtyNeeded) {
            stock.set(id, stock.get(id) - qtyNeeded);
            if (stock.get(id) < 0) {
                const { rarity, recipe = undefined } = items[id];
                if (rarity > 2 && recipe) {
                    recipe.forEach(({ id: matId, count }) => searchForDeficits(matId, -stock.get(id)*count));
                    stock.set(id, 0);
                } else {
                    deficits.add(id);
                }
            }
        };

        function patchDeficits(itemId) {
            const { recipe = undefined } = items[itemId];
            if (recipe) {
                let minCraftable = Infinity;
                for (const { id, count } of recipe) {
                    const craftable = Math.floor(stock.get(id)/count);
                    if (craftable <= 0) return;
                    else if (craftable < minCraftable) minCraftable = craftable;
                }
                recipe.forEach(({ id, count }) => stock.set(id, stock.get(id) - minCraftable*count));
                stock.set(itemId, stock.get(itemId) + minCraftable);
            }
        };

        for (const [id, count] of costs) {
            searchForDeficits(id, count);
        }

        Array.from(deficits)
             .sort((prev, curr) => items[prev].rarity - items[curr].rarity)
             .forEach(id => patchDeficits(id));
        
        return normalize(stock).filter(({ id, count }) => deficits.has(id) && count < 0);
    };
</script>



<svelte:head>
    <title>Cost Calculator</title>
    <meta name="description" content="A calculator for upgrade costs of operators in Arknights.">
</svelte:head>

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
        <input type="checkbox" bind:checked={$makeT3}>
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

{#key [$makeT3, $costFilter, $itemFilter, $inventory]}
<section class="costs">
    <div>
        <h1 class="title">Upgrade Costs</h1>
        {#if itemCounter.size > 0}
            {@const costs = sortItems(normalize($makeT3 ? convertToT3(itemCounter) : itemCounter))}
            <section class="items">
                {#each costs as item}
                    <ItemIcon {...item} --size="100px" />
                {/each}
            </section>
        {:else}
            <p class="placeholder">No upgrades found</p>
        {/if}
    </div>
    
    {#if itemCounter.size > 0}
        {@const deficits = sortItems($makeT3 ? getDeficitsT3($inventory, itemCounter) : getDeficits($inventory, itemCounter))}
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
    {/if}
</section>
{/key}

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