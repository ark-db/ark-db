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
	main {
		margin: auto;
        padding: 5px;
		max-width: clamp(1200px, 70vw, 1800px);
		display: flex;
        flex-direction: column;
        gap: 10px;
	}
	:global(main > h1) {
        margin: 0.6em 0 0.2em 0;
        text-align: center;
		color: var(--light-moderate);
		text-shadow: 3px 3px var(--dark-strong);
    }
	:global(main > section) {
		border-radius: 8px;
		box-shadow: 5px 5px 5px 5px rgba(0, 0, 0, 0.4);
	}
	:global(body) {
		--dark-strong: #111827;
		--dark-moderate: #1f2937;
		--dark-mild: #3a4558;
		--med-strong: #d1d5db;
		--med-moderate: #d4d4d8;
		--med-mild: #e4e4e7;
		--light-strong: #f3f4f6;
		--light-moderate: #f9fafb;
		--green-strong: #22c55e;
		--green-moderate: #4ade80;
		--green-mild: #69e896;

		margin: 0px;
        background-image: url("$lib/images/main-dark.svg");
		background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
	}
	:global(input[type=checkbox]) {
		/**max-width: 100%;*/
		width: auto;
		transform: scale(1.5);
        margin-right: 0.5em;
	}
	:global(.placeholder) {
		margin: 15px;
		border: 1px dashed var(--light-moderate);
        border-radius: 10px;
        padding: 1em;
        text-align: center;
		color: var(--light-moderate);
	}
</style>