<script>
    import { page } from "$app/stores";
    import { fly } from "svelte/transition";
    import { links } from "@utils";
    import bars from "../images/bars.svg";
    import RegionSelect from "./RegionSelect.svelte";

    let active = false;
    $: pageTitle = links.get($page.url.pathname);

    const toggle = () => active = !active;

    const handleKeydown = event => {
        if (event.key === "Escape") active = false;
    };
</script>



<svelte:window on:keydown={handleKeydown}/>

{#if active}
    <div class="filter" on:click={toggle} transition:fly={{x: 100, duration: 150}} />
    <div class="sidebar" transition:fly={{x: -100, duration: 300}}>
        <div class="top">
            <div class="logo">
                <slot name="logo" />
            </div>
            <h1 class="name">ArkDB</h1>
        </div>
        <div class="divider" />
        <nav>
            {#each [...links.entries()] as [ href, title ]}
			    <a {href}
                   class:active={href === "/" ? $page.url.pathname === href : $page.url.pathname.startsWith(href)}
                   on:click={toggle}
                >
				    {title}
			    </a>
		    {/each}
        </nav>
        <div class="container">
            <div class="region-select">
                <RegionSelect />
            </div>
        </div>
    </div>
{/if}

<header>
    <input type="image" src={bars} alt="Open navigation menu" on:click={toggle}>
    {#if pageTitle}
        <h1 class="page-title">{pageTitle}</h1>
    {:else}
        <div class="gap" />
    {/if}
</header>



<style>
    input[type=image] {
        position: fixed;
        width: 100%;
        left: 1em;
        max-width: 2em;
        min-width: 2em;
    }
    .sidebar {
        position: fixed;
        width: min(65%, 250px);
        height: 100%;
        z-index: 3;
        padding: 0.5em;
        background-color: var(--dark-moderate);
        box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
    }
    .top {
        padding: 0.75em 0.5em 1em;
        display: flex;
        align-items: center;
        gap: 1em;
    }
    .logo {
        width: 100%;
        max-width: 3em;
        min-width: 3em;
    }
    h1 {
        color: var(--light-moderate);
    }
    .name {
        margin: 0;
        font-size: 2em;
    }
    .divider {
        position: absolute;
        left: 2.5%;
        right: 2.5%;
        border-bottom: 1px solid white;
    }
    nav {
        margin-top: 0.5em;
        display: flex;
        flex-direction: column;
    }
    a {
        padding: 0.75em;
        font-weight: 500;
		text-decoration: none;
        color: var(--med-strong);
    }
    .active {
        border-radius: 0.5em;
        color: var(--light-moderate);
        background-color: var(--dark-strong);
    }
    .container {
        position: absolute;
        bottom: 0;
    }
    .region-select {
        position: relative;
        left: 1em;
        bottom: 2.5em;
    }
    .filter {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: 3;
        background: rgba(0, 0, 0, 0.5);
    }
    header {
        padding: 0.25em;
        position: fixed;
        width: 100%;
        z-index: 2;
        background-color: #2f3133;
		box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75em;
    }
    .page-title {
        margin: 0.5em 0;
        font-size: 1.5em;
        font-weight: 600;
    }
    .gap {
        height: 3.35em;
    }
</style>