<script>
    import operators from "../data/operators.json";
    export let selectedChar;
    $: src = new URL(`../images/operators/${$selectedChar}.png`, import.meta.url).href;
    let { name } = operators[$selectedChar];
</script>

<img {src} alt={name} />