import items from "$lib/data/items.json";

export const sortItems = (list) => list.sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);

export const links = new Map([
    ["/", "Home"],
    ["/planner", "Planner"],
    ["/farming", "Farming"],
    ["/shops", "Shops"],
]);