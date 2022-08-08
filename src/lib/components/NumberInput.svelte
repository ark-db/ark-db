<script>
    import addIcon from "../images/plus.svg";
    import minusIcon from "../images/minus.svg";

    export let value = null;
    export let max = undefined;
    export let min = undefined;
    export let invalidText = "";

    function updateValue(direction) {
        value = Math.max(min, Math.min(value + direction, max));
    }

    $: error = value == null || value > max || value < min;

    function parse(raw) {
      return raw != "" ? Number(raw) : null;
    }

    function onInput({ target }) {
      value = parse(target.value);
    }
</script>

<div>
    <div>
        <div>
            <input type="number"
                   pattern="[0-9]+"
                   aria-label="Numeric input field with increment and decrement buttons"
                   max="{max}"
                   min="{min}"
                   step=1
                   value="{value ?? ''}"
                   on:input="{onInput}"
            >
            <div>
                <button type="button"
                        title="decrement"
                        aria-label="decrement"
                        on:click="{() => updateValue(-1)}"
                >
                    <img src={minusIcon} alt="decrement">
                </button>
                <button type="button"
                        title="increment"
                        aria-label="increment"
                        on:click="{() => updateValue(1)}"
                >
                    <img src={addIcon} alt="increment">
                </button>
            </div>
        </div>
        {#if error}
            <div>
                {invalidText}
            </div>
        {/if}
    </div>
</div>