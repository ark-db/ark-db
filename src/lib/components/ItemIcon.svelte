<script>
    import items from "../data/items.json";
    export let itemId;
    export let qty = undefined;

    let itemSrc = new URL(`../images/items/${itemId}.png`, import.meta.url).href;
    let { name, rarity } = items[itemId];
    let bgSrc = new URL(`../images/ranks/rarity/${rarity}.png`, import.meta.url).href;
</script>

<div>
    <img src={bgSrc} alt="background" />
    <img src={itemSrc} alt={name} />
    {#if qty !== undefined}
        <p>{qty}</p>
    {/if}
</div>

<style>
    div {
        display: grid;
        grid-template-columns: var(--size);
        grid-template-rows: var(--size);
    }
    div img {
        grid-area: 1 / 1 / 2 / 2;
        place-self: center;
    }
    div p {
        grid-area: 1 / 1 / 2 / 2;
        place-self: end;
        margin: 0 calc(var(--size) / 20) calc(var(--size) / 20) 0;
        padding: 0.2em;
        background-color: rgba(0, 0, 0, 0.7);
    }
</style>