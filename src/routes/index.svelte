<svelte:head>
    <title>ArkDB</title>
    <meta name="description" content="Utility website for Arknights players" />
</svelte:head>

<h1>ArkDB</h1>
<h2>A utility website for Arknights players</h2>
<p>v0.3.1-beta</p>
<a href="https://form.typeform.com/to/gSMV12RK"
   target="_blank"
   rel="noreferrer">
    Submit feedback
</a>

<style>
    h1, h2, p, a {
        color: white;
    }
    h1 {
        margin-bottom: 0.2em;
        text-align: center;
        font-size: clamp(5em, 10vw, 10em);
    }
    h2 {
        text-align: center;
        font-size: clamp(1em, 5vw, 2em);
    }
    p {
        text-align: center;
    }
    a {
        margin: 5em 30vw;
        padding: 10px;
        border-radius: 6px;
        background-color: var(--dark-moderate);
        display: block;
        text-align: center;
        text-decoration: none;
    }
    a:hover {
        background-color: var(--dark-mild);
    }
</style>