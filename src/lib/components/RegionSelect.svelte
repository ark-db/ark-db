<script>
    import { region } from "@stores";
    import globe from "../images/globe.svg";
</script>



<div>
    <img src={globe} alt="Globe">
    <select bind:value={$region}>
        <option value="glb">US/JP/KR</option>
        <option value="cn">CN</option>
    </select>
</div>



<style>
    div {
        margin-right: 0.25em;
        display: flex;
        gap: 15px;
    }
    img {
        width: 100%;
        max-width: 20px;
        min-width: 20px;
    }
    select {
        border: 1px solid white;
        border-radius: 0.75em;
        padding: 0.75em 2em 0.75em 1em;
        background-color: transparent;
        width: 100%;
        max-width: 10em;
        color: var(--light-moderate);
        font-weight: 600;
        appearance: none;
        background-image: url("../images/arrow-down.svg");
        background-repeat: no-repeat;
        background-position-x: calc(100% - 10px);
        background-position-y: 50%;
        background-size: 10px;
    }
    option {
        color: black;
    }
</style>