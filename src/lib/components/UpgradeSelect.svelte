<script>
    export let text;
</script>

<div class="select">
    <input type="checkbox" on:click>
    <p>{text}</p>
</div>

<style>
    .select {
        padding: 0 0.75em 0 1em;
        background-color: rgb(215, 218, 224);
        display: flex;
        align-items: center;
        column-gap: 0.5em;
    }
    input[type=checkbox] {
        transform: scale(1.5);
    }
</style>