<script>
    import addIcon from "../images/plus.svg";
    import minusIcon from "../images/minus.svg";

    export let value = null;
    export let max = undefined;
    export let min = undefined;

    $: error = value == null || value > max || value < min;

    function updateValue(direction) {
        value = Math.max(min, Math.min(value + direction, max));
    };
    function parse(raw) {
        return raw != "" ? Number(raw) : null;
    };
</script>



<div>
    <button type="button"
            title="decrement"
            aria-label="decrement"
            disabled={value < min}
            on:click={() => updateValue(-1)}
    >
        <img src={minusIcon} alt="decrement">
    </button>
    <input type="number"
           pattern="[0-9]+"
           aria-label="Numeric input field with increment and decrement buttons"
           max={max}
           min={min}
           step=1
           value={value ?? ""}
           on:input={({ target }) => value = parse(target.value)}
           on:blur={() => updateValue(0)}
    >
    <button type="button"
            title="increment"
            aria-label="increment"
            disabled={value > max}
            on:click={() => updateValue(1)}
    >
        <img src={addIcon} alt="increment">
    </button>
</div>
{#if error}
    <p>Number must be between {min} and {max}.</p>
{/if}



<style>
    div {
        margin-top: 6px;
        display: flex;
    }
    button {
        border: transparent;
        background: transparent;
        display: flex;
        align-items: center;
    }
    img {
        width: 100%;
        max-width: 20px;
        min-width: 20px;
    }
    /* Chrome, Safari, Edge, Opera */
    input::-webkit-outer-spin-button, input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input[type=number] {
        -moz-appearance: textfield; /* Firefox */
        height: 1.5em;
        width: 4em;
        border: 1px solid rgba(0, 0, 0, 0.3);
        border-radius: 1em;
        background: transparent;
        text-align: center;
    }
    p {
        margin-top: 0.5em;
        color: red;
        font-size: 0.75em;
    }
</style>