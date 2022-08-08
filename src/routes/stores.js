import { writable } from "svelte/store";
import items from "$lib/data/items.json";

export const selectedChar = writable();
export const activeCategory = writable();
export const allSelected = writable([]);
export const inventory = writable(
    Object.keys(items).filter(id => id !== "4001").map(id => ({id, count: 0}))
);

export const splitByStatus = writable(false);
export const showCost = writable(false);
export const costFilter = writable([false]);
export const makeT3 = writable(false);