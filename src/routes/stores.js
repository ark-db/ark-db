import { writable } from "svelte/store";

export const selectedChar = writable();
export const activeCategory = writable();
export const selectedUpgradeNames = writable({
    elite: new Set(),
    skill: new Set(),
    mastery1: new Set(),
    mastery2: new Set(),
    mastery3: new Set(),
    module1: new Set(),
    module2: new Set(),
})