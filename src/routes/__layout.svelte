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
		background-color: #1f2937;
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
		color: #d1d5db;
	}
	nav a:hover:not(.active) {
		background-color: #3a4558;
		color: white;
	}
	a.active {
		background-color: #111827;
		color: white;
	}
	main {
		margin: 10px;
	}

	:global(body) {
		margin: 0px;
        background-image: url("$lib/images/mainbg.svg");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover
	}
	:global(.placeholder) {
		margin: 15px;
		border: 1px dashed black;
        border-radius: 10px;
        padding: 1em;
        background-color: rgb(245, 248, 254);
        text-align: center;
	}
</style>