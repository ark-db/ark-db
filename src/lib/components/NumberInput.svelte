<script>
    import { createEventDispatcher } from "svelte";
    import plusIcon from "../images/plus.svg";
    import minusIcon from "../images/minus.svg";

    export let value = null;
    export let min = 0;
    export let max = 999999;

    const dispatch = createEventDispatcher();

    function updateValue(direction) {
        const nextValue = (value += direction);

        if (nextValue < min) {
            value = min;
        } else if (nextValue > max) {
            value = max;
        } else {
            value = nextValue;
        }

        // value = Math.max(min, Math.min(value + direction, max))

        dispatch("input", value);
        dispatch("change", value);
    }

    function onInput({ target }) {
        value = parse(target.value);
        dispatch("input", value);
    }

    function onChange({ target }) {
        // needs symmetry?
        dispatch("change", parse(target.value));
    }
</script>



<div>
    <input type="image" src={minusIcon} alt="decrement" on:click={() => updateValue(-1)}>
    <input type="number" {min} {max} value={value ?? ""} on:change={onChange} on:input={onInput}>
    <input type="image" src={plusIcon} alt="increment" on:click={() => updateValue(1)}>
</div>



<style>
    div {
        display: flex;
        align-items: center;
    }
    input[type=image] {
        margin: 0 5px;
        width: 100%;
        max-width: 15px;
        min-width: 15px;
    }
    input[type=number] {
        width: 80px;
    }
</style>