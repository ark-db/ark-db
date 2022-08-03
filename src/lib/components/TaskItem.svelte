<script>
    import operators from "../data/operators.json";
    import OperatorIcon from "./OperatorIcon.svelte";
    import deleteIcon from "../images/delete.svg";
    export let splitByStatus;
    export let showCost;
    export let ready;
    export let charId;
    export let upgradeName;
</script>

<section class={ready ? "ready" : "notready"}>
    <div class="left">
        {#if !$splitByStatus}
            <input type="checkbox" bind:checked={ready}>
        {/if}
        <div id="icon">
            <OperatorIcon {charId} --size="50px" --border="0px" />
        </div>
        {#if $showCost}
            {{}}
        {:else}
            <div class="name">
                <h3>{operators[charId].name}</h3>
                <p>{upgradeName}</p>
            </div>
        {/if}
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
    section .left {
        display: flex;
        column-gap: 0.75em;
    }
    section .left #icon {
        align-self: center;
        align-items: center;
        justify-content: center;
    }
    section .left .name {
        display: flex;
        flex-direction: column;
    }
    .name h3 {
        margin: 0.1em 0 0.2em 0;
    }
    .name p {
        margin: 0.1em 0 0.2em 0;
    }
    input[type=image] {
        width: 100%;
        max-width: 15px;
        min-width: 15px;
    }
</style>