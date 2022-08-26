import { writable } from "svelte/store";
import items from "$lib/data/items.json";

// planner
export const selectedChar = writable();
export const activeCategory = writable();
export const allSelected = writable([]);

export const splitByStatus = writable(false);
export const showCost = writable(false);



// planner/cost
const restrictedItems = ["4001",
                         "2001", "2002", "2003", "2004",
                         "3112", "3113", "3114",
                         "3003",
                         "7003", "4003"]
export const inventory = writable(
    Object.keys(items)
          .sort((prev, curr) => items[prev].sortId - items[curr].sortId)
          .filter(id => !restrictedItems.includes(id))
          .map(id => ({id, count: 0}))
);

export const costFilter = writable([false]);
export const itemFilter = writable(["material", "skill", "module", "chip", "misc"]);
export const makeT3 = writable(false);



// farming
export const region = writable("glb");
export const sortMode = writable("effic");