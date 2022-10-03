<script>
    import { browser } from "$app/environment";
    import { page } from "$app/stores";

    export let title, desc;
</script>

<svelte:head>
    <title>{title}</title>
    <meta property="og:title" content={title}>
    <meta name="description" content={desc}>
    <meta property="og:description" content={desc}>
    {#if browser}
		<meta property="og:url" content={`https://${location.hostname}${$page.url.pathname}`}>
	{/if}
</svelte:head>