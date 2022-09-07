<script>
    import { assets } from "$app/paths";
    import { region } from "@stores";
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

{#if ssName}
    {@const ssMaxEffic = Math.max(...ssShopItems.map(item => item.effic))}
    <section class="event">
        <div class="top">
            <h1 class="title">{ssName}</h1>
            <img class="banner" src={ssSrc} alt={ssName}>
        </div>
        <div class="items">
            {#each ssShopItems as { id, count, effic }}
                <div class="item">
                    <ItemIcon {id} {count} --size="75px"/>
                    <p class={categorize(effic / ssMaxEffic)} title="Sanity value per token">
                        {effic}
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
            {#each ccShopItems as { id, count, effic }}
                <div class="item">
                    <ItemIcon {id} {count} --size="75px"/>
                    <p class={categorize(effic / ccMaxEffic)} title="Sanity value per token">
                        {effic}
                    </p>
                </div>
            {/each}
        </div>
    </section>
{/if}



<style>
    .event {
        margin-top: 1em;
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
        grid-template-columns: repeat(auto-fill, calc(75px + 5em));
        justify-content: center;
        gap: 20px;
    }
    .item {
        display: flex;
        align-items: center;
        gap: 1em;
    }
    .item p {
        font-weight: 600;
    }
    .poor {
        color: #f13737;
    }
    .bad {
        color: #ff9505;
    }
    .fair {
        color: #f3dc48;
    }
    .good {
        color: #9be564;
    }
    .great {
        color: #00be43;
    }
</style>