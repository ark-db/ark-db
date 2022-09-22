<script>
    export let toggled = false;
</script>



<label class="toggle">
    <input type="checkbox" class="toggle-input" bind:checked={toggled}>
    <span class="track">
        <span class="indicator">
            <span class="check">
                <svg viewBox="0 0 24 24" role="presentation" aria-hidden="true">
                    <path d="M9.86 18a1 1 0 01-.73-.32l-4.86-5.17a1.001 1.001 0 011.46-1.37l4.12 4.39 8.41-9.2a1 1 0 111.48 1.34l-9.14 10a1 1 0 01-.73.33h-.01z"></path>
                </svg>
            </span>
        </span>
    </span>
</label>



<style>
    :root {
        --indicator-size: 24px;
        --track-height: calc(var(--indicator-size) + 6px);
        --track-width: calc(var(--indicator-size) * 2.5);
        --high-contrast: solid 2px transparent;
        
        --track-border: var(--med-moderate);
        --track-background: var(--light-moderate);
        --focus-ring: 0 0 0 2px var(--dark-moderate);
        
        --speed: 0.15s;
    }
    .toggle {
        align-items: center;
        border-radius: 100px;
        display: flex;
        font-weight: 700;
        margin-bottom: 16px;
    }
    .toggle:last-of-type {
        margin: 0
    }
    .toggle-input {
        clip: rect(0 0 0 0);
        clip-path: inset(50%);
        height: 1px;
        overflow: hidden;
        position: absolute;
        white-space: nowrap;
        width: 1px;
    }
    .toggle-input:not([disabled]):active + .track,
    .toggle-input:not([disabled]):focus + .track {
        border: 1px solid transparent;
        box-shadow: var(--focus-ring);
    }
    .toggle-input:disabled + .track {
        cursor: not-allowed;
        opacity: 0.7;
    }
    .track {
        background: var(--track-background);
        border: 1px solid var(--track-border);
        border-radius: 100px;
        cursor: pointer;
        display: flex;
        height: calc(var(--track-height) - 2px);
        margin: 0 calc(var(--indicator-size) / 2);
        position: relative;
        width: var(--track-width);
    }
    .indicator {
        align-items: center;
        background: var(--dark-moderate);
        border-radius: var(--indicator-size);
        bottom: 2px;
        display: flex;
        height: var(--indicator-size);
        justify-content: center;
        left: 2px;
        outline: var(--high-contrast);
        position: absolute;
        transition: var(--speed);
        width: var(--indicator-size);
    }
    .check {
        fill: #fff;
        height: calc(var(--indicator-size) - 4px);
        width: calc(var(--indicator-size) - 4px);
        opacity: 0;
        transition: opacity var(--speed) ease-in-out;
    }
    .toggle-input:checked + .track .indicator {
        background: var(--dark-moderate);
        transform: translateX(calc(var(--track-width) - var(--track-height)));
    }
    .toggle-input:checked + .track .indicator .check {
        opacity: 1;
        transition: opacity var(--speed) ease-in-out;
    }
    @media screen and (prefers-contrast: more) {
        .track {
            border-radius: 0;
        }
    }
</style>