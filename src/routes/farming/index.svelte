<svelte:head>
    <title>Farming Stages</title>
    <meta name="description"
          content="A list of the best Arknights farming stages for materials,
                   with stage efficiencies, drop rates, and expected sanity costs."
    />
</svelte:head>

<script>
    import { region } from "../stores.js";
    import farming from "$lib/data/farming.json";
    import items from "$lib/data/items.json";
    import ItemIcon from "$lib/components/ItemIcon.svelte";
</script>

<p>Lorem Ipsum</p>

<section class="items">
    {#each farming[$region].sort((prev, curr) => items[prev.itemId].sortId - items[curr.itemId].sortId) as { itemId, stages }}
        <ItemIcon id={itemId} />
    {/each}
</section>

<style>
    .items {
        padding: 0;
    }
</style>