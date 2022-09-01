<script>
    import { assets } from "$app/paths";

    export let activeCategory, selectedUpgradeNames, category, idx;

    const { names } = category;
    let selectedNames = new Set();

    function replaceAt(index, value) {
        let temp = $selectedUpgradeNames.slice(0);
        temp[index] = value;
        return temp;
    };

    const setActiveCategory = () => {
        if (category?.cls === "mastery") $activeCategory = `${assets}/images/skills/${category.skillId}.webp`;
        else if (category?.cls === "module") $activeCategory = `${assets}/images/modules/${category.moduleId}.webp`;
    };

    const unsetActiveCategory = () => $activeCategory = "";

    const onCheckName = event => {
        event.target.checked ? selectedNames.add(event.target.value) : selectedNames.delete(event.target.value);
        selectedNames = selectedNames;
        $selectedUpgradeNames = replaceAt(idx, selectedNames)
    };

    const onSelectAll = event => {
        event.target.checked ? selectedNames = new Set(names) : selectedNames.clear();
        selectedNames = selectedNames;
        $selectedUpgradeNames = replaceAt(idx, selectedNames)
    };
</script>

<ol on:mouseenter={setActiveCategory} on:mouseleave={unsetActiveCategory}>
    {#if names.length > 1}
        <li>
            <label>
                <input type="checkbox" checked={selectedNames.size === names.length} on:change={onSelectAll}>
                <strong>Select All</strong>
            </label>
        </li>
    {/if}
    {#each names as name}
        <li>
            <label>
                <input type="checkbox" value={name} checked={selectedNames.has(name)} on:change={onCheckName}>
                {name}
            </label>
        </li>
    {/each}
</ol>

<style>
    ol {
        list-style-type: none;
        margin: 5px;
        padding: 10px;
        border-radius: 8px;
        background-color: var(--med-mild);
        display: flex;
        flex-direction: column;
        row-gap: 1em;
    }
</style>