<script>
    import { assets } from "$app/paths";

    export let charId, size;
    export let border = 0;

    const src = `${assets}/images/operators/${charId}.webp`;
    let name, rarity;
    
    fetch(`./api/operators?id=${charId}&categories=name,rarity`)
        .then(res => res.json())
        .then(res => {
            ({ name, rarity } = res);
        });
</script>



<img class={rarity}
     {src}
     title={name}
     alt={name}
     height={size}
     width={size}
     loading="lazy"
     style="--border:{border}px; --size:{size}px;"
>



<style>
    img {
        border-width: var(--border);
        border-style: solid;
        width: auto;
        height: auto;
        max-width: var(--size);
        max-height: var(--size);
    }
    .\36 {
        border-color: #ed702d;
    }
    .\35 {
        border-color: #f3b13e;
    }
    .\34 {
        border-color: #d4b3d8;
    }
    .\33 {
        border-color: #4faff0;
    }
</style>