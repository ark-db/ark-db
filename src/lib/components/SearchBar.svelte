<script>
    import Typeahead from "svelte-typeahead";
    import operators from "../data/operators.json";

    export let selectedChar;

    const stripTags = str => str.replace(/(<([^>]+)>)/ig, "");
</script>



<Typeahead hideLabel={true}
           placeholder={"Search operators..."}
           data={Object.values(operators)}
           extract={(id) => id.name}
           inputAfterSelect="clear"
           let:value
           let:result
           on:select={({ detail }) => $selectedChar = detail.original}
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