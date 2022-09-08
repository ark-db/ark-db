<script>
    import ItemIcon from "./ItemIcon.svelte";
    export let items, normalizeValues;

    let maxValue = Math.max(...items.map(item => item.value));

    function categorize(score) {
        if (score < 0.5) return "poor";
        else if (score < 0.7) return "bad";
        else if (score < 0.8) return "fair"
        else if (score < 0.9) return "good";
        else return "great";
    };
</script>



<div class="items">
    {#each items as { id, count, stock, value }}
        {@const effic = value / maxValue}
        <div class="item">
            <ItemIcon {id} {count} --size="75px"/>
            {#if stock !== -2}
                <p class="stock" title="Item stock">
                    {stock !== -1 ? stock : "∞"}
                </p>
            {/if}
            {#if value !== -1}
                <p class="effic {categorize(effic)}"
                   title={$normalizeValues ? "Relative efficiency" : "Sanity value per token"}
                >
                    {$normalizeValues ? effic.toFixed(3) : value}
                </p>
            {:else}
                <p class="effic none"
                   title={$normalizeValues ? "Relative efficiency" : "Sanity value per token"}
                >
                    ——
                </p>
            {/if}
        </div>
    {/each}
</div>



<style>
    .items {
        display: grid;
        grid-template-columns: repeat(auto-fill, calc(75px + 6em));
        justify-content: center;
        gap: 20px;
    }
    .item {
        position: relative;
        display: flex;
        align-items: center;
        gap: 2.5em;
    }
    .effic {
        font-weight: 600;
    }
    .effic.none {
        color: var(--light-moderate);
    }
    .stock {
        position: absolute;
        top: -5px;
        left: 30px;
        z-index: -1;
        padding: 0.15em 0.5em 0.15em 3em;
        border-radius: 1em;
        background-color: var(--light-moderate);
        font-weight: 500;
    }
</style>