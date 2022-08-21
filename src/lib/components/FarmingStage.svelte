<script>
    export let stage, effic, rate, espd;

    function categorize(eff) {
        if (eff < 0.75) {
            return "poor";
        } else if (eff < 0.9) {
            return "bad";
        } else if (eff < 0.95) {
            return "fair"
        } else if (eff < 0.99) {
            return "good";
        } else {
            return "great";
        };
    };
    const toPercent = new Intl.NumberFormat("en-US", {
        style: "percent",
        minimumFractionDigits: 1
    });
</script>

<div class={categorize(effic)}>
    <h2>{stage}</h2>
    <div class="stats">
        <p>{effic}</p>
        <p>{toPercent.format(rate)}</p>
        <p>{espd}</p>
    </div>
</div>

<style>
    .poor, .bad, .fair, .good, .great {
        display: flex;
        align-items: center;
    }
    .poor * {
        color: #e84141;
    }
    .bad * {
        color: #ff9505;
    }
    .fair * {
        color: #ffb627;
    }
    .good * {
        color: #9be564;
    }
    .great * {
        color: #118fee;
    }
    h2 {
        font-size: 2em;
    }
    .stats {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>