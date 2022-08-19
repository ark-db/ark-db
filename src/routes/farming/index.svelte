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

    let farmingItems = Object.values(items)
                             .filter(({ item }) => item.type === "material" || item.type === "misc")
</script>

<section class="settings">

</section>

<section class="items">
    {#each farmingItems as item}
        {{}}
    {/each}
</section>