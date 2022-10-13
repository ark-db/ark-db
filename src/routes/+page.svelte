<script>
    import HeadTags from "$lib/components/HeadTags.svelte";
    import ghLogo from "$lib/images/github-logo.svg";
</script>



<HeadTags
    title={"ArkDB"}
    desc={"Utility website for Arknights players"}
/>

<h1 class="title">ArkDB</h1>
<h2>A utility website for Arknights players</h2>
<p>v0.14.5</p>
<a href="https://github.com/ark-db/ark-db/" target="_blank" rel="noreferrer">
    <img src={ghLogo} alt="GitHub logo" height=32 width=32>
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
