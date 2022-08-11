<script>
    import items from "../data/items.json";
    export let id;
    export let count = undefined;

    $: itemSrc = new URL(`../images/items/${id}.webp`, import.meta.url).href;
    $: ({ name, rarity } = items[id]);
    $: bgSrc = new URL(`../images/rarities/${rarity}.webp`, import.meta.url).href;

    const compactNum = Intl.NumberFormat("en-US", {
        notation: "compact",
        maximumFractionDigits: 2
    });
</script>

<div>
    <img src={bgSrc} alt="background" />
    <img src={itemSrc} alt={name} />
    {#if count !== undefined}
        <p class:neg={count < 0}>{compactNum.format(count)}</p>
    {/if}
</div>

<style>
    div {
        display: grid;
        grid-template-columns: var(--size);
        grid-template-rows: var(--size);
    }
    img {
        grid-area: 1 / 1 / 2 / 2;
        place-self: center;
        max-width: var(--size);
        max-height: var(--size);
    }
    p {
        grid-area: 1 / 1 / 2 / 2;
        place-self: end;
        margin: 0 calc(var(--size) / 6.1) calc(var(--size) / 9.2) 0;
        padding: 0.1em 0.3em 0.05em 0.3em;
        background-color: rgba(0, 0, 0, 0.7);
        box-shadow: 0.1em 0.2em 0.2em rgba(0, 0, 0, 0.45);
        color: white;
        font-weight: 300;
        font-size: clamp(85%, 1em, calc(var(--size) / 5))
    }
    .neg {
        color: rgb(255, 61, 61);
    }
</style>