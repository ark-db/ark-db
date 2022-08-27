<script>
    import bars from "../images/bars.svg";
    import leftArrow from "../images/left-arrow.svg";

    export let page;

    let active = false;
</script>



{#if active}
    {{}}
{:else}
    <header>
        <div class="logo">
            <slot name="logo" />
        </div>
        <h1>ArkDB</h1>
    </header>
{/if}



<style>
    header {
        padding: 0.25em;
        background-color: var(--dark-moderate);
		box-shadow: 0.1em 0.1em 0.5em rgba(0, 0, 0, 0.75);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5em;
    }
    .logo {
        width: 100%;
        max-width: 2em;
        min-width: 2em;
    }
</style>