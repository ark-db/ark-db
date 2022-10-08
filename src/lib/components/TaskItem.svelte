<script>
    import OperatorIcon from "./OperatorIcon.svelte";
    import ItemIcon from "./ItemIcon.svelte";
    import deleteIcon from "../images/delete.svg";

    export let showCost, charId, charName, name, ready, id;

    id; // stops SvelteKit from complaining
    const size = 60;
    let upgradeCost = [];

    fetch(`./api/operators/cost?id=${charId}&upgrade=${name}`)
        .then(res => res.json())
        .then(res => upgradeCost = res);
</script>



<section class:ready={ready}>
    <div class="left">
        <input type="checkbox" bind:checked={ready}>
        <div class="info">
            <div class="top">
                <OperatorIcon {charId} {size} />
                <div class="upgrade-desc">
                    <h3>{charName}</h3>
                    <p>{name}</p>
                </div>
            </div>
            {#if $showCost}
                <div class="cost">
                    {#each upgradeCost as item}
                        <ItemIcon {...item} {size} />
                    {/each}
                </div>
            {/if}
        </div>
    </div>
    <input type="image" src={deleteIcon} alt="delete" loading="lazy" on:click>
</section>



<style>
    section {
        padding: 10px;
        border-radius: 10px;
        background-color: rgb(255, 140, 140);
        display: flex;
        align-items: center;
        justify-content: space-between;
        column-gap: 10px;
    }
    .ready {
        background-color: rgb(151, 255, 148);
    }
    .left {
        flex-grow: 1;
        display: flex;
        column-gap: 0.5em;
    }
    .info {
        flex-grow: 1;
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: space-between;
        gap: 1em 2em;
    }
    .top {
        display: flex;
        align-items: center;
        column-gap: 0.75em;
    }
    .upgrade-desc {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    h3 {
        margin: 0.1em 0 0.2em 0;
    }
    p {
        margin: 0.1em 0 0.2em 0;
    }
    .cost {
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        column-gap: 10px;
    }
    input[type=image] {
        margin-left: 10px;
        width: 100%;
        max-width: 15px;
        min-width: 15px;
    }
</style>