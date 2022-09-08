<script>
    import { assets } from "$app/paths";
    import { region, normalizeValues } from "@stores";
    import shops from "$lib/data/event_shops.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";

    function categorize(score) {
        if (score < 0.5) return "poor";
        else if (score < 0.7) return "bad";
        else if (score < 0.8) return "fair"
        else if (score < 0.9) return "good";
        else return "great";
    };
</script>



<svelte:head>
    <title>Shop Efficiencies</title>
    <meta name="description" content="A list of item efficiencies of certificate and current event shops.">
</svelte:head>

<section class="content settings">
    <label>
        <input type="checkbox" bind:checked={$normalizeValues}>
        Normalize item efficiencies
    </label>
</section>

{#each ["ss", "cc"] as type}
    {@const eventName = shops.events[$region]?.[type]}
    {@const shopItems = shops.shops[$region]?.[type]}
    {#if eventName}
        {@const src = `${assets}/images/events/${$region}_${type}_banner.webp`}
        {@const maxValue = Math.max(...shopItems.map(item => item.value))}
        <section class="event">
            <div class="top">
                <h1 class="title">{eventName}</h1>
                <img class="banner" {src} alt={eventName}>
            </div>
            <div class="items">
                {#each shopItems as { id, count, stock, value }}
                    {@const effic = value / maxValue}
                    <div class="item">
                        <ItemIcon {id} {count} --size="75px"/>
                        <p class="stock" title="Item stock">
                            {stock !== -1 ? stock : "∞"}
                        </p>
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
        </section>
    {/if}
{/each}



<style>
    .settings {
        margin-top: 0.5em;
        padding: 1em;
        background-color: var(--light-moderate);
    }
    .event {
        margin: 1em 0;
        padding: 1em;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .event + .event {
        margin-top: 3em;
    }
    .top {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 1em 5em;
    }
    .title {
        margin: 0 0.5em;
        font-size: 2.5em;
    }
    .banner {
        width: clamp(1px, 80vw, 600px);
    }
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
        gap: 2.75em;
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