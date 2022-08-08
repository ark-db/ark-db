import { writable } from "svelte/store";
import items from "$lib/data/items.json";

function initSelectedUpgradeNames() {
    const { subscribe, set, update } = writable(new Array(7).fill(new Set()));

	return {
		subscribe,
		set,
        update,
        reset: () => set(new Array(7).fill(new Set()))
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