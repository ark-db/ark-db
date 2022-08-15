<script>
    import { page } from '$app/stores';
</script>



<nav>
    <a href="/planner" class:active={$page.url.pathname === "/planner"}>Upgrade Planner</a>
    <a href="/planner/cost" class:active={$page.url.pathname === "/planner/cost"}>Cost Calculator</a>
</nav>

<slot />



<style>
    nav {
        margin: 20px 0;
        display: flex;
        flex-flow: row wrap;
        align-items: center;
        justify-content: space-evenly;
        gap: 0.5em;
    }
    a {
        flex-grow: 1;
        display: flex;
        justify-content: center;
        border: 1px solid var(--light-moderate);
        border-radius: 8px;
        padding: 0.5em 1em;
        background-color: transparent;
        max-width: 20em;
        font-weight: 500;
        text-decoration: none;
        color: var(--light-moderate);
        transition: all 0.1s ease;
    }
    a.active {
        outline: 1px solid var(--light-moderate);
        outline-offset: 3px;
        padding: calc(0.5em - 1px) calc(1em - 1px);
        background-color: var(--light-moderate);
        color: var(--dark-moderate);
    }
    a:hover:not(.active) {
        background-color: var(--med-mild);
        color: var(--dark-moderate);
    }
</style>