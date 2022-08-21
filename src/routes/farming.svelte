<svelte:head>
    <title>Farming Stages</title>
    <meta name="description" content="A list of the best Arknights farming stages for materials, with stage efficiencies, drop rates, and expected sanity costs." />
</svelte:head>

<script>
    import { region, sortMode } from "./stores.js";
    import farming from "$lib/data/farming.json";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    import FarmingStage from "$lib/components/FarmingStage.svelte";

    function sortItems(list) {
        return list.sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };
    function sortStages(stages, mode) {
        return stages.sort((prev, curr) => (prev[mode] - curr[mode]) * (mode === "effic" ? -1 : 1))
    }
</script>

<section class="content settings">
    <div class="group">
        <label>
            <input type=radio bind:group={$region} value={"glb"}>
            US/JP/KR
        </label>
        <label>
            <input type=radio bind:group={$region} value={"cn"}>
            CN
        </label>
    </div>
    <div class="group">
        <label>
            <input type=radio bind:group={$sortMode} value={"effic"}>
            Sort by stage efficiency
        </label>
        <label>
            <input type=radio bind:group={$sortMode} value={"espd"}>
            Sort by expected sanity per drop
        </label>
    </div>
</section>

<section class="grid">
    {#each sortItems(farming[$region]) as { id, stages }}
        <div class="item">
            <ItemIcon {id} --size="75px" />
            <div class="stages">
                {#each sortStages(stages, $sortMode).slice(0, 3) as stage}
                    <FarmingStage {...stage} />
                {/each}
            </div>
        </div>
    {/each}
</section>

<style>
    .settings {
        margin-top: 2em;
        padding: 1em;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 1em;
    }
    .group {
        display: flex;
        gap: 2em;
    }
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
    label {
        display: flex;
        align-items: center;
    }
    input[type=radio] {
        transform: scale(1.25);
        margin-right: 1em;
    }
</style>