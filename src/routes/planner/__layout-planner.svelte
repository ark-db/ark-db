<script>
    import { page } from '$app/stores';
</script>



<header>
    <nav>
        <a href="/planner" class:active={$page.url.pathname === "/planner"}>Goal Tracker</a>
        <a href="/planner/tally" class:active={$page.url.pathname === "/planner/tally"}>Cost Tracker</a>
    </nav>
</header>

<main>
    <slot />
</main>



<style>
    header {
        margin-top: 10px;
    }
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
        background-color: rgb(235, 245, 253);
        border-bottom: 2px solid transparent;
        box-sizing: border-box;
        max-width: 25em;
        text-decoration: none;
        color: initial;
    }
    a.active {
        border-bottom: 2px solid rgb(109, 112, 114);
    }
</style>