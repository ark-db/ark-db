<script>
    import operators from "../data/operators.json";
    export let selectedChar;
    $: src = new URL(`../images/operators/${$selectedChar.charId}.png`, import.meta.url).href;
    $: ({ name, rarity } = operators[$selectedChar.charId]);
</script>

<img class="{rarity}" {src} alt={name} />

<style>
    img {
        border-width: 5px;
        border-style: solid;
    }
    img.\36 {
        border-color: #ed702d;
    }
    img.\35 {
        border-color: #f3b13e;
    }
    img.\34 {
        border-color: #d4b3d8;
    }
    img.\33 {
        border-color: #4faff0;
    }
</style>