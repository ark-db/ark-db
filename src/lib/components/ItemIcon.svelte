<script>
    import items from "../data/items.json";
    export let id;
    export let count = undefined;

    let itemSrc = new URL(`../images/items/${id}.png`, import.meta.url).href;
    let { name, rarity } = items[id];
    let bgSrc = new URL(`../images/rarities/${rarity}.png`, import.meta.url).href;
</script>

<div>
    <img src={bgSrc} alt="background" />
    <img src={itemSrc} alt={name} />
    {#if count !== undefined}
        <p>{count}</p>
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
        max-width: var(--size);
        max-height: var(--size);
    }
    div p {
        grid-area: 1 / 1 / 2 / 2;
        place-self: end;
        margin: 0 calc(var(--size) / 6.1) calc(var(--size) / 9.2) 0;
        padding: 0.1em 0.3em 0.1em 0.3em;
        background-color: rgba(0, 0, 0, 0.7);
        box-shadow: 0.1em 0.2em 0.2em rgba(0, 0, 0, 0.45);
        color: white;
        font-weight: 300;
    }
</style>