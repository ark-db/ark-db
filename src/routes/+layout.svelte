<script>
	import { page } from '$app/stores';
    import logo from "$lib/images/logo.svg";
	import Navbar from "$lib/components/Navbar.svelte";
	import Sidebar from "$lib/components/Sidebar.svelte";
	let w;
</script>

<svelte:window bind:innerWidth={w} />

{#if w > 450}
	<Navbar {page}>
		<img slot="logo" src={logo} alt="ArkDB logo">
	</Navbar>
{:else}
	<Sidebar {page}>
		<img slot="logo" src={logo} alt="ArkDB logo">
	</Sidebar>
{/if}

<main>
    <slot />
</main>



<style>
	main {
		margin: auto;
        padding: 5px;
		max-width: clamp(800px, 100vw, 1500px);
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
		font-size: 2em;
        text-align: center;
		color: var(--light-moderate);
		text-shadow: 3px 3px var(--dark-strong);
    }
	:global(main > .content) {
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
		margin: 1.5em 15px;
		border: 1px dashed var(--light-moderate);
        border-radius: 10px;
        padding: 1em;
        text-align: center;
		color: var(--light-moderate);
	}
</style>