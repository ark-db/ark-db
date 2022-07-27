<script>
    import Typeahead from "svelte-typeahead";
    import operators from "../data/operators.json";
    export let selectedChar;

    const data = Object.values(operators)
    const extract = (id) => id.name;
    const stripTags = (str) => {
        return str.replace( /(<([^>]+)>)/ig, '');
    }
    const sendCharInfo = (data) => {
        $selectedChar.charId = data.charId;
        $selectedChar.name = data.name;
    }
</script>
  
<Typeahead
    hideLabel={true}
    placeholder={"Search for operators..."}
    {data}
    {extract}
    inputAfterSelect="clear"
    let:value
    let:result
    on:select={({ detail }) => sendCharInfo(detail.original)}
>
    <svelte:fragment slot="no-results">
        No results found for "{value}"
    </svelte:fragment>
    {stripTags(result.string)}
</Typeahead>