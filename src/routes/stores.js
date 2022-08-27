import { writable } from "svelte/store";
import { sortItems } from "./utils.js";

// planner
export const selectedChar = writable();
export const activeCategory = writable();
export const allSelected = writable([])

export const splitByStatus = writable(false);
export const showCost = writable(false);



// planner/cost
export const inventory = writable(
    sortItems(Object.keys(items)).filter(id => items[id].type !== "misc")
                                 .map(id => ({id, count: 0}))
);

export const costFilter = writable([false]);
export const itemFilter = writable(["material", "skill", "module", "chip", "misc"]);
export const makeT3 = writable(false);



// farming
export const region = writable("glb");
export const sortMode = writable("effic");