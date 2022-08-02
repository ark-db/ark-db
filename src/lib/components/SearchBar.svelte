<script>
    import Typeahead from "svelte-typeahead";
    import operators from "../data/operators.json";
    export let selectedChar;
    export let splitByStatus;

    const data = Object.values(operators)
    const extract = (id) => id.name;
    function handleSelect({ detail }) {
        $selectedChar = detail.original;
        $splitByStatus = false;
    }
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
    on:select={handleSelect}
>
    <svelte:fragment slot="no-results">
        No results found for "{value}"
    </svelte:fragment>
    {stripTags(result.string)}
</Typeahead>