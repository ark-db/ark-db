import { writable } from "svelte/store";
import { browser } from "$app/environment";
import items from "$lib/data/items.json";

// preloaded data
let storedUpgrades;
let storedInventory;

if (browser) {
    storedUpgrades = JSON.parse(localStorage.getItem("upgrades"));
    storedInventory = JSON.parse(localStorage.getItem("inventory"));
}



// general
export const region = writable("glb");



// planner
export const selectedChar = writable();
export const activeCategory = writable();
export const allSelected = writable(storedUpgrades ?? []);
export function updateStoredUpgrades(upgrades) {
    if (browser) {
        let reindexed = structuredClone(upgrades);
        for (let [idx, upgrade] of reindexed.entries()) {
            upgrade.id = idx;
        }
        localStorage.upgrades = JSON.stringify(reindexed);
    }
};

export const splitByStatus = writable(false);
export const showCost = writable(false);



// planner/cost
const defaultInventory = Object.keys(items)
                               .sort((prev, curr) => items[prev].sortId - items[curr].sortId)
                               .filter(id => items[id].type !== "misc" && items[id].type !== "other")
                               .map(id => ({id, count: 0}));

export const inventory = writable(storedInventory ?? defaultInventory);
if (browser) {
    inventory.subscribe(value => {
        localStorage.inventory = JSON.stringify(value);
    });
}

export const costFilter = writable([false]);
export const itemFilter = writable(["material", "skill", "module", "chip", "misc"]);
export const makeT3 = writable(false);



// farming
export const sortMode = writable("effic");



// shops
export const normalizeValues = writable(false);