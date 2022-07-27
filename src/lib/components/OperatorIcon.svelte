<script>
    import operators from "../data/operators.json";
    export let charId;
    let src = new URL(`../images/operators/${charId}.png`, import.meta.url).href;
    let { name } = operators[charId];
</script>

<img {src} alt={name} />