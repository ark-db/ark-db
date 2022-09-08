<script>
    import { assets } from "$app/paths";
    import { region, normalizeValues } from "@stores";
    import shops from "$lib/data/event_shops.json";
    import ShopItems from "$lib/components/ShopItems.svelte";
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
        <section class="event">
            <div class="top">
                <h1 class="title">{eventName}</h1>
                <img class="banner" {src} alt={eventName}>
            </div>
            <ShopItems items={shopItems} {normalizeValues}/>
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
</style>