<svelte:head>
    <title>Farming Stages</title>
    <meta name="description" content="A list of the best Arknights farming stages for materials, with stage efficiencies, drop rates, and expected sanity costs." />
</svelte:head>

<script>
    import { region, sortMode } from "@stores";
    import { sortItems } from "@utils";
    import farming from "$lib/data/farming.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
    import FarmingStage from "$lib/components/FarmingStage.svelte";

    function sortStages(stages, mode) {
        return stages.sort((prev, curr) => (prev[mode] - curr[mode]) * (mode === "effic" ? -1 : 1))
    }
</script>

<section class="content settings">
    <div>
        <label>
            <input type=radio bind:group={$region} value={"glb"}>
            US/JP/KR
        </label>
        <label>
            <input type=radio bind:group={$region} value={"cn"}>
            CN
        </label>
    </div>
    <div>
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
        margin-top: 1em;
        padding: 0.5em;
        background-color: var(--light-strong);
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 0.5em 1.5em;
    }
    .settings label {
        margin: 0.5em;
        display: flex;
        align-items: center;
    }
    .grid {
        margin: 2em 0;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(10em, 30em));
        justify-content: center;
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
    input[type=radio] {
        transform: scale(1.25);
        margin-right: 1em;
    }
</style>