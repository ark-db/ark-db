<svelte:head>
    <title>Upgrade Planner - ArkDB</title>
    <meta name="description" content="Arknights operator upgrade cost calculator and planner" />
</svelte:head>

<script>
    import { selectedChar, activeUpgrade } from "./stores.js"
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    import UpgradeSelect from "$lib/components/UpgradeSelect.svelte";
    
    $: ({ elite, skill, mastery, modules } = $selectedChar);
</script>

<div class="top">
    <div class="search">
        <SearchBar {selectedChar} />
    </div>
    <div class="settings">
        <p>There's nothing here yet!</p>
    </div>
</div>

{#if $selectedChar}
    <div class="banner">
        <div class="card">
            <OperatorIcon {...$selectedChar} />
            <h1>{$selectedChar.name}</h1>
        </div>
        {#if $activeUpgrade}
            <div class="tooltip">
                <img src={$activeUpgrade} alt="Upgrade icon" />
            </div>
        {/if}
    </div>
    <div class="quickselect">
        {#if elite.length > 1}
            <UpgradeSelect
                text="All promotions"
                type="elite"
                {activeUpgrade}
            />
        {/if}
        <UpgradeSelect
            text="All skill levels"
            type="skill"
            {activeUpgrade}
        />
        {#if mastery.length > 1}
            {#each mastery as skill, num}
                <UpgradeSelect
                    text={`All skill ${num+1} masteries`}
                    type="mastery"
                    id={skill.skillId}
                    {activeUpgrade}
                />
            {/each}
        {/if}
        {#each modules as mod}
            <UpgradeSelect
                text={`All ${mod.type} stages`}
                type="module"
                id={mod.moduleId}
                {activeUpgrade}
            />
        {/each}
    </div>
    <div class="upgrades">
        <div class="upgrade">
            {#each elite as costs, rank}
                <UpgradeSelect
                    text={`Elite ${rank+1}`}
                    type="elite"
                    {activeUpgrade}
                />
            {/each}
        </div>
        <div class="upgrade">
            {#each skill as costs, level}
                <UpgradeSelect
                    text={`Skill Level ${level+2}`}
                    type="skill"
                    {activeUpgrade}
                />
            {/each}
        </div>
        {#each mastery as skill, num}
            <div class="upgrade">
                {#each skill.costs as costs, rank}
                    <UpgradeSelect
                        text={`Skill ${num+1} Mastery ${rank+1}`}
                        type="mastery"
                        id={skill.skillId}
                        {activeUpgrade}
                    />
                {/each}
            </div>
        {/each}
        {#each modules as mod}
            <div class="upgrade">
                {#each mod.costs as costs, stage}
                    <UpgradeSelect
                        text={`${mod.type} Stage ${stage+1}`}
                        type="module"
                        id={mod.moduleId}
                        {activeUpgrade}
                    />
                {/each}
            </div>
        {/each}
    </div>
{/if}

<style>


    .top {
        margin: 10px 0px 10px 0px;
        padding: 5px 10px 5px 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: center;
    }
    .top .settings p {
        text-align: center;
    }
    .top .settings {
        flex-grow: 1;
        display: flex;
        justify-content: center;
    }

    .banner {
        margin-bottom: 10px;
        padding: 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: space-between;
        gap: 1em;
    }
    .banner .card {
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: center;
        column-gap: 1em;
    }
    .banner .card h1 {
        text-align: center;
    }
    .banner .tooltip img {
        width: 100%;
        max-width: 80px;
        min-width: 80px;
    }

    .quickselect {
        margin-bottom: 10px;
        padding: 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: flex-start;
        justify-content: center;
        gap: 0.5em 0.5em;
    }

    .upgrades {
        padding: 10px;
        background-color: rgb(235, 238, 244);
        display: flex;
        flex-flow: row wrap;
        align-items: flex-start;
        gap: 2em 1%;
    }
    .upgrade {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        gap: 0.5em;
    }
</style>