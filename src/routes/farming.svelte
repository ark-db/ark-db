<svelte:head>
    <title>Farming Stages</title>
    <meta name="description" content="A list of the best Arknights farming stages for materials, with stage efficiencies, drop rates, and expected sanity costs." />
</svelte:head>

<script>
    import { region } from "./stores.js";
    import farming from "$lib/data/farming.json";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    import FarmingStage from "$lib/components/FarmingStage.svelte";

    function sortItems(list) {
        return list.sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };
</script>

<section class="grid">
    {#each sortItems(farming[$region]) as { id, stages }}
        <div class="item">
            <ItemIcon {id} --size="100px" />
            {#each stages.slice(0, 3) as stage}
                <FarmingStage {...stage} />
            {/each}
        </div>
    {/each}
    </section>

<style>
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, 30em);
        gap: 1em;
    }
    .item {
        flex-grow: 1;
        display: flex;
        align-items: center;
    }
</style>