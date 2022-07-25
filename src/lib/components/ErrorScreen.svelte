<script>
    import skalter from "./skalter.jpg"
    export let status;
    export let message;
</script>

<h1>
    {status} - {message}
</h1>

<figure>
    <img src={skalter} alt="Fallen Skalter">
    <figcaption>Illustration by KuroTofu - <a href="https://twitter.com/Kuro_Tofu/status/1454254316710096899">source</a></figcaption>
</figure>

<style>
    h1 {
        text-align: center;
    }

    figure {
        text-align: center;
    }
</style>