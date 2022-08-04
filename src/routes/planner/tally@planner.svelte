<script>
    import { allSelected } from "../stores.js";

    $: itemCounter = counter($allSelected.map(upgrade => upgrade.cost).flat());
    $: console.log(itemCounter);

    const counter = (list) => {
        return Object.entries(list.reduce((prev, curr) => ({...prev, [curr.id]: curr.count + (prev[curr.id] ?? 0)}), {}))
                     .map(item => ({id: item[0], count: item[1]}));
    };
</script>