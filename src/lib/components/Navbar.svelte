<script>
    import { page } from "$app/stores";
	import { links } from "@utils";
</script>



<header>
    <a href="/">
		<slot name="logo" />
	</a>
    <nav>
		{#each [...links.entries()] as [ href, title ]}
		<a {href} class:active={href === "/" ? $page.url.pathname === href : $page.url.pathname.startsWith(href)}>
			{title}
		</a>
		{/each}
    </nav>
</header>



<style>
    header {
        position: fixed;
        width: 100%;
        z-index: 2;
		background-color: var(--dark-moderate);
		box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
		display: flex;
		align-items: center;
	}
	header > a {
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