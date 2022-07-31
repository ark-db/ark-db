<script>
    import operators from "../data/operators.json";
    export let charId;
    
    let src, name, rarity;
    $: src = `./src/lib/images/operators/${charId}.png`;
    $: ({ name, rarity } = operators[charId]);
</script>

<img class="{rarity}" {src} alt={name} />

<style>
    img {
        border-width: 5px;
        border-style: solid;
        width: 100%;
        max-width: 100px;
        min-width: 100px;
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