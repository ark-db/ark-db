<script>
    import { fly } from "svelte/transition";
    import bars from "../images/bars.svg";

    export let page;

    let active = false;

    const toggle = () => active = !active;

    function getPageTitle(path) {
        if (path === "/") {
            return "Home"
        }  else if (path.startsWith("/planner")) {
            return "Planner"
        } else if (path === "/farming") {
            return "Farming"
        }
    }
</script>



{#if active}
    <div class="sidebar" transition:fly={{x: -100, duration: 300}}>
        <div class="top">
            <div class="logo">
                <slot name="logo" />
            </div>
            <h1>ArkDB</h1>
        </div>
        <div class="divider" />
        <nav>
            <a href="/" class:active={$page.url.pathname === "/"} on:click={toggle}>
                Home
            </a>
		    <a href="/planner" class:active={$page.url.pathname.startsWith("/planner")} on:click={toggle}>
                Planner
            </a>
		    <a href="/farming" class:active={$page.url.pathname === "/farming"} on:click={toggle}>
                Farming
            </a>
        </nav>
    </div>
    <div class="filter" on:click={toggle} transition:fly={{x: 100, duration: 150}} />
{/if}

<header>
    <input type="image" src={bars} alt="Open navigation menu" on:click={toggle}>
    <h1 class="page-title">{getPageTitle($page.url.pathname)}</h1>
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
        width: 65%;
        height: 100%;
        z-index: 3;
        padding: 0.5em;
        background-color: var(--dark-moderate);
        box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
    }
    .top {
        padding: 1em 0.5em;
        display: flex;
        align-items: center;
        gap: 1em;
    }
    .logo {
        width: 100%;
        max-width: 3em;
        min-width: 3em;
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
    a.active {
        border-radius: 0.5em;
        color: var(--light-moderate);
        background-color: var(--dark-strong);
    }
    .filter {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: 2;
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
    h1{
        margin: 0.25em 0;
        font-size: 1.5em;
        color: var(--light-moderate);
    }
    h1.page-title {
        font-weight: 600;
    }
</style>