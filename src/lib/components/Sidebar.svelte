<script>
    import bars from "../images/bars.svg";
    import leftArrow from "../images/left-arrow.svg";

    export let page;

    let active = false;

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
    {{}}
{:else}
    <header>
        <input type="image" src={bars} alt="Open navigation menu" on:click={() => active = true}>
        <!--<div class="logo">
            <slot name="logo" />
        </div>-->
        <h1>{getPageTitle($page.url.pathname)}</h1>
    </header>
{/if}



<style>
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
    input[type=image] {
        position: fixed;
        left: 1em;
        width: 100%;
        max-width: 2em;
        min-width: 2em;
    }
    /**
    .logo {
        width: 100%;
        max-width: 2em;
        min-width: 2em;
    }
    */
    h1 {
        margin: 0.25em 0;
        font-weight: 500;
        font-size: 1.5em;
        color: var(--light-moderate);
    }
</style>