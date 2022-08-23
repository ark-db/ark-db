<script>
    export let activeCategory, selectedUpgradeNames;
    export let category, idx;

    $: names = category.data.map(upgrade => upgrade.name);
    let selectedNames = new Set();

    function replaceAt(index, value) {
        let temp = $selectedUpgradeNames.slice(0);
        temp[index] = value;
        return temp;
    }

    const setActiveCategory = () => {
        if (category?.cls === "mastery") {
            $activeCategory = new URL(`../images/skills/${category.skillId}.webp`, import.meta.url).href;
        } else if (category?.cls === "module") {
            $activeCategory = new URL(`../images/modules/${category.moduleId}.webp`, import.meta.url).href;
        }
    };
    const unsetActiveCategory = () => {
        $activeCategory = "";
    };

    const onCheckName = event => {
        if (event.target.checked) {
            selectedNames.add(event.target.value);
        } else {
            selectedNames.delete(event.target.value);
        }
        selectedNames = selectedNames;
        $selectedUpgradeNames = replaceAt(idx, selectedNames)
    };
    const onSelectAll = event => {
        if (event.target.checked) {
            selectedNames = new Set(names);
        } else {
            selectedNames.clear();
        }
        selectedNames = selectedNames;
        $selectedUpgradeNames = replaceAt(idx, selectedNames)
    };
</script>

<ol on:mouseenter={setActiveCategory} on:mouseleave={unsetActiveCategory}>
    {#if category.data.length > 1}
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