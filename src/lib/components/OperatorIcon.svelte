<script>
    import operators from "../data/operators.json";
    export let charId;
    
    $: src = new URL(`../images/operators/${charId}.webp`, import.meta.url).href;
    $: ({ name, rarity } = operators[charId]);
</script>

<img class={rarity} {src} alt={name} />

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