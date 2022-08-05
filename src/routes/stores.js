import { writable } from "svelte/store";
import items from "$lib/data/items.json";

function initSelectedUpgradeNames() {
    const { subscribe, set, update } = writable({
        elite: new Set(),
        skill: new Set(),
        mastery1: new Set(),
        mastery2: new Set(),
        mastery3: new Set(),
        module1: new Set(),
        module2: new Set(),
    });

	return {
		subscribe,
		set,
        update,
        reset: () => set({
            elite: new Set(),
            skill: new Set(),
            mastery1: new Set(),
            mastery2: new Set(),
            mastery3: new Set(),
            module1: new Set(),
            module2: new Set(),
        })
	};
}

export const selectedChar = writable();
export const activeCategory = writable();
export const selectedUpgradeNames = initSelectedUpgradeNames();
export const allSelected = writable([]);
export const inventory = writable(
    Object.keys(items).filter(id => id !== "4001").map(id => ({id, count: 0}))
);

export const splitByStatus = writable(false);
export const showCost = writable(false);
export const costFilter = writable([false]);
export const makeT3 = writable(false);