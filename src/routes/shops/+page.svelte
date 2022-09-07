<script>
    import { assets } from "$app/paths";
    import { region, normalizeEffics } from "@stores";
    import shops from "$lib/data/shops.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";

    $: ({ ss: ssName = undefined, cc: ccName = undefined } = shops.events[$region]);
    $: ({ ss: ssShopItems = undefined, cc: ccShopItems = undefined } = shops.shops[$region]);

    $: ssSrc = `${assets}/images/events/${$region}_ss_banner.webp`;
    $: ccSrc = `${assets}/images/events/${$region}_cc_banner.webp`;

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
        <input type="checkbox" bind:checked={$normalizeEffics}>
        Normalize item efficiencies
    </label>
</section>

{#if ssName}
    {@const ssMaxEffic = Math.max(...ssShopItems.map(item => item.effic))}
    <section class="event">
        <div class="top">
            <h1 class="title">{ssName}</h1>
            <img class="banner" src={ssSrc} alt={ssName}>
        </div>
        <div class="items">
            {#each ssShopItems as { id, count, stock, effic }}
                {@const normEffic = effic / ssMaxEffic}
                <div class="item">
                    <ItemIcon {id} {count} --size="75px"/>
                    <p class="stock" title="Item stock">
                        {stock !== -1 ? stock : "∞"}
                    </p>
                    <p class="effic {categorize(normEffic)}"
                       title={$normalizeEffics ? "Relative efficiency" : "Sanity value per token"}
                    >
                        {$normalizeEffics ? normEffic.toFixed(3) : effic}
                    </p>
                </div>
            {/each}
        </div>
    </section>
{/if}

{#if ccName}
    {@const ccMaxEffic = Math.max(...ccShopItems.map(item => item.effic))}
    <section class="event">
        <div class="top">
            <h1 class="title">{ccName}</h1>
            <img class="banner" src={ccSrc} alt={ccName}>
        </div>
        <div class="items">
            {#each ccShopItems as { id, count, stock, effic }}
                {@const normEffic = effic / ccMaxEffic}
                <div class="item">
                    <ItemIcon {id} {count} --size="75px"/>
                    <p class="stock" title="Item stock">
                        {stock !== -1 ? stock : "∞"}
                    </p>
                    <p class="effic {categorize(normEffic)}"
                       title={$normalizeEffics ? "Relative efficiency" : "Sanity value per token"}
                    >
                        {$normalizeEffics ? normEffic.toFixed(3) : effic}
                    </p>
                </div>
            {/each}
        </div>
    </section>
{/if}



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