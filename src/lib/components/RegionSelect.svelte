<script>
    import { region } from "@stores";
</script>



<select bind:value={$region}>
    <option value="glb">US/JP/KR</option>
    <option value="cn">CN</option>
</select>



<style>
    select {
        border: 1px solid white;
        border-radius: 0.75em;
        padding: 0.75em 1em;
        background-color: transparent;
        width: 100%;
        max-width: 10em;
        color: var(--light-moderate);
        font-weight: 600;
    }
</style>