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
		box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
		display: flex;
        gap: 1em;
	}
	img {
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
		max-width: clamp(800px, 90vw, 1500px);
		display: flex;
        flex-direction: column;
        gap: 10px;
	}
	:global(:root) {
		--dark-strong: #161921;
		--dark-moderate: #27292c;
		--dark-mild: #3f4652;
		--med-strong: #d1d5db;
		--med-moderate: #d4d4d8;
		--med-mild: #e4e4e7;
		--light-strong: #f3f4f6;
		--light-moderate: #f9fafb;
		--green-strong: #22c55e;
		--green-moderate: #4ade80;
		--green-mild: #69e896;
	}
	:global(.title) {
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
		margin: 0px;
        background-image: url("$lib/images/main-dark.svg");
		background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
	}
	:global(input[type=checkbox]) {
		max-width: 20px;
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