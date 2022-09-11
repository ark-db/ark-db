<script>
    import { assets } from "$app/paths";
    import { region, normalizeValues } from "@stores";
    import eventShops from "$lib/data/event_shops.json";
    import permaShops from "$lib/data/perma_shops.json";
    import ShopItems from "$lib/components/ShopItems.svelte";
    import ItemIcon from "$lib/components/ItemIcon.svelte";

    async function getItemName(id) {
        let res = await fetch(`/api/items?id=${id}&categories=name`);
        let resData = await res.json();
        return resData.name;
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
    {@const eventName = eventShops.events[$region]?.[type]}
    {@const shopItems = eventShops.shops[$region]?.[type]}
    {#if eventName}
        {@const src = `${assets}/images/events/${$region}_${type}_banner.webp`}
        <section class="event">
            <div class="top">
                <h1 class="title">{eventName}</h1>
                <img class="banner" {src} alt={eventName}>
            </div>
            <ShopItems items={shopItems} {normalizeValues}/>
        </section>
    {/if}
{/each}

{#each permaShops[$region] as shop}
    <section class="event">
        <div class="top">
            <ItemIcon id={shop.currency} --size="100px"/>
            {#await getItemName(shop.currency) then name}
                <h1 class="title">{name} Store</h1>
            {/await}
        </div>
        {#each shop.items as tier}
            <div class="tier">
                <ShopItems items={tier} {normalizeValues}/>
            </div>
        {/each}
    </section>
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
        padding-bottom: 1em;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 1em 2em;
    }
    .title {
        margin: 0 0.5em;
        font-size: 2.5em;
    }
    .banner {
        width: clamp(1px, 80vw, 600px);
    }
    .tier {
        padding-top: 1em;
    }
    .tier + .tier {
        border-top: 0.5px solid var(--med-strong);
    }
</style>