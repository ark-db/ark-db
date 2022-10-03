<script>
    export let title, desc;
</script>

<svelte:head>
    <title>{title}</title>
    <meta property="og:title" content={title}>
    <meta name="description" content={desc}>
    <meta property="og:description" content={desc}>
</svelte:head>