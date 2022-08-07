<script>
    import { page } from '$app/stores';
</script>



<nav>
    <a href="/planner" class:active={$page.url.pathname === "/planner"}>Goal Tracker</a>
    <a href="/planner/tally" class:active={$page.url.pathname === "/planner/tally"}>Cost Tracker</a>
</nav>

<main>
    <slot />
</main>



<style>
    nav {
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
        padding: 0.5em 1em 0.5em 1em;
        background-color: var(--light-strong);
        border-radius: 8px;
        border-bottom: 2px solid transparent;
        box-sizing: border-box;
        max-width: 20em;
        text-decoration: none;
        color: initial;
    }
    a.active {
        border-bottom: 2px solid var(--dark-moderate);
    }
</style>