<script>
    import operators from "../data/operators.json";
    import OperatorIcon from "./OperatorIcon.svelte";
    import ItemIcon from "./ItemIcon.svelte";
    import deleteIcon from "../images/delete.svg";
    export let splitByStatus;
    export let showCost;
    export let name, cost, charId, id, ready;
</script>

<section class={ready ? "ready" : "notready"}>
    <div class="left">
        {#if !$splitByStatus}
            <input type="checkbox" bind:checked={ready}>
        {/if}
        <div class="info">
            <div class="top">
                <OperatorIcon {charId} --size="60px" --border="0px" />
                <div class="title">
                    <h3>{operators[charId].name}</h3>
                    <p>{name}</p>
                </div>
            </div>
            {#if $showCost}
                <div class="cost">
                    {#each cost as item}
                        <ItemIcon {...item} --size="60px" />
                    {/each}
                </div>
            {/if}
        </div>
    </div>
    <input type="image" src={deleteIcon} alt="delete" on:click />
</section>

<style>
    section {
        padding: 10px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        column-gap: 10px;
    }
    .ready {
        background-color: rgb(151, 255, 148);
    }
    .notready {
        background-color: rgb(255, 140, 140);
    }

    input[type=checkbox] {
        transform: scale(1.5);
    }

    .left {
        display: flex;
        column-gap: 0.75em;
    }
    .left .info {
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: start;
        gap: 1em 2em;
    }
    .left .top {
        display: flex;
        align-items: center;
        column-gap: 0.75em;
    }
    .left .title {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .left .title h3 {
        margin: 0.1em 0 0.2em 0;
    }
    .left .title p {
        margin: 0.1em 0 0.2em 0;
    }

    .left .cost {
        flex-grow: 1;
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: space-evenly;
        column-gap: 5px;
    }

    input[type=image] {
        width: 100%;
        max-width: 15px;
        min-width: 15px;
    }
</style>