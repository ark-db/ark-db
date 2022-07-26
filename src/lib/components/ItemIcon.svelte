<script>
    import items from "../data/items.json";
    export let itemId;

    let itemSrc = new URL(`../data/images/items/${itemId}.png`, import.meta.url).href;
    let name = items[itemId].name;
    let bgSrc = new URL(`../data/images/bg/${items[itemId].rarity}.png`, import.meta.url).href;
</script>

<img src={bgSrc} alt="background" />
<img src={itemSrc} alt={name} />

<style>
    img {
        position: absolute;
        top: 0;
        left: 0;
        transform: translate(-50%, -50%);
    }
</style>