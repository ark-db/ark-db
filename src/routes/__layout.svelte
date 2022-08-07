<script>
    import { page } from '$app/stores';
    const logo = "/favicon.svg"
</script>



<header>
    <a href="/">
		<img src={logo} alt="ArkDB">
	</a>

    <nav>
        <a href="/" class:active={$page.url.pathname === '/'}>Home</a>
		<a href="/planner" class:active={$page.url.pathname.startsWith("/planner")}>Planner</a>
    </nav>
</header>

<main>
    <slot />
</main>



<style>
	header {
		background-color: var(--dark-moderate);
		display: flex;
        gap: 1em;
	}
	header > a {
		margin: 0 10px;
		width: 100%;
		max-width: 40px;
		min-width: 40px;
	}
	nav {
		display: flex;
		align-items: center;
		gap: 1em;
	}
	a {
		border-radius: 6px;
		padding: 0.5em 1em;
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
	main {
		margin: 10px;
	}

	:global(body) {
		margin: 0px;
		--dark-strong: #111827;
		--dark-moderate: #1f2937;
		--dark-mild: #3a4558;
		--med-strong: #d1d5db;
		--light-strong: #ebeef4;
		--light-moderate: #f5f8fe;
		--green-strong: #22c55e;
		--green-moderate: #4ade80;
	}
	:global(.placeholder) {
		margin: 15px;
		border: 1px dashed black;
        border-radius: 10px;
        padding: 1em;
        background-color: var(--light-moderate);
        text-align: center;
	}
</style>