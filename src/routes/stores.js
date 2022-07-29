import { writable, derived } from "svelte/store";

export const selectedChar = writable();
export const activeCategory = writable();
export const allUpgrades = derived(
    selectedChar,
    $selectedChar => $selectedChar?.upgrades.map((category) => category.data)
                                            .flat()
                                            .map(upgrade => ({...upgrade, selected: false}))
);