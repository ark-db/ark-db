<script>
    import { region, sortMode } from "@stores";
    import { sortItems } from "@utils";
    import farming from "$lib/data/farming.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    import FarmingStage from "$lib/components/FarmingStage.svelte";

    // by decreasing efficiency or increasing expected sanity per drop
    const sortStages = (stages, mode) => stages.sort((prev, curr) => (prev[mode] - curr[mode]) * (mode === "effic" ? -1 : 1));
</script>



<svelte:head>
    <title>Farming Stages</title>
    <meta property="og:title" content="Farming Stages">
    <meta name="description" content="A list of the best Arknights farming stages for materials, with stage efficiencies, drop rates, and expected sanity costs.">
</svelte:head>

<section class="content settings">
    <label>
        <input type=radio bind:group={$sortMode} value={"effic"}>
        Sort by stage efficiency
    </label>
    <label>
        <input type=radio bind:group={$sortMode} value={"espd"}>
        Sort by expected sanity per drop
    </label>
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
        margin-top: 0.5em;
        padding: 0.5em;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        gap: 0.25em 1.5em;
    }
    .settings label {
        margin: 0.5em;
    }
    input[type=radio] {
        transform: scale(1.5);
        margin-right: 0.5em;
        margin-bottom: 0.25em;
    }
    .grid {
        margin: 2em 0;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(10em, 30em));
        justify-content: center;
        gap: 4em 1em;
    }
    .item {
        display: flex;
        align-items: center;
    }
    .stages {
        margin-left: 1em;
        display: flex;
        flex-wrap: wrap;
        gap: 1.5em;
    }
</style>