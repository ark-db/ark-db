<script>
    export let charId;
    export let name;
    export let rarity;
    $: src = new URL(`../images/operators/${charId}.png`, import.meta.url).href;
</script>

<img class="{rarity}" {src} alt={name} />

<style>
    img {
        border-width: 5px;
        border-style: solid;
        width: 100%;
        max-width: 80px;
        min-width: 80px;
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