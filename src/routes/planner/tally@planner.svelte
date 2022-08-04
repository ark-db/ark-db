<script>
    import { allSelected } from "../stores.js";
    import items from "/src/lib/data/items.json?import"

    $: itemCounter = counter($allSelected.map(upgrade => upgrade.cost).flat());
    $: console.log(itemCounter);

    const counter = (list) => {
        return Object.entries(list.reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {}))
                     .map(item => ({id: item[0], count: item[1]}))
                     .sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
    };
</script>