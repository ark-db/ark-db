<script>
    import { allSelected } from "../stores.js";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";

    $: itemCounter = counter($allSelected.map(upgrade => upgrade.cost).flat());

    const counter = (list) => {
        return Object.entries(list.reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {}))
                     .map(item => ({id: item[0], count: item[1]}))
                     .sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };
</script>

<div class="page">
    <div class="costs">
        {#if itemCounter}
            {#each itemCounter as item}
                <ItemIcon {...item} --size="100px" />
            {/each}
        {/if}
    </div>
</div>

<style>
    .page {
        margin: 5px;
        padding: 5px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .costs {
        display: grid;
        grid-template-columns: repeat(auto-fit, 100px);
        justify-content: center;
        gap: 8px;
        padding: 10px;
        background-color: rgb(235, 238, 244);
    }
</style>