<script>
    import operators from "../data/operators.json";
    import OperatorIcon from "./OperatorIcon.svelte";
    export let charId;
    export let upgradeName;
</script>

<section>
    <div class="icon">
        <OperatorIcon {charId} --size="50px" />
    </div>
    <h2>{operators[charId].name}</h2>
    <p>{upgradeName}</p>
</section>

<style>
    section {
        padding: 10px;
        margin-top: 5px;
        background-color: rgb(235, 238, 244);
        display: grid;
        grid-template-columns: 50px 20em;
        grid-template-rows: 30px 30px;
        column-gap: 1.25em;
        justify-items: start;
        align-items: center;
    }
    .icon {
        grid-column: 1 / 2;
        grid-row: 1 / 3;
        display: flex;
        align-items: center;
    }
    h2 {
        grid-column: 2 / 3;
        grid-row: 1 / 2;
    }
    p {
        grid-column: 2 / 3;
        grid-row: 2 / 3;
    }

</style>