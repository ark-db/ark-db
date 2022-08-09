<script>
    import Typeahead from "svelte-typeahead";
    import operators from "../data/operators.json";
    export let selectedChar;

    const data = Object.values(operators)
    const extract = (id) => id.name;
    const stripTags = (str) => {
        return str.replace( /(<([^>]+)>)/ig, '');
    }
</script>
  
<Typeahead
    hideLabel={true}
    placeholder={"Search operators..."}
    {data}
    {extract}
    inputAfterSelect="clear"
    let:value
    let:result
    on:select={({ detail }) => $selectedChar = detail.original}
>
    <svelte:fragment slot="no-results">
        No results found for "{value}"
    </svelte:fragment>
    {stripTags(result.string)}
</Typeahead>

<style>
    :global([data-svelte-typeahead]) {
        z-index: 1;
}
</style>