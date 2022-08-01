<script context="module">
    export function load({ error, status }) {
        return {
            props: {
                status,
                message: error.message,
            }
        };
    }
</script>
  
<script>
    import ErrorScreen from "$lib/components/ErrorScreen.svelte";
    export let status;
    export let message;
</script>
  
<ErrorScreen {status} {message} />