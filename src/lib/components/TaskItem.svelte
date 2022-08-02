<script>
    import operators from "../data/operators.json";
    import OperatorIcon from "./OperatorIcon.svelte";
    import deleteIcon from "../images/delete.svg";
    export let ready;
    export let charId;
    export let upgradeName;
</script>

<section class={ready ? "ready" : "notready"}>
    <div>
        <input type="checkbox" bind:checked={ready}>
        <div class="icon">
            <OperatorIcon {charId} --size="50px" --border="0px" />
        </div>
        <h2>{operators[charId].name}</h2>
        <p>{upgradeName}</p>
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
    }
    .ready {
        background-color: rgb(151, 255, 148);
    }
    .notready {
        background-color: rgb(255, 140, 140);
    }
    section div {
        display: grid;
        grid-template-columns: 1.25em 50px auto;
        grid-template-rows: 30px 30px;
        column-gap: 1em;
        align-items: center;
    }
    input[type=checkbox] {
        grid-column: 1 / 2;
        grid-row: 1 / 3;
        transform: scale(1.5);
        justify-self: center
    }
    .icon {
        grid-column: 2 / 3;
        grid-row: 1 / 3;
        display: flex;
        justify-self: center;
        align-items: center;
    }
    h2 {
        grid-column: 3 / 4;
        grid-row: 1 / 2;
    }
    p {
        grid-column: 3 / 4;
        grid-row: 2 / 3;
    }
    input[type=image] {
        width: 100%;
        max-width: 15px;
        min-width: 15px;
    }
</style>