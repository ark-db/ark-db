<script>
    export let stage, effic, rate, espd;

    function categorize(eff) {
        if (eff < 0.75) return "poor";
        else if (eff < 0.9) return "bad";
        else if (eff < 0.95) return "fair"
        else if (eff < 0.99) return "good";
        else return "great";
    };

    const toPercent = new Intl.NumberFormat("en-US", {
        style: "percent",
        minimumFractionDigits: 1
    });
</script>



<div class={categorize(effic)}>
    <h2 title="Stage">{stage}</h2>
    <div class="stats">
        <p title="Stage efficiency">
            {effic === 1 ? effic.toFixed(1) : effic}
        </p>
        <p title="Drop rate">
            {toPercent.format(rate)}
        </p>
        <p title="Expected sanity per drop">
            {espd}
        </p>
    </div>
</div>



<style>
    .poor, .bad, .fair, .good, .great {
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    h2 {
        font-size: 1.5em;
    }
    .stats {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    p {
        margin: 0.25em 0.1em;
        font-size: 0.75em;
    }
</style>