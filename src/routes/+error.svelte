<script>
    import { page } from "$app/stores";
    import src from "$lib/images/skalter.webp";
</script>



<h1 class="title">
    {$page.status} | {$page.error.message}
</h1>

<figure>
    <img {src} alt="Fallen Skalter" height=622 width=880>
    <figcaption>
        Illustration by KuroTofu - 
        <a href="https://twitter.com/Kuro_Tofu/status/1454254316710096899"
           target="_blank"
           rel="noreferrer"
        >
            source
        </a>
    </figcaption>
</figure>



<style>
    h1 {
        font-size: 3em;
    }
    figure {
        text-align: center;
    }
    img {
        max-width: clamp(0px, 80vw, 800px);
        object-fit: contain;
    }
    figcaption {
        margin: 1em 20vw;
        padding: 0.5em;
        border-radius: 8px;
        background-color: var(--dark-moderate);
        color: var(--light-moderate);
    }
    a {
        text-decoration: none;
    }
</style>