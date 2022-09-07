<script>
    import { page } from "$app/stores";
	import { links } from "@utils";
	import RegionSelect from "./RegionSelect.svelte";
</script>



<header>
    <a href="/">
		<div class="logo">
			<slot name="logo" />
		</div>
		<h1>ArkDB</h1>
	</a>
    <nav>
		{#each [...links.entries()] as [ href, title ]}
			<a {href} class:active={href === "/" ? $page.url.pathname === href : $page.url.pathname.startsWith(href)}>
				{title}
			</a>
		{/each}
    </nav>
	<div class="region-select">
		<RegionSelect />
	</div>
</header>



<style>
    header {
		background-color: var(--dark-moderate);
		box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
		position: fixed;
        width: 100%;
        z-index: 2;
		display: flex;
		align-items: center;
	}
	.logo {
		width: 100%;
		max-width: 40px;
		min-width: 40px;
	}
	a > h1 {
		margin: 0;
		color: var(--light-moderate);
		font-size: 1.5em;
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
		display: flex;
		align-items: center;
		gap: 0.75em;
	}
	nav a:hover:not(.active) {
		background-color: var(--dark-mild);
		color: white;
	}
	a.active {
		background-color: var(--dark-strong);
		color: white;
	}
	.region-select {
		position: fixed;
		top: 1em;
		right: 1em;
	}
</style>