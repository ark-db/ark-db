<script>
    import Typeahead from "svelte-typeahead";
    import operators from "../data/operators.json";

    const data = Object.values(operators)
    const extract = (id) => id.name;
</script>
  
<Typeahead {data} {extract} />