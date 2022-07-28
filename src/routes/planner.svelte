<svelte:head>
    <title>Upgrade Planner - ArkDB</title>
    <meta name="description" content="Arknights operator upgrade cost calculator and planner" />
</svelte:head>

<script>
    import { writable } from 'svelte/store';
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    import UpgradeSelect from "$lib/components/UpgradeSelect.svelte";
    const selectedChar = writable("");
    $: ({ elite, skill, mastery, modules } = $selectedChar);
    const handleClick = () => {
        console.log("Click!")
    }
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
    </div>
    <div class="quickselect">
        {#if elite.length > 1}
            <UpgradeSelect text="All promotions" />
        {/if}
        <UpgradeSelect text="All skill levels" />
        {#if mastery.length > 1}
            {#each mastery as _, skill}
                <UpgradeSelect text={`All skill ${skill+1} masteries`} />
            {/each}
        {/if}
        {#each modules as mod}
            <UpgradeSelect text={`All ${mod.type} stages`} />
        {/each}
    </div>
    <div class="upgrades">
        <div class="upgrade">
            {#each elite as costs, rank}
                <UpgradeSelect text={`Elite ${rank+1}`} />
            {/each}
        </div>
        <div class="upgrade">
            {#each skill as costs, level}
                <UpgradeSelect text={`Skill Level ${level+2}`} />
            {/each}
        </div>
        {#each mastery as masteries, skill}
            <div class="upgrade">
                {#each masteries.costs as costs, rank}
                    <UpgradeSelect text={`Skill ${skill+1} Mastery ${rank+1}`} />
                {/each}
            </div>
        {/each}
        {#each modules as mod}
            <div class="upgrade">
                {#each mod.costs as costs, stage}
                    <UpgradeSelect text={`${mod.type} Stage ${stage+1}`} />
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