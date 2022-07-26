<script>
    export let itemId;
    let src = new URL(`../data/images/items/${itemId}.png`, import.meta.url).href
</script>

<img {src} alt="item" />