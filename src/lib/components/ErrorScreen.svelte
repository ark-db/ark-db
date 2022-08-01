<script>
    import src from "../images/skalter.jpg";
    export let status;
    export let message;
</script>

<h1>
    {status} - {message}
</h1>

<figure>
    <img {src} alt="Fallen Skalter">
    <figcaption>
        Illustration by KuroTofu - 
        <a href="https://twitter.com/Kuro_Tofu/status/1454254316710096899"
           target="_blank"
           rel="noreferrer">
           source
        </a>
    </figcaption>
</figure>

<style>
    h1, figure {
        text-align: center;
    }
</style>