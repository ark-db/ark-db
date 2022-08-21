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

<div class="grid">
    {#each sortItems(farming[$region]) as { id, stages }}
        <div class="item">
            <ItemIcon {id} --size="75px" />
            <div class="stages">
                {#each stages.slice(0, 3) as stage}
                    <FarmingStage {...stage} />
                {/each}
            </div>
        </div>
    {/each}
</div>

<style>
    .grid {
        margin: 2em 0;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(10em, 30em));
        gap: 3em 1em;
    }
    .item {
        display: flex;
        align-items: center;
    }
    .stages {
        margin-left: 0.75em;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5em 1.5em;
    }
</style>