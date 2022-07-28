<script>
    export let text;
    export let type;
    export let id = null;
    export let activeUpgrade;

    const setActive = () => {
        if (type === "mastery") {
            $activeUpgrade = `./src/lib/images/skills/${id}.png`;
        } else if (type === "module") {
            $activeUpgrade = `./src/lib/images/modules/${id}.png`;
        }
    };
    const unsetActive = () => {
        $activeUpgrade = "";
    };
</script>

<label on:mouseenter={setActive} on:mouseleave={unsetActive} >
    <input type="checkbox">
    {text}
</label>

<style>
    label {
        padding: 1em;
        background-color: rgb(215, 218, 224);
    }
    input {
        margin-right: 0.5em;
        transform: scale(1.5);
    }
</style>