<script>
    import Typeahead from "svelte-typeahead";

    export let selectedChar;

    let data;

    fetch("/api/operators?categories=charId,name")
        .then(res => res.json())
        .then(res => data = Object.values(res));

    async function getCharData(id) {
        let res = await fetch(`/api/operators?id=${id}&categories=charId,name,upgrades`);
        let resData = await res.json();
        $selectedChar = resData;
    };

    const stripTags = str => str.replace(/(<([^>]+)>)/ig, "");
</script>



<Typeahead hideLabel={true}
           placeholder={"Search operators..."}
           {data}
           extract={(id) => id.name}
           inputAfterSelect="clear"
           let:value
           let:result
           on:select={({ detail }) => getCharData(detail.original.charId)}
>
    <svelte:fragment slot="no-results">
        <span class="notfound">
            No results found for "{value}"
        </span>
    </svelte:fragment>
    {stripTags(result.string)}
</Typeahead>



<style>
    .notfound {
        overflow-wrap: anywhere;
    }
</style>