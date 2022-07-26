<script>
    export let itemId;
    let url = `./images/items/${itemId}.png`
</script>

<img src={url} alt="item" />