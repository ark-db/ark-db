<svelte:head>
    <title>Upgrade Planner - ArkDB</title>
    <meta name="description" content="Arknights operator upgrade cost calculator and planner" />
</svelte:head>

<script>
    import { writable } from 'svelte/store';
    import SearchBar from "$lib/components/SearchBar.svelte";
    import OperatorIcon from "$lib/components/OperatorIcon.svelte";
    const selectedChar = writable("");
    $: ({ elite, skill, mastery, modules } = $selectedChar);
</script>

<div class="select">
    <SearchBar {selectedChar} />
    {#if $selectedChar}
        <div class="heading">
            <OperatorIcon {...$selectedChar} />
            <h1>{$selectedChar.name}</h1>
        </div>
        {#each elite as cost, rank}
            <div class="check elite">
                <input type="checkbox">
                <p>Elite {rank+1}</p>
            </div>
        {/each}
        {#each skill as cost, level}
            <div class="check skill">
                <input type="checkbox">
                <p>Skill Level {level+2}</p>
            </div>
        {/each}
        {#each mastery as skill, skill_num}
            {#each skill.costs as cost, rank}
                <div class="check mastery">
                    <input type="checkbox">
                    <p>Skill {skill_num+1} Mastery {rank+1}</p>
                </div>
            {/each}
        {/each}
        {#each modules as mod}
            {#each mod.costs as cost, stage}
                <div class="check module">
                    <input type="checkbox">
                    <p>{mod.type} Stage {stage+1}</p>
                </div>
            {/each}
        {/each}
    {/if}
</div>

<style>
    .select {
        margin-top: 10px;
        background-color: rgb(235, 238, 244);
        padding: 10px;
    }
    .heading {
        margin: 20px;
        display: flex;
        align-items: center;
    }
    .heading h1 {
        margin-left: 0.75em;
    }
    .check {
        margin: 5px;
        padding: 10px;
        background-color: rgb(192, 192, 192);
        display: flex;
        align-items: center;
        gap: 0.5em;
        max-height: 10px;
    }
</style>