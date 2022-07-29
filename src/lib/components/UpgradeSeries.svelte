<script>
    export let category;
    export let activeCategory;

    $: names = category.data.map(upgrade => upgrade.name);
    let selectedNames = new Set();

    const setActiveCategory = () => {
        if (category.type === "mastery") {
            $activeCategory = `./src/lib/images/skills/${category.skillId}.png`;
        } else if (category.type === "module") {
            $activeCategory = `./src/lib/images/modules/${category.moduleId}.png`;
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
    };
    const onSelectAll = event => {
        if (event.target.checked) {
            selectedNames = new Set(names);
        } else {
            selectedNames.clear();
        }
        selectedNames = selectedNames;
    };
</script>

<ol class={category.data.length > 0 ? "visible" : "invisible"} on:mouseenter={setActiveCategory} on:mouseleave={unsetActiveCategory}>
    {#if category.data.length > 1}
        <li>
            <input type="checkbox" id="select-all" checked={selectedNames.size === names.length} on:change={onSelectAll}>
            <label for="select-all">
                <strong>Select All</strong>
            </label>
        </li>
    {/if}
    {#each names as name}
        <li>
            <input type="checkbox" id={name} value={name} checked={selectedNames.has(name)} on:change={onCheckName}>
            <label for={name}>
                {name}
            </label>
        </li>
    {/each}
</ol>

<style>
    ol {
        list-style-type: none;
        padding-left: 0;
    }
    .visible {
        margin: 5px;
        padding: 10px;
        background-color: rgb(215, 218, 224);
        display: flex;
        flex-direction: column;
        row-gap: 1em;
    }
    input[type=checkbox] {
        transform: scale(1.5);
        margin-right: 0.5em;
    }
</style>