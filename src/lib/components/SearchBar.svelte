<script>
    import { createEventDispatcher } from 'svelte';
    import Typeahead from "svelte-typeahead";
    import operators from "../data/operators.json";

    const data = Object.values(operators)
    const extract = (id) => id.name;
    const stripTags = (str) => {
        return str.replace( /(<([^>]+)>)/ig, '');
    }
    const dispatch = createEventDispatcher();
    const sendCharId = (data) => {
        let { charId } = data;
		dispatch("message", {
			charId
		});
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
    on:select={({ detail }) => sendCharId(detail.original)}
>
    <svelte:fragment slot="no-results">
        No results found for "{value}"
    </svelte:fragment>
    {stripTags(result.string)}
</Typeahead>