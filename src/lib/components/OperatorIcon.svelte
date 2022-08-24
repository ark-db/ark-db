<script>
    import { onMount } from "svelte";
    import operators from "../data/operators.json";
    export let charId;

    let { name, rarity } = operators[charId];
    let src;

    onMount(async () => {
        src = (await import(`../images/operators/${charId}.webp`)).default;
    });
</script>

<img class={rarity} {src} title={name} alt={name} />

<style>
    img {
        border-width: var(--border);
        border-style: solid;
        width: 100%;
        max-width: var(--size);
        min-width: var(--size);
    }
    .\36 {
        border-color: #ed702d;
    }
    .\35 {
        border-color: #f3b13e;
    }
    .\34 {
        border-color: #d4b3d8;
    }
    .\33 {
        border-color: #4faff0;
    }
</style>