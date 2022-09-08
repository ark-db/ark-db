<script>
    import ghLogo from "$lib/images/github-logo.svg";
</script>



<svelte:head>
    <title>ArkDB - Arknights Tools</title>
    <meta name="description" content="Utility website for Arknights players">
</svelte:head>

<h1 class="title">ArkDB</h1>
<h2>A utility website for Arknights players</h2>
<p>v0.11.0</p>
<a href="https://github.com/ark-db/ark-db/" target="_blank" rel="noreferrer">
    <img src={ghLogo} alt="GitHub logo">
</a>



<style>
    h2, p, a {
        margin: 0 1em 2em;
        color: white;
        text-align: center;
    }
    h1 {
        font-size: clamp(5em, 10vw, 10em);
    }
    h2 {
        font-size: clamp(1em, 5vw, 2em);
    }
    img {
        width: 100%;
        max-width: 32px;
        min-width: 32px;
    }
</style>
