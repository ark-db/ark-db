<script>
    export let page;
    export let logo;
</script>

<header>
    <a href="/">
		<img src={logo} alt="ArkDB">
	</a>

    <nav>
        <a href="/" class:active={$page.url.pathname === "/"}>Home</a>
		<a href="/planner" class:active={$page.url.pathname.startsWith("/planner")}>Planner</a>
		<a href="/farming" class:active={$page.url.pathname === "/farming"}>Farming</a>
    </nav>
</header>

<style>
    header {
		background-color: var(--dark-moderate);
		box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
		display: flex;
		align-items: center;
	}
	img {
		margin-left: 1em;
		width: 100%;
		max-width: 40px;
		min-width: 40px;
	}
	nav {
		padding: 1em;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 1em;
	}
	a {
		border-radius: 6px;
		padding: 0.5em 1em;
		font-weight: 500;
		text-decoration: none;
		color: var(--med-strong);
	}
	nav a:hover:not(.active) {
		background-color: var(--dark-mild);
		color: white;
	}
	a.active {
		background-color: var(--dark-strong);
		color: white;
	}
</style>