<script>
    import { fly } from "svelte/transition";
    import bars from "../images/bars.svg";
    import leftArrow from "../images/left-arrow.svg";

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
    <input type="image" class="close" src={leftArrow} alt="Close navigation menu" on:click={toggle} transition:fly={{x: 50, duration: 300}}>
    <div class="sidebar" transition:fly={{x: -100, duration: 300}}>
        <div class="logo">
            <slot name="logo" />
        </div>
        <nav>

        </nav>
    </div>
{/if}

<header>
    <input type="image" class="open" src={bars} alt="Open navigation menu" on:click={toggle}>
    <h1>{getPageTitle($page.url.pathname)}</h1>
</header>



<style>
    input[type=image] {
        position: fixed;
        width: 100%;
    }
    input[type=image].close {
        top: 0.5em;
        left: 80%;
        max-width: 1.5em;
        min-width: 1.5em;
        z-index: 3;
    }
    .sidebar {
        position: fixed;
        width: 75%;
        z-index: 3;
        background-color: var(--dark-moderate);
        box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
    }
    header {
        padding: 0.25em;
        position: fixed;
        width: 100%;
        z-index: 2;
        background-color: var(--dark-moderate);
		box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75em;
    }
    input[type=image].open {
        left: 1em;
        max-width: 2em;
        min-width: 2em;
    }
    .logo {
        width: 100%;
        max-width: 4em;
        min-width: 4em;
    }
    h1 {
        margin: 0.25em 0;
        font-weight: 500;
        font-size: 1.5em;
        color: var(--light-moderate);
    }
</style>